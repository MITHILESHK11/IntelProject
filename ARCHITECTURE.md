# 🏗 System Architecture

## Data Flow Diagram

```ascii
[ PDF FILE ]
     ⬇
[ FRONTEND (Streamlit) ]
     ⬇ (HTTP POST /upload)
[ BACKEND (FastAPI) ]
     ⬇
[ PIPELINE MANAGER ]
     |
     +--- (Mode: OCR) ---> [ PyMuPDF / Tesseract ] ---+
     |                                                |
     +--- (Mode: GEMINI) -> [ Google Vision API ] ----+
                                                      |
                                             [ EXTRACTED CONTENT ]
                                             (Text, Tables, Images)
                                                      ⬇
                                          +-----------+-----------+
                                          ⬇                       ⬇
                                   [ VECTOR STORE ]        [ METADATA STORE ]
                                   (ChromaDB)              (JSON + Static Files)
                                   - Embeddings            - Table Structures
                                   - Search Index          - High-Res Images
```

## Service Interactions

### 1. Upload Phase
1. User Drags PDF -> Frontend.
2. User Selects Mode (OCR/Gemini).
3. Frontend sends file + mode to Backend.
4. Backend processes synchronously (blocking) but in a threadpool to enable concurrency.
5. Backend returns `doc_id`.

### 2. Exploration Phase
1. User clicks "Knowledge Explorer" item.
2. Frontend requests `GET /documents/{doc_id}`.
3. Backend stitches together JSON metadata + Static Image URLs.
4. Frontend renders Tree View.

### 3. Search (RAG) Phase
1. User types query.
2. Frontend requests `GET /search?q=...`.
3. Backend embeds query -> Queries ChromaDB.
4. Returns top `k` chunks with Metadata (Page #, Source).
5. Frontend displays Answer + Citations.

## File System Artifacts

The system generates a `data/` folder at runtime:

- `data/static/pdfs/`: Original files.
- `data/static/images/`: Extracted figures/diagrams.
- `data/static/pages/`: Full page screenshots (for visual verification).
- `data/processed/*.json`: Logical structure of documents.
- `data/vectordb/`: The searchable brain.
