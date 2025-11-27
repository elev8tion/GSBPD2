"""
Migration Adapter: Drop-in replacement for Memvid using Kre8VidMems
This allows gradual migration without breaking existing code.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional
from kre8vidmems import Kre8VidMemory


class MemvidEncoder:
    """
    Drop-in replacement for memvid.MemvidEncoder using Kre8VidMems.
    Mimics the old API but uses the new backend.
    """

    def __init__(self):
        self.memory = Kre8VidMemory()
        self.chunks = []

    def add_text(self, text: str, chunk_size: int = 1000, overlap: int = 50):
        """Add text to be encoded (old API)"""
        self.memory.add(text, chunk_size, overlap)
        self.chunks.append(text)

    def add_chunks(self, chunks: List[str]):
        """Add pre-chunked text (old API)"""
        for chunk in chunks:
            self.memory.add(chunk, chunk_size=len(chunk), overlap=0)
            self.chunks.append(chunk)

    def build(self, name: str, show_progress: bool = True):
        """Build video memory (old API)"""
        # Convert old naming convention to new
        base_name = name.replace('_index', '').replace('.mp4', '')
        self.memory.save(base_name, show_progress=show_progress)

        # Create old-style index files for compatibility
        self._create_compatibility_files(base_name)

    def build_video(self, video_path: str, index_path: str, show_progress: bool = True):
        """Build video with specific paths (old API)"""
        # Extract base name from paths
        base_name = Path(video_path).stem
        self.memory.save(base_name, show_progress=show_progress)

        # Create compatibility files
        self._create_compatibility_files(base_name)

    def _create_compatibility_files(self, base_name: str):
        """Create old-style index files for backward compatibility"""
        # The new system creates .idx files, we need _index.json for old code
        new_idx = Path(f"{base_name}.idx")
        old_json = Path(f"{base_name}_index.json")

        if new_idx.exists() and not old_json.exists():
            # Create a compatibility JSON file
            compat_data = {
                "chunks": self.chunks,
                "num_chunks": len(self.chunks),
                "migrated": True,
                "backend": "kre8vidmems"
            }
            with open(old_json, 'w') as f:
                json.dump(compat_data, f, indent=2)


class MemvidRetriever:
    """
    Drop-in replacement for memvid.MemvidRetriever using Kre8VidMems.
    Provides backward compatibility for existing code.
    """

    def __init__(self, video_path: str, index_path: str):
        """
        Initialize retriever with old-style paths.

        Args:
            video_path: Path to .mp4 file
            index_path: Path to _index.json file (ignored, uses .idx internally)
        """
        # Extract base name and load with new system
        self.video_path = video_path
        self.index_path = index_path

        # Try to load with Kre8VidMems
        base_name = Path(video_path).stem

        try:
            self.memory = Kre8VidMemory.load(base_name)
            self.available = True
        except FileNotFoundError:
            # Memory doesn't exist in new format yet
            print(f"⚠️ Memory '{base_name}' not found in Kre8VidMems format")
            print(f"   Will need conversion from old Memvid format")
            self.available = False
            self.memory = None

            # Try to load chunks from old JSON index for fallback
            self._load_fallback_chunks()

    def _load_fallback_chunks(self):
        """Load chunks from old JSON index as fallback"""
        self.fallback_chunks = []

        try:
            if os.path.exists(self.index_path):
                with open(self.index_path, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and 'chunks' in data:
                        self.fallback_chunks = data['chunks']
                    elif isinstance(data, list):
                        self.fallback_chunks = data
        except Exception as e:
            print(f"⚠️ Could not load fallback chunks: {e}")

    def search(self, query: str, top_k: int = 5) -> List[str]:
        """
        Search for relevant chunks (old API).

        Returns:
            List of text chunks (old format)
        """
        if self.available and self.memory:
            # Use new search
            results = self.memory.search(query, top_k=top_k)
            # Extract just the text for backward compatibility
            return [r['text'] for r in results]
        else:
            # Fallback: return random chunks or empty
            if hasattr(self, 'fallback_chunks') and self.fallback_chunks:
                print(f"⚠️ Using fallback mode - returning first {top_k} chunks")
                return self.fallback_chunks[:top_k]
            else:
                print(f"⚠️ No search available - memory needs conversion")
                return []

    def search_with_scores(self, query: str, top_k: int = 5) -> List[tuple]:
        """
        Search with similarity scores (extended API).

        Returns:
            List of (text, score) tuples
        """
        if self.available and self.memory:
            results = self.memory.search(query, top_k=top_k)
            return [(r['text'], r['score']) for r in results]
        else:
            # Fallback with fake scores
            if hasattr(self, 'fallback_chunks') and self.fallback_chunks:
                return [(chunk, 0.5) for chunk in self.fallback_chunks[:top_k]]
            else:
                return []

    def get_all_chunks(self) -> List[str]:
        """Get all chunks (utility method)"""
        if hasattr(self, 'fallback_chunks'):
            return self.fallback_chunks
        return []


def convert_memvid_to_kre8vidmems(video_path: str, index_path: str, output_name: str = None):
    """
    Convert an existing Memvid memory to Kre8VidMems format.

    Args:
        video_path: Path to existing .mp4 file
        index_path: Path to existing _index.json file
        output_name: Optional new name (defaults to same name)
    """
    print(f"Converting Memvid memory to Kre8VidMems format...")
    print(f"  Video: {video_path}")
    print(f"  Index: {index_path}")

    # Load chunks from old index
    chunks = []
    try:
        with open(index_path, 'r') as f:
            data = json.load(f)

            # Handle different index formats
            if isinstance(data, dict):
                if 'metadata' in data:
                    # New format: {"metadata": [{"text": "..."}, ...]}
                    for item in data['metadata']:
                        if 'text' in item:
                            chunks.append(item['text'])
                elif 'chunks' in data:
                    # Old format: {"chunks": [...]}
                    chunks = data['chunks']
                else:
                    # Try to extract any text fields
                    for key, value in data.items():
                        if isinstance(value, list):
                            for item in value:
                                if isinstance(item, dict) and 'text' in item:
                                    chunks.append(item['text'])
                                elif isinstance(item, str):
                                    chunks.append(item)
            elif isinstance(data, list):
                # Direct list of chunks
                chunks = data
    except Exception as e:
        print(f"❌ Error loading index: {e}")
        return False

    if not chunks:
        print(f"❌ No chunks found in index")
        return False

    print(f"  Found {len(chunks)} chunks to convert")

    # Create new memory with Kre8VidMems
    if not output_name:
        output_name = Path(video_path).stem

    new_memory = Kre8VidMemory()
    for chunk in chunks:
        if isinstance(chunk, dict):
            # Extract text from dict if needed
            text = chunk.get('text', str(chunk))
        else:
            text = str(chunk)
        new_memory.add(text)

    # Save in new format
    new_memory.save(output_name, show_progress=True)

    print(f"✅ Successfully converted to Kre8VidMems format: {output_name}")
    return True


# Optional: Monkey-patch for truly transparent migration
# Uncomment to replace memvid imports globally
# import sys
# sys.modules['memvid'] = sys.modules[__name__]