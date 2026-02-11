"""
GuardianPDF - Enhanced FastAPI Backend with Security Features

Integrates Module 3 (Security Auditor) with Modules 1 & 2.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
from typing import Optional, List, Dict
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../cpp_engine/build"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../security_auditor"))

import pdf_shredder
from embeddings import EmbeddingGenerator
from vector_store import VectorStore
from rag_pipeline import RAGPipeline
from perplexity_analyzer import PerplexityAnalyzer
from signature_verifier import SignatureVerifier


# Pydantic models
class QueryRequest(BaseModel):
    question: str
    n_chunks: int = 3
    include_security: bool = True


class SecurityWarning(BaseModel):
    type: str
    severity: str
    message: str
    details: Optional[Dict] = None


class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict]
    security_warnings: List[SecurityWarning] = []
    metadata: Optional[Dict] = None


class UploadResponse(BaseModel):
    filename: str
    total_chunks: int
    unique_chunks: int
    integrity_verified: bool
    security_analysis: Dict
    warnings: List[str]
    message: str


# Initialize FastAPI app
app = FastAPI(
    title="GuardianPDF API - Audit-First Edition",
    description="PDF assistant with RAG and AI integrity verification",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
embedding_generator: Optional[EmbeddingGenerator] = None
vector_store: Optional[VectorStore] = None
rag_pipeline: Optional[RAGPipeline] = None
perplexity_analyzer: Optional[PerplexityAnalyzer] = None
signature_verifier: Optional[SignatureVerifier] = None

# Store AI analysis results per PDF
ai_analysis_cache: Dict[str, List[Dict]] = {}


@app.on_event("startup")
async def startup_event():
    """Initialize all components."""
    global embedding_generator, vector_store, rag_pipeline
    global perplexity_analyzer, signature_verifier
    
    print("🚀 Initializing GuardianPDF with Security Features...")
    
    # Module 2: RAG components
    embedding_generator = EmbeddingGenerator()
    
    persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
    vector_store = VectorStore(persist_directory=persist_dir)
    
    # Initialize RAG with provider from environment
    provider = os.getenv("LLM_PROVIDER", "nvidia").lower()
    
    if provider == "nvidia":
        api_key = os.getenv("NVIDIA_API_KEY")
        model = os.getenv("NVIDIA_MODEL", "meta/llama3-70b-instruct")
        
        if not api_key:
            print("⚠️  NVIDIA_API_KEY not found in environment")
            print("   Set it in .env file or environment variables")
            print("   Falling back to Ollama...")
            provider = "ollama"
    
    try:
        rag_pipeline = RAGPipeline(
            vector_store=vector_store,
            embedding_generator=embedding_generator,
            provider=provider,
            model_name=model if provider == "nvidia" else None,
            api_key=api_key if provider == "nvidia" else None
        )
    except Exception as e:
        print(f"❌ Error initializing RAG pipeline: {e}")
        print("   Please check your configuration")
        raise
    
    # Module 3: Security components
    perplexity_analyzer = PerplexityAnalyzer()
    signature_verifier = SignatureVerifier()
    
    print("✅ GuardianPDF ready with security auditing!")
    print(f"   Provider: {provider.upper()}")
    print(f"   Model: {rag_pipeline.model_name}")



@app.get("/api/health")
async def health_check():
    """Health check."""
    return {
        "service": "GuardianPDF - Audit-First Edition",
        "status": "online",
        "version": "2.0.0",
        "features": ["RAG", "AI Detection", "Integrity Verification"]
    }


@app.post("/upload_pdf", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...), verify_integrity: bool = True):
    """
    Upload and process PDF with security auditing.
    
    Steps:
    1. Verify PDF integrity (signatures, metadata)
    2. Process with C++ (extract → chunk → deduplicate)
    3. Analyze chunks for AI-generated content
    4. Generate embeddings
    5. Store in vector database with security metadata
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files supported")
    
    # Save temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        warnings = []
        
        # Ensure embedding model is unloaded to free space for AI detection
        if embedding_generator:
            embedding_generator.unload_model()
        
        # Step 1: Integrity verification
        integrity_result = {"verified": True}
        if verify_integrity:
            print(f"🔒 Verifying integrity: {file.filename}")
            integrity_result = signature_verifier.verify_pdf(tmp_path)
            if not integrity_result.get("verified", True):
                warnings.append(f"Integrity check failed: {integrity_result.get('error', 'Unknown')}")
            if "warnings" in integrity_result:
                warnings.extend(integrity_result["warnings"])
        
        # Step 2: C++ processing
        print(f"⚙️  Processing PDF: {file.filename}")
        chunks = pdf_shredder.process_pdf(
            tmp_path,
            chunk_size=500,
            overlap_size=50,
            dedup=True
        )
        
        if not chunks:
            raise HTTPException(status_code=400, detail="No text extracted")
        
        # Step 3: AI detection
        # (PerplexityAnalyzer handles its own loading/unloading)
        print(f"🔍 Analyzing for AI-generated content...")
        try:
            ai_analysis = perplexity_analyzer.analyze_multiple(chunks)
            ai_summary = perplexity_analyzer.get_document_summary(ai_analysis)
            
            # Cache AI analysis for this PDF
            ai_analysis_cache[file.filename] = ai_analysis
            
            # Add AI warnings
            if ai_summary["warning_level"] in ["MEDIUM", "HIGH"]:
                warnings.append(
                    f"{ai_summary['overall_label']} ({ai_summary['ai_percentage']}% AI)"
                )
        except Exception as e:
            print(f"⚠️  AI Detection skipped due to resource limits: {e}")
            # Generate placeholder analysis
            ai_analysis = [
                {
                    "perplexity": 0,
                    "is_ai": None,
                    "confidence": 0,
                    "label": "Analysis Skipped"
                }
                for _ in chunks
            ]
            ai_summary = {
                "overall_label": "AI Check Skipped (Resource Limit)",
                "warning_level": "LOW",
                "ai_percentage": 0,
                "ai_chunks": 0,
                "uncertain_chunks": len(chunks),
                "human_chunks": 0,
                "average_perplexity": 0
            }
            warnings.append("AI Detection skipped (Server Load)")
        
        # Explicit garbage collection to free model memory
        import gc
        gc.collect()
        
        # Step 4: Generate embeddings
        print(f"🧮 Generating embeddings...")
        # Explicitly load model now
        embedding_generator.load_model()
        embeddings = embedding_generator.generate(chunks)
        
        # Step 5: Store with security metadata
        if not ai_analysis:
            # Fallback metadata if AI check skipped
            metadata = [
                {
                    "source": file.filename,
                    "chunk_index": i,
                    "ai_probability": 0,
                    "perplexity": 0,
                    "security_label": "Checking Skipped"
                }
                for i in range(len(chunks))
            ]
        else:
            metadata = [
                {
                    "source": file.filename,
                    "chunk_index": i,
                    "ai_probability": result["confidence"] if result["is_ai"] else 0,
                    "perplexity": result["perplexity"],
                    "security_label": result["label"]
                }
                for i, result in enumerate(ai_analysis)
            ]
        
        vector_store.add_chunks(
            chunks=chunks,
            embeddings=embeddings.tolist(),
            metadata=metadata,
            pdf_name=file.filename
        )
        
        # Unload embedding model to save memory for next request
        embedding_generator.unload_model()
        
        return UploadResponse(
            filename=file.filename,
            total_chunks=len(chunks),
            unique_chunks=len(chunks),
            integrity_verified=integrity_result.get("verified", True),
            security_analysis=ai_summary,
            warnings=warnings,
            message=f"Processed with security analysis"
        )
        
    except Exception as e:
        # Ensure cleanup even on error
        if embedding_generator:
            embedding_generator.unload_model()
        if perplexity_analyzer:
            perplexity_analyzer.unload_model()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.post("/query", response_model=QueryResponse)
async def query_pdf(request: QueryRequest):
    """
    Query with RAG + security warnings.
    
    Returns answer with warnings if sources contain AI-generated content.
    """
    try:
        # Ensure embedding model is loaded for query embedding
        embedding_generator.load_model()
        
        # Get RAG answer
        result = rag_pipeline.query(
            question=request.question,
            n_chunks=request.n_chunks,
            include_metadata=True
        )
        
        # Unload model after query
        embedding_generator.unload_model()
        
        # Add security warnings
        security_warnings = []
        
        if request.include_security:
            for source in result["sources"]:
                source_name = source["source"]
                chunk_idx = source["chunk_index"]
                
                # Check cached AI analysis
                if source_name in ai_analysis_cache:
                    ai_results = ai_analysis_cache[source_name]
                    if chunk_idx < len(ai_results):
                        ai_data = ai_results[chunk_idx]
                        
                        if ai_data["is_ai"] and ai_data["confidence"] > 0.7:
                            security_warnings.append(SecurityWarning(
                                type="AI_GENERATED_CONTENT",
                                severity="HIGH" if ai_data["confidence"] > 0.8 else "MEDIUM",
                                message=ai_data["label"],
                                details={
                                    "chunk_index": chunk_idx,
                                    "confidence": ai_data["confidence"],
                                    "perplexity": ai_data["perplexity"]
                                }
                            ))
        
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            security_warnings=security_warnings,
            metadata=result.get("metadata")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/security/analysis/{filename}")
async def get_security_analysis(filename: str):
    """Get detailed security analysis for a PDF."""
    if filename not in ai_analysis_cache:
        raise HTTPException(status_code=404, detail="PDF not found in cache")
    
    ai_results = ai_analysis_cache[filename]
    summary = perplexity_analyzer.get_document_summary(ai_results)
    
    return {
        "filename": filename,
        "summary": summary,
        "chunk_analysis": ai_results
    }


@app.get("/stats")
async def get_stats():
    """System statistics."""
    vector_stats = vector_store.get_stats()
    
    return {
        "vector_store": vector_stats,
        "embedding_model": {
            "name": "all-MiniLM-L6-v2",
            "dimension": embedding_generator.get_dimension()
        },
        "llm_model": rag_pipeline.model_name,
        "security": {
            "ai_detection": "enabled",
            "integrity_check": "enabled",
            "cached_analyses": len(ai_analysis_cache)
        }
    }





@app.delete("/clear")
async def clear_database():
    """Clear all data."""
    vector_store.clear()
    ai_analysis_cache.clear()
    return {"message": "Database and cache cleared"}


# Mount frontend files (must be last to avoid overriding API routes)
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    print(f"⚠️ Warning: Frontend directory not found at {frontend_path}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
