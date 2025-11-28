#!/usr/bin/env python3
"""
Test script to verify NFL field goals stats memory
"""

import os
import sys
from pathlib import Path

# Add backend path for imports
backend_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_path)
sys.path.insert(0, os.path.join(backend_path, 'lib', 'kre8vidmems'))

# Import Kre8VidMems
from kre8vidmems import Kre8VidMemory

def test_query():
    """Test querying the field goals memory"""

    print("\n" + "="*60)
    print("TESTING NFL FIELD GOALS MEMORY")
    print("="*60)

    # Load the memory
    memory_name = "data/memories/nfl-player-fieldgoals-stats"

    try:
        memory = Kre8VidMemory.load(memory_name)
        print(f"✓ Memory loaded successfully from: {memory_name}")
    except Exception as e:
        print(f"✗ Failed to load memory: {e}")
        return

    # Test queries
    test_queries = [
        "elite kickers",
        "perfect season 100%",
        "60+ yard field goal",
        "Brandon Aubrey",
        "most accurate kicker",
        "distance kicker specialist"
    ]

    print("\nRunning test queries...")
    print("-" * 60)

    for query in test_queries:
        print(f"\nQuery: '{query}'")
        try:
            results = memory.search(query, top_k=3)
            print(f"  Found {len(results)} results")
            if results:
                # Show first result preview
                first_result = results[0]['text'][:150].replace('\n', ' ')
                print(f"  Top result: {first_result}...")
        except Exception as e:
            print(f"  Error: {e}")

    print("\n" + "="*60)
    print("MEMORY TEST COMPLETED!")
    print("="*60)

if __name__ == "__main__":
    test_query()