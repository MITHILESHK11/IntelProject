# 🔌 API Reference

The backend exposes a RESTful API built with FastAPI.

## Base URL
`http://localhost:8000`

---

## Endpoints

### 1. Document Management

#### `POST /upload`
Uploads and ingest a document.
- **Form Data**: `file` (PDF)
- **Query Param**: `mode` ("OCR" or "GEMINI")
- **Response**:
```json
{
  "status": "success",
  "doc_id": "report_2024",
  "chunks": 45,
  "tables": 2,
  "images": 5
}
```

#### `GET /documents/{doc_id}`
Retrieve artifacts for inspection.
- **Response**: JSON object containing lists of tables, images, and the static PDF URL.

#### `DELETE /documents/{doc_id}`
Delete a document and all related data.

### 2. Search & Retrieval

#### `GET /search`
Perform RAG search.
- **Query Param**: `q` (Search query), `limit` (default 5)
- **Response**:
```json
{
  "ids": [...],
  "documents": ["Chunk text 1...", ...],
  "metadatas": [{"page": 1, "bbox": [...]}, ...],
  "answer": "Generated AI answer..."
}
```

### 3. System

#### `GET /database/inspect`
Dump of grouped database content for debugging.

#### `GET /database/reset`
**WARNING**: Wipes all data.

#### `GET /citation/{doc_id}/{page}/{bbox_str}`
Dynamically generates a PNG crop of the PDF page based on bounding box coordinates (format: `x0,y0,x1,y1`).
- **Response**: Image (image/png)
