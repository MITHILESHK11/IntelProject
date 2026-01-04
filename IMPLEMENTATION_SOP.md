# Standard Operating Procedure (SOP): Next-Gen RAG Upgrade

This document outlines the step-by-step procedure to upgrade the Enterprise Document Analyzer with Layout-Aware Extraction, Visual Citations, and Advanced Table Handling.

## Phase 1: Upgrade Extraction Logic (Docling Integration)

**Objective**: Replace basic text extraction with `Docling` to capture document layout, tables, and bounding boxes.

### Step 1.1: Installation
Add the following to your `requirements.txt` and install:
```bash
docling
pandas
```

### Step 1.2: Create New Parser Module
Create a new file `backend/parsers/docling_parser.py`:

1.  **Import Docling**: Use `DocumentConverter` from `docling.document_converter`.
2.  **Conversion Logic**:
    *   Initialize `DocumentConverter`.
    *   Convert the PDF file.
    *   Iterate through `doc.pages` and `page.cells` (or `text_elements`) to extract text chunks.
    *   **CRITICAL**: Capture the `bbox` (bounding box) for every paragraph/table. Format: `[x0, y0, x1, y1]`.
3.  **Output Structure**:
    Return a list of dicts:
    ```python
    {
        "text": "Extracted text content...",
        "page_num": 1,
        "bbox": [100.5, 200.0, 450.0, 250.0],
        "type": "text"  # or "table"
    }
    ```

### Step 1.3: Update Pipeline
Modify `backend/pipeline.py` to use `DoclingParser` instead of the current simple extractor.

---

## Phase 2: Visual Citation Architecture

**Objective**: Enable the specific cropping of PDF pages based on retrieval results "on the fly".

### Step 2.1: Update Metadata Storage
Ensure your `backend/custom_storage/metadata.py` saves the extra `bbox` field for every chunk.

### Step 2.2: Implement Crop API
Add a new endpoint to `backend/main.py` using `PyMuPDF` (already in use) to render crops.

**Functionality**:
1.  Receive `doc_id`, `page_num`, and `bbox`.
2.  Locate the original PDF in `data/static/pdfs`.
3.  Open PDF with `fitz.open()`.
4.  Load page: `page = doc.load_page(page_num)`.
5.  Set crop box: `page.set_cropbox(fitz.Rect(bbox))`.
6.  Render image: `pix = page.get_pixmap(dpi=150)`.
7.  Return bytes as `image/png`.

**Endpoint Signature**:
```python
@app.get("/citation/{doc_id}/{page}/{bbox_str}")
async def get_visual_citation(doc_id: str, page: int, bbox_str: str):
    # bbox_str format: "100,200,300,400"
    ...
```

---

## Phase 3: Frontend "Wow" Factors

**Objective**: specific UI changes to display the visual extraction.

### Step 3.1: Update Streamlit RAG Display
In `frontend/app.py`:
1.  When displaying retrieval results (the "Sources" expander), check if `metadata` contains a `bbox`.
2.  If `bbox` exists, construct the URL:
    `http://localhost:8000/citation/{doc_id}/{page}/{bbox}`
3.  Use `st.image(url)` to show the exact snippet of the PDF.

---

## Phase 4: Advanced Table Handling (Multi-Vector)

**Objective**: Fix the issue where tables are chopped up and become meaningless.

### Step 4.1: Decoupled Retrieval
1.  **Splitting**: When `Docling` identifies a Table element:
    *   **Do NOT** chunk it normally.
    *   Send the full HTML/Markdown of the table to an LLM (running locally or API) with the prompt: *"Summarize this table's key data points in 3 sentences."*
2.  **Storage**:
    *   **Vector Store**: Store the *Summary* embedding.
    *   **Doc Store**: Key-Value store where Key=UUID, Value=Original HTML Table.
3.  **Retrieval**:
    *   Search hits the Summary.
    *   Code retrieves the full HTML Table by UUID.
    *   LLM gets the full table in the `context`.

---

## Summary of Work
1.  **Install** `docling`.
2.  **Code** the `DoclingParser` class.
3.  **Add** `bbox` support to `MetadataStore`.
4.  **Create** `GET /citation` API.
5.  **Update** Streamlit to render images.
