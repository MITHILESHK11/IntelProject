import google.generativeai as genai
import os
import time
from typing import Dict, Any, List
from config import GOOGLE_API_KEY, GEMINI_MODEL

class GeminiProcessor:
    def __init__(self, api_key: str = None, model_name: str = None):
        self.api_key = api_key or GOOGLE_API_KEY
        self.model_name = model_name or GEMINI_MODEL
        
        if not self.api_key:
             print("WARNING: GOOGLE_API_KEY not found. Gemini Vision will fail.")
        else:
             genai.configure(api_key=self.api_key)
             self.model = genai.GenerativeModel(self.model_name)

    def extract_text_from_image(self, image_path: str) -> Dict[str, Any]:
        """
        Uses Gemini Vision to read text from an image.
        """
        if not self.api_key:
             return {"text": "ERR: NO API KEY", "confidence": 0}

        try:
             # Load image for Gemini
             sample_file = genai.upload_file(path=image_path, display_name=os.path.basename(image_path))
             
             # Prompt
             prompt = """
             You are an expert document reader. Carefully read the provided scanned or handwritten document image.
             Extract all readable text accurately.
             Preserve paragraph breaks and logical order.
             Do not hallucinate missing content.
             If text is unclear, mark it as [UNREADABLE].
             Return only the extracted text.
             """
             
             response = self.model.generate_content([sample_file, prompt])
             
             # Cleanup uploaded file if possible (though genai auto-expire usually)
             # genai.delete_file(sample_file.name)
             
             return {
                 "text": response.text,
                 "confidence": 1.0, # Synthetic confidence for LLM
                 "source": "gemini_vision"
             }
             
        except Exception as e:
             return {"text": f"ERR: GEMINI FAILED {str(e)}", "confidence": 0}

    def summarize_text(self, text: str) -> str:
        """
        Summarize a text block using Gemini Pro.
        """
        if not self.api_key: return "Summary Unavail (No Key)"
        try:
             prompt = f"Summarize the following table data in 2 concise sentences, focusing on key trends and numbers:\n\n{text}"
             response = self.model.generate_content(prompt)
             return response.text.replace("\n", " ").strip()
        except Exception as e:
             return f"Summary Failed: {str(e)}"

    def generate_answer(self, query: str, context: str) -> str:
        """
        Generates a concise answer based on provided context chunks.
        """
        if not self.api_key: return "Answer generation unavailable (No API Key)."
        try:
             prompt = f"""
             You are a helpful AI assistant. Use the following document extracts (context) to answer the user's question.
             Keep your answer concise (2-4 sentences) and professional.
             If the answer is not in the context, say that you don't have enough information.
             
             Context:
             {context}
             
             User Question: {query}
             
             Answer:
             """
             response = self.model.generate_content(prompt)
             return response.text.strip()
        except Exception as e:
             return f"Error Generating Answer: {str(e)}"
