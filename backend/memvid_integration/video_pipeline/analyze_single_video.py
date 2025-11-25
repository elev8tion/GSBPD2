#!/usr/bin/env python3
"""
Single Video Frame Analysis - Wrapper for frame_analyzer.py
Handles a single video folder path directly
"""

import os
import sys
import json
from pathlib import Path
from frame_analyzer import FrameAnalyzer

def main():
    if len(sys.argv) > 1:
        video_path = Path(sys.argv[1])
    else:
        video_path = Path.cwd()

    if not video_path.exists():
        print(f"❌ Error: Path does not exist: {video_path}")
        sys.exit(1)

    # If it's a directory with frames, use it directly
    if video_path.is_dir():
        frames = sorted(list(video_path.glob('frame_*.png')))
        if frames:
            print(f"🎯 Analyzing single video: {video_path.name}")
            print(f"📊 Total frames found: {len(frames)}")
            print()

            # Run analyzer on parent directory
            parent_dir = video_path.parent
            analyzer = FrameAnalyzer(parent_dir)

            # Filter to only analyze this specific folder
            original_get_video_folders = analyzer.get_video_folders
            def get_single_folder():
                return [video_path]
            analyzer.get_video_folders = get_single_folder

            # Run analysis
            plan = analyzer.generate_analysis_plan()

            # Save to the video folder itself
            output_path = video_path / "analysis_plan.json"
            with open(output_path, 'w') as f:
                json.dump(plan, f, indent=2)

            analyzer.print_summary(plan)
            print(f"\n✅ Analysis plan saved to: {output_path}")

            return

    print(f"❌ Error: No frames found in {video_path}")
    print("Expected frame files named: frame_0001.png, frame_0002.png, etc.")
    sys.exit(1)

if __name__ == "__main__":
    main()
