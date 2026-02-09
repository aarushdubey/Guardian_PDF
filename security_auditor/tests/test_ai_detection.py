"""
GuardianPDF - Security Auditor Tests

Test AI detection and integrity verification.
"""

import pytest
import sys
import os

# Add paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(base_dir, "security_auditor"))

from perplexity_analyzer import PerplexityAnalyzer


class TestPerplexityAnalyzer:
    """Test AI detection via perplexity analysis."""
    
    @pytest.fixture
    def analyzer(self):
        """Create perplexity analyzer."""
        return PerplexityAnalyzer()
    
    def test_human_text_high_perplexity(self, analyzer):
        """Test that natural human text has higher perplexity."""
        # Natural, varied human text
        human_text = """
        The autumn leaves danced chaotically in the wind, their vibrant 
        colors painting an unexpected masterpiece against the gray sky. 
        Nobody could have predicted such beauty emerging from decay.
        """
        
        result = analyzer.analyze_chunk(human_text)
        
        # Human text should have higher perplexity
        assert result["perplexity"] > 30
        print(f"Human text perplexity: {result['perplexity']}")
    
    def test_ai_text_low_perplexity(self, analyzer):
        """Test that AI-generated text typically has lower perplexity."""
        # Typical AI-generated text (predictable patterns)
        ai_text = """
        The benefits of artificial intelligence are numerous and significant.
        First, AI can process large amounts of data quickly. Second, it can
        identify patterns that humans might miss. Third, it can automate
        repetitive tasks efficiently.
        """
        
        result = analyzer.analyze_chunk(ai_text)
        
        # AI text often has lower perplexity (more predictable)
        assert result["perplexity"] is not None
        assert "is_ai" in result
        print(f"AI-like text perplexity: {result['perplexity']}")
    
    def test_multiple_chunks_analysis(self, analyzer):
        """Test analyzing multiple chunks."""
        chunks = [
            "This is test chunk one.",
            "This is test chunk two.",
            "This is test chunk three."
        ]
        
        results = analyzer.analyze_multiple(chunks)
        
        assert len(results) == 3
        assert all("perplexity" in r for r in results)
        assert all("chunk_index" in r for r in results)
    
    def test_document_summary(self, analyzer):
        """Test document-level summary generation."""
        # Mock analysis results
        chunks = ["Test text"] * 10
        results = analyzer.analyze_multiple(chunks)
        
        summary = analyzer.get_document_summary(results)
        
        assert "total_chunks" in summary
        assert summary["total_chunks"] == 10
        assert "ai_percentage" in summary
        assert "warning_level" in summary


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
