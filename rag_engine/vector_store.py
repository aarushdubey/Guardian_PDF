"""
GuardianPDF - Vector Store Module

ChromaDB wrapper for storing and retrieving PDF chunks with embeddings.
Provides semantic search capabilities for RAG.
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import os


class VectorStore:
    """
    ChromaDB-based vector store for PDF chunks.
    
    Stores:
    - Text chunks
    - Embeddings
    - Metadata (page number, chunk index, source file)
    """
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Initialize ChromaDB client.
        
        Args:
            persist_directory: Directory to persist the database
        """
        os.makedirs(persist_directory, exist_ok=True)
        
        # Use PersistentClient for data persistence
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="guardian_pdf_chunks",
            metadata={"description": "PDF chunks with integrity metadata"}
        )
        
        print(f"✅ Vector store initialized | Collection: {self.collection.name}")
    
    def add_chunks(
        self,
        chunks: List[str],
        embeddings: List[List[float]],
        metadata: Optional[List[Dict]] = None,
        pdf_name: str = "unknown"
    ) -> None:
        """
        Add chunks to the vector store.
        
        Args:
            chunks: List of text chunks
            embeddings: List of embedding vectors
            metadata: Optional metadata for each chunk
            pdf_name: Source PDF filename
        """
        if not chunks:
            return
        
        # Generate IDs
        ids = [f"{pdf_name}_chunk_{i}" for i in range(len(chunks))]
        
        # Prepare metadata
        if metadata is None:
            metadata = [{"source": pdf_name, "chunk_index": i} for i in range(len(chunks))]
        else:
            # Ensure source is included
            for i, meta in enumerate(metadata):
                meta["source"] = pdf_name
                meta["chunk_index"] = i
        
        # Add to collection
        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadata
        )
        
        print(f"✅ Added {len(chunks)} chunks to vector store")
    
    def search(
        self,
        query_embedding: List[float],
        n_results: int = 3,
        filter_metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Search for similar chunks using query embedding.
        
        Args:
            query_embedding: Query vector
            n_results: Number of results to return
            filter_metadata: Optional metadata filter
            
        Returns:
            Dict with 'documents', 'metadatas', and 'distances'
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter_metadata
        )
        
        return {
            "documents": results["documents"][0] if results["documents"] else [],
            "metadatas": results["metadatas"][0] if results["metadatas"] else [],
            "distances": results["distances"][0] if results["distances"] else []
        }
    
    def clear(self) -> None:
        """Clear all chunks from the collection."""
        # Delete and recreate collection
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(
            name="guardian_pdf_chunks",
            metadata={"description": "PDF chunks with integrity metadata"}
        )
        print("✅ Vector store cleared")
    
    def get_stats(self) -> Dict:
        """Get collection statistics."""
        count = self.collection.count()
        return {
            "total_chunks": count,
            "collection_name": self.collection.name
        }
