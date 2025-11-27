#!/bin/bash
# Auto-setup script for Kre8VidMems
# This script automatically creates and activates a virtual environment

set -e  # Exit on error

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

echo "🚀 Kre8VidMems Auto-Setup"
echo "========================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    echo ""
    echo "Please install Python 3:"
    echo "  Option 1 - Homebrew (recommended):"
    echo "    /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    echo "    brew install python3"
    echo ""
    echo "  Option 2 - Download from python.org:"
    echo "    https://www.python.org/downloads/"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    echo "✓ Virtual environment created: $VENV_DIR"
else
    echo "✓ Virtual environment exists: $VENV_DIR"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies if requirements.txt exists
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip install -r "$PROJECT_DIR/requirements.txt" --quiet
    echo "✓ Dependencies installed"
fi

# Install package in development mode
if [ -f "$PROJECT_DIR/setup.py" ]; then
    echo "📦 Installing kre8vidmems in development mode..."
    pip install -e "$PROJECT_DIR" --quiet
    echo "✓ Kre8vidmems installed"
fi

# Check for FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo ""
    echo "⚠️  FFmpeg not found (required for video creation)"
    echo "Install with: brew install ffmpeg"
else
    echo "✓ FFmpeg found: $(ffmpeg -version 2>&1 | head -1 | cut -d' ' -f3)"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment in the future:"
echo "  source .venv/bin/activate"
echo ""
echo "Or run this script again:"
echo "  source setup.sh"
