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
    
    def __init__(self, model_name: str = "distilgpt2"):
        """
        Initialize perplexity analyzer configuration (lazy loading).
        
        Args:
            model_name: HuggingFace model (default: distilgpt2)
        """
        print(f"Configuring perplexity model: {model_name} (Lazy Load)")
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        
    def load_model(self):
        """Load model into memory."""
        if self.model is not None:
            return
            
        print(f"Loading perplexity model: {self.model_name}...")
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)
        self.model.eval()
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        print("✅ Perplexity model loaded")
        
    def unload_model(self):
        """Unload model from memory."""
        print("Unloading perplexity model to free memory...")
        self.tokenizer = None
        self.model = None
        import gc
        gc.collect()
        print("✅ Perplexity model unloaded")
    
    def calculate_perplexity(self, text: str, max_length: int = 512) -> float:
        """Calculate perplexity with error handling for unloaded model."""
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
            
        if not text.strip():
            return float('inf')
        
        # Tokenize (cpu only)
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
        """Analyze a single chunk."""
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
        Analyze multiple chunks with automatic model loading/unloading.
        """
        results = []
        
        try:
            self.load_model()
            
            print(f"Analyzing {len(chunks)} chunks for AI content...")
            for i, chunk in enumerate(chunks):
                result = self.analyze_chunk(chunk)
                result["chunk_index"] = i
                results.append(result)
                
                if (i + 1) % 10 == 0:
                    print(f"  Processed {i + 1}/{len(chunks)} chunks")
            
            print("✅ Analysis complete")
            return results
            
        finally:
            # Always ensure we unload to free up RAM for RAG/Vectors
            self.unload_model()
    
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
