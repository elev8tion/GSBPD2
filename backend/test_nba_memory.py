#!/usr/bin/env python3
"""
Test script to diagnose Kre8VidMems loading issues for NBA player data
"""
import sys
import os
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / 'lib' / 'kre8vidmems'))

from kre8vidmems import Kre8VidMemory
import time

def test_load_memory(memory_name: str):
    """Test loading a specific memory"""
    memory_path = Path(__file__).parent / 'data' / 'memories' / memory_name

    print(f"\n{'='*60}")
    print(f"Testing: {memory_name}")
    print(f"{'='*60}")

    # Check if files exist
    mp4_file = memory_path.with_suffix('.mp4')
    ann_file = memory_path.with_suffix('.ann')
    meta_file = memory_path.with_suffix('.meta')
    idx_file = memory_path.with_suffix('.idx')

    print(f"\nFile Check:")
    print(f"  .mp4:  {'✓' if mp4_file.exists() else '✗'} ({mp4_file.stat().st_size / 1024 / 1024:.1f} MB)" if mp4_file.exists() else f"  .mp4:  ✗ MISSING")
    print(f"  .ann:  {'✓' if ann_file.exists() else '✗'} ({ann_file.stat().st_size / 1024:.1f} KB)" if ann_file.exists() else f"  .ann:  ✗ MISSING")
    print(f"  .meta: {'✓' if meta_file.exists() else '✗'} ({meta_file.stat().st_size / 1024:.1f} KB)" if meta_file.exists() else f"  .meta: ✗ MISSING")

    if not all([mp4_file.exists(), ann_file.exists(), meta_file.exists()]):
        print(f"\n❌ Missing required files, skipping load test")
        return None

    # Try to load memory
    print(f"\nAttempting to load memory...")
    start_time = time.time()

    try:
        memory = Kre8VidMemory.load(str(memory_path))
        load_time = time.time() - start_time

        print(f"✅ Memory loaded successfully in {load_time:.2f}s")
        print(f"   Chunks: {len(memory.vector_store.metadata)}")

        # Try a search
        print(f"\nTesting search functionality...")
        search_start = time.time()

        results = memory.search("LeBron James", top_k=3)
        search_time = time.time() - search_start

        print(f"✅ Search completed in {search_time:.2f}s")
        print(f"   Found {len(results)} results")

        if results:
            print(f"\nTop result preview:")
            print(f"   Score: {results[0]['score']:.4f}")
            print(f"   Text: {results[0]['text'][:200]}...")

        return memory

    except Exception as e:
        load_time = time.time() - start_time
        print(f"❌ Failed to load memory after {load_time:.2f}s")
        print(f"   Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Run tests on all NBA memories"""

    print(f"\n🔍 Kre8VidMems NBA Memory Diagnostic Test")
    print(f"{'='*60}\n")

    # Test each NBA memory
    memories = [
        'nba-nba-player-profiles-2025',
        'nba-nba-season-averages-2025',
        'nba-nba-player-gamelogs-2025',
        'nba-nba-teams-2025',
        'nba-nba-schedule-2025'
    ]

    results = {}
    for memory_name in memories:
        memory = test_load_memory(memory_name)
        results[memory_name] = memory is not None

    # Summary
    print(f"\n\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")

    for memory_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {memory_name}")

    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} memories loaded successfully")

    if passed == total:
        print(f"\n🎉 All memories working! No FAISS/Annoy hang detected.")
        print(f"   The issue may be specific to how nba_service.py loads memories.")
    else:
        print(f"\n⚠️  Some memories failed to load.")
        print(f"   This indicates a problem with the memory files or Kre8VidMems.")

if __name__ == "__main__":
    main()
