#!/usr/bin/env python3
"""
Test script to verify kre8vidmems functionality
"""
import sys
import tempfile
from pathlib import Path

def test_imports():
    """Test that all modules can be imported"""
    print("✓ Testing imports...")
    try:
        from kre8vidmems import Kre8VidMemory
        from kre8vidmems.core import chunk_text, encode_to_qr, decode_qr
        from kre8vidmems.storage import VectorStore, VideoStore
        print("  ✓ All imports successful")
        return True
    except Exception as e:
        print(f"  ✗ Import failed: {e}")
        return False

def test_chunking():
    """Test text chunking"""
    print("\n✓ Testing chunking...")
    try:
        from kre8vidmems.core import chunk_text
        text = "This is a test. " * 100
        chunks = chunk_text(text, chunk_size=50, overlap=10)
        assert len(chunks) > 1, "Should create multiple chunks"
        print(f"  ✓ Created {len(chunks)} chunks")
        return True
    except Exception as e:
        print(f"  ✗ Chunking failed: {e}")
        return False

def test_qr_codes():
    """Test QR code generation and decoding"""
    print("\n✓ Testing QR codes...")
    try:
        from kre8vidmems.core import encode_to_qr, decode_qr, qr_to_numpy
        
        test_data = "Hello, Kre8VidMems!"
        qr_img = encode_to_qr(test_data)
        frame = qr_to_numpy(qr_img, (256, 256))
        decoded = decode_qr(frame)
        
        assert decoded == test_data, f"Expected '{test_data}', got '{decoded}'"
        print(f"  ✓ QR encode/decode successful")
        return True
    except Exception as e:
        print(f"  ✗ QR test failed: {e}")
        return False

def test_vectorizer():
    """Test embedding generation"""
    print("\n✓ Testing vectorizer...")
    try:
        from kre8vidmems.core import Vectorizer
        
        vectorizer = Vectorizer()
        texts = ["Hello world", "Machine learning"]
        embeddings = vectorizer.encode(texts)
        
        assert embeddings.shape[0] == 2, "Should have 2 embeddings"
        assert embeddings.shape[1] == 384, "Should have 384 dimensions"
        print(f"  ✓ Generated embeddings: {embeddings.shape}")
        return True
    except Exception as e:
        print(f"  ✗ Vectorizer failed: {e}")
        return False

def test_vector_store():
    """Test Annoy vector store"""
    print("\n✓ Testing vector store...")
    try:
        from kre8vidmems.storage import VectorStore
        from kre8vidmems.core import Vectorizer
        import tempfile
        
        # Create embeddings
        vectorizer = Vectorizer()
        texts = ["Quantum computing", "Machine learning", "Artificial intelligence"]
        embeddings = vectorizer.encode(texts)
        
        # Create store
        store = VectorStore()
        for i in range(len(texts)):
            store.add_items([i], embeddings[i:i+1])
            store.add_metadata(i, i, texts[i])
        
        store.build(n_trees=5)
        
        # Test search
        query_embedding = vectorizer.encode(["quantum physics"])[0]
        results = store.search(query_embedding, k=2)
        
        assert len(results) == 2, "Should return 2 results"
        print(f"  ✓ Vector search successful: {len(results)} results")
        return True
    except Exception as e:
        print(f"  ✗ Vector store failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ffmpeg():
    """Test FFmpeg availability"""
    print("\n✓ Testing FFmpeg...")
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print(f"  ✓ FFmpeg available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"  ⚠ FFmpeg not found (install with: brew install ffmpeg)")
        print(f"  ℹ Video creation will not work without FFmpeg")
        return False

def main():
    print("="*60)
    print("Kre8VidMems Verification Tests")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Chunking", test_chunking()))
    results.append(("QR Codes", test_qr_codes()))
    results.append(("Vectorizer", test_vectorizer()))
    results.append(("Vector Store", test_vector_store()))
    results.append(("FFmpeg", test_ffmpeg()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    elif passed >= total - 1 and not results[-1][1]:  # Only FFmpeg failed
        print("\n⚠️ Core functionality works, but FFmpeg is missing")
        print("Install FFmpeg to enable video creation:")
        print("  macOS: brew install ffmpeg")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
