"""
Annoy-based vector storage and search
"""
from annoy import AnnoyIndex
import numpy as np
import json
from pathlib import Path
from typing import List, Tuple, Optional
from kre8vidmems.config import EMBEDDING_DIMENSION, ANNOY_METRIC, ANNOY_TREES

class VectorStore:
    """Memory-mapped vector index using Annoy"""
    
    def __init__(self, dimension: int = EMBEDDING_DIMENSION):
        self.dimension = dimension
        self.metric = ANNOY_METRIC
        self.index = AnnoyIndex(dimension, self.metric)
        self.metadata = []  # Stores chunk IDs and text
        self.built = False
        
    def add_items(self, ids: List[int], vectors: np.ndarray):
        """Add vectors to index"""
        if self.built:
            raise RuntimeError("Cannot add items to a built index")
            
        for idx, vector in zip(ids, vectors):
            self.index.add_item(idx, vector)
            
    def build(self, n_trees: int = ANNOY_TREES):
        """Build the index"""
        self.index.build(n_trees)
        self.built = True
        
    def save(self, path: str):
        """Save index and metadata"""
        path = Path(path)
        
        # Save annoy index
        self.index.save(str(path.with_suffix('.ann')))
        
        # Save metadata
        metadata_file = {
            'metadata': self.metadata,
            'dimension': self.dimension,
            'metric': self.metric
        }
        with open(path.with_suffix('.meta'), 'w') as f:
            json.dump(metadata_file, f, indent=2)
            
    def load(self, path: str):
        """Load index and metadata"""
        path = Path(path)
        
        # Load metadata first to get dimension
        with open(path.with_suffix('.meta'), 'r') as f:
            metadata_file = json.load(f)
            
        self.dimension = metadata_file['dimension']
        self.metric = metadata_file['metric']
        self.metadata = metadata_file['metadata']
        
        # Load annoy index
        self.index = AnnoyIndex(self.dimension, self.metric)
        self.index.load(str(path.with_suffix('.ann')))
        self.built = True
        
    def search(self, vector: np.ndarray, k: int = 5) -> List[Tuple[int, float]]:
        """Search for k nearest neighbors"""
        if not self.built:
            raise RuntimeError("Index not built. Call build() first.")
            
        ids, distances = self.index.get_nns_by_vector(
            vector, k, include_distances=True
        )
        return list(zip(ids, distances))
        
    def add_metadata(self, chunk_id: int, frame_id: int, text: str):
        """Store metadata for a chunk"""
        self.metadata.append({
            'chunk_id': chunk_id,
            'frame_id': frame_id,
            'text': text
        })
        
    def get_metadata(self, chunk_id: int) -> Optional[dict]:
        """Retrieve metadata by chunk ID"""
        for meta in self.metadata:
            if meta['chunk_id'] == chunk_id:
                return meta
        return None
