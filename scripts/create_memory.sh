#!/bin/bash
# Helper script to create memvid memories for GSBPD2
# Usage: ./scripts/create_memory.sh <memory_name> <docs_dir>

set -e

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export MEMVID_BASE_PATH="$(pwd)/backend/memories"

# Run the memvid helper
python3 backend/memvid_integration/helpers/memvid_helper.py create "$@"

echo ""
echo "✅ Memory created successfully!"
echo "   You can now query it via the Knowledge Base tab in the frontend"
