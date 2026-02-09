"""
GuardianPDF - RAG Pipeline Module

Orchestrates Retrieval-Augmented Generation:
1. Retrieve relevant chunks from vector store
2. Construct prompt with context
3. Call LLM for grounded answer
"""

from typing import List, Dict, Optional
import ollama
from embeddings import EmbeddingGenerator
from vector_store import VectorStore


class RAGPipeline:
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
