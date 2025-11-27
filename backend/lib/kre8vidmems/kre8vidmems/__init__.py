"""
Kre8VidMems - Video-based AI Memory using QR codes and semantic search
"""
from .api.memory import Kre8VidMemory
from .core import chunk_text, Vectorizer
from .storage import VideoStore, VectorStore

__version__ = "0.1.0"
__all__ = ['Kre8VidMemory', 'chunk_text', 'Vectorizer', 'VideoStore', 'VectorStore']
