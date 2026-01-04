import os

# Project Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Static Storage (Served via HTTP)
STATIC_DIR = os.path.join(DATA_DIR, "static")
PDF_DIR = os.path.join(STATIC_DIR, "pdfs")
IMAGE_DIR = os.path.join(STATIC_DIR, "images")

# Internal Processing Paths
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
VECTOR_DB_DIR = os.path.join(DATA_DIR, "vectordb")

# Upload (Temporary)
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")

# Tesseract Configuration


# Model Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyBq0k3xsFa8ggyD8kSaKkjIRVUMkDPoN_k")
GEMINI_MODEL = "gemini-2.5-pro"
