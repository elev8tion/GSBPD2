#!/bin/bash
# Test that the OpenMP fix resolves the server crash

echo "========================================="
echo "Testing OpenMP Library Conflict Fix"
echo "========================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Kill any existing servers
echo "[1] Stopping any existing servers..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
sleep 2

# Set the OpenMP library fix
export KMP_DUPLICATE_LIB_OK=TRUE
export DYLD_INSERT_LIBRARIES="$SCRIPT_DIR/memvid_venv/lib/python3.12/site-packages/torch/lib/libomp.dylib"
export OMP_NUM_THREADS=4
export KMP_AFFINITY=disabled
export MKL_THREADING_LAYER=GNU

echo "[2] Starting server with OpenMP fix..."
echo "    DYLD_INSERT_LIBRARIES=$DYLD_INSERT_LIBRARIES"
echo ""

# Activate venv and start server in background
source "$SCRIPT_DIR/memvid_venv/bin/activate"
python -m uvicorn main:app --port 8000 --log-level info > /tmp/openmp_test.log 2>&1 &
SERVER_PID=$!

echo "[3] Server PID: $SERVER_PID"
echo "[4] Waiting for server to start..."
sleep 8

# Check if server is still running
if ! ps -p $SERVER_PID > /dev/null; then
    echo "❌ Server crashed during startup!"
    echo "    Check logs: /tmp/openmp_test.log"
    exit 1
fi

echo "✓ Server started successfully"
echo ""

# Test endpoints
echo "[5] Testing /health endpoint..."
HEALTH_RESPONSE=$(curl -s -m 5 http://localhost:8000/health)
if [ $? -eq 0 ]; then
    echo "✓ /health: $HEALTH_RESPONSE"
else
    echo "❌ /health failed"
fi
echo ""

# Critical test: NBA teams endpoint (this is where it crashed before)
echo "[6] Testing /nba/teams endpoint (crash point)..."
echo "    This may take 10-15 seconds..."
TEAMS_RESPONSE=$(curl -s -m 30 http://localhost:8000/nba/teams)
CURL_EXIT=$?

if [ $CURL_EXIT -eq 0 ]; then
    TEAM_COUNT=$(echo "$TEAMS_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('total', 0))" 2>/dev/null)
    echo "✓ /nba/teams: Retrieved $TEAM_COUNT teams"
    echo ""
else
    echo "❌ /nba/teams failed (exit code: $CURL_EXIT)"
    echo ""
fi

# Check if server is still alive after the critical test
sleep 2
if ps -p $SERVER_PID > /dev/null; then
    echo "✓ Server still running after FAISS query!"
    echo ""
    echo "========================================="
    echo "✅ FIX SUCCESSFUL - Server Stable"
    echo "========================================="
    echo ""
    echo "Server is running on http://localhost:8000"
    echo "PID: $SERVER_PID"
    echo ""
    echo "To stop: kill $SERVER_PID"
    echo "To view logs: tail -f /tmp/openmp_test.log"
    echo ""
else
    echo "❌ Server crashed after FAISS query"
    echo "    Check crash logs: /tmp/openmp_test.log"
    echo ""
    echo "========================================="
    echo "❌ FIX FAILED - Further Investigation Needed"
    echo "========================================="
    exit 1
fi
