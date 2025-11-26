#!/bin/bash
# Start FastAPI server with OpenMP library conflict fix

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Critical fix for multiple OpenMP libraries
export KMP_DUPLICATE_LIB_OK=TRUE

# Force single OpenMP library (PyTorch's version for best compatibility)
export DYLD_INSERT_LIBRARIES="$SCRIPT_DIR/memvid_venv/lib/python3.12/site-packages/torch/lib/libomp.dylib"

# Limit OpenMP threads to prevent excessive threading
export OMP_NUM_THREADS=4

# Additional OpenMP environment variables for stability
export KMP_AFFINITY=disabled
export MKL_THREADING_LAYER=GNU

echo "========================================="
echo "FastAPI Server with OpenMP Fix"
echo "========================================="
echo "OpenMP Library: $DYLD_INSERT_LIBRARIES"
echo "Max Threads: $OMP_NUM_THREADS"
echo "========================================="
echo ""

# Activate virtual environment and start server
source "$SCRIPT_DIR/memvid_venv/bin/activate"

# Start uvicorn with reload for development
python -m uvicorn main:app --reload --port 8000 --host 0.0.0.0
