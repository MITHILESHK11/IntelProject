import time
import requests
import os
import sys

API_URL = "http://127.0.0.1:8000"

def benchmark_system(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"--- Benchmarking with {os.path.basename(file_path)} ---")
    
    # 1. Upload & Process
    start_time = time.time()
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(f"{API_URL}/upload", files=files)
    
    end_time = time.time()
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Ingestion Success")
        print(f"   - Time Taken: {end_time - start_time:.2f} seconds")
        print(f"   - Chunks Created: {data.get('chunks')}")
        print(f"   - Tables Extracted: {data.get('tables')}")
    else:
        print(f"❌ Ingestion Failed: {response.text}")
        return

    # 2. Search Latency
    query = "test query"
    start_time = time.time()
    requests.get(f"{API_URL}/search", params={"q": query})
    end_time = time.time()
    
    print(f"✅ Search Latency: {(end_time - start_time) * 1000:.2f} ms")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python benchmarks.py <path_to_pdf>")
    else:
        benchmark_system(sys.argv[1])
