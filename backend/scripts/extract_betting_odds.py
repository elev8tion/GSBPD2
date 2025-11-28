#!/usr/bin/env python3
"""
Extract betting odds from screen recording video using backend frame processing pipeline.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Any
import json
from lib.kre8vidmems.kre8vidmems.storage.video_store import VideoStore

def get_video_info(video_path: str) -> Dict[str, Any]:
    """Get basic video information."""
    cap = cv2.VideoCapture(video_path)
    try:
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = total_frames / fps if fps > 0 else 0

        return {
            'total_frames': total_frames,
            'fps': fps,
            'width': width,
            'height': height,
            'duration_seconds': duration,
            'duration_formatted': f"{int(duration // 60)}:{int(duration % 60):02d}"
        }
    finally:
        cap.release()

def extract_sample_frames(video_path: str, num_samples: int = 20) -> List[int]:
    """Calculate frame numbers to sample evenly throughout video."""
    info = get_video_info(video_path)
    total_frames = info['total_frames']

    # Sample frames evenly throughout the video
    step = total_frames // num_samples
    frame_numbers = [i * step for i in range(num_samples)]

    return frame_numbers

def save_frames_for_analysis(video_path: str, output_dir: str = '/tmp/betting_odds_analysis'):
    """Extract and save frames from video for odds extraction."""
    print(f"Processing video: {video_path}")

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Get video info
    info = get_video_info(video_path)
    print(f"Video info:")
    print(f"  Duration: {info['duration_formatted']}")
    print(f"  Total frames: {info['total_frames']}")
    print(f"  FPS: {info['fps']:.2f}")
    print(f"  Resolution: {info['width']}x{info['height']}")

    # Initialize VideoStore
    video_store = VideoStore()

    # Extract sample frames
    print("\nExtracting sample frames...")
    frame_numbers = extract_sample_frames(video_path, num_samples=20)
    frames = video_store.extract_frames(video_path, frame_numbers)

    # Save frames
    saved_frames = []
    for i, (frame_num, frame) in enumerate(zip(frame_numbers, frames)):
        timestamp = frame_num / info['fps']
        minutes = int(timestamp // 60)
        seconds = int(timestamp % 60)

        frame_filename = f"frame_{i:03d}_t{minutes:02d}m{seconds:02d}s.png"
        frame_path = output_path / frame_filename
        cv2.imwrite(str(frame_path), frame)

        saved_frames.append({
            'index': i,
            'frame_number': frame_num,
            'timestamp': f"{minutes:02d}:{seconds:02d}",
            'path': str(frame_path)
        })

    print(f"\nSaved {len(saved_frames)} frames to: {output_dir}")

    # Save metadata
    metadata = {
        'video_path': video_path,
        'video_info': info,
        'frames': saved_frames
    }

    metadata_path = output_path / 'metadata.json'
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"Metadata saved to: {metadata_path}")

    return metadata

def analyze_frames_for_odds(metadata_path: str):
    """Analyze extracted frames to find betting odds information."""
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    print("\nAnalyzing frames for betting odds...")
    print("=" * 60)

    odds_data = []

    for frame_info in metadata['frames']:
        print(f"\nFrame {frame_info['index']} @ {frame_info['timestamp']}")
        print(f"  Path: {frame_info['path']}")

        # Load frame
        frame = cv2.imread(frame_info['path'])

        # Here you could add OCR or other analysis
        # For now, we'll just output the frame info
        odds_data.append({
            'timestamp': frame_info['timestamp'],
            'frame_path': frame_info['path'],
            'needs_manual_review': True
        })

    return odds_data

if __name__ == "__main__":
    video_path = "/Users/kcdacre8tor/Downloads/ScreenRecording_11-28-2025 13-20-35_1.mov"

    # Extract frames
    metadata = save_frames_for_analysis(video_path)

    # Analyze frames
    metadata_path = '/tmp/betting_odds_analysis/metadata.json'
    odds_data = analyze_frames_for_odds(metadata_path)

    print("\n" + "=" * 60)
    print("EXTRACTION COMPLETE")
    print("=" * 60)
    print(f"\nNext steps:")
    print(f"1. Review frames in: /tmp/betting_odds_analysis/")
    print(f"2. Identify frames with betting odds visible")
    print(f"3. Extract odds data structure from those frames")
