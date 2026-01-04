# implementation_plan.md

## Project: Enterprise PDF Knowledge Extraction & Search System

### Phase 1: Setup & Architecture
- [ ] Create project directory structure (`backend`, `frontend`, `data`, `docs`)
- [ ] Define `requirements.txt` for Python dependencies
- [ ] Create `README.md` with system overview and prerequisites (e.g., Tesseract OCR)

### Phase 2: Core Processing Modules (Backend)
- [ ] **Ingestion Module** (`backend/modules/ingestion.py`):
    - PDF Loading
    - Type Detection (Digital/Scanned/Mixed) via `pymupdf` (fitz)
- [ ] **OCR Module** (`backend/modules/ocr.py`):
    - Image extraction from PDF pages
    - Text extraction using `pytesseract` (or `easyocr` placeholder)
    - Image preprocessing (denoising with `opencv`)
- [ ] **Parsing & Layout Module** (`backend/modules/parsing.py`):
    - Extract hierarchy (Headers, Chapters) using font styles/sizes
    - Detect tables
- [ ] **Content Segregation** (`backend/modules/segregation.py`):
    - Separate Text, Tables, Images
    - `pdfplumber` for table extraction
    - Image saving for Vision module
- [ ] **Chunking Module** (`backend/modules/chunking.py`):
    - Semantic text chunking with metadata

### Phase 3: Storage & Indexing
- [ ] **Vector Store** (`backend/custom_storage/vector.py`):
    - Initialize ChromaDB (persistent)
    - Embedding generation (SentenceTransformers)
    - Add/Query functions
- [ ] **Structured Store** (`backend/custom_storage/relational.py`):
    - JSON/SQLite store for Tables and Image metadata

### Phase 4: API & Search Interface
- [ ] **FastAPI Backend** (`backend/main.py`):
    - Endpoints: `/upload`, `/search`, `/process`
- [ ] **Search Logic** (`backend/search.py`):
    - Hybrid search (Vector + Structured filter)
    - Reranking (optional)

### Phase 5: Frontend
- [ ] **Streamlit UI** (`frontend/app.py`):
    - File Upload Widget
    - Processing Status Dashboard
    - Search Bar & Result Display (Text highlights, Tables, Images)

### Phase 6: Documentation & Benchmarks
- [ ] Add docstrings and architectural diagrams (mermaid) in `docs/`
- [ ] Benchmark script for latency
