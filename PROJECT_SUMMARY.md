# 📋 Project Summary & Technical Deep Dive

## System Overview
The **Enterprise Hybrid RAG (Retrieval-Augmented Generation)** system is designed to bridge the gap between traditional document management and modern AI. It solves the "Dark Data" problem where knowledge is trapped in scanned PDFs, handwritten notes, and complex tables that standard scrapers miss.

## 🛠 Technology Stack

| Component | Technology | Reason for Choice |
|-----------|------------|-------------------|
| **Frontend** | Streamlit | Rapid prototyping of interactive data/chat apps. |
| **Backend** | FastAPI | High-performance, async-capable Python web framework. |
| **OCR Engine** | Tesseract 5 | Industry standard for offline, high-volume OCR. |
| **AI Vision** | Google Gemini | SoTA Multimodal model for "reasoning" over visual documents. |
| **Vector DB** | ChromaDB | Lightweight, embeddable vector search engine. |
| **Embeddings** | all-MiniLM-L6-v2 | Fast, efficient sentence transformer for semantic search. |
| **PDF Tools** | PyMuPDF (Fitz) | Extremely fast PDF rendering and low-level extraction. |

## ⚙️ Core Modules Explained

### 1. Ingestion Pipeline (`backend/pipeline.py`)
This is the central nervous system.
- **Classification**: Determines if a PDF is "Digital" (selectable text), "Scanned", or "Mixed".
- **Router**: Based on User Selection (OCR vs. Gemini), it routes the PDF pages to the correct extractor.
- **Synthesizer**: It combines raw text, tables, and images back into a unified "Document Object" for storage.

### 2. The Vision Module (`backend/modules/gemini_vision.py`)
Instead of just "reading text", this module sends the *image* of the page to the LLM with a prompt: *"Transcribe this document exactly, preserving layout and tables."*
- **Why?** Better at handwriting, messy forms, and weird fonts than Tesseract.
- **Cost**: Slower and requires API calls, hence it's an optional mode.

### 3. Custom Storage Layer
We don't use a monolithic database.
- **`backend/custom_storage/vector.py`**: Wraps ChromaDB. Handles chunking text and storing embeddings.
- **`backend/custom_storage/metadata.py`**: File-system based storage for "heavy" assets like table JSONs and extracted images. This keeps the Vector DB lean.

### 4. The Agentic Frontend (`frontend/app.py`)
A state-of-the-art Streamlit implementation.
- **Session State Management**: Handles complex flows like switching from Chat to Inspector mode without losing context.
- **Custom CSS**: Injects "Dark Glassmorphism" styles for an enterprise look.
- **Sync/Async Bridge**: Uses `requests` to talk to the FastAPI backend, handling timeouts and retries for long-running AI tasks.

## 🔮 Future Roadmap
- **Multi-File Chat**: Talk to the entire repository at once (already partially supported via Vector Search).
- **Table RAG**: Specialized handling for querying inside CSV/DataFrame structures.
- **User Auth**: Adding Keycloak/OAuth for multi-user support.
