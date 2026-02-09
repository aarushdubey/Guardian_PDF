# GuardianPDF - Production Image

# Stage 1: Build C++ module
FROM python:3.13-slim as cpp-builder

# Install C++ build dependencies
RUN apt-get update && apt-get install -y \
    g++ \
    cmake \
    make \
    libpoppler-cpp-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install pybind11
RUN pip install pybind11

# Copy C++ source
WORKDIR /app
COPY cpp_engine/ ./cpp_engine/

# Build C++ module
RUN cd cpp_engine && \
    mkdir -p build && \
    cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release && \
    make -j$(nproc)

# Stage 2: Production image
FROM python:3.13-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpoppler-cpp0v5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy built C++ module
COPY --from=cpp-builder /app/cpp_engine/build/*.so ./cpp_engine/build/

# Copy Python code
COPY rag_engine/ ./rag_engine/
COPY security_auditor/ ./security_auditor/
COPY .env.example .env
COPY start_server.sh ./

# Install Python dependencies
RUN pip install --no-cache-dir -r rag_engine/requirements.txt && \
    pip install --no-cache-dir -r security_auditor/requirements.txt

# Pre-download models (optional, increases image size but faster startup)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')" && \
    python -c "from transformers import GPT2LMHeadModel, GPT2Tokenizer; GPT2LMHeadModel.from_pretrained('gpt2'); GPT2Tokenizer.from_pretrained('gpt2')"

# Create volume for ChromaDB
VOLUME ["/app/chroma_db"]

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run
CMD ["python", "rag_engine/app.py"]
