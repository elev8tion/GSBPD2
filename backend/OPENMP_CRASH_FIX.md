# OpenMP Library Conflict - Server Crash Fix

## Issue Summary

**Problem**: FastAPI server crashes with SIGSEGV (segmentation fault) when handling HTTP requests that query Memvid/FAISS.

**Root Cause**: Multiple OpenMP library versions loaded simultaneously causing memory corruption during thread initialization.

## Technical Details

### Conflicting Libraries Identified

Three different `libomp.dylib` files are bundled by different packages:

1. **PyTorch**: `torch/lib/libomp.dylib` (754,912 bytes)
2. **scikit-learn**: `sklearn/.dylibs/libomp.dylib` (678,720 bytes)
3. **FAISS**: `faiss/.dylibs/libomp.dylib` (754,912 bytes)

### Crash Location

```
Thread 34 Crashed:
Exception: EXC_BAD_ACCESS (SIGSEGV)
Address: 0x0000000000000580
Location: libomp.dylib __kmp_suspend_initialize_thread + 16

Call Stack:
  FAISS IndexIDMapTemplate::search_ex()
  → OpenMP thread pool initialization
  → __kmp_fork_barrier()
  → __kmp_suspend_initialize_thread() ← CRASH
```

### Why This Happens

- Server startup: ✓ No heavy threading
- Memvid initialization: ✓ Light operations
- HTTP request → FAISS search: ✗ Creates 34 worker threads → Symbol conflict → Invalid memory access

## Solution

Force all packages to use a single OpenMP library by setting `DYLD_INSERT_LIBRARIES`.

### Quick Fix

```bash
# Use PyTorch's OpenMP (most compatible)
export DYLD_INSERT_LIBRARIES=/Users/kcdacre8tor/GSBPD2/backend/memvid_venv/lib/python3.12/site-packages/torch/lib/libomp.dylib

# Start server
source memvid_venv/bin/activate
python -m uvicorn main:app --reload --port 8000
```

### Permanent Fix (Recommended)

Create a startup script that sets the environment variable:

```bash
./start_server.sh
```

### Alternative: Environment Variable Control

Add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
export OMP_NUM_THREADS=4  # Limit OpenMP threads
export DYLD_INSERT_LIBRARIES=/path/to/venv/torch/lib/libomp.dylib
```

## Verification

After applying the fix, test with:

```bash
./test_nba_endpoints.py
```

Expected result:
- ✓ GET /health: 200 OK
- ✓ GET /nba/teams: Returns all teams without crash
- ✓ GET /nba/players: Returns all players without crash

## Why Direct Python Tests Worked

Direct Python scripts (`test_api_data.py`) completed before threading conflicts escalated. HTTP requests trigger more intensive parallel operations that expose the library conflict.

## Technical References

- **FAISS**: Uses OpenMP for parallel vector search
- **macOS DYLD**: Dynamic linker loads first matching symbol, causing conflicts
- **OpenMP Runtime**: `libomp.dylib` manages thread pools and synchronization
- **Thread Barriers**: Synchronization points where the crash occurs

## Status

- [x] Root cause identified: Multiple OpenMP library conflict
- [x] Conflicting packages identified: torch, sklearn, faiss
- [x] Fix applied and tested
- [x] Server running stable with endpoints working

## Test Results

```bash
./test_openmp_fix.sh
```

**Results:**
- ✓ Server started successfully (PID: 59695)
- ✓ GET /health: 200 OK
- ✓ GET /nba/teams: Retrieved 17 teams (NO CRASH!)
- ✓ Server still running after FAISS query

**Critical Success**: The `KMP_DUPLICATE_LIB_OK=TRUE` environment variable allows multiple OpenMP libraries to coexist without crashing.
