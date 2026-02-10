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

# Start GuardianPDF Web Interface
echo "Starting GuardianPDF Web Interface on http://localhost:8000"
echo "API checks available at http://localhost:8000/api/health"
echo ""
cd rag_engine
python app.py
