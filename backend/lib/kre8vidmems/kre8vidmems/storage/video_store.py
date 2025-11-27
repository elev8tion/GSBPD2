"""
Video storage using FFmpeg (Mac optimized)
"""
import subprocess
import cv2
import json
import tempfile
import shutil
from pathlib import Path
from typing import List
import numpy as np
from tqdm import tqdm
from kre8vidmems.config import get_ffmpeg_codec_args, VIDEO_FPS, FRAME_WIDTH, FRAME_HEIGHT

class VideoStore:
    """Handles video encoding with native FFmpeg"""
    
    def __init__(self):
        self.fps = VIDEO_FPS
        self.width = FRAME_WIDTH
        self.height = FRAME_HEIGHT
        self._verify_ffmpeg()
        
    def _verify_ffmpeg(self):
        """Check if FFmpeg is available"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError(
                "FFmpeg not found. Please install it:\n"
                "  macOS: brew install ffmpeg\n"
                "  Linux: sudo apt install ffmpeg\n"
                "  Windows: Download from ffmpeg.org"
            )
            
    def create_video(self, frames: List[np.ndarray], output_path: str, show_progress: bool = True):
        """Create video from frames using FFmpeg"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create temporary directory for frames
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Save frames as PNGs
            if show_progress:
                frame_iter = tqdm(enumerate(frames), total=len(frames), desc="Saving frames")
            else:
                frame_iter = enumerate(frames)
                
            for i, frame in frame_iter:
                frame_path = temp_path / f"frame_{i:06d}.png"
                cv2.imwrite(str(frame_path), frame)
                
            # Build FFmpeg command
            codec_args = get_ffmpeg_codec_args()
            cmd = [
                'ffmpeg', '-y',
                '-framerate', str(self.fps),
                '-i', str(temp_path / 'frame_%06d.png'),
                *codec_args,
                '-pix_fmt', 'yuv420p',
                str(output_path)
            ]
            
            # Run FFmpeg
            if show_progress:
                print(f"Encoding video with FFmpeg...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise RuntimeError(f"FFmpeg encoding failed:\n{result.stderr}")
                
        # Get file size
        size_mb = output_path.stat().st_size / (1024 * 1024)
        if show_progress:
            print(f"✓ Video created: {output_path} ({size_mb:.2f} MB)")
            
        return {
            'path': str(output_path),
            'frames': len(frames),
            'size_mb': size_mb,
            'fps': self.fps
        }
        
    def extract_frame(self, video_path: str, frame_number: int) -> np.ndarray:
        """Extract a single frame from video"""
        cap = cv2.VideoCapture(video_path)
        try:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = cap.read()
            if not ret:
                raise ValueError(f"Could not read frame {frame_number}")
            return frame
        finally:
            cap.release()
            
    def extract_frames(self, video_path: str, frame_numbers: List[int]) -> List[np.ndarray]:
        """Extract multiple frames from video"""
        cap = cv2.VideoCapture(video_path)
        frames = []
        
        try:
            for frame_num in sorted(frame_numbers):
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                ret, frame = cap.read()
                if ret:
                    frames.append(frame)
        finally:
            cap.release()
            
        return frames
