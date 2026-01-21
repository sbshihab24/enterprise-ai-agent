import faiss
import numpy as np
import os
import pickle
from typing import List, Tuple, Dict
from app.core.logger import logger

class VectorStore:
    """
    Wrapper around FAISS for vector storage and retrieval.
    Persists data to disk in 'data/faiss_index/'.
    """
    
    def __init__(self, index_path: str = "data/faiss_index/"):
        self.index_path = index_path
        self.index_file = os.path.join(index_path, "index.faiss")
        self.metadata_file = os.path.join(index_path, "metadata.pkl")
        self.dimension = 384  # Default for all-MiniLM-L6-v2
        self.index = None
        self.metadata: Dict[int, Dict] = {}  # Maps FAISS ID -> Metadata (original text, etc)
        
        self._load_or_create_index()

    def _load_or_create_index(self):
        """Loads existing index/metadata or creates new ones."""
        if not os.path.exists(self.index_path):
            os.makedirs(self.index_path)

        if os.path.exists(self.index_file) and os.path.exists(self.metadata_file):
            logger.info("Loading existing FAISS index...")
            try:
                self.index = faiss.read_index(self.index_file)
                with open(self.metadata_file, "rb") as f:
                    self.metadata = pickle.load(f)
            except Exception as e:
                logger.error(f"Failed to load index, creating new one: {e}")
                self._create_new_index()
        else:
            self._create_new_index()

    def _create_new_index(self):
        logger.info("Creating new FAISS index...")
        # L2 Distance (Euclidean) is standard. For cosine, vectors must be normalized.
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = {}

    def add_vector(self, vector: np.ndarray, meta: Dict):
        """Adds a single vector and its metadata to the store."""
        if self.index is None:
            raise ValueError("Index not initialized")
        
        # FAISS expects a matrix of shape (1, d)
        vec_reshaped = vector.reshape(1, -1)
        self.index.add(vec_reshaped)
        
        # ID is the current size - 1 (since we just added)
        # Note: IndexFlatL2 doesn't have custom IDs, it's just sequential.
        id_ = self.index.ntotal - 1
        self.metadata[id_] = meta
        
        self._save_index()

    def search(self, vector: np.ndarray, k: int = 3) -> List[Dict]:
        """
        Searches for the k nearest neighbors.
        Returns a list of metadata dicts.
        """
        if self.index is None or self.index.ntotal == 0:
            return []
            
        vec_reshaped = vector.reshape(1, -1)
        distances, indices = self.index.search(vec_reshaped, k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx in self.metadata:
                item = self.metadata[idx]
                item['score'] = float(distances[0][i])
                results.append(item)
                
        return results

    def _save_index(self):
        """Persists the index and metadata to disk."""
        try:
            faiss.write_index(self.index, self.index_file)
            with open(self.metadata_file, "wb") as f:
                pickle.dump(self.metadata, f)
        except Exception as e:
            logger.error(f"Failed to save index: {e}")
