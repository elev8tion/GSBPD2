# macOS Server Crash Fix

## Problem
The Python backend server was crashing on macOS with "Python Terminated" popups due to:

1. **OpenMP Library Conflicts** - FAISS (used by Memvid) loading multiple OpenMP libraries causing crashes
2. **Multiprocessing Semaphore Leaks** - Resources not being cleaned up properly, triggering macOS fork safety warnings
3. **Resource Tracker Warnings** - macOS being strict about cleanup during server shutdown

## Solution

### Environment Variables
The following environment variables prevent crashes:

```bash
# Critical fix for multiple OpenMP libraries
export KMP_DUPLICATE_LIB_OK=TRUE

# Force single OpenMP library (PyTorch's version)
export DYLD_INSERT_LIBRARIES="<path>/torch/lib/libomp.dylib"

# Limit OpenMP threads
export OMP_NUM_THREADS=4

# OpenMP stability
export KMP_AFFINITY=disabled
export MKL_THREADING_LAYER=GNU

# macOS fork safety and semaphore leak prevention
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
export PYTHONWARNINGS="ignore::UserWarning:multiprocessing.resource_tracker"
```

### Usage

**There is ONLY ONE way to start the server:**

```bash
cd backend
./start
```

**DO NOT run any of these:**
```bash
uvicorn main:app --reload              # ❌ Will crash - missing environment variables
python -m uvicorn main:app --reload    # ❌ Will crash - missing environment variables
./scripts/start.sh                     # ❌ Wrong - use ./start instead
```

The `./start` launcher ensures all crash prevention environment variables are set correctly.

### Monitoring

Server logs are saved to `logs/server.log` for debugging. If you see crashes:

1. Check `logs/server.log` for error messages
2. Verify all environment variables are set in `scripts/start.sh`
3. Ensure no other processes are using port 8000
4. Make sure you're using `./start` not running uvicorn directly

### Technical Details

- **OpenMP**: FAISS vectorization library requires OpenMP. Multiple OpenMP libraries cause crashes on macOS
- **Fork Safety**: macOS High Sierra+ enforces strict fork safety. We disable this for multiprocessing
- **Semaphore Leaks**: Python multiprocessing creates semaphores that aren't always cleaned up properly on crashes
- **Auto-Cleanup**: Script kills stale processes on port 8000 before starting

### Verification

To verify the server is running without crashes:

```bash
# Check server health
curl http://localhost:8000/health

# Monitor logs for semaphore warnings
tail -f logs/server.log

# Check process is stable
ps aux | grep uvicorn
```

If you see "resource_tracker" warnings, it means resources leaked during a previous crash. The current session should be stable with the fixes applied.
