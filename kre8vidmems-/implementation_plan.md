# Kre8VidMems Redesign Plan

## Goal Description
Rebuild the system as a new library named **`kre8vidmems`**.
1.  **Rename**: Change all `memvid` references to `kre8vidmems`.
2.  **Remove Docker**: Native FFmpeg only (Mac optimized).
3.  **Replace FAISS with Annoy**: Simpler, mmap-friendly vector storage.
4.  **Modularize**: Clean, component-based architecture.

## User Review Required
> [!IMPORTANT]
> **Workspace Access**: I currently do not have access to `/Users/kckc/Desktop/kre8vidmems`. Please add this folder to your workspace or allow me to build it in the current directory (`/Users/kckc/Downloads/memvideo/kre8vidmems`).
> **No Docker**: Relies on local `ffmpeg`.
> **Breaking Change**: New file formats and API.

## Proposed Architecture

### 1. Directory Structure
```text
kre8vidmems/
├── core/
│   ├── __init__.py
│   ├── chunker.py       # Text splitting
│   ├── qr_generator.py  # QR creation
│   └── vectorizer.py    # Embeddings
├── storage/
│   ├── __init__.py
│   ├── video_store.py   # FFmpeg wrapper (Native)
│   └── vector_store.py  # Annoy wrapper
├── api/
│   ├── __init__.py
│   ├── memory.py        # Main "Kre8VidMems" class
│   └── chat.py          # LLM integration
├── config.py            # Configuration
└── utils.py             # Helpers
```

### 2. Key Components

#### `kre8vidmems/config.py`
- Default to `hevc_videotoolbox` on macOS.
- Annoy index settings (trees, metric).

#### `kre8vidmems/api/memory.py`
- **`Kre8VidMemory`** (Main Class):
    - `add(text)`
    - `save(path)`
    - `load(path)`
    - `search(query)`

#### `kre8vidmems/storage/video_store.py`
- Detects OS.
- Builds FFmpeg command line:
    - Mac: `-c:v hevc_videotoolbox -q:v 50`
    - Other: `-c:v libx265 -crf 28`

### 3. Dependencies
- `annoy`
- `sentence-transformers`
- `opencv-python`
- `qrcode[pil]`
- `numpy`
- `tqdm`

## Verification Plan
1.  **Environment**: Check `ffmpeg` and `annoy`.
2.  **Build**: Create a memory video from sample text.
3.  **Search**: Verify retrieval accuracy.
