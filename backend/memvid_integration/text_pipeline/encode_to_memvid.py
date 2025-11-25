#!/usr/bin/env python3
"""
Encode to Memvid - Convert scraped text files into memvid memory.

This script takes content from the scraped folder and encodes it into
a memvid memory (compressed video + FAISS index).

Usage:
    # Encode a specific category
    python encode_to_memvid.py --name flutter-widgets

    # Encode with custom chunk size
    python encode_to_memvid.py --name flutter-docs --chunk-size 1024

    # List available categories to encode
    python encode_to_memvid.py --list

    # Encode all categories
    python encode_to_memvid.py --all
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime

# Directories
SCRIPT_DIR = Path(__file__).parent
SCRAPED_DIR = SCRIPT_DIR.parent / "scraped"
PROCESSED_DIR = SCRIPT_DIR.parent / "processed"
MEMORIES_DIR = Path(__file__).parent.parent.parent / "memories"  # /backend/memories/

def get_categories():
    """List all available categories in scraped folder."""
    if not SCRAPED_DIR.exists():
        return []
    return [d.name for d in SCRAPED_DIR.iterdir() if d.is_dir()]

def count_files(category: str) -> int:
    """Count files in a category."""
    category_dir = SCRAPED_DIR / category
    if not category_dir.exists():
        return 0
    extensions = {'.txt', '.md', '.markdown'}
    return sum(1 for f in category_dir.rglob('*') if f.is_file() and f.suffix.lower() in extensions)

def encode_category(name: str, chunk_size: int = 512, force: bool = False):
    """Encode a category's content into memvid memory."""
    category_dir = SCRAPED_DIR / name

    if not category_dir.exists():
        print(f"Error: Category '{name}' not found in {SCRAPED_DIR}")
        print(f"Available categories: {', '.join(get_categories()) or 'none'}")
        return False

    # Check if memory already exists
    memory_dir = MEMORIES_DIR / name
    if memory_dir.exists() and not force:
        print(f"Memory '{name}' already exists. Use --force to overwrite.")
        return False

    # Import memvid (lazy import to avoid issues if not installed)
    try:
        from memvid import MemvidEncoder
    except ImportError:
        print("Error: memvid not installed. Run: pip install memvid")
        return False

    print(f"\nEncoding category: {name}")
    print(f"Source: {category_dir}")
    print(f"Chunk size: {chunk_size}")
    print("-" * 50)

    encoder = MemvidEncoder()
    files_processed = []
    total_chars = 0
    extensions = {'.txt', '.md', '.markdown'}

    # Process all text files
    for filepath in sorted(category_dir.rglob('*')):
        if filepath.is_file() and filepath.suffix.lower() in extensions:
            print(f"  Adding: {filepath.name}")
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Skip YAML frontmatter if present
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        content = parts[2].strip()

                if content:
                    encoder.add_text(content, chunk_size=chunk_size)
                    files_processed.append(str(filepath))
                    total_chars += len(content)
            except Exception as e:
                print(f"    Warning: Failed to process {filepath}: {e}")

    if not files_processed:
        print("No content to encode.")
        return False

    # Create memory directory
    memory_dir.mkdir(parents=True, exist_ok=True)
    video_path = memory_dir / f"{name}.mp4"
    index_path = memory_dir / f"{name}_index.json"
    metadata_path = memory_dir / "metadata.json"

    print(f"\nBuilding video memory...")
    print(f"  Files: {len(files_processed)}")
    print(f"  Characters: {total_chars:,}")

    # Build the video
    encoder.build_video(str(video_path), str(index_path))

    # Save metadata
    metadata = {
        "project_name": name,
        "file_count": len(files_processed),
        "files_processed": files_processed,
        "chunk_size": chunk_size,
        "total_characters": total_chars,
        "created_at": datetime.now().isoformat(),
        "source_dir": str(category_dir)
    }

    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    # Report results
    video_size = video_path.stat().st_size / (1024 * 1024)
    index_size = index_path.stat().st_size / 1024

    print(f"\nMemory created successfully!")
    print(f"  Video: {video_path} ({video_size:.2f} MB)")
    print(f"  Index: {index_path} ({index_size:.2f} KB)")
    print(f"\nQuery with:")
    print(f"  ~/memvid-projects/memvid query {name} \"your search query\"")

    # Mark as processed
    processed_marker = PROCESSED_DIR / f"{name}.json"
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    with open(processed_marker, 'w') as f:
        json.dump({
            "category": name,
            "encoded_at": datetime.now().isoformat(),
            "files": len(files_processed),
            "video_size_mb": video_size
        }, f, indent=2)

    return True

def list_categories():
    """List all categories with their status."""
    categories = get_categories()

    if not categories:
        print("No categories found in scraped folder.")
        print(f"Add content using: python scrape_to_text.py --name <category>")
        return

    print("\nAvailable Categories:")
    print("-" * 60)
    print(f"{'Category':<25} {'Files':<10} {'Status':<15}")
    print("-" * 60)

    for cat in sorted(categories):
        file_count = count_files(cat)
        memory_exists = (MEMORIES_DIR / cat / f"{cat}.mp4").exists()
        status = "encoded" if memory_exists else "pending"
        print(f"{cat:<25} {file_count:<10} {status:<15}")

    print("-" * 60)

def main():
    parser = argparse.ArgumentParser(description="Encode scraped content to memvid memory")
    parser.add_argument("--name", "-n", help="Category name to encode")
    parser.add_argument("--chunk-size", "-c", type=int, default=512, help="Chunk size (default: 512)")
    parser.add_argument("--force", "-f", action="store_true", help="Overwrite existing memory")
    parser.add_argument("--list", "-l", action="store_true", help="List available categories")
    parser.add_argument("--all", "-a", action="store_true", help="Encode all pending categories")

    args = parser.parse_args()

    if args.list:
        list_categories()
        return

    if args.all:
        categories = get_categories()
        for cat in categories:
            memory_exists = (MEMORIES_DIR / cat / f"{cat}.mp4").exists()
            if not memory_exists or args.force:
                encode_category(cat, args.chunk_size, args.force)
        return

    if args.name:
        success = encode_category(args.name, args.chunk_size, args.force)
        sys.exit(0 if success else 1)

    # No arguments - show help
    parser.print_help()

if __name__ == "__main__":
    main()
