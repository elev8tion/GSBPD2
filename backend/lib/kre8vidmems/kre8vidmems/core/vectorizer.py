"""
Vector embedding generation
"""
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union
from kre8vidmems.config import EMBEDDING_MODEL

class Vectorizer:
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model = SentenceTransformer(model_name)
        
    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """Generate embeddings for text(s)"""
        embeddings = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        return embeddings
