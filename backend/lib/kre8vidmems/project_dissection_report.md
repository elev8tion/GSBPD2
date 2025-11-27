# Memvid Project Code Dissection Report

## 1. Project Overview
**Memvid** is a Python library that compresses large knowledge bases into searchable MP4 video files. It encodes text chunks as QR codes in video frames and uses semantic search (via embeddings) to retrieve relevant frames, decode them, and provide context to an LLM for conversational interaction. This approach offers a portable, offline-first, and highly compressed "SQLite for AI memory".

## 2. Directory Structure
The project follows a standard Python package layout with a core library (`memvid`), supporting Docker scripts, examples, and tests.

```text
olow304-memvid/
├── memvid/                 # Core Python package
│   ├── __init__.py         # Exports main classes
│   ├── chat.py             # Conversational interface (MemvidChat)
│   ├── config.py           # Configuration defaults and constants
│   ├── docker_manager.py   # Docker backend management
│   ├── encoder.py          # Video creation (MemvidEncoder)
│   ├── index.py            # Vector index management (IndexManager)
│   ├── interactive.py      # CLI chat functions
│   ├── llm_client.py       # LLM provider abstraction
│   ├── retriever.py        # Search and retrieval (MemvidRetriever)
│   └── utils.py            # Shared utilities (QR, Video I/O)
├── docker/                 # Docker environment for encoding
│   ├── Dockerfile          # Image definition
│   ├── scripts/            # Scripts run inside container
│   └── ...                 # Helper scripts (start_docker_container.sh)
├── examples/               # Usage examples (book_chat.py, etc.)
├── tests/                  # Unit tests
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
└── setup.py                # Package installation script
```

## 3. Core Modules Dissection

### 3.1. `memvid/encoder.py` (MemvidEncoder)
**Role**: The "Writer". Responsible for converting text into a video memory file.
*   **Key Functions**:
    *   `add_chunks()`, `add_text()`, `add_pdf()`, `add_epub()`: Ingests data.
    *   `build_video()`: Orchestrates the creation of QR frames and the final video file.
    *   `_generate_qr_frames()`: Creates QR code images for each text chunk.
    *   `_encode_with_ffmpeg()` / `_encode_with_opencv()`: Assembles frames into a video.
*   **Interconnections**:
    *   Uses `memvid.utils` for QR generation.
    *   Uses `memvid.index.IndexManager` to generate embeddings and save the index.
    *   Uses `memvid.docker_manager.DockerManager` to offload H.265 encoding to Docker.
    *   Reads settings from `memvid.config`.

### 3.2. `memvid/retriever.py` (MemvidRetriever)
**Role**: The "Reader". Responsible for searching and reading from the video memory.
*   **Key Functions**:
    *   `search()`: Semantic search returning text chunks.
    *   `search_with_metadata()`: Returns text plus score and metadata.
    *   `_decode_frames_parallel()`: Efficiently reads and decodes multiple frames.
    *   `prefetch_frames()`: Caches frames for performance.
*   **Interconnections**:
    *   Uses `memvid.index.IndexManager` to find relevant frame numbers based on query embeddings.
    *   Uses `memvid.utils` for video frame extraction and QR decoding.
    *   Reads settings from `memvid.config`.

### 3.3. `memvid/chat.py` (MemvidChat)
**Role**: The "Brain". Manages the conversation loop.
*   **Key Functions**:
    *   `chat()`: Main entry point for user messages.
    *   `_get_context()`: Retrieves relevant info using the Retriever.
    *   `_build_messages()`: Constructs the prompt with history and context.
    *   `interactive_chat()`: Runs a CLI chat loop.
*   **Interconnections**:
    *   Instantiates `MemvidRetriever` to get context.
    *   Uses `memvid.llm_client.LLMClient` to talk to AI models (OpenAI, Google, Anthropic).
    *   Manages session state (history).

### 3.4. `memvid/index.py` (IndexManager)
**Role**: The "Librarian". Manages embeddings and the vector index.
*   **Key Functions**:
    *   `add_chunks()`: Generates embeddings (using `sentence-transformers`) and adds them to the FAISS index.
    *   `search()`: Performs nearest-neighbor search.
    *   `save()` / `load()`: Persists the index and metadata to disk.
*   **Interconnections**:
    *   Used by `Encoder` to build the index.
    *   Used by `Retriever` to query the index.
    *   Wraps `faiss` and `sentence_transformers`.

### 3.5. `memvid/llm_client.py` (LLMClient)
**Role**: The "Translator". Abstracts different LLM APIs.
*   **Key Functions**:
    *   `chat()` / `chat_stream()`: Unified interface for sending messages.
    *   `OpenAIProvider`, `GoogleProvider`, `AnthropicProvider`: Concrete implementations.
*   **Interconnections**:
    *   Used by `MemvidChat`.
    *   Requires API keys (via environment variables).

### 3.6. `memvid/docker_manager.py` (DockerManager)
**Role**: The "Infrastructure". Manages the Docker container for heavy encoding tasks.
*   **Key Functions**:
    *   `ensure_container_ready()`: Builds/checks the Docker image.
    *   `execute_ffmpeg()`: Runs FFmpeg inside the container, handling path mapping (especially for WSL).
*   **Interconnections**:
    *   Used by `MemvidEncoder` when high-efficiency codecs (H.265/AV1) are selected.

### 3.7. `memvid/utils.py`
**Role**: The "Toolbox". Low-level helper functions.
*   **Key Functions**:
    *   `encode_to_qr()` / `decode_qr()`: QR code handling (with gzip compression for large data).
    *   `chunk_text()`: Splits text into overlapping chunks.
    *   `extract_frame()` / `batch_extract_frames()`: Video I/O using OpenCV.

### 3.8. `memvid/config.py`
**Role**: The "Settings". Central configuration.
*   **Content**:
    *   Default parameters for QR codes, codecs (H.264, H.265, AV1), retrieval (top_k), and LLM models.

## 4. Supporting Components

### 4.1. `docker/`
Contains the `Dockerfile` (Ubuntu + FFmpeg + Python) and scripts to run inside it. This ensures a consistent environment for video encoding, which can be dependency-heavy.

### 4.2. `examples/`
Scripts demonstrating how to use the library:
*   `build_memory.py`: Creating a video from text.
*   `chat_memory.py`: Chatting with a created video.
*   `book_chat.py`: Ingesting a PDF/EPUB.

## 5. Data Flow & Interconnections

1.  **Ingestion (Encoder)**:
    *   `User Input` (Text/PDF) -> `Encoder.add_text()` -> `utils.chunk_text()` -> `Encoder.chunks`.

2.  **Build Process (Encoder)**:
    *   **Visual Path**: `Encoder.chunks` -> `utils.encode_to_qr()` -> `QR Images` -> `Encoder._encode_with_ffmpeg()` (via `DockerManager` if needed) -> **`video.mp4`**.
    *   **Semantic Path**: `Encoder.chunks` -> `IndexManager.add_chunks()` -> `sentence-transformers` -> `Embeddings` -> `FAISS Index` -> **`index.json/.faiss`**.

3.  **Retrieval (Retriever)**:
    *   `User Query` -> `IndexManager.search()` -> `Frame Numbers`.
    *   `Frame Numbers` -> `utils.batch_extract_frames()` (from **`video.mp4`**) -> `utils.decode_qr()` -> `Text Context`.

4.  **Interaction (Chat)**:
    *   `User Message` -> `Retriever.search()` -> `Context`.
    *   `Context` + `History` -> `LLMClient` -> `LLM API` -> **`Response`**.

## 6. Key Dependencies
*   **Video/Image**: `opencv-python`, `qrcode[pil]`, `pyzbar`, `Pillow`.
*   **AI/ML**: `sentence-transformers`, `faiss-cpu`, `numpy`.
*   **LLM SDKs** (Optional): `openai`, `google-genai`, `anthropic`.
*   **System**: `ffmpeg` (required for encoding), `docker` (optional, for advanced encoding).
