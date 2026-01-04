import fitz
import os
from PIL import Image
import io
from backend.config import IMAGE_DIR, GOOGLE_API_KEY

class VisionProcessor:
    def __init__(self, gemini_processor=None):
        self.images_dir = IMAGE_DIR
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
        self.gemini = gemini_processor

    def extract_images(self, file_path: str, doc_id: str):
        doc = fitz.open(file_path)
        image_metadata = []
        
        for i, page in enumerate(doc):
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                ext = base_image["ext"]
                
                image_filename = f"{doc_id}_page{i+1}_img{img_index}.{ext}"
                image_path = os.path.join(self.images_dir, image_filename)
                
                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                
                # Generate AI Caption using Gemini Vision
                caption = self._generate_caption(image_path, i+1)
                
                image_metadata.append({
                    "image_id": image_filename,
                    "path": image_path,
                    "page": i+1,
                    "caption": caption
                })
                
        return image_metadata
    
    def _generate_caption(self, image_path: str, page_num: int) -> str:
        """Generate descriptive caption for image using Gemini Vision"""
        if self.gemini and self.gemini.api_key:
            try:
                import google.generativeai as genai
                # Note: self.gemini should be an instance of GeminiProcessor
                # which already has self.model configured with the right model name from config.py
                
                sample_file = genai.upload_file(path=image_path)
                prompt = """Analyze this image extracted from a document. 
                Summarize its context and content in 1-2 concise sentences. 
                Identify if it's a chart, diagram, photograph, or logo and what it represents."""
                
                response = self.gemini.model.generate_content([sample_file, prompt])
                return response.text.strip()
            except Exception as e:
                print(f"Caption generation failed: {e}")
                return f"Image extracted from page {page_num}"
        return f"Image extracted from page {page_num}"
