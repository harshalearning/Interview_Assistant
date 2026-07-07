"""RAG module for retrieval-augmented generation."""

from typing import List, Dict, Any, Optional
import json
from datetime import datetime

class VectorStore:
    """Vector database for storing and retrieving embeddings."""
    
    def __init__(self, collection_name: str = "interview-knowledge"):
        """Initialize vector store.
        
        Args:
            collection_name: Name of ChromaDB collection
        """
        self.collection_name = collection_name
        try:
            import chromadb
            self.client = chromadb.Client()
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            self.available = True
        except Exception as e:
            print(f"ChromaDB initialization warning: {e}")
            self.client = None
            self.collection = None
            self.available = False
    
    async def add_documents(
        self,
        documents: List[str],
        metadatas: List[Dict[str, Any]] = None,
        ids: List[str] = None
    ) -> bool:
        """Add documents to vector store.
        
        Args:
            documents: List of document texts
            metadatas: Optional metadata for each document
            ids: Optional IDs for documents
            
        Returns:
            Success status
        """
        if not self.available:
            print("Vector store not available")
            return False
        
        try:
            if ids is None:
                ids = [f"doc_{i}" for i in range(len(documents))]
            
            if metadatas is None:
                metadatas = [{"source": "interview"} for _ in documents]
            
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            return True
        except Exception as e:
            print(f"Error adding documents: {e}")
            return False
    
    async def query(
        self,
        query_text: str,
        n_results: int = 5,
        where: Optional[Dict] = None
    ) -> dict:
        """Query vector store for similar documents.
        
        Args:
            query_text: Query text
            n_results: Number of results to return
            where: Optional filtering criteria
            
        Returns:
            Query results
        """
        if not self.available:
            return {"results": [], "error": "Vector store not available"}
        
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where=where
            )
            return {
                "query": query_text,
                "results": results.get("documents", [[]])[0],
                "distances": results.get("distances", [[]])[0],
                "metadatas": results.get("metadatas", [[]])[0]
            }
        except Exception as e:
            return {"error": str(e), "results": []}
    
    async def delete_documents(self, ids: List[str]) -> bool:
        """Delete documents from vector store.
        
        Args:
            ids: Document IDs to delete
            
        Returns:
            Success status
        """
        if not self.available:
            return False
        
        try:
            self.collection.delete(ids=ids)
            return True
        except Exception as e:
            print(f"Error deleting documents: {e}")
            return False


class EmbeddingGenerator:
    """Generate embeddings for text."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize embedding generator.
        
        Args:
            model_name: HuggingFace model name
        """
        self.model_name = model_name
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
            self.available = True
        except Exception as e:
            print(f"Embedding model initialization warning: {e}")
            self.model = None
            self.available = False
    
    async def encode(self, texts: List[str]) -> list:
        """Encode texts to embeddings.
        
        Args:
            texts: List of texts to encode
            
        Returns:
            List of embeddings
        """
        if not self.available:
            return []
        
        try:
            embeddings = self.model.encode(texts, convert_to_tensor=False)
            return embeddings.tolist()
        except Exception as e:
            print(f"Error encoding texts: {e}")
            return []
    
    async def similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0-1)
        """
        if not self.available:
            return 0.0
        
        try:
            from sentence_transformers.util import cos_sim
            embeddings = self.model.encode([text1, text2])
            similarity = cos_sim(embeddings[0], embeddings[1]).item()
            return float(similarity)
        except Exception as e:
            print(f"Error calculating similarity: {e}")
            return 0.0


class KnowledgeBase:
    """Manage interview knowledge base."""
    
    def __init__(self):
        """Initialize knowledge base."""
        self.vector_store = VectorStore()
        self.embedding_generator = EmbeddingGenerator()
        self.documents = {}
    
    async def index_knowledge(
        self,
        topic: str,
        content: str,
        metadata: Dict[str, Any] = None
    ) -> bool:
        """Index knowledge about a topic.
        
        Args:
            topic: Topic name
            content: Knowledge content
            metadata: Additional metadata
            
        Returns:
            Success status
        """
        doc_id = f"{topic}_{len(self.documents)}"
        
        if metadata is None:
            metadata = {}
        
        metadata.update({
            "topic": topic,
            "created_at": datetime.utcnow().isoformat()
        })
        
        self.documents[doc_id] = {
            "topic": topic,
            "content": content,
            "metadata": metadata
        }
        
        return await self.vector_store.add_documents(
            documents=[content],
            metadatas=[metadata],
            ids=[doc_id]
        )
    
    async def retrieve_context(
        self,
        question: str,
        topic: str = None,
        n_results: int = 3
    ) -> List[str]:
        """Retrieve relevant context for a question.
        
        Args:
            question: Question to find context for
            topic: Optional topic filter
            n_results: Number of results
            
        Returns:
            List of relevant context documents
        """
        where = None
        if topic:
            where = {"topic": {"$eq": topic}}
        
        results = await self.vector_store.query(
            query_text=question,
            n_results=n_results,
            where=where
        )
        
        return results.get("results", [])
    
    async def get_question_hints(
        self,
        question: str,
        n_hints: int = 3
    ) -> List[str]:
        """Get hints for answering a question.
        
        Args:
            question: Question to get hints for
            n_hints: Number of hints
            
        Returns:
            List of helpful hints
        """
        context = await self.retrieve_context(question, n_results=n_hints)
        
        hints = [
            f"Tip {i+1}: {doc[:100]}..."
            for i, doc in enumerate(context)
        ]
        
        return hints


class ContextInjector:
    """Inject context into prompts for RAG."""
    
    @staticmethod
    def create_rag_prompt(
        original_prompt: str,
        context_documents: List[str],
        context_limit: int = 500
    ) -> str:
        """Create RAG prompt with injected context.
        
        Args:
            original_prompt: Original prompt
            context_documents: Retrieved context documents
            context_limit: Max characters for context
            
        Returns:
            Augmented prompt with context
        """
        context_text = "\n\n".join(context_documents)
        
        if len(context_text) > context_limit:
            context_text = context_text[:context_limit] + "..."
        
        rag_prompt = f"""Context information:
{context_text}

Based on the context above, answer the following question:

{original_prompt}"""
        
        return rag_prompt
