"""
Configuration for Kre8VidMems
"""
import os
import platform

# System Detection
IS_MAC = platform.system() == "Darwin"
IS_ARM = platform.machine() == "arm64"

# QR Code Settings
QR_VERSION = 35  # High capacity
QR_ERROR_CORRECTION = 'M'
QR_BOX_SIZE = 5
QR_BORDER = 3
QR_FILL_COLOR = "black"
QR_BACK_COLOR = "white"

# Chunking
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_OVERLAP = 50

# Embedding
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

# Vector Index (Annoy)
ANNOY_METRIC = 'angular'
ANNOY_TREES = 15  # More trees = more accurate, slower build

# Video Encoding
VIDEO_FPS = 15
FRAME_WIDTH = 256
FRAME_HEIGHT = 256

def get_ffmpeg_codec_args():
    """Get optimized FFmpeg arguments based on platform"""
    if IS_MAC:
        # Use VideoToolbox hardware acceleration on Mac
        return [
            '-c:v', 'hevc_videotoolbox',
            '-q:v', '50',  # Quality (0-100, higher is better for videotoolbox)
            '-allow_sw', '1'
        ]
    else:
        # Fallback to software encoding (x265)
        return [
            '-c:v', 'libx265',
            '-crf', '24',  # Quality (0-51, lower is better for x265)
            '-preset', 'medium'
        ]
