"""
GuardianPDF - Embeddings Module

Converts text chunks into vector embeddings using HuggingFace models.
Uses sentence-transformers for efficient, high-quality embeddings.
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List


class EmbeddingGenerator:
    """
    Generate embeddings for text chunks using HuggingFace sentence-transformers.
    
    Default model: all-MiniLM-L6-v2
    - Lightweight (~80MB)
    - Fast inference
    - Good quality (384 dimensions)
    - Ideal for semantic search
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding model configuration.
        
        Args:
            model_name: HuggingFace model identifier
        """
        print(f"Configuring embedding model: {model_name} (Lazy Load)")
        self.model_name = model_name
        self.model = None
        self.embedding_dim = 384  # Hardcoded for all-MiniLM-L6-v2, updated on load
        
    def load_model(self):
        """Load model into memory."""
        if self.model is not None:
            return
            
        print(f"Loading embedding model: {self.model_name}...")
        self.model = SentenceTransformer(self.model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        print(f"✅ Embedding model loaded | Dimensions: {self.embedding_dim}")
        
    def unload_model(self):
        """Unload model from memory."""
        print("Unloading embedding model to free memory...")
        self.model = None
        import gc
        gc.collect()
        print("✅ Embedding model unloaded")
    
    def generate(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings with auto-loading."""
        if not texts:
            return np.array([])
            
        # Ensure model is loaded
        was_loaded = self.model is not None
        if not was_loaded:
            self.load_model()
        
        try:
            # Batch encoding for efficiency
            embeddings = self.model.encode(
                texts,
                show_progress_bar=True,
                convert_to_numpy=True,
                normalize_embeddings=True
            )
            return embeddings
        finally:
            # If we auto-loaded just for this call, maybe unload?
            # For now, keep loaded as it's used frequently in RAG
            pass
    
    def generate_single(self, text: str) -> np.ndarray:
        """Generate single embedding."""
        was_loaded = self.model is not None
        if not was_loaded:
            self.load_model()
            
        try:
            embedding = self.model.encode(
                text,
                convert_to_numpy=True,
                normalize_embeddings=True
            )
            return embedding
        finally:
            pass
            
    def get_dimension(self) -> int:
        """Get the embedding dimension."""
        if self.model:
            return self.model.get_sentence_embedding_dimension()
        return self.embedding_dim
