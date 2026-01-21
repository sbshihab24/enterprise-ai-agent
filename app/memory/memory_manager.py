from typing import List, Dict
from app.memory.embeddings import EmbeddingService
from app.memory.vector_store import VectorStore
from app.core.logger import logger

class MemoryManager:
    """
    High-level manager for Long-Term Memory.
    Agents interact with this class, not the low-level stores.
    """
    
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def save_memory(self, user_id: str, text: str, role: str):
        """
        Embeds and saves a conversation turn to long-term memory.
        """
        logger.info(f"Saving memory for user {user_id}: {text[:50]}...")
        vector = self.embedding_service.get_embedding(text)
        
        metadata = {
            "user_id": user_id,
            "text": text,
            "role": role,
            "timestamp": "TODO: Add timestamp"  # Optional improvement
        }
        
        self.vector_store.add_vector(vector, metadata)

    def retrieve_relevant_memory(self, query: str, user_id: str, top_k: int = 3) -> List[str]:
        """
        Retrieves the most semantically relevant past messages.
        Filters by user_id to ensure privacy/session isolation.
        """
        logger.info(f"Retrieving memory for query: {query[:50]}...")
        query_vector = self.embedding_service.get_embedding(query)
        results = self.vector_store.search(query_vector, k=top_k * 2) # Fetch more, then filter
        
        # Filter by user_id
        relevant_texts = []
        for result in results:
            if result.get("user_id") == user_id:
                relevant_texts.append(f"{result['role'].upper()}: {result['text']}")
                if len(relevant_texts) >= top_k:
                    break
                    
        return relevant_texts
