# Kre8VidMems - Setup Guide

## 🚀 Quick Start (Automatic Virtual Environment)

### Step 1: Install Python & Homebrew

**Install Homebrew** (if not installed):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Install Python**:
```bash
brew install python3
```

**Install FFmpeg** (required for video creation):
```bash
brew install ffmpeg
```

### Step 2: Run Auto-Setup

```bash
cd /Users/kckc/Downloads/memvideo
source setup.sh
```

This will automatically:
- ✅ Create a virtual environment (`.venv/`)
- ✅ Activate it
- ✅ Install all dependencies
- ✅ Install kre8vidmems in development mode

### Step 3: Use the CLI Wrapper

Instead of manually activating the venv each time, use the `./kre8` wrapper:

```bash
# Run tests
./kre8 test

# Run example
./kre8 example

# Run your own script
./kre8 python my_script.py

# Start Python shell (with kre8vidmems available)
./kre8 shell
```

## 📋 Manual Virtual Environment Usage

If you prefer manual control:

```bash
# Activate
source .venv/bin/activate

# Use normally
python test_build.py
python examples/simple_example.py

# Deactivate when done
deactivate
```

## 🔄 Updating Dependencies

```bash
source .venv/bin/activate
pip install -r requirements.txt --upgrade
```

## 🎯 Quick Test

After setup, verify everything works:

```bash
./kre8 test
```

## 📂 File Structure

```
/Users/kckc/Downloads/memvideo/
├── setup.sh          # Auto-setup script (source this)
├── kre8              # CLI wrapper (./kre8 command)
├── .venv/            # Virtual environment (auto-created)
├── kre8vidmems/      # Main package
├── examples/         # Example scripts
└── test_build.py     # Verification tests
```

## 💡 Tips

1. **Always use `./kre8`** - No need to remember to activate venv
2. **Re-run `source setup.sh`** if you delete `.venv/`
3. **Add to your `.zshrc`** for convenience:
   ```bash
   alias kre8vid='cd /Users/kckc/Downloads/memvideo && source .venv/bin/activate'
   ```

## ⚠️ Troubleshooting

**"command not found: python3"**
- Install Python: `brew install python3`

**"command not found: brew"**
- Install Homebrew (see Step 1 above)

**"FFmpeg not found"**
- Install FFmpeg: `brew install ffmpeg`

**Virtual environment issues**
- Delete and recreate: `rm -rf .venv && source setup.sh`
