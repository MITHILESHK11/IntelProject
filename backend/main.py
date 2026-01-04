from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pipeline import Pipeline
from custom_storage.vector import VectorStore
from custom_storage.metadata import MetadataStore
from config import DATA_DIR
import os
import fitz
from fastapi.responses import Response
import uvicorn

app = FastAPI(title="PDF Knowledge System")

# CORS for frontend (though currently local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files (PDFs and Images)
# URL: http://localhost:8000/static/pdfs/...
# URL: http://localhost:8000/static/images/...
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(DATA_DIR, "static")),
    name="static"
)

pipeline = Pipeline()
vector_store = VectorStore()
metadata_store = MetadataStore()

@app.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    mode: str = "OCR",
    background_tasks: BackgroundTasks = None # Kept for signature compatibility if needed, but unused
):
    """
    Upload and process a PDF document.
    Processing runs in FastAPI's threadpool (sync-safe).
    Blocking the request until done is intended for this UI flow.
    """
    try:
        # Run pipeline synchronously (in threadpool) so we return ONLY when done
        result = pipeline.run(file.file, file.filename, extraction_mode=mode)
        return result
    except Exception as e:
        print(f"Pipeline Error: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/search")
async def search(q: str, limit: int = 5):
    results = vector_store.search(q, limit)
    
    # Synthesize Answer
    if results and results.get("documents") and results["documents"][0]:
        context_chunks = results["documents"][0]
        context_str = "\n---\n".join(context_chunks)
        
        # Call Gemini for synthesis
        answer = pipeline.gemini.generate_answer(q, context_str)
        results["answer"] = answer
    else:
        results["answer"] = "I couldn't find any relevant information in the documents to answer your question."
        
    return results

@app.get("/documents/{doc_id}")
async def get_document_artifacts(doc_id: str):
    """
    Returns all extracted artifacts for a specific document
    to populate the Knowledge Explorer.
    """
    tables = metadata_store.load_tables(doc_id)
    images = metadata_store.load_images(doc_id)

    return {
        "doc_id": doc_id,
        "tables": tables,
        "images": images,
        "pdf_url": f"http://127.0.0.1:8000/static/pdfs/{doc_id}.pdf"
    }

@app.get("/database/inspect")
async def inspect_database():
    """
    Returns grouped chunks from the Vector DB for inspection.
    """
    raw_data = vector_store.get_all_chunks()
    
    # Group by doc_id
    grouped_data = {}
    
    ids = raw_data["ids"]
    metas = raw_data["metadatas"]
    docs = raw_data["documents"]
    
    # Handle case where db is empty or lists are None
    if not ids:
        return {}

    for i, chunk_id in enumerate(ids):
        # Safety check if meta is missing
        meta = metas[i] if metas[i] else {}
        doc_id = meta.get("doc_id", "Unknown Document")
        
        if doc_id not in grouped_data:
            grouped_data[doc_id] = []
            
        grouped_data[doc_id].append({
            "chunk_id": chunk_id,
            "text": docs[i],
            "metadata": meta
        })
        
    return grouped_data

@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """
    Deletes all data (chunks, metadata, static files) for a given document.
    """
    try:
        vector_store.delete_document(doc_id)
        metadata_store.delete_document(doc_id)
        return {"status": "success", "message": f"Deleted document: {doc_id}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.delete("/database/reset")
async def reset_database():
    """
    Danger Zone: Wipes the entire database and all static files.
    """
    try:
        vector_store.reset_database()
        metadata_store.reset_database()
        return {"status": "success", "message": "Database successfully reset."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/citation/{doc_id}/{page}/{bbox_str}")
async def get_visual_citation(doc_id: str, page: int, bbox_str: str):
    """
    Returns a cropped image of the PDF based on bbox coordinates.
    """
    try:
        # Construct path using correct structure
        # config.py: PDF_DIR = STATIC_DIR/pdfs = DATA_DIR/static/pdfs
        pdf_path = os.path.join(DATA_DIR, "static", "pdfs", f"{doc_id}.pdf") 
        if not os.path.exists(pdf_path):
             return Response(content=b"PDF not found", status_code=404)
             
        doc = fitz.open(pdf_path)
        
        # Validate page (1-based input -> 0-based index)
        page_idx = page - 1
        if page_idx < 0 or page_idx >= len(doc):
             return Response(content=b"Page out of range", status_code=404)
        
        pdf_page = doc[page_idx]
        
        # Parse bbox
        try:
            coords = [float(x) for x in bbox_str.split(",")]
            if len(coords) != 4: raise ValueError
        except:
             # If bad format, return full page or error? Error is safer.
             return Response(content=b"Invalid BBox format", status_code=400)

        rect = fitz.Rect(coords)
        
        # Add visual padding (optional, e.g. 10px) to give context
        # Check bounds to avoid crashing? get_pixmap usually handles out-of-bounds via clipping
        rect.x0 -= 10
        rect.y0 -= 10
        rect.x1 += 10
        rect.y1 += 10
        
        pix = pdf_page.get_pixmap(clip=rect, dpi=200) # 200 DPI for good quality
        img_bytes = pix.tobytes("png")
        
        return Response(content=img_bytes, media_type="image/png")
    except Exception as e:
        print(f"Citation Generation Error: {e}")
        return Response(content=str(e), status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
