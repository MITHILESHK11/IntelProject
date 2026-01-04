# 📘 User Guide: Enterprise Document Analyzer

## Introduction
The **Enterprise Document Analyzer** is a premium, AI-powered platform designed to extract, index, and query information from complex PDF documents. Whether dealing with digital text, scanned invoices, or handwritten notes, the system uses a hybrid approach combining traditional OCR and Google's Gemini Vision to ensure high-accuracy data retrieval.

---

## 🧭 Navigation
The application uses a streamlined 3-view interface. You can switch between views using the sidebar or context buttons.

### 1. Landing Page (Ingestion)
The starting point for all new workflows.
![Landing Page](images/landing_page.png)

**Features:**
- **Drag & Drop Upload**: Support for PDF files.
- **Previewer**: Instant visual confirmation of the file.
- **Extraction Modes**:
    - **OCR (Default)**: Best for standard digital PDFs or clean scans. Uses `Docling` and `Tesseract`.
    - **GEMINI**: Advanced AI Vision mode. Best for handwriting, poor scans, or complex layouts where OCR fails.
- **Ingest Button**: Starts the pipeline. This processes the document, extracts tables/images, creates vector chunks, and indexes them.

### 2. Dashboard
The main command center.
![Dashboard](images/dashboard.png)

#### A. 💬 Chat Interface
Interact with your indexed knowledge base using natural language.
- **History**: Switch between multiple conversation threads on the left.
- **Chat Window**: Ask questions like "What is the total revenue in Q3?" or "Summarize the safety protocols."
- **Citations**: 
    - **Quick Sources**: Small pills showing page numbers.
    - **Visual References**: The right-hand panel shows the exact text chunk and a **visual snapshot** of the source page with the relevant section highlighted.

#### B. 👁 Inspector
A deep-dive tool to verify extraction quality.
![Inspector](images/inspector.png)

- **Images Tab**: View all extracted figures, diagrams, and scanned pages. Click to zoom.
- **Tables Tab**: View extracted tables converted into interactive DataFrames.
- **Chunks Tab**: Audit the text chunks created during ingestion.
- **Full Doc**: View the original PDF in an embedded frame.

#### C. 💾 Database Management
Manage your knowledge repository.
![Database](images/database_view.png)

- **Document List**: See all indexed files.
- **Activate**: Switch the "Current Context" to a specific document for the Inspector.
- **Delete**: Remove a document and its vectors from the system.
- **Nuclear Reset**: A "Danger Zone" option to wipe the entire database clean.

---

## 🧠 Core Capabilities

### Hybrid Extraction Strategy
| Feature | OCR Mode | Gemini Vision Mode |
| :--- | :--- | :--- |
| **Speed** | Fast ⚡ | Slower (API dependant) 🐢 |
| **Cost** | Low (Local compute) | Higher (Token costs) |
| **Best For** | Contracts, Reports, Clean Forms | Handwritten notes, Faded receipts, Charts |
| **Table Extraction** | Heuristic/Structural | Visual Understanding |

### Intelligent RAG (Retrieval Augmented Generation)
1. **Query Analysis**: The system understands your question.
2. **Vector Search**: It retrieves the top 5 most relevant text chunks from ChromaDB.
3. **Synthesis**: Google Gemini summarizes the chunks into a coherent answer.
4. **Citation**: Every answer is backed by verifiable source evidence.
