# Kre8VidMems - Complete Package

**Video-based AI Memory using QR codes and semantic search**

## 📦 What's Included

This package contains everything needed to build and run Kre8VidMems:

### Core Library
- `kre8vidmems/` - Complete Python package
  - `core/` - Text processing, QR codes, embeddings
  - `storage/` - Video encoding (FFmpeg), Vector index (Annoy)
  - `api/` - Main `Kre8VidMemory` class
  - `config.py` - Mac-optimized settings

### Setup & Installation
- `setup.py` - Package installer
- `requirements.txt` - Python dependencies
- `setup.sh` - Auto-setup script (creates venv, installs deps)
- `kre8` - CLI wrapper (auto-uses venv)

### Documentation
- `README.md` - Main documentation
- `SETUP_GUIDE.md` - Detailed installation guide
- `BUILD_COMPLETE.md` - Build verification
- `TEST_RESULTS.md` - Expected test outcomes

### Design Specifications
- `ui_design/` - Complete UI design (framework-agnostic)
  - Wireframes for all 5 screens
  - User flows
  - Component specifications
  - Design system (colors, typography, spacing)

### Testing
- `test_build.py` - Comprehensive verification tests
- `examples/simple_example.py` - Demo script

### Utilities
- `auto_venv.zsh` - Shell integration for auto-activation

### Reports (from original analysis)
- `project_dissection_report.md` - Original codebase analysis
- `redesign_strategy_report.md` - Architecture redesign rationale
- `implementation_plan.md` - Development plan

## 🚀 Quick Start on New Machine

### 1. Prerequisites
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and FFmpeg
brew install python3 ffmpeg
```

### 2. Extract and Setup
```bash
# Navigate to extracted folder
cd kre8vidmems

# Run auto-setup
source setup.sh
```

This will:
- Create virtual environment (`.venv/`)
- Install all Python dependencies
- Install kre8vidmems in development mode

### 3. Verify Installation
```bash
# Run tests
./kre8 test

# Or manually
python test_build.py
```

### 4. Run Example
```bash
./kre8 example
```

## 📖 Key Features

- ✅ **No Docker** - Native FFmpeg with Mac hardware acceleration
- ✅ **Simple API** - Create and search memories in 3 lines
- ✅ **Annoy Index** - Memory-mapped vector search
- ✅ **Modular** - Clean separation: core/storage/api
- ✅ **Portable** - Share memories as MP4 files

## 🎯 Basic Usage

```python
from kre8vidmems import Kre8VidMemory

# Create memory
mem = Kre8VidMemory()
mem.add("Your knowledge here...")
mem.save("my_memory")

# Search memory
mem = Kre8VidMemory.load("my_memory")
results = mem.search("query")

for result in results:
    print(result['text'])
```

## 📂 Directory Structure

```
kre8vidmems/
├── kre8vidmems/          # Main package
│   ├── core/             # Text, QR, embeddings
│   ├── storage/          # Video, index
│   └── api/              # Memory class
├── ui_design/            # UI specifications
├── examples/             # Usage examples
├── setup.sh              # Auto-setup script
├── kre8                  # CLI wrapper
└── README.md             # This file
```

## 🎨 Building the UI

See `ui_design/README.md` for complete UI specifications.

**Recommended frameworks:**
- **Quick prototype**: Streamlit (1-3 days)
- **Production**: Tauri + Svelte (1-2 weeks)

## 🔧 Configuration

Edit `kre8vidmems/config.py` to customize:
- QR code settings
- Chunk size and overlap
- Video encoding (codec, quality)
- Annoy index parameters

## 📝 Dependencies

**Python packages:**
- annoy
- sentence-transformers
- opencv-python
- qrcode[pil]
- numpy
- tqdm

**System requirements:**
- Python 3.8+
- FFmpeg
- ~500MB disk space (for dependencies)

## 🐛 Troubleshooting

**"command not found: python3"**
```bash
brew install python3
```

**"FFmpeg not found"**
```bash
brew install ffmpeg
```

**Virtual environment issues**
```bash
rm -rf .venv
source setup.sh
```

## 📄 License

MIT

## 🙏 Credits

Built focusing on simplicity and Mac optimization.
