#!/usr/bin/env python3
"""
Convert existing Memvid memories to Kre8VidMems format.
This script migrates all NBA memories from FAISS to Annoy-based indexing.
"""

import os
import sys
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from services.memvid_adapter import convert_memvid_to_kre8vidmems


def main():
    """Convert all existing Memvid memories to Kre8VidMems format."""

    print("=" * 60)
    print("MEMVID TO KRE8VIDMEMS CONVERSION")
    print("=" * 60)
    print("\nThis script will convert all existing memories from")
    print("FAISS-based Memvid to Annoy-based Kre8VidMems format.")
    print("\n✅ Benefits:")
    print("  - No more FAISS crashes on macOS")
    print("  - No OpenMP conflicts")
    print("  - Memory-mapped files (faster loading)")
    print("  - Zero configuration needed")
    print("\n" + "=" * 60)

    memories_dir = Path(__file__).parent / "memories"

    # List of memories to convert
    memories_to_convert = [
        {
            "name": "nba-players",
            "video": "nba-players.mp4",
            "index": "nba-players_index.json",
            "description": "NBA player rosters and stats"
        },
        {
            "name": "nba-games",
            "video": "nba-games.mp4",
            "index": "nba-games_index.json",
            "description": "NBA team standings and game data"
        },
        {
            "name": "nba-schedule",
            "video": "nba-schedule.mp4",
            "index": "nba-schedule_index.json",
            "description": "NBA season schedule"
        }
    ]

    # Also check for knowledge_base at root
    kb_video = Path(__file__).parent / "knowledge_base.mp4"
    kb_index = Path(__file__).parent / "knowledge_base_index.json"
    if kb_video.exists() and kb_index.exists():
        memories_to_convert.append({
            "name": "knowledge_base",
            "video": str(kb_video),
            "index": str(kb_index),
            "description": "Betting knowledge base",
            "root_level": True
        })

    # Track results
    successful = []
    failed = []
    skipped = []

    print(f"\n📦 Found {len(memories_to_convert)} memories to convert\n")

    for i, memory in enumerate(memories_to_convert, 1):
        print(f"\n[{i}/{len(memories_to_convert)}] Converting: {memory['name']}")
        print(f"     Description: {memory['description']}")

        # Determine paths
        if memory.get('root_level'):
            video_path = memory['video']
            index_path = memory['index']
        else:
            memory_dir = memories_dir / memory['name']
            video_path = memory_dir / memory['video']
            index_path = memory_dir / memory['index']

        # Check if files exist
        if not Path(video_path).exists():
            print(f"     ⚠️ Video not found: {video_path}")
            skipped.append(memory['name'])
            continue

        if not Path(index_path).exists():
            print(f"     ⚠️ Index not found: {index_path}")
            skipped.append(memory['name'])
            continue

        # Check if already converted
        new_idx = Path(str(video_path).replace('.mp4', '.idx'))
        new_ann = Path(str(video_path).replace('.mp4', '.ann'))

        if new_idx.exists() or new_ann.exists():
            print(f"     ✅ Already converted to Kre8VidMems format")
            successful.append(memory['name'])
            continue

        # Perform conversion
        print(f"     🔄 Converting from Memvid to Kre8VidMems...")

        try:
            success = convert_memvid_to_kre8vidmems(
                str(video_path),
                str(index_path),
                output_name=memory['name']
            )

            if success:
                successful.append(memory['name'])
                print(f"     ✅ Successfully converted!")

                # Remove old FAISS index if exists
                faiss_index = Path(str(index_path).replace('_index.json', '_index.faiss'))
                if faiss_index.exists():
                    faiss_index.unlink()
                    print(f"     🗑️ Removed old FAISS index: {faiss_index.name}")
            else:
                failed.append(memory['name'])
                print(f"     ❌ Conversion failed")

        except Exception as e:
            failed.append(memory['name'])
            print(f"     ❌ Error during conversion: {e}")

    # Print summary
    print("\n" + "=" * 60)
    print("CONVERSION SUMMARY")
    print("=" * 60)

    print(f"\n✅ Successfully converted: {len(successful)}")
    for name in successful:
        print(f"   - {name}")

    if skipped:
        print(f"\n⚠️ Skipped (not found): {len(skipped)}")
        for name in skipped:
            print(f"   - {name}")

    if failed:
        print(f"\n❌ Failed: {len(failed)}")
        for name in failed:
            print(f"   - {name}")

    print("\n" + "=" * 60)

    if not failed:
        print("\n🎉 All memories successfully migrated to Kre8VidMems!")
        print("   No more FAISS crashes! 🚀")
    else:
        print(f"\n⚠️ {len(failed)} memories failed to convert.")
        print("   Check the error messages above for details.")

    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())