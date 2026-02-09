#!/bin/bash
set -e

echo "🚀 Building GuardianPDF for Railway..."

# Install system dependencies
echo "📦 Installing system dependencies..."
apt-get update
apt-get install -y g++ cmake make libpoppler-cpp-dev git

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install --no-cache-dir pybind11
pip install --no-cache-dir -r rag_engine/requirements.txt
pip install --no-cache-dir -r security_auditor/requirements.txt

# Build C++ module
echo "⚙️  Building C++ module..."
cd cpp_engine
mkdir -p build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
cd ../..

# Pre-download models (reduces startup time)
echo "📥 Downloading AI models..."
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
python -c "from transformers import GPT2LMHeadModel, GPT2Tokenizer; GPT2LMHeadModel.from_pretrained('gpt2'); GPT2Tokenizer.from_pretrained('gpt2')"

echo "✅ Build complete!"
