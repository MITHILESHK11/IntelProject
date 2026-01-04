import fitz  # PyMuPDF
import os
from typing import Dict, Any, List
from config import DATA_DIR

class PDFIngestor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.doc = fitz.open(file_path)

    def extract_page_images(self, doc_id: str) -> List[str]:
        """
        Converts all PDF pages to images and saves them for inspection/OCR.
        """
        output_dir = os.path.join(DATA_DIR, "static", "pages", doc_id)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        image_paths = []
        for i, page in enumerate(self.doc):
            pix = page.get_pixmap(dpi=300) # High DPI for OCR
            filename = f"page_{i+1:03d}.png"
            path = os.path.join(output_dir, filename)
            pix.save(path)
            image_paths.append(path)
            
        return image_paths

    def classify_pdf(self) -> str:
        """
        Classifies the PDF as DIGITAL, SCANNED, or MIXED based on text content.
        """
        total_pages = len(self.doc)
        text_pages = 0
        
        for page in self.doc:
            text = page.get_text()
            if len(text.strip()) > 50: # Threshold for considering a page as having text
                text_pages += 1
        
        if text_pages == 0:
            return "SCANNED"
        elif text_pages == total_pages:
            return "DIGITAL"
        else:
            return "MIXED"

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "filename": os.path.basename(self.file_path),
            "page_count": len(self.doc),
            "type": self.classify_pdf(),
            "metadata": self.doc.metadata
        }
