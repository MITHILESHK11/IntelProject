import os
import fitz
import shutil
from config import UPLOAD_DIR, PDF_DIR, GOOGLE_API_KEY, GEMINI_MODEL
from modules.ingestion import PDFIngestor
from parsers.docling_parser import DoclingParser
from modules.chunking import Chunker
from custom_storage.vector import VectorStore
from custom_storage.metadata import MetadataStore
from modules.vision import VisionProcessor
from modules.gemini_vision import GeminiProcessor

class Pipeline:
    def __init__(self):
        try:
             self.docling = DoclingParser()
             print("Docling Parser initialized successfully.")
        except Exception as e:
             print(f"Warning: Docling failed to init: {e}")
             self.docling = None
            
        self.vector_store = VectorStore()
        self.metadata_store = MetadataStore()
        self.chunker = Chunker()
        self.gemini = GeminiProcessor(api_key=GOOGLE_API_KEY)
        self.vision = VisionProcessor(gemini_processor=self.gemini)
        
        if not os.path.exists(PDF_DIR):
            os.makedirs(PDF_DIR)

    def run(self, file_object, filename: str, extraction_mode: str = "OCR"):
        print(f"--- Processing {filename} with Mode: {extraction_mode} ---")
        # 1. Save File to PERSISTENT Static Directory
        file_path = os.path.join(PDF_DIR, filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file_object, f)
            
        doc_id = filename.replace(".pdf", "").strip().replace(" ", "_")
        doc_id = "".join(c for c in doc_id if c.isalnum() or c in ("_", "-")).strip()
        
        # 2. Ingest
        ingestor = PDFIngestor(file_path)
        # Always extract raw pages for transparency
        raw_pages = ingestor.extract_page_images(doc_id)
        
        # 3. Classify
        classification = ingestor.classify_pdf()
        print(f"[{filename}] Classification: {classification}")
        
        structure = []
        tables = []
        images = []

        # 4. Extraction Logic
        
        # Mode 1: GEMINI (Mental for Handwriting/Impossible Docs)
        if extraction_mode == "GEMINI":
             print(f"[{filename}] Using Gemini Vision for content extraction...")
             full_text_accum = ""
             for i, page_img_path in enumerate(raw_pages):
                print(f"[{filename}] Gemini Vision Page {i+1}/{len(raw_pages)}")
                gemini_result = self.gemini.extract_text_from_image(page_img_path)
                page_text = gemini_result["text"]
                
                # Gemini doesn't give bboxes in this straightforward mode
                structure.append({
                    "text": page_text,
                    "role": "content",
                    "page": i + 1,
                    "confidence": 1.0,
                    "source": "gemini_vision"
                })
                full_text_accum += page_text + "\n"
             
             # Also treat pages as images
             for i, path in enumerate(raw_pages):
                 images.append({
                     "image_id": os.path.basename(path),
                     "page": i + 1,
                     "caption": f"Page {i+1} (Gemini Source)",
                     "type": "scanned_page"
                 })
             tables = [] 

        # Mode 2: UNIFIED DOCLING (Digital + Scanned/OCR)
        else:
            print(f"[{filename}] Running Unified Docling Extraction (OCR enabled)...")
            
            if self.docling:
                try:
                    # Docling handles both Digital text and OCR (if configured in init)
                    # It also handles Table Structure automatically.
                    docling_result = self.docling.process(file_path)
                    
                    structure = docling_result["chunks"]
                    tables = docling_result["tables"]
                    
                    # Phase 4 (Enhanced): LLM Summarization of Tables
                    # Iterating through chunks to find tables
                    print(f"[{filename}] Enhancing {len(structure)} chunks (LLM Table Summary)...")
                    for chunk in structure:
                         if chunk.get("type") == "table" and "full_content" in chunk:
                             # Generate LLM Summary to replace the weak heuristic one
                             table_md = chunk["full_content"]
                             # Only summarize if it's substantial
                             if len(table_md) > 50:
                                 llm_summary = self.gemini.summarize_text(table_md)
                                 chunk["text"] = f"LLM Summary: {llm_summary}"
                                 print(f" > Summarized Table on Pg {chunk['page']}")
                    
                    # Log success
                    print(f"[{filename}] Docling success: {len(structure)} chunks, {len(tables)} tables.")
                    # if the user wants to see them. Docling works on the PDF directly.
                    # Since we already extracted 'raw_pages' separately, we can still link them.
                    
                    # Logic: If tables/chunks found are minimal, maybe it failed? 
                    # Docling is robust; trust it.
                    
                except Exception as e:
                    print(f"CRITICAL: Docling failed: {e}")
                    structure = [{"text": f"Extraction Failed: {str(e)}", "role": "error", "page": 1}]
            else:
                 print("Docling not initialized. Attempting fallback...")

            # --- FALLBACK MECHANISM ---
            # If structure is empty or contains errors, fallback to standard PyMuPDF text extraction
            if not structure or (len(structure) == 1 and structure[0].get("role") == "error"):
                 print(f"[{filename}] Falling back to Standard PDF Text Extraction...")
                 try:
                     doc = fitz.open(file_path)
                     structure = []
                     for i, page in enumerate(doc):
                         text = page.get_text()
                         # Basic cleanup
                         text = text.strip()
                         if text:
                             structure.append({
                                 "text": text,
                                 "role": "content",
                                 "page": i + 1,
                                 "type": "text"
                                 # No bbox check triggers basic chunker
                             })
                     print(f"[{filename}] Fallback success: Extracted {len(structure)} pages of text.")
                 except Exception as e:
                     print(f"[{filename}] Fallback failed: {e}")
                     structure = [{"text": "Extraction Failed Completely", "role": "error", "page": 1}]

            # Extract standard images (figures) from PDF separate from Docling 
            # (Docling can do this in v2, but keeping our vision module for now is safer conflict resolution)
            print(f"[{filename}] Extracting Images/Figures...")
            images = self.vision.extract_images(file_path, doc_id)
            
            # If no embedded images found but it was scanned, maybe add the full pages as images?
            if not images and (classification == "SCANNED" or len(images) == 0):
                for i, path in enumerate(raw_pages):
                    images.append({
                        "image_id": os.path.basename(path),
                        "page": i + 1,
                        "caption": f"Scanned Page {i+1}",
                        "type": "scanned_page"
                    })

        # 5. Chunking & Storage (Common)
        print(f"[{filename}] Chunking {len(structure)} structure blocks...")
        chunks = self.chunker.chunk_by_structure(structure)
        
        print(f"[{filename}] Storing {len(chunks)} chunks and artifacts...")
        self.vector_store.add_chunks(chunks, doc_id)
        self.metadata_store.save_tables(tables, doc_id)
        self.metadata_store.save_images(images, doc_id)
        
        return {
            "status": "success", 
            "doc_id": doc_id, 
            "chunks": len(chunks), 
            "tables": len(tables), 
            "images": len(images),
            "type": classification,
            "mode": extraction_mode
        }
