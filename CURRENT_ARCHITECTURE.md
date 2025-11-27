# Current Architecture Documentation - Kre8VidMems Migration
## KC DaCRE8TOR's Sports Betting Prediction Dashboard

**Document Purpose**: Complete documentation of the system architecture after migrating from Memvid/FAISS to Kre8VidMems/Annoy.

**Last Updated**: 2025-11-26
**Version**: 2.0 (Kre8VidMems Migration)

**STATUS**: 🔄 MIGRATION IN PROGRESS

---

## Table of Contents
1. [Migration Overview](#migration-overview)
2. [System Architecture](#system-architecture)
3. [Kre8VidMems vs Memvid](#kre8vidmems-vs-memvid)
4. [File Structure](#file-structure)
5. [Backend Services](#backend-services)
6. [Data Storage](#data-storage)
7. [API Endpoints](#api-endpoints)
8. [Migration Status](#migration-status)

---

## 1. Migration Overview

### What Changed
We are replacing the problematic Memvid/FAISS system with Kre8VidMems/Annoy to solve critical macOS compatibility issues.

### Why This Migration
- **FAISS causes crashes** on macOS due to OpenMP library conflicts
- **Threading issues** with FastAPI's uvicorn reload
- **Complex workarounds** required (KMP_DUPLICATE_LIB_OK, DYLD_INSERT_LIBRARIES)
- **Fork safety violations** and semaphore leaks

### Benefits of Kre8VidMems
- ✅ **No OpenMP** - Uses Annoy instead of FAISS
- ✅ **Memory-mapped files** - Perfect for macOS/ARM
- ✅ **Zero configuration** - No environment variables needed
- ✅ **Platform-aware** - Detects macOS and optimizes accordingly
- ✅ **Stable** - No threading conflicts, no crashes

---

## 2. System Architecture

### Current Stack
- **Frontend**: React 19.2.0 + Vite 7.2.4
- **Backend**: FastAPI + Uvicorn
- **ML Engine**: XGBoost + SHAP
- **Storage**: ~~Memvid~~ → **Kre8VidMems** (video-based compression)
- **Vector Search**: ~~FAISS~~ → **Annoy** (memory-mapped)
- **Video Processing**: OpenCV + QR codes
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)

### Architecture Diagram
```
Frontend (React)
    ↓
FastAPI Backend
    ↓
Kre8VidMems API
    ├── Annoy (Vector Search)
    ├── VideoStore (QR + MP4)
    └── Vectorizer (Embeddings)
```

---

## 3. Kre8VidMems vs Memvid

### Component Mapping

| Component | Old (Memvid) | New (Kre8VidMems) |
|-----------|--------------|-------------------|
| **Main API** | MemvidEncoder/Retriever | Kre8VidMemory |
| **Vector Search** | FAISS | Annoy |
| **Index Format** | .faiss | .ann |
| **Metadata** | _index.json | .meta |
| **Video** | .mp4 | .mp4 |
| **Threading** | OpenMP (crashes) | Memory-mapped (stable) |
| **Config** | Environment vars | Zero config |

### API Comparison

**Creating Memory:**
```python
# OLD (Memvid)
from memvid import MemvidEncoder
encoder = MemvidEncoder()
encoder.add_text(text)
encoder.build(name="memory")

# NEW (Kre8VidMems)
from kre8vidmems import Kre8VidMemory
mem = Kre8VidMemory()
mem.add(text)
mem.save("memory")
```

**Searching Memory:**
```python
# OLD (Memvid)
from memvid import MemvidRetriever
retriever = MemvidRetriever('memory.mp4', 'memory_index.json')
results = retriever.search('query')

# NEW (Kre8VidMems)
from kre8vidmems import Kre8VidMemory
mem = Kre8VidMemory.load("memory")
results = mem.search('query', top_k=5)
```

---

## 4. File Structure

### New Kre8VidMems Package
```
kre8vidmems-/
├── kre8vidmems/
│   ├── __init__.py
│   ├── config.py              # Platform detection, Annoy settings
│   ├── api/
│   │   └── memory.py          # Main Kre8VidMemory class
│   ├── core/
│   │   ├── chunker.py         # Text chunking
│   │   ├── vectorizer.py      # Embeddings generation
│   │   └── qr_generator.py    # QR code handling
│   └── storage/
│       ├── vector_store.py    # Annoy index (replaces FAISS)
│       └── video_store.py     # Video/QR storage
├── setup.py
└── requirements.txt
```

### Backend Structure (Updated)
```
backend/
├── main.py                     # FastAPI endpoints
├── services/
│   ├── nba_service.py         # NBA data (needs migration)
│   ├── nfl_service.py         # NFL data (needs migration)
│   ├── knowledge_base.py     # Betting storage (needs migration)
│   └── semantic_search.py    # NEW: Migration adapter
├── memories/                   # Existing Memvid data
│   ├── nba-players/           # To be converted
│   ├── nba-games/             # To be converted
│   └── nba-schedule/          # To be converted
└── embeddings/                 # NEW: Kre8VidMems indices
    ├── nba-players/
    │   ├── embeddings.npy     # Annoy embeddings
    │   └── data.json          # Metadata
    └── ...
```

---

## 5. Backend Services

### 5.1 NBA Data Service (`services/nba_service.py`)

**Current State**: Using Memvid with FAISS (causes hangs)
```python
# OLD CODE (TO BE REPLACED)
from memvid import MemvidRetriever
self.players_retriever = MemvidRetriever(video_path, index_path)
```

**Migration Target**: Kre8VidMems with Annoy
```python
# NEW CODE
from kre8vidmems import Kre8VidMemory
self.players_memory = Kre8VidMemory.load("nba-players")
```

### 5.2 Knowledge Base Service (`services/knowledge_base.py`)

**Current State**: Memvid for bet storage
**Migration Target**: Kre8VidMems for all storage operations

### 5.3 Migration Adapter (`services/semantic_search.py`)

**Purpose**: Temporary compatibility layer during migration
```python
class MemvidRetriever:
    """Drop-in replacement using Kre8VidMems"""
    def __init__(self, video_path, index_path):
        name = video_path.replace('.mp4', '')
        self.memory = Kre8VidMemory.load(name)

    def search(self, query, top_k=5):
        results = self.memory.search(query, top_k)
        return [r['text'] for r in results]
```

---

## 6. Data Storage

### 6.1 Vector Index Migration

**Old (FAISS)**:
- Format: `.faiss` binary files
- Issues: OpenMP conflicts, threading problems
- Size: ~51KB per index

**New (Annoy)**:
- Format: `.ann` memory-mapped files
- Benefits: No threading issues, works on macOS
- Size: Similar (~50KB per index)
- Config: 15 trees, angular distance metric

### 6.2 Memory Files

**Existing Memories to Convert**:
1. `nba-players` - All NBA rosters with stats
2. `nba-games` - Team standings and records
3. `nba-schedule` - Game schedules
4. `knowledge-base` - Betting history

**Conversion Process**:
```python
# Extract from Memvid
old_retriever = MemvidRetriever(video, index)
texts = extract_all_texts(old_retriever)

# Re-encode with Kre8VidMems
new_memory = Kre8VidMemory()
for text in texts:
    new_memory.add(text)
new_memory.save("converted-memory")
```

---

## 7. API Endpoints

No changes to API endpoints - backend migration is transparent to frontend.

### NBA Endpoints
- `GET /nba/teams` - Get all teams
- `GET /nba/teams/{id}` - Get team by ID
- `GET /nba/players` - Get all players
- `GET /nba/teams/{id}/roster` - Get team roster

### Betting Endpoints
- `GET /portfolio` - Get betting history
- `POST /portfolio/bet` - Place bet
- `POST /portfolio/resolve` - Resolve bet

### ML Endpoints
- `POST /predict` - Generate prediction
- `POST /train` - Retrain model

---

## 8. Migration Status

### ✅ Completed
- [x] Delete old Memvid documentation
- [x] Create Kre8VidMems migration guide
- [x] Map out architecture changes
- [x] Identify all Memvid dependencies (22 files)

### 🔄 In Progress
- [ ] Create migration adapter for compatibility
- [ ] Test Kre8VidMems installation

### 📋 To Do
- [ ] Migrate NBA service to Kre8VidMems
- [ ] Migrate NFL service
- [ ] Migrate Knowledge Base service
- [ ] Convert existing Memvid memories to Annoy
- [ ] Update requirements.txt
- [ ] Remove Memvid dependencies
- [ ] Test complete system
- [ ] Remove migration adapter (after verification)

### Files to Modify

**High Priority** (Core Services):
1. `backend/services/nba_service.py`
2. `backend/services/nfl_service.py`
3. `backend/services/knowledge_base.py`
4. `backend/requirements.txt`

**Medium Priority** (Helper Scripts):
1. `backend/build_nba_games_memory.py`
2. `backend/build_nba_memvid_database.py`
3. `backend/save_rosters_to_memvid.py`
4. `backend/save_schedule_to_memvid.py`

**Low Priority** (Can be deleted):
1. All files in `backend/memvid_integration/`
2. `backend/services/portfolio.py` (deprecated)
3. Old crash fix scripts

---

## 9. Testing Plan

### Unit Tests
1. Verify Kre8VidMemory API compatibility
2. Test Annoy search accuracy
3. Validate data conversion

### Integration Tests
1. Test FastAPI endpoints with new backend
2. Verify search performance (<100ms)
3. Check memory usage

### Platform Tests
1. **macOS ARM** (M1/M2) - Primary target
2. **macOS Intel** - Compatibility check
3. **Linux** - CI/CD environment
4. **No Windows testing required**

---

## 10. Performance Expectations

### Search Performance
- **Old (FAISS)**: <50ms but crashes on macOS
- **New (Annoy)**: <100ms, stable everywhere
- **Trade-off**: Slightly slower but 100% stable

### Memory Usage
- **Old**: High due to FAISS in-memory index
- **New**: Lower due to memory-mapped files

### Startup Time
- **Old**: Slow due to FAISS initialization
- **New**: Fast due to memory-mapped loading

---

## 11. Success Criteria

✅ **No crashes on macOS**
✅ **No environment variables needed**
✅ **All existing features working**
✅ **Search latency under 100ms**
✅ **Zero OpenMP dependencies**
✅ **Clean, simple codebase**

---

## 12. Rollback Plan

If issues arise during migration:
1. Adapter layer allows switching between implementations
2. Original Memvid memories are preserved (not deleted)
3. Feature flag can toggle old/new system
4. Git history allows full reversion

---

**End of Documentation**

This document reflects the current state of the Kre8VidMems migration as of 2025-11-26.