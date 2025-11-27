"""
Text chunking logic
"""
from typing import List

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks.
    Attempts to break at sentence boundaries.
    """
    if not text:
        return []
        
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = start + chunk_size
        
        # If we are not at the end of text, try to find a sentence break
        if end < text_len:
            # Look for the last period in the chunk
            chunk_slice = text[start:end]
            last_period = chunk_slice.rfind('.')
            
            # If a period is found reasonably close to the end (last 20%), break there
            if last_period > chunk_size * 0.8:
                end = start + last_period + 1
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
            
        # Move start forward, minus overlap
        start = end - overlap
        
        # Ensure we make forward progress
        if start >= end:
            start = end
            
    return chunks
