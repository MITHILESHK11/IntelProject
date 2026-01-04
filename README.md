# 🧠 Intel Nexus: Enterprise Document Analyzer

> **A Premium, Agentic Document Intelligence Platform** that combines Traditional OCR with Generative AI Vision.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Frontend](https://img.shields.io/badge/frontend-Streamlit-red)
![Backend](https://img.shields.io/badge/backend-FastAPI-green)
![AI](https://img.shields.io/badge/AI-Gemini%20Vision-purple)

---

## 📸 Snapshots

| Landing Page | Dashboard & Chat |
| :---: | :---: |
| ![Landing](docs/images/landing_page.png) | ![Dashboard](docs/images/dashboard.png) |

| Inspector | Knowledge Base |
| :---: | :---: |
| ![Inspector](docs/images/inspector.png) | ![Database](docs/images/database_view.png) |

---

## 🌟 Overview

The **Intel Enterprise Document Analyzer** is designed to solve the "Last Mile" problem of document intelligence: extracting structured data from unstructured, messy real-world PDFs. By dynamically switching between **Tesseract OCR** (for speed) and **Google Gemini Vision** (for reasoning), it achieves high accuracy even on handwritten or complex documents.

[**📘 Read the Full Architecture**](ARCHITECTURE.md)

### Key Capabilities
- **Hybrid Extraction Engine**: Automatically handles Digital vs. Scanned vs. Handwriting.
- **Deep Artifact Extraction**: Isolates tables into DataFrames and crops images for separate indexing.
- **Visual RAG**: Search results provide not just text, but visual "evidence" crops from the original PDF.
- **Agentic Inspector**: A dedicated UI to audit every chunk, image, and table found in a document.

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+**
- **Tesseract OCR** (Installed and in system PATH)
- **Google Cloud API Key** (for Gemini Vision)

### Installation

1. **Clone & Install**
   ```bash
   git clone <repo>
   pip install -r requirements.txt
   ```

2. **Configure Key**
   Export your Gemini API Key:
   ```bash
   export GOOGLE_API_KEY="your_api_key"
   # Or set in backend/config.py
   ```

3. **Run the System**
   You need two terminals:

   **Backend (API)**:
   ```bash
   uvicorn backend.main:app --host 127.0.0.1 --port 8000
   ```

   **Frontend (UI)**:
   ```bash
   streamlit run frontend/app.py
   ```

---

## 📚 Documentation
- [**User Guide**](docs/USER_GUIDE.md): Detailed walkthrough of features.
- [**System Architecture**](docs/ARCHITECTURE.md): Technical deep-dive.
- [**API Reference**](docs/API_REFERENCE.md): Backend endpoints.

---

## 🛠️ utility: Screenshot Capture
To generate the images for this README, ensure the app is running and execute:
```bash
pip install playwright
playwright install
python util/capture_screenshots.py
```

## 📜 License
MIT
