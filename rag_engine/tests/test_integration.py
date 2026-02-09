"""
GuardianPDF - Integration Tests

Tests the complete Python-to-C++ pipeline.
"""

import pytest
import sys
import os

# Add paths - get absolute paths
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
cpp_build = os.path.join(base_dir, "cpp_engine", "build")
rag_engine = os.path.join(base_dir, "rag_engine")

sys.path.insert(0, cpp_build)
sys.path.insert(0, rag_engine)

import pdf_shredder
from embeddings import EmbeddingGenerator
from vector_store import VectorStore


class TestCppIntegration:
    """Test Python-C++ integration."""
    
    def test_import_module(self):
        """Test that C++ module can be imported."""
        assert hasattr(pdf_shredder, 'process_pdf')
        assert hasattr(pdf_shredder, 'PDFShredder')
        assert hasattr(pdf_shredder, 'TextChunker')
        assert hasattr(pdf_shredder, 'RabinKarpDeduplicator')
    
    def test_chunker_basic(self):
        """Test TextChunker basic functionality."""
        chunker = pdf_shredder.TextChunker(chunk_size=10, overlap_size=2)
        
        # Create test text
        text = " ".join([f"word{i}" for i in range(25)])
        chunks = chunker.chunk(text)
        
        assert len(chunks) > 0
        assert len(chunks) <= 3  # 25 words with chunk_size=10
    
    def test_deduplicator_removes_duplicates(self):
        """Test that deduplicator removes identical chunks."""
        dedup = pdf_shredder.RabinKarpDeduplicator(similarity_threshold=0.9)
        
        test_chunks = [
            "This is a test chunk",
            "This is another chunk",
            "This is a test chunk",  # Duplicate
            "Completely different text"
        ]
        
        unique = dedup.deduplicate(test_chunks)
        stats = dedup.get_stats()
        
        assert stats.original_count == 4
        assert stats.unique_count < 4
        assert stats.duplicates_removed > 0


class TestEmbeddings:
    """Test embedding generation."""
    
    @pytest.fixture
    def embedder(self):
        """Create embedding generator."""
        return EmbeddingGenerator()
    
    def test_embedding_generation(self, embedder):
        """Test that embeddings are generated correctly."""
        texts = ["This is a test", "Another test sentence"]
        embeddings = embedder.generate(texts)
        
        assert embeddings.shape[0] == 2
        assert embeddings.shape[1] == embedder.get_dimension()
    
    def test_single_embedding(self, embedder):
        """Test single text embedding."""
        text = "Single test sentence"
        embedding = embedder.generate_single(text)
        
        assert len(embedding) == embedder.get_dimension()


class TestVectorStore:
    """Test vector store operations."""
    
    @pytest.fixture
    def vector_store(self, tmp_path):
        """Create temporary vector store."""
        db_path = tmp_path / "test_db"
        return VectorStore(persist_directory=str(db_path))
    
    @pytest.fixture
    def embedder(self):
        """Create embedding generator."""
        return EmbeddingGenerator()
    
    def test_add_and_search(self, vector_store, embedder):
        """Test adding chunks and searching."""
        chunks = ["First test chunk", "Second test chunk", "Third test chunk"]
        embeddings = embedder.generate(chunks)
        
        # Add chunks
        vector_store.add_chunks(
            chunks=chunks,
            embeddings=embeddings.tolist(),
            pdf_name="test.pdf"
        )
        
        # Search
        query_embedding = embedder.generate_single("test chunk")
        results = vector_store.search(query_embedding.tolist(), n_results=2)
        
        assert len(results["documents"]) == 2
        assert len(results["metadatas"]) == 2
    
    def test_stats(self, vector_store, embedder):
        """Test getting statistics."""
        chunks = ["Test chunk"]
        embeddings = embedder.generate(chunks)
        
        vector_store.add_chunks(
            chunks=chunks,
            embeddings=embeddings.tolist(),
            pdf_name="test.pdf"
        )
        
        stats = vector_store.get_stats()
        assert stats["total_chunks"] >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
