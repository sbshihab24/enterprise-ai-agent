from sentence_transformers import SentenceTransformer
from app.core.logger import logger
import numpy as np

class EmbeddingService:
    """
    Handles converting text to vector embeddings using a local model.
    Model: all-MiniLM-L6-v2 (fast and efficient for CPU).
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        logger.info(f"Loading embedding model: {model_name}...")
        try:
            self.model = SentenceTransformer(model_name)
            self.dimension = self.model.get_sentence_embedding_dimension()
            logger.info("Embedding model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise e

    def get_embedding(self, text: str) -> np.ndarray:
        """
        Generates an embedding vector for the given text.
        Returns a numpy array (float32).
        """
        try:
            embedding = self.model.encode(text)
            return np.array(embedding).astype('float32')
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return np.array([])
