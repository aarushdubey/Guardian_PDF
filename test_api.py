#!/usr/bin/env python3
"""
GuardianPDF - API Test Client

Simple client to test the FastAPI backend.
"""

import requests
import json
import sys


BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint."""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200


def upload_pdf(filepath: str):
    """Upload a PDF file."""
    print(f"Uploading PDF: {filepath}...")
    
    with open(filepath, 'rb') as f:
        files = {'file': (filepath.split('/')[-1], f, 'application/pdf')}
        response = requests.post(f"{BASE_URL}/upload_pdf", files=files)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Upload successful!")
        print(f"   Filename: {data['filename']}")
        print(f"   Total chunks: {data['total_chunks']}")
        print(f"   Unique chunks: {data['unique_chunks']}\n")
        return True
    else:
        print(f"❌ Error: {response.text}\n")
        return False


def query(question: str, n_chunks: int = 3):
    """Ask a question."""
    print(f"Asking: '{question}'...")
    
    payload = {
        "question": question,
        "n_chunks": n_chunks
    }
    
    response = requests.post(f"{BASE_URL}/query", json=payload)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"\n📝 Answer:\n{data['answer']}\n")
        print(f"📚 Sources ({len(data['sources'])}):")
        for i, source in enumerate(data['sources'], 1):
            print(f"   {i}. {source['source']} (chunk {source['chunk_index']})")
            print(f"      Relevance: {source['relevance_score']:.2%}")
            print(f"      Preview: {source['text'][:100]}...\n")
        return True
    else:
        print(f"❌ Error: {response.text}\n")
        return False


def get_stats():
    """Get system statistics."""
    print("Getting stats...")
    response = requests.get(f"{BASE_URL}/stats")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Stats: {json.dumps(response.json(), indent=2)}\n")
        return True
    return False


def main():
    """Run test suite."""
    print("=" * 60)
    print("GuardianPDF API Test Client")
    print("=" * 60)
    print()
    
    # Test 1: Health check
    if not test_health():
        print("⚠️  Server not running. Start with:")
        print("   cd rag_engine && source ../venv/bin/activate && python app.py")
        sys.exit(1)
    
    # Test 2: Get stats
    get_stats()
    
    # Test 3: Upload PDF (if provided)
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        if upload_pdf(pdf_path):
            # Test 4: Query
            query("What is this document about?")
            query("Summarize the main points")
    else:
        print("💡 To test PDF upload, run:")
        print("   python test_api.py path/to/your.pdf")
    
    print("=" * 60)
    print("✅ Tests complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
