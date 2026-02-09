"""
GuardianPDF - RAG Pipeline Module

Orchestrates Retrieval-Augmented Generation with multiple LLM providers:
- NVIDIA AI API (recommended)
- Ollama (local)
"""

from typing import List, Dict, Optional
import os
from embeddings import EmbeddingGenerator
from vector_store import VectorStore


class RAGPipeline:
    """
    Complete RAG pipeline for question answering over PDFs.
    
    Supports multiple LLM providers:
    - NVIDIA AI (meta/llama3-70b-instruct, etc.)
    - Ollama (local models)
    """
    
    def __init__(
        self,
        vector_store: VectorStore,
        embedding_generator: EmbeddingGenerator,
        provider: str = "nvidia",
        model_name: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize RAG pipeline.
        
        Args:
            vector_store: Vector store instance
            embedding_generator: Embedding generator instance
            provider: LLM provider ('nvidia' or 'ollama')
            model_name: Model name (provider-specific)
            api_key: API key (for NVIDIA)
        """
        self.vector_store = vector_store
        self.embeddings = embedding_generator
        self.provider = provider.lower()
        
        # Set up provider-specific configuration
        if self.provider == "nvidia":
            self._setup_nvidia(model_name, api_key)
        elif self.provider == "ollama":
            self._setup_ollama(model_name)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def _setup_nvidia(self, model_name: Optional[str], api_key: Optional[str]):
        """Set up NVIDIA AI API."""
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("Please install openai: pip install openai")
        
        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv("NVIDIA_API_KEY")
        if not self.api_key:
            raise ValueError(
                "NVIDIA API key required. Set NVIDIA_API_KEY environment variable "
                "or pass api_key parameter"
            )
        
        # Default to llama3-70b-instruct
        self.model_name = model_name or os.getenv(
            "NVIDIA_MODEL", 
            "meta/llama3-70b-instruct"
        )
        
        # Initialize NVIDIA client
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=self.api_key
        )
        
        print(f"✅ NVIDIA AI ready: {self.model_name}")
    
    def _setup_ollama(self, model_name: Optional[str]):
        """Set up Ollama (local LLM)."""
        try:
            import ollama
            self.ollama = ollama
        except ImportError:
            raise ImportError("Please install ollama: pip install ollama")
        
        self.model_name = model_name or "llama3.2:latest"
        
        # Verify Ollama model
        try:
            self.ollama.show(self.model_name)
            print(f"✅ Ollama model ready: {self.model_name}")
        except Exception as e:
            print(f"⚠️  Warning: Ollama model '{self.model_name}' not found")
            print(f"   Run: ollama pull {self.model_name}")
    
    def query(
        self,
        question: str,
        n_chunks: int = 3,
        include_metadata: bool = True
    ) -> Dict[str, any]:
        """
        Answer a question using RAG.
        
        Args:
            question: User's question
            n_chunks: Number of chunks to retrieve
            include_metadata: Include source metadata in response
            
        Returns:
            Dict with 'answer', 'sources', and optional 'metadata'
        """
        # Step 1: Embed the question
        query_embedding = self.embeddings.generate_single(question)
        
        # Step 2: Retrieve relevant chunks
        search_results = self.vector_store.search(
            query_embedding=query_embedding.tolist(),
            n_results=n_chunks
        )
        
        chunks = search_results["documents"]
        metadatas = search_results["metadatas"]
        distances = search_results["distances"]
        
        if not chunks:
            return {
                "answer": "No relevant information found in the PDF.",
                "sources": [],
                "metadata": None
            }
        
        # Step 3: Construct prompt with context
        context = "\n\n".join([
            f"[Context {i+1}] {chunk}"
            for i, chunk in enumerate(chunks)
        ])
        
        prompt = self._build_prompt(question, context)
        
        # Step 4: Call LLM (provider-specific)
        try:
            if self.provider == "nvidia":
                answer = self._query_nvidia(prompt)
            else:  # ollama
                answer = self._query_ollama(prompt)
        except Exception as e:
            answer = f"Error calling {self.provider.upper()}: {str(e)}"
        
        # Step 5: Prepare response
        result = {
            "answer": answer,
            "sources": [
                {
                    "text": chunk[:200] + "...",  # Preview
                    "source": meta.get("source", "unknown"),
                    "chunk_index": meta.get("chunk_index", 0),
                    "relevance_score": 1 - dist  # Convert distance to similarity
                }
                for chunk, meta, dist in zip(chunks, metadatas, distances)
            ]
        }
        
        if include_metadata:
            result["metadata"] = {
                "n_chunks_retrieved": len(chunks),
                "model": self.model_name,
                "provider": self.provider
            }
        
        return result
    
    def _query_nvidia(self, prompt: str) -> str:
        """Query NVIDIA AI API."""
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are GuardianPDF, an AI assistant that answers questions based strictly on provided PDF context. Never make up information."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=1024
        )
        
        return completion.choices[0].message.content
    
    def _query_ollama(self, prompt: str) -> str:
        """Query Ollama (local LLM)."""
        response = self.ollama.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are GuardianPDF, an AI assistant that answers questions based strictly on provided PDF context. Never make up information."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        return response["message"]["content"]
    
    def _build_prompt(self, question: str, context: str) -> str:
        """
        Build RAG prompt with context.
        
        Args:
            question: User's question
            context: Retrieved context chunks
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""Based on the following context from a PDF document, answer the question.

Context:
{context}

Question: {question}

Instructions:
- Answer ONLY based on the provided context
- If the context doesn't contain relevant information, say so
- Be concise and accurate
- Quote specific parts of the context when relevant

Answer:"""
        
        return prompt

    """
    Complete RAG pipeline for question answering over PDFs.
    
    Uses:
    - EmbeddingGenerator: Convert questions to vectors
    - VectorStore: Retrieve relevant chunks
    - Ollama: Generate grounded answers
    """
    
    def __init__(
        self,
        vector_store: VectorStore,
        embedding_generator: EmbeddingGenerator,
        model_name: str = "llama3.2:latest"
    ):
        """
        Initialize RAG pipeline.
        
        Args:
            vector_store: Vector store instance
            embedding_generator: Embedding generator instance
            model_name: Ollama model name
        """
        self.vector_store = vector_store
        self.embeddings = embedding_generator
        self.model_name = model_name
        
        # Verify Ollama model is available
        try:
            ollama.show(model_name)
            print(f"✅ Ollama model ready: {model_name}")
        except Exception as e:
            print(f"⚠️  Warning: Ollama model '{model_name}' not found")
            print(f"   Run: ollama pull {model_name}")
    
    def query(
        self,
        question: str,
        n_chunks: int = 3,
        include_metadata: bool = True
    ) -> Dict[str, any]:
        """
        Answer a question using RAG.
        
        Args:
            question: User's question
            n_chunks: Number of chunks to retrieve
            include_metadata: Include source metadata in response
            
        Returns:
            Dict with 'answer', 'sources', and optional 'metadata'
        """
        # Step 1: Embed the question
        query_embedding = self.embeddings.generate_single(question)
        
        # Step 2: Retrieve relevant chunks
        search_results = self.vector_store.search(
            query_embedding=query_embedding.tolist(),
            n_results=n_chunks
        )
        
        chunks = search_results["documents"]
        metadatas = search_results["metadatas"]
        distances = search_results["distances"]
        
        if not chunks:
            return {
                "answer": "No relevant information found in the PDF.",
                "sources": [],
                "metadata": None
            }
        
        # Step 3: Construct prompt with context
        context = "\n\n".join([
            f"[Context {i+1}] {chunk}"
            for i, chunk in enumerate(chunks)
        ])
        
        prompt = self._build_prompt(question, context)
        
        # Step 4: Call LLM
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are GuardianPDF, an AI assistant that answers questions based strictly on provided PDF context. Never make up information."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            answer = response["message"]["content"]
        except Exception as e:
            answer = f"Error calling Ollama: {str(e)}"
        
        # Step 5: Prepare response
        result = {
            "answer": answer,
            "sources": [
                {
                    "text": chunk[:200] + "...",  # Preview
                    "source": meta.get("source", "unknown"),
                    "chunk_index": meta.get("chunk_index", 0),
                    "relevance_score": 1 - dist  # Convert distance to similarity
                }
                for chunk, meta, dist in zip(chunks, metadatas, distances)
            ]
        }
        
        if include_metadata:
            result["metadata"] = {
                "n_chunks_retrieved": len(chunks),
                "model": self.model_name
            }
        
        return result
    
    def _build_prompt(self, question: str, context: str) -> str:
        """
        Build RAG prompt with context.
        
        Args:
            question: User's question
            context: Retrieved context chunks
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""Based on the following context from a PDF document, answer the question.

Context:
{context}

Question: {question}

Instructions:
- Answer ONLY based on the provided context
- If the context doesn't contain relevant information, say so
- Be concise and accurate
- Quote specific parts of the context when relevant

Answer:"""
        
        return prompt
