import json
import os
from typing import List, Dict, Any
from config import PROCESSED_DIR

class MetadataStore:
    def __init__(self):
        if not os.path.exists(PROCESSED_DIR):
            os.makedirs(PROCESSED_DIR)

    def save_tables(self, tables: List[Dict[str, Any]], doc_id: str):
        path = os.path.join(PROCESSED_DIR, f"{doc_id}_tables.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(tables, f, indent=2)

    def save_images(self, images: List[Dict[str, Any]], doc_id: str):
        path = os.path.join(PROCESSED_DIR, f"{doc_id}_images.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(images, f, indent=2)

    def load_tables(self, doc_id: str) -> List[Dict[str, Any]]:
        path = os.path.join(PROCESSED_DIR, f"{doc_id}_tables.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def load_images(self, doc_id: str) -> List[Dict[str, Any]]:
        path = os.path.join(PROCESSED_DIR, f"{doc_id}_images.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def delete_document(self, doc_id: str):
        """Deletes metadata files and associated static content for a document."""
        # Delete JSONs
        for suffix in ["_tables.json", "_images.json"]:
            path = os.path.join(PROCESSED_DIR, f"{doc_id}{suffix}")
            if os.path.exists(path):
                os.remove(path)
        
        # Delete Static Content
        from config import STATIC_DIR, PDF_DIR
        
        # Delete Scanned Pages Dir
        pages_dir = os.path.join(STATIC_DIR, "pages", doc_id)
        if os.path.exists(pages_dir):
            import shutil
            shutil.rmtree(pages_dir)
            
        # Delete Original PDF
        pdf_path = os.path.join(PDF_DIR, f"{doc_id}.pdf")
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

    def reset_database(self):
        """Clears all metadata and static files."""
        # Clear PROCESSED_DIR (Metadata)
        import shutil
        if os.path.exists(PROCESSED_DIR):
            shutil.rmtree(PROCESSED_DIR)
            os.makedirs(PROCESSED_DIR)
        
        # Clear Static Dirs
        from config import STATIC_DIR, PDF_DIR, IMAGE_DIR
        
        # Pages
        pages_root = os.path.join(STATIC_DIR, "pages")
        if os.path.exists(pages_root):
            shutil.rmtree(pages_root)
            os.makedirs(pages_root)
            
        # PDFs
        if os.path.exists(PDF_DIR):
            shutil.rmtree(PDF_DIR)
            os.makedirs(PDF_DIR)
            
        # Extracted Images
        if os.path.exists(IMAGE_DIR):
             shutil.rmtree(IMAGE_DIR)
             os.makedirs(IMAGE_DIR)
