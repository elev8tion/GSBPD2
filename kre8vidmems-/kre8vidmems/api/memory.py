"""
Main Memory API for Kre8VidMems
"""
import json
from pathlib import Path
from typing import List, Optional, Dict
from kre8vidmems.core import chunk_text, encode_to_qr, decode_qr, qr_to_numpy, Vectorizer
from kre8vidmems.storage import VideoStore, VectorStore
from kre8vidmems.config import FRAME_WIDTH, FRAME_HEIGHT

class Kre8VidMemory:
    """Main interface for creating and querying video memories"""
    
    def __init__(self):
        self.chunks = []
        self.vectorizer = Vectorizer()
        self.video_store = VideoStore()
        self.vector_store = VectorStore()
        self.video_path = None
        self.index_path = None
        
    def add(self, text: str, chunk_size: int = 1000, overlap: int = 50):
        """Add text to memory"""
        new_chunks = chunk_text(text, chunk_size, overlap)
        self.chunks.extend(new_chunks)
        print(f"Added {len(new_chunks)} chunks (Total: {len(self.chunks)})")
        
    def add_file(self, file_path: str, chunk_size: int = 1000, overlap: int = 50):
        """Add text file to memory"""
        with open(file_path, 'r', encoding='utf-8') as f:
            self.add(f.read(), chunk_size, overlap)
            
    def save(self, name: str, show_progress: bool = True):
        """Build and save video memory"""
        if not self.chunks:
            raise ValueError("No chunks to save. Use add() first.")
            
        base_path = Path(name)
        video_path = base_path.with_suffix('.mp4')
        index_path = base_path.with_suffix('.idx')
        
        if show_progress:
            print(f"\n🎬 Creating Kre8VidMem: {name}")
            print(f"   Chunks: {len(self.chunks)}")
            
        # 1. Generate embeddings
        if show_progress:
            print("   [1/3] Generating embeddings...")
        embeddings = self.vectorizer.encode(self.chunks)
        
        # 2. Build vector index
        if show_progress:
            print("   [2/3] Building vector index...")
        for i in range(len(self.chunks)):
            self.vector_store.add_items([i], embeddings[i:i+1])
            self.vector_store.add_metadata(i, i, self.chunks[i])
        self.vector_store.build()
        self.vector_store.save(str(index_path))
        
        # 3. Create video
        if show_progress:
            print("   [3/3] Creating video...")
        frames = []
        for i, chunk in enumerate(self.chunks):
            # Create QR code with chunk data
            chunk_data = json.dumps({
                'id': i,
                'text': chunk
            })
            qr_img = encode_to_qr(chunk_data)
            frame = qr_to_numpy(qr_img, (FRAME_WIDTH, FRAME_HEIGHT))
            frames.append(frame)
            
        stats = self.video_store.create_video(frames, str(video_path), show_progress=False)
        
        self.video_path = str(video_path)
        self.index_path = str(index_path)
        
        if show_progress:
            print(f"\n✓ Memory created successfully!")
            print(f"   Video: {video_path} ({stats['size_mb']:.2f} MB)")
            print(f"   Index: {index_path}")
            
        return stats
        
    @classmethod
    def load(cls, name: str) -> 'Kre8VidMemory':
        """Load existing video memory"""
        memory = cls()
        
        base_path = Path(name)
        video_path = base_path.with_suffix('.mp4')
        index_path = base_path.with_suffix('.idx')
        
        if not video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")
        if not index_path.exists():
            raise FileNotFoundError(f"Index not found: {index_path}")
            
        memory.video_path = str(video_path)
        memory.index_path = str(index_path)
        memory.vector_store.load(str(index_path))
        
        print(f"✓ Loaded memory: {name}")
        print(f"   Chunks: {len(memory.vector_store.metadata)}")
        
        return memory
        
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search memory for relevant chunks"""
        if not self.video_path:
            raise RuntimeError("Memory not loaded. Use load() first.")
            
        # Generate query embedding
        query_embedding = self.vectorizer.encode([query])[0]
        
        # Search vector store
        results = self.vector_store.search(query_embedding, top_k)
        
        # Retrieve actual text from video
        output = []
        for chunk_id, distance in results:
            metadata = self.vector_store.get_metadata(chunk_id)
            if metadata:
                # Extract frame from video
                frame_id = metadata['frame_id']
                frame = self.video_store.extract_frame(self.video_path, frame_id)
                
                # Decode QR
                decoded = decode_qr(frame)
                if decoded:
                    try:
                        chunk_data = json.loads(decoded)
                        text = chunk_data['text']
                    except:
                        text = metadata['text']  # Fallback
                else:
                    text = metadata['text']  # Fallback
                    
                output.append({
                    'text': text,
                    'score': 1.0 / (1.0 + distance),  # Convert distance to similarity
                    'chunk_id': chunk_id
                })
                
        return output
