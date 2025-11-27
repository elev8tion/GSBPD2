# Kre8VidMems

**Video-based AI Memory** - Store and search knowledge in MP4 files using QR codes and semantic search.

## 🚀 Features
- ✅ **No Docker** - Native FFmpeg with Mac hardware acceleration
- ✅ **Simple API** - Create and search memories in 3 lines of code
- ✅ **Tiny Storage** - Compress knowledge bases 50-100x smaller than databases
- ✅ **Fast Search** - Sub-second retrieval with Annoy vector search
- ✅ **Portable** - Share memories as simple MP4 files

## 📦 Installation

### Prerequisites
```bash
# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg libzbar0

# Windows
# Download FFmpeg from https://ffmpeg.org/download.html
```

### Install Package
```bash
pip install -e .
```

## 🎯 Quick Start

### Create a Memory
```python
from kre8vidmems import Kre8VidMemory

# Create memory
mem = Kre8VidMemory()
mem.add("Quantum computing uses qubits for parallel processing.")
mem.add("Machine learning requires large datasets for training.")
mem.save("my_knowledge")  # Creates my_knowledge.mp4 and my_knowledge.idx
```

### Search a Memory
```python
# Load and search
mem = Kre8VidMemory.load("my_knowledge")
results = mem.search("quantum physics")

for result in results:
    print(f"Score: {result['score']:.2f}")
    print(f"Text: {result['text']}\n")
```

## 🏗️ Architecture

```
Text → Chunks → Embeddings → Annoy Index
         ↓
      QR Codes → Video Frames → MP4 File
```

- **Core**: Text chunking, QR generation, embeddings
- **Storage**: Annoy index (mmap), FFmpeg video encoding
- **API**: Simple `Kre8VidMemory` interface

## 🎨 Example Use Cases

### Knowledge Base
```python
mem = Kre8VidMemory()
mem.add_file("documentation.txt")
mem.add_file("notes.txt")
mem.save("knowledge_base")
```

### Search
```python
mem = Kre8VidMemory.load("knowledge_base")
results = mem.search("how to install", top_k=3)
```

## 🔧 Configuration

Edit `kre8vidmems/config.py` to customize:
- QR code settings
- Chunk size and overlap
- Video encoding parameters
- Annoy index trees

## 📖 Differences from Memvid
- ❌ No Docker required
- ✅ Native FFmpeg with Mac hardware acceleration (`hevc_videotoolbox`)
- ✅ Annoy instead of FAISS (memory-mapped, simpler)
- ✅ Modular architecture (core/storage/api)
- ✅ Cleaner, simpler codebase

## 📝 License
MIT
