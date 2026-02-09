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
        Initialize the embedding model.
        
        Args:
            model_name: HuggingFace model identifier
        """
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        print(f"✅ Model loaded | Dimensions: {self.embedding_dim}")
    
    def generate(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            numpy array of shape (len(texts), embedding_dim)
        """
        if not texts:
            return np.array([])
        
        # Batch encoding for efficiency
        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True  # L2 normalization for cosine similarity
        )
        
        return embeddings
    
    def generate_single(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.
        
        Args:
            text: Single text string
            
        Returns:
            numpy array of shape (embedding_dim,)
        """
        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        
        return embedding
    
    def get_dimension(self) -> int:
        """Get the embedding dimension."""
        return self.embedding_dim
