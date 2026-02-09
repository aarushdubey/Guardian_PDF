#!/bin/bash

# GuardianPDF Server Startup Script

echo "🚀 Starting GuardianPDF Server..."
echo ""

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "⚠️  Ollama not running. Starting Ollama..."
    echo "   If not installed: brew install ollama"
    echo "   Then run: ollama serve"
    echo ""
fi

# Activate virtual environment
source venv/bin/activate

# Start FastAPI server
echo "Starting FastAPI backend on http://localhost:8000"
echo ""
cd rag_engine
python app.py
