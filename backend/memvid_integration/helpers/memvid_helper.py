#!/usr/bin/env python3
"""
Memvid Helper - Create and search video-based memories for multiple projects.

Usage:
    # Create a new memory from files
    python memvid_helper.py create <project_name> --files file1.txt file2.pdf
    python memvid_helper.py create <project_name> --dir /path/to/docs

    # Search a memory (human-readable)
    python memvid_helper.py search <project_name> "your query here"

    # Search with JSON output (for MCP/programmatic use)
    python memvid_helper.py search <project_name> "your query" --json

    # Query command (optimized for MCP - JSON only, minimal output)
    python memvid_helper.py query <project_name> "your query here"

    # List all memories
    python memvid_helper.py list
    python memvid_helper.py list --json

    # Get info about a memory
    python memvid_helper.py info <project_name>
"""

import argparse
import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory for all memvid projects
MEMVID_BASE = Path(os.getenv('MEMVID_BASE_PATH', str(Path(__file__).parent.parent.parent / 'memories')))

# Suppress warnings for cleaner programmatic output
import warnings
warnings.filterwarnings("ignore")

def get_memory_path(project_name):
    """Get the path for a project's memory files."""
    project_dir = MEMVID_BASE / project_name
    return {
        "dir": project_dir,
        "video": project_dir / f"{project_name}.mp4",
        "index": project_dir / f"{project_name}_index.json",
        "metadata": project_dir / "metadata.json"
    }

def create_memory(project_name, files=None, directory=None, chunk_size=512):
    """Create a new memvid memory from files or a directory."""
    from memvid import MemvidEncoder

    paths = get_memory_path(project_name)
    paths["dir"].mkdir(parents=True, exist_ok=True)

    encoder = MemvidEncoder()
    file_count = 0

    files_to_process = []

    if files:
        files_to_process.extend(files)

    if directory:
        dir_path = Path(directory)
        # Supported extensions
        extensions = {'.txt', '.md', '.pdf', '.py', '.js', '.ts', '.json', '.yaml', '.yml',
                     '.html', '.css', '.java', '.go', '.rs', '.cpp', '.c', '.h', '.hpp',
                     '.rb', '.php', '.swift', '.kt', '.scala', '.sh', '.bash', '.zsh', '.dart'}
        for f in dir_path.rglob("*"):
            if f.is_file() and f.suffix.lower() in extensions:
                files_to_process.append(str(f))

    for filepath in files_to_process:
        filepath = Path(filepath)
        if not filepath.exists():
            print(f"Warning: {filepath} not found, skipping...", file=sys.stderr)
            continue

        print(f"Processing: {filepath}", file=sys.stderr)

        if filepath.suffix.lower() == '.pdf':
            try:
                encoder.add_pdf(str(filepath))
                file_count += 1
            except Exception as e:
                print(f"Error processing PDF {filepath}: {e}", file=sys.stderr)
        else:
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    encoder.add_text(content, chunk_size=chunk_size)
                    file_count += 1
            except Exception as e:
                print(f"Error processing {filepath}: {e}", file=sys.stderr)

    if file_count == 0:
        print("No files processed. Memory not created.", file=sys.stderr)
        return False

    print(f"\nBuilding video memory from {file_count} files...", file=sys.stderr)
    encoder.build_video(str(paths["video"]), str(paths["index"]))

    # Save metadata
    metadata = {
        "project_name": project_name,
        "file_count": file_count,
        "files_processed": files_to_process,
        "chunk_size": chunk_size
    }
    with open(paths["metadata"], 'w') as f:
        json.dump(metadata, f, indent=2, default=str)

    print(f"\nMemory created successfully!", file=sys.stderr)
    print(f"  Video: {paths['video']}", file=sys.stderr)
    print(f"  Index: {paths['index']}", file=sys.stderr)
    return True

def search_memory(project_name, query, top_k=5, output_json=False):
    """Search a memvid memory."""
    from memvid import MemvidRetriever

    paths = get_memory_path(project_name)

    if not paths["video"].exists():
        if output_json:
            print(json.dumps({"error": f"Memory '{project_name}' not found", "results": []}))
        else:
            print(f"Error: Memory '{project_name}' not found.", file=sys.stderr)
            print(f"Use 'memvid_helper.py list' to see available memories.", file=sys.stderr)
        return None

    retriever = MemvidRetriever(str(paths["video"]), str(paths["index"]))
    results = retriever.search(query, top_k=top_k)

    if output_json:
        # JSON output for programmatic use
        output = {
            "memory": project_name,
            "query": query,
            "count": len(results),
            "results": results
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable output
        print(f"\nSearch results for: '{query}'\n")
        print("-" * 60)
        for i, result in enumerate(results, 1):
            text = result if isinstance(result, str) else str(result)
            print(f"\n[{i}] {text[:500]}{'...' if len(text) > 500 else ''}")
        print("-" * 60)

    return results

def query_memory(project_name, query, top_k=3):
    """
    Query a memory - optimized for MCP/programmatic use.
    Returns JSON only, suppresses all other output.
    """
    import io
    import contextlib

    # Suppress all stdout/stderr from memvid
    with contextlib.redirect_stderr(io.StringIO()):
        from memvid import MemvidRetriever

    paths = get_memory_path(project_name)

    if not paths["video"].exists():
        print(json.dumps({"error": f"Memory '{project_name}' not found", "results": []}))
        return None

    with contextlib.redirect_stderr(io.StringIO()):
        retriever = MemvidRetriever(str(paths["video"]), str(paths["index"]))
        results = retriever.search(query, top_k=top_k)

    output = {
        "memory": project_name,
        "query": query,
        "count": len(results),
        "results": results
    }
    print(json.dumps(output))
    return results

def query_multiple(memories, query, top_k=3):
    """
    Query multiple memories at once - for searching across all Flutter docs.
    Returns combined JSON results.
    """
    import io
    import contextlib

    all_results = []

    with contextlib.redirect_stderr(io.StringIO()):
        from memvid import MemvidRetriever

    for memory_name in memories:
        paths = get_memory_path(memory_name)
        if not paths["video"].exists():
            continue

        with contextlib.redirect_stderr(io.StringIO()):
            retriever = MemvidRetriever(str(paths["video"]), str(paths["index"]))
            results = retriever.search(query, top_k=top_k)

        for result in results:
            all_results.append({
                "memory": memory_name,
                "text": result
            })

    output = {
        "query": query,
        "memories_searched": memories,
        "total_results": len(all_results),
        "results": all_results
    }
    print(json.dumps(output))
    return all_results

def list_memories(output_json=False):
    """List all available memories."""
    if not MEMVID_BASE.exists():
        if output_json:
            print(json.dumps({"memories": []}))
        else:
            print("No memories found.")
        return []

    memories = []
    for project_dir in MEMVID_BASE.iterdir():
        if project_dir.is_dir():
            metadata_path = project_dir / "metadata.json"
            video_path = project_dir / f"{project_dir.name}.mp4"
            if metadata_path.exists():
                with open(metadata_path) as f:
                    metadata = json.load(f)
                metadata["size_mb"] = round(video_path.stat().st_size / (1024 * 1024), 2) if video_path.exists() else 0
                memories.append(metadata)

    if output_json:
        print(json.dumps({"memories": memories}, indent=2))
        return memories

    if not memories:
        print("No memories found.")
        return []

    print("\nAvailable Memories:")
    print("-" * 40)
    for m in memories:
        print(f"  {m['project_name']}")
        print(f"    Files: {m['file_count']} | Size: {m.get('size_mb', 0):.2f} MB")
    print("-" * 40)

    return memories

def get_info(project_name, output_json=False):
    """Get detailed info about a memory."""
    paths = get_memory_path(project_name)

    if not paths["metadata"].exists():
        if output_json:
            print(json.dumps({"error": f"Memory '{project_name}' not found"}))
        else:
            print(f"Memory '{project_name}' not found.")
        return None

    with open(paths["metadata"]) as f:
        metadata = json.load(f)

    video_size = paths["video"].stat().st_size / (1024 * 1024) if paths["video"].exists() else 0
    index_size = paths["index"].stat().st_size / 1024 if paths["index"].exists() else 0

    info = {
        **metadata,
        "video_size_mb": round(video_size, 2),
        "index_size_kb": round(index_size, 2),
        "video_path": str(paths["video"]),
        "index_path": str(paths["index"])
    }

    if output_json:
        print(json.dumps(info, indent=2))
        return info

    print(f"\nMemory: {project_name}")
    print("-" * 40)
    print(f"  Files indexed: {metadata['file_count']}")
    print(f"  Chunk size: {metadata['chunk_size']}")
    print(f"  Video size: {video_size:.2f} MB")
    print(f"  Index size: {index_size:.2f} KB")
    print(f"\n  Video: {paths['video']}")
    print(f"  Index: {paths['index']}")
    print("-" * 40)

    return info

def delete_memory(project_name):
    """
    Delete a memory and all its files.

    Args:
        project_name: Name of the memory to delete

    Returns:
        bool: True if deleted successfully, False otherwise
    """
    import shutil

    paths = get_memory_path(project_name)

    if not paths["dir"].exists():
        print(f"Error: Memory '{project_name}' not found.", file=sys.stderr)
        return False

    try:
        shutil.rmtree(paths["dir"])
        print(f"Successfully deleted memory '{project_name}'", file=sys.stderr)
        return True
    except Exception as e:
        print(f"Error deleting memory '{project_name}': {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Memvid Helper - Manage video-based memories")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new memory")
    create_parser.add_argument("project_name", help="Name for the memory/project")
    create_parser.add_argument("--files", "-f", nargs="+", help="Files to index")
    create_parser.add_argument("--dir", "-d", help="Directory to index recursively")
    create_parser.add_argument("--chunk-size", type=int, default=512, help="Chunk size (default: 512)")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search a memory")
    search_parser.add_argument("project_name", help="Memory to search")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--top-k", "-k", type=int, default=5, help="Number of results")
    search_parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    # Query command (MCP-optimized)
    query_parser = subparsers.add_parser("query", help="Query a memory (JSON output, MCP-optimized)")
    query_parser.add_argument("project_name", help="Memory to query (or 'all' for all memories)")
    query_parser.add_argument("query", help="Search query")
    query_parser.add_argument("--top-k", "-k", type=int, default=3, help="Number of results per memory")

    # List command
    list_parser = subparsers.add_parser("list", help="List all memories")
    list_parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    # Info command
    info_parser = subparsers.add_parser("info", help="Get info about a memory")
    info_parser.add_argument("project_name", help="Memory name")
    info_parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.command == "create":
        if not args.files and not args.dir:
            print("Error: Provide --files or --dir", file=sys.stderr)
            sys.exit(1)
        create_memory(args.project_name, args.files, args.dir, args.chunk_size)

    elif args.command == "search":
        search_memory(args.project_name, args.query, args.top_k, getattr(args, 'json', False))

    elif args.command == "query":
        if args.project_name == "all":
            # Query all memories
            memories = [m["project_name"] for m in list_memories(output_json=False) if not m]
            # Get actual memory names
            if MEMVID_BASE.exists():
                memories = [d.name for d in MEMVID_BASE.iterdir() if d.is_dir() and (d / "metadata.json").exists()]
            query_multiple(memories, args.query, args.top_k)
        elif "," in args.project_name:
            # Query specific memories
            memories = [m.strip() for m in args.project_name.split(",")]
            query_multiple(memories, args.query, args.top_k)
        else:
            query_memory(args.project_name, args.query, args.top_k)

    elif args.command == "list":
        list_memories(getattr(args, 'json', False))

    elif args.command == "info":
        get_info(args.project_name, getattr(args, 'json', False))

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
