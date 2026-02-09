# GuardianPDF - Quick Start Guide

Get GuardianPDF running in under 5 minutes!

## Prerequisites

```bash
# macOS
brew install poppler pybind11 catch2 cmake ollama

# Verify installations
clang++ --version  # Should be 17+
cmake --version    # Should be 4.2+
python3 --version  # Should be 3.10+
```

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/guardian_pdf
cd guardian_pdf
```

### 2. Build C++ Module (1 minute)

```bash
cd cpp_engine
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j4
cd ../..
```

**Verify**:
```bash
./cpp_engine/build/test_pdfshredder
# Should show: ✅ All tests passed (11 assertions)
```

### 3. Set Up Python Environment (2 minutes)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r rag_engine/requirements.txt
pip install -r security_auditor/requirements.txt
```

### 4. Pull LLM Model (1 minute)

```bash
ollama pull llama3.2:latest
```

## Run GuardianPDF

### Start Server

```bash
./start_server.sh
```

Server runs at: `http://localhost:8000`

### Test the System

**Terminal 1** (server running):
```bash
./start_server.sh
```

**Terminal 2** (testing):
```bash
# Test with API client
python test_api.py

# Test security features
python test_security.py

# Or test with curl
curl http://localhost:8000/
```

## Your First Query

### 1. Upload a PDF

```bash
curl -X POST http://localhost:8000/upload_pdf \
  -F "file=@your_document.pdf"
```

Response shows:
- Chunk count
- AI detection summary  
- Integrity verification
- Security warnings (if any)

### 2. Ask Questions

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is this document about?",
    "n_chunks": 3,
    "include_security": true
  }'
```

You'll get:
- ✅ AI-generated answer
- 📚 Source citations
- ⚠️  Security warnings (if AI-generated content detected)

## Quick Tests

### Test AI Detection

```bash
python test_security.py
```

Expected output:
```
✅ Human text → Perplexity ~70 → "Uncertain/Human"
✅ AI text → Perplexity ~25 → "High probability AI"
```

### Test C++ Performance

```python
import sys
sys.path.insert(0, 'cpp_engine/build')
import pdf_shredder

chunks = pdf_shredder.process_pdf("test.pdf")
print(f"Extracted {len(chunks)} chunks")
```

## Troubleshooting

**Ollama not running**:
```bash
ollama serve
# In another terminal:
ollama pull llama3.2:latest
```

**C++ build fails**:
```bash
# Install dependencies
brew install poppler pybind11 catch2

# Clean build
rm -rf cpp_engine/build
cd cpp_engine && mkdir build && cd build
cmake .. && make -j4
```

**Import errors**:
```bash
export PYTHONPATH="${PWD}/cpp_engine/build:${PWD}/rag_engine:${PYTHONPATH}"
```

**Port 8000 in use**:
```bash
# Edit rag_engine/app.py, change port to 8001
uvicorn.run(app, host="0.0.0.0", port=8001)
```

## Next Steps

- 📖 Read the full [README](README.md)
- 🧪 Run all tests: `pytest rag_engine/tests/ -v`
- 🔒 Explore security features: `python test_security.py your.pdf`
- 📊 Check system stats: `curl http://localhost:8000/stats`

## Architecture Overview

```
┌─────────────────────────────────────────┐
│           Your PDF Document              │
└──────────────┬──────────────────────────┘
               │
       ┌───────▼────────┐
       │  Module 1: C++  │  (7.5x faster)
       │  PDFShredder    │
       └───────┬────────┘
               │
       ┌───────▼────────┐
       │  Module 3:      │  AI Detection
       │  Security       │  Integrity Check
       └───────┬────────┘
               │
       ┌───────▼────────┐
       │  Module 2:      │  Embeddings
       │  RAG Engine     │  ChromaDB
       └───────┬────────┘
               │
          ┌────▼─────┐
          │  Ollama  │  LLM Answer
          │  (Local) │  + Warnings
          └──────────┘
```

## Need Help?

- 🐛 [Report Issues](https://github.com/yourusername/guardian_pdf/issues)
- 📧 Email: your.email@example.com
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/guardian_pdf/discussions)

---

**Built with ❤️ for secure, intelligent PDF processing**
