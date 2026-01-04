from typing import List, Dict, Any

class Chunker:
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_by_structure(self, structure: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Groups content by the most recent heading and chunks large sections.
        If 'bbox' is present (Docling), it preserves semantic layout units.
        """
        # Check for Docling-style Layout-Aware structure
        if structure and "bbox" in structure[0]:
             return self._chunk_docling(structure)

        chunks = []
        current_heading = "Introduction"
        current_buffer = ""
        current_page = 1
        
        for item in structure:
            text = item["text"]
            role = item["role"]
            page = item["page"]
            
            if role == "heading":
                # Flush current buffer as a chunk
                if current_buffer:
                    chunks.extend(self._create_chunks(current_buffer, current_heading, current_page))
                    current_buffer = ""
                
                current_heading = text
                current_page = page
            else:
                current_buffer += " " + text
        
        # Flush remaining
        if current_buffer:
             chunks.extend(self._create_chunks(current_buffer, current_heading, current_page))
             
        return chunks

    def _chunk_docling(self, structure: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        chunks = []
        current_heading = "Page Content"
        
        for item in structure:
             # If heading, update context
             role = item.get("role", "content")
             text = item.get("text", "")
             
             if role == "heading":
                 current_heading = text
                 # Headings are also valid chunks for searching
                 chunks.append({
                     "heading": "Section Hdr",
                     "content": text,
                     "page": item["page"],
                     "bbox": item["bbox"],
                     "type": "heading"
                 })
                 continue
            
             # Keep Table/Content as is
             chunks.append({
                 "heading": current_heading,
                 "content": text,  # This is the SEARCH SUMMARY for tables
                 "full_content": item.get("full_content"), # The REAL data
                 "page": item["page"],
                 "bbox": item.get("bbox"),
                 "type": item.get("type", "text")
             })
        return chunks

    def _create_chunks(self, text: str, heading: str, page: int) -> List[Dict[str, Any]]:
        """
        Splits text into smaller chunks with overlap.
        """
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk_text = " ".join(words[i : i + self.chunk_size])
            chunks.append({
                "heading": heading,
                "content": chunk_text,
                "page": page
            })
            
        return chunks
