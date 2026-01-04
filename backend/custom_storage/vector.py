import chromadb
from chromadb.config import Settings
import uuid
from typing import List, Dict, Any
from backend.config import VECTOR_DB_DIR, EMBEDDING_MODEL

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=VECTOR_DB_DIR)
        self.collection_name = "knowledge_base"
        
        # Using built-in default embedding function for simplicity (all-MiniLM-L6-v2)
        # In production, might want to explicitly define it.
        from chromadb.utils import embedding_functions
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
        
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_fn
        )

    def add_chunks(self, chunks: List[Dict[str, Any]], doc_id: str):
        if not chunks:
            return
            
        ids = [str(uuid.uuid4()) for _ in chunks]
        # Handle 'text' or 'content' key from chunks
        documents = [c.get("text") or c.get("content") or "" for c in chunks]
        metadatas = []
        
        for c in chunks:
            # Serialize bbox if present (Chroma flat metadata requirement)
            bbox = c.get("bbox")
            if bbox and isinstance(bbox, list):
                bbox_str = ",".join(str(x) for x in bbox)
            elif bbox:
                 bbox_str = str(bbox)
            else:
                 bbox_str = ""
                 
            meta = {
                "doc_id": doc_id,
                "page": c.get("page", 1),
                "source": c.get("source", "unknown"),
                "role": c.get("role", "content"),
                "bbox": bbox_str,
                # Phase 4: Decoupled Storage
                "full_content": c.get("full_content", "") # Store raw table markdown here
            }
            metadatas.append(meta)
            
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

    def search(self, query: str, n_results: int = 5):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        # Swizzle: If full_content exists, replace the 'document' snippet with it
        # The frontend expects 'documents' list.
        # Chroma results structure: {'ids': [[...]], 'documents': [[...]], 'metadatas': [[...]]}
        
        if not results['documents']: return results

        for i, doc_list in enumerate(results['documents']):
             for j, doc in enumerate(doc_list):
                 meta = results['metadatas'][i][j]
                 full = meta.get('full_content')
                 if full and len(full) > 10:
                      # SWAP: Return the full real data, not the summary
                      results['documents'][i][j] = full
                      
        return results

    def get_all_chunks(self) -> Dict[str, Any]:
        """
        Retrieves all chunks from the DB to visualize stored knowledge.
        Limiting to first 1000 items to prevent UI crashes on large DBs.
        """
        # Fetch metadata and documents
        data = self.collection.get(limit=1000, include=["metadatas", "documents"])
        return data

    def delete_document(self, doc_id: str):
        """Deletes all chunks associated with a specific document ID."""
        print(f"Deleting chunks for {doc_id}...")
        self.collection.delete(where={"doc_id": doc_id})

    def reset_database(self):
        """Resets the entire vector database by re-creating the collection."""
        print("Resetting Vector Database...")
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name, 
            embedding_function=self.embedding_fn
        )
