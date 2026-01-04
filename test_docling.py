from backend.parsers.docling_parser import DoclingParser
try:
    print("Initializing Docling...")
    parser = DoclingParser()
    print("Success!")
except Exception as e:
    print(f"Failed: {e}")
