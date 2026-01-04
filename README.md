# 🧠 Intel Nexus: Enterprise Document Analyzer

> **A Premium, Agentic Document Intelligence Platform** that combines Traditional OCR with Generative AI Vision.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Frontend](https://img.shields.io/badge/frontend-Streamlit-red)
![Backend](https://img.shields.io/badge/backend-FastAPI-green)
![AI](https://img.shields.io/badge/AI-Gemini%20Vision-purple)

---

## 👥 Meet the Team

This project was designed and developed by students from **Nutan College of Engineering and Research, Talegaon Dhabade, Pune** under **Intel Unnati Industrail Training 2025 Programme**.
Feel free to connect with us and explore our work!

### 👤 Mithilesh Kolhapurkar  

[![Email](https://img.shields.io/badge/Email-m.kolhapurkar3529%40gmail.com-red?style=flat&logo=gmail)](mailto:m.kolhapurkar3529@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Mithilesh%20Kolhapurkar-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/mithilesh-kolhapurkar-258001214)

---

### 👤 Ankita Patil  

[![Email](https://img.shields.io/badge/Email-95ankita.s.patil%40gmail.com-red?style=flat&logo=gmail)](mailto:95ankita.s.patil@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Ankita%20Patil-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/ankita-patil-10b0732ab/)

---

### 👤 Vedant Thorat  

[![Email](https://img.shields.io/badge/Email-vedantthorat019%40gmail.com-red?style=flat&logo=gmail)](mailto:vedantthorat019@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Vedant%20Thorat-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/vedant-thorat-156b8628b/)

---

## 🙏 Special Thanks

A huge thank you to our mentor for their guidance, insights, and continuous support throughout the development of this project.

**Prof. Priyanka Vyas**  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Priyanka%20Vyas-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/priyankavyas6/)

---
## 📸 Snapshots

| Landing Page | Dashboard & Chat |
| :---: | :---: |
| ![Landing](frontend/Images/landing_page.png) | ![Dashboard](frontend/Images/dashboard.png) |

| Inspector | Knowledge Base |
| :---: | :---: |
| ![Inspector](frontend/Images/inspector.png) | ![Database](frontend/Images/database_view.png) |

---

## 🎥 Demo Video

▶️ **Watch the full system walkthrough on YouTube**  
👉 https://youtu.be/nZSyUKTinMs

This video demonstrates:
- End-to-end document ingestion
- OCR vs Gemini Vision switching
- Visual RAG responses
- Inspector & Knowledge Base auditing

---

## 🌟 Overview

The **Intel Enterprise Document Analyzer** is designed to solve the "Last Mile" problem of document intelligence: extracting structured data from unstructured, messy real-world PDFs. By dynamically switching between **Tesseract OCR** (for speed) and **Google Gemini Vision** (for reasoning), it achieves high accuracy even on handwritten or complex documents.

[**📘 Read the Full User Guide**](USER_GUIDE.md)  
[**📘 Read the System Architecture**](ARCHITECTURE.md)  
[**📘 Read the API Reference**](API_REFERENCE.md)

### Key Capabilities
- **Hybrid Extraction Engine**: Automatically handles Digital vs. Scanned vs. Handwriting PDFs
- **Deep Artifact Extraction**: Isolates tables into DataFrames and crops images for separate indexing
- **Visual RAG**: Search results provide not just text, but visual "evidence" crops from the original PDF
- **Agentic Inspector**: Dedicated UI to audit every chunk, image, and table found in a document
- **Enterprise-Ready Pipeline**: Modular ingestion, parsing, chunking, embedding, and retrieval

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- **Python 3.9+**
- **Docling OCR**
- **Google Gemini API Key**

### Installation

1. **Clone & Install**
   ```bash
   git clone <repo>
   cd IntelProject
   pip install -r requirements.txt
   
2. Configure API Key

   ```bash
   Copy code
   export GOOGLE_API_KEY="your_api_key"
   # or configure inside backend/config.py
   Run the System (Two Terminals)

3. Backend (FastAPI):

   ```bash
   Copy code
   uvicorn backend.main:app --host 127.0.0.1 --port 8000
   Frontend (Streamlit):
   ```
   ```bash
   Copy code
   streamlit run frontend/app.py
   ```
## 📂 Data Directory Structure (Auto / Manual)

The backend expects the following structure:

   ```
   data/
   ├── processed/
   ├── uploads/
   ├── vectordb/
   └── static/
       ├── images/
       ├── pages/
       └── pdfs/
   ```

Create manually if needed:

   ```
   mkdir -p data/processed \
            data/static/images \
            data/static/pages \
            data/static/pdfs \
            data/uploads \
            data/vectordb
   ```
---

## 🧠 Architectural Highlights

FastAPI Backend: High-performance async API

Streamlit Frontend: Interactive enterprise dashboard

Vector Store: Persistent document embeddings

Vision + Text RAG: Multi-modal retrieval with visual grounding

Inspector Mode: Transparent AI auditing

---

## 🔐 Security & Configuration Notes

API keys are never hardcoded (recommended via environment variables)

Containers run isolated via Docker network

Designed for private VM / enterprise network usage

---

## 📚 Documentation

User Guide
: Detailed walkthrough of features

System Architecture
: Technical deep-dive

API Reference
: Backend endpoints

---

## 📜 License

MIT License

---

## ⭐ If you find this project useful

Give it a star ⭐ and feel free to fork or extend it for research, enterprise pilots, or hackathons.

