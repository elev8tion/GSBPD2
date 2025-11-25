#!/usr/bin/env python3
"""
Scrape to Text - Saves Firecrawl output to text files for memvid processing.

This script processes content you've scraped with Firecrawl MCP and saves it
in a format ready for memvid encoding.

Usage:
    # Process a single URL's content (paste markdown content)
    python scrape_to_text.py --name "flutter-widgets" --content "markdown content here"

    # Process from a file
    python scrape_to_text.py --name "flutter-widgets" --file scraped_content.md

    # Process multiple files from a directory
    python scrape_to_text.py --name "flutter-docs" --dir ./raw_scrapes/
"""

import argparse
import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

# Base directory for scraped content
SCRAPED_DIR = Path(__file__).parent.parent / "scraped"

def sanitize_filename(name: str) -> str:
    """Convert a string to a safe filename."""
    # Remove or replace unsafe characters
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = re.sub(r'\s+', '_', name)
    return name[:100]  # Limit length

def save_content(name: str, content: str, source_url: str = None, metadata: dict = None):
    """Save scraped content to a text file."""
    # Create category directory
    category_dir = SCRAPED_DIR / sanitize_filename(name)
    category_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if source_url:
        # Extract page name from URL
        url_name = source_url.split('/')[-1] or 'index'
        url_name = sanitize_filename(url_name.replace('.html', '').replace('.md', ''))
        filename = f"{url_name}_{timestamp}.md"
    else:
        filename = f"content_{timestamp}.md"

    filepath = category_dir / filename

    # Add metadata header
    header = f"""---
source: {source_url or 'manual input'}
scraped_at: {datetime.now().isoformat()}
category: {name}
"""
    if metadata:
        for key, value in metadata.items():
            header += f"{key}: {value}\n"
    header += "---\n\n"

    # Save file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header + content)

    print(f"Saved: {filepath}")
    return filepath

def process_firecrawl_output(name: str, firecrawl_json: dict):
    """Process Firecrawl JSON output and save each page."""
    saved_files = []

    # Handle different Firecrawl output formats
    if isinstance(firecrawl_json, list):
        # Multiple pages
        for item in firecrawl_json:
            content = item.get('markdown') or item.get('content') or item.get('text', '')
            url = item.get('url') or item.get('sourceURL', '')
            metadata = {
                'title': item.get('title', ''),
            }
            if content:
                saved_files.append(save_content(name, content, url, metadata))
    elif isinstance(firecrawl_json, dict):
        # Single page
        content = firecrawl_json.get('markdown') or firecrawl_json.get('content') or firecrawl_json.get('text', '')
        url = firecrawl_json.get('url') or firecrawl_json.get('sourceURL', '')
        metadata = {
            'title': firecrawl_json.get('title', ''),
        }
        if content:
            saved_files.append(save_content(name, content, url, metadata))

    return saved_files

def process_directory(name: str, directory: Path):
    """Process all text/markdown files in a directory."""
    saved_files = []
    extensions = {'.txt', '.md', '.markdown', '.json'}

    for filepath in directory.rglob('*'):
        if filepath.is_file() and filepath.suffix.lower() in extensions:
            print(f"Processing: {filepath}")

            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Check if it's JSON (Firecrawl output)
            if filepath.suffix == '.json':
                try:
                    data = json.loads(content)
                    saved_files.extend(process_firecrawl_output(name, data))
                except json.JSONDecodeError:
                    # Not valid JSON, treat as text
                    saved_files.append(save_content(name, content, str(filepath)))
            else:
                saved_files.append(save_content(name, content, str(filepath)))

    return saved_files

def main():
    parser = argparse.ArgumentParser(description="Save scraped content for memvid processing")
    parser.add_argument("--name", "-n", required=True, help="Category name for this content")
    parser.add_argument("--content", "-c", help="Direct content to save")
    parser.add_argument("--file", "-f", help="File containing content to save")
    parser.add_argument("--dir", "-d", help="Directory of files to process")
    parser.add_argument("--url", "-u", help="Source URL (optional)")
    parser.add_argument("--json", "-j", action="store_true", help="Content is Firecrawl JSON output")

    args = parser.parse_args()

    if args.dir:
        # Process directory
        dir_path = Path(args.dir)
        if not dir_path.exists():
            print(f"Error: Directory not found: {args.dir}")
            sys.exit(1)
        files = process_directory(args.name, dir_path)
        print(f"\nProcessed {len(files)} files into: {SCRAPED_DIR / args.name}")

    elif args.file:
        # Process single file
        filepath = Path(args.file)
        if not filepath.exists():
            print(f"Error: File not found: {args.file}")
            sys.exit(1)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if args.json or filepath.suffix == '.json':
            try:
                data = json.loads(content)
                files = process_firecrawl_output(args.name, data)
                print(f"Processed {len(files)} pages")
            except json.JSONDecodeError:
                save_content(args.name, content, args.url)
        else:
            save_content(args.name, content, args.url)

    elif args.content:
        # Direct content
        if args.json:
            try:
                data = json.loads(args.content)
                process_firecrawl_output(args.name, data)
            except json.JSONDecodeError:
                save_content(args.name, args.content, args.url)
        else:
            save_content(args.name, args.content, args.url)
    else:
        # Read from stdin
        print("Paste content (Ctrl+D when done):")
        content = sys.stdin.read()
        save_content(args.name, content, args.url)

    print(f"\nContent saved to: {SCRAPED_DIR / args.name}")
    print(f"Run 'python encode_to_memvid.py --name {args.name}' to create memory")

if __name__ == "__main__":
    main()
