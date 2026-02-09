"""
GuardianPDF - Perplexity Analyzer

Detects AI-generated text using perplexity analysis.

Low perplexity = predictable text = likely AI-generated
High perplexity = unpredictable text = likely human-written
"""

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import numpy as np
from typing import Dict, List
import warnings

warnings.filterwarnings('ignore')


class PerplexityAnalyzer:
    """
    Analyze text perplexity to detect AI-generated content.
    
    Uses GPT-2 as the reference model to calculate perplexity.
    Lower perplexity indicates more "AI-like" text.
    """
    
    def __init__(self, model_name: str = "gpt2"):
        """
        Initialize perplexity analyzer.
        
        Args:
            model_name: HuggingFace model (default: gpt2)
        """
        print(f"Loading perplexity model: {model_name}...")
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.model.eval()
        
        # Set pad token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        print("✅ Perplexity analyzer ready")
    
    def calculate_perplexity(self, text: str, max_length: int = 512) -> float:
        """
        Calculate perplexity for a text chunk.
        
        Args:
            text: Input text
            max_length: Maximum sequence length
            
        Returns:
            Perplexity score (lower = more predictable/AI-like)
        """
        if not text.strip():
            return float('inf')
        
        # Tokenize
        encodings = self.tokenizer(
            text,
            return_tensors='pt',
            truncation=True,
            max_length=max_length,
            padding=True
        )
        
        # Calculate perplexity
        with torch.no_grad():
            outputs = self.model(**encodings, labels=encodings['input_ids'])
            loss = outputs.loss
            perplexity = torch.exp(loss).item()
        
        return perplexity
    
    def analyze_chunk(self, text: str) -> Dict[str, any]:
        """
        Analyze a chunk and classify as AI or human.
        
        Thresholds (empirically determined):
        - Perplexity < 30: High confidence AI
        - Perplexity 30-50: Moderate confidence AI
        - Perplexity 50-100: Uncertain
        - Perplexity > 100: Likely human
        
        Args:
            text: Text chunk to analyze
            
        Returns:
            Dict with 'perplexity', 'is_ai', 'confidence', 'label'
        """
        perplexity = self.calculate_perplexity(text)
        
        # Classify
        if perplexity < 30:
            is_ai = True
            confidence = 0.9
            label = "High probability AI-generated"
        elif perplexity < 50:
            is_ai = True
            confidence = 0.7
            label = "Moderate probability AI-generated"
        elif perplexity < 100:
            is_ai = None
            confidence = 0.5
            label = "Uncertain origin"
        else:
            is_ai = False
            confidence = 0.8
            label = "Likely human-written"
        
        return {
            "perplexity": round(perplexity, 2),
            "is_ai": is_ai,
            "confidence": round(confidence, 2),
            "label": label
        }
    
    def analyze_multiple(self, chunks: List[str]) -> List[Dict]:
        """
        Analyze multiple chunks.
        
        Args:
            chunks: List of text chunks
            
        Returns:
            List of analysis results
        """
        results = []
        
        print(f"Analyzing {len(chunks)} chunks for AI content...")
        for i, chunk in enumerate(chunks):
            result = self.analyze_chunk(chunk)
            result["chunk_index"] = i
            results.append(result)
            
            if (i + 1) % 10 == 0:
                print(f"  Processed {i + 1}/{len(chunks)} chunks")
        
        print("✅ Analysis complete")
        return results
    
    def get_document_summary(self, analysis_results: List[Dict]) -> Dict:
        """
        Summarize AI detection results for entire document.
        
        Args:
            analysis_results: List of chunk analysis results
            
        Returns:
            Summary statistics
        """
        if not analysis_results:
            return {}
        
        ai_chunks = sum(1 for r in analysis_results if r["is_ai"] is True)
        uncertain_chunks = sum(1 for r in analysis_results if r["is_ai"] is None)
        human_chunks = sum(1 for r in analysis_results if r["is_ai"] is False)
        
        total = len(analysis_results)
        avg_perplexity = np.mean([r["perplexity"] for r in analysis_results])
        
        # Overall classification
        ai_ratio = ai_chunks / total
        if ai_ratio > 0.5:
            overall_label = "Document contains significant AI-generated content"
            warning_level = "HIGH"
        elif ai_ratio > 0.2:
            overall_label = "Document contains some AI-generated content"
            warning_level = "MEDIUM"
        else:
            overall_label = "Document appears mostly human-written"
            warning_level = "LOW"
        
        return {
            "total_chunks": total,
            "ai_chunks": ai_chunks,
            "uncertain_chunks": uncertain_chunks,
            "human_chunks": human_chunks,
            "ai_percentage": round(ai_ratio * 100, 2),
            "average_perplexity": round(avg_perplexity, 2),
            "overall_label": overall_label,
            "warning_level": warning_level
        }
