#!/bin/bash
# Start FastAPI server with OpenMP library conflict fix

# Get the backend directory (parent of scripts/)
BACKEND_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

# Critical fix for multiple OpenMP libraries
export KMP_DUPLICATE_LIB_OK=TRUE

# Force single OpenMP library (PyTorch's version for best compatibility)
export DYLD_INSERT_LIBRARIES="$BACKEND_DIR/memvid_venv/lib/python3.12/site-packages/torch/lib/libomp.dylib"

# Limit OpenMP threads to prevent excessive threading
export OMP_NUM_THREADS=4

# Additional OpenMP environment variables for stability
export KMP_AFFINITY=disabled
export MKL_THREADING_LAYER=GNU

# Fix for macOS fork safety warnings and semaphore leaks
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
export PYTHONWARNINGS="ignore::UserWarning:multiprocessing.resource_tracker"

# Cleanup stale processes on port 8000
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

echo "========================================="
echo "FastAPI Server with OpenMP Fix"
echo "========================================="
echo "OpenMP Library: $DYLD_INSERT_LIBRARIES"
echo "Max Threads: $OMP_NUM_THREADS"
echo "Fork Safety: Disabled"
echo "Resource Tracker: Warnings Suppressed"
echo "========================================="
echo ""

# Change to backend directory
cd "$BACKEND_DIR"

# Activate virtual environment and start server
source "$BACKEND_DIR/memvid_venv/bin/activate"

# Create log directory if it doesn't exist
mkdir -p "$BACKEND_DIR/logs"

# Start uvicorn with reload for development and log to file
echo "Starting server... Logs: $BACKEND_DIR/logs/server.log"
python -m uvicorn main:app --reload --port 8000 --host 0.0.0.0 2>&1 | tee "$BACKEND_DIR/logs/server.log"
