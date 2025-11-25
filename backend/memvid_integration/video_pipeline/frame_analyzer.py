#!/usr/bin/env python3
"""
Intelligent Frame Analysis System
Uses hybrid change detection + fixed sampling strategy
"""

import os
import json
from pathlib import Path
from PIL import Image
import numpy as np
from collections import defaultdict

class FrameAnalyzer:
    def __init__(self, base_dir="."):
        self.base_dir = Path(base_dir)
        self.change_threshold = 0.05  # 5% change threshold
        self.first_pass_interval = 30  # Every 30th frame
        self.second_pass_interval = 10  # Every 10th frame in high-change areas

    def get_video_folders(self):
        """Get all video frame folders"""
        folders = [f for f in self.base_dir.iterdir()
                  if f.is_dir() and not f.name.startswith('.')]
        return sorted(folders)

    def get_frames(self, folder):
        """Get all frame files from a folder"""
        frames = sorted([f for f in folder.glob('frame_*.png')])
        return frames

    def calculate_frame_difference(self, img1_path, img2_path):
        """Calculate visual difference between two frames"""
        try:
            # Load images and resize to reduce computation
            img1 = Image.open(img1_path).resize((320, 180)).convert('L')
            img2 = Image.open(img2_path).resize((320, 180)).convert('L')

            # Convert to numpy arrays
            arr1 = np.array(img1, dtype=np.float32)
            arr2 = np.array(img2, dtype=np.float32)

            # Calculate normalized difference
            diff = np.abs(arr1 - arr2)
            change_ratio = np.mean(diff) / 255.0

            return change_ratio
        except Exception as e:
            print(f"Error comparing frames: {e}")
            return 0.0

    def first_pass_analysis(self, folder):
        """
        First pass: Analyze every 30th frame to create change map
        Returns list of frame indices with their change scores
        """
        frames = self.get_frames(folder)
        total_frames = len(frames)

        print(f"\n{'='*60}")
        print(f"First Pass: {folder.name}")
        print(f"Total frames: {total_frames}")
        print(f"Sampling every {self.first_pass_interval}th frame")
        print(f"{'='*60}")

        change_map = []
        prev_frame_idx = None
        prev_frame_path = None

        # Sample every 30th frame
        for idx in range(0, total_frames, self.first_pass_interval):
            if idx >= len(frames):
                break

            current_frame = frames[idx]

            # Calculate change from previous sampled frame
            if prev_frame_path:
                change_score = self.calculate_frame_difference(
                    prev_frame_path, current_frame
                )
                change_map.append({
                    'frame_idx': idx,
                    'frame_path': str(current_frame),
                    'change_score': float(change_score),
                    'prev_frame_idx': prev_frame_idx
                })

                print(f"Frame {idx:4d}: change={change_score:.3f} "
                      f"{'🔥 HIGH CHANGE' if change_score > self.change_threshold else ''}")
            else:
                # First frame - always include
                change_map.append({
                    'frame_idx': idx,
                    'frame_path': str(current_frame),
                    'change_score': 1.0,  # Always include first frame
                    'prev_frame_idx': None
                })
                print(f"Frame {idx:4d}: FIRST FRAME (always included)")

            prev_frame_idx = idx
            prev_frame_path = current_frame

        return change_map, frames

    def identify_high_change_regions(self, change_map):
        """
        Identify regions with high visual changes
        Returns list of frame ranges that need dense sampling
        """
        high_change_regions = []

        for entry in change_map:
            if entry['change_score'] > self.change_threshold:
                # Mark region around this high-change frame for dense sampling
                frame_idx = entry['frame_idx']
                prev_idx = entry['prev_frame_idx']

                if prev_idx is not None:
                    # Sample densely between prev_idx and current frame_idx
                    high_change_regions.append({
                        'start': prev_idx,
                        'end': frame_idx,
                        'change_score': float(entry['change_score'])
                    })

        print(f"\n🎯 Identified {len(high_change_regions)} high-change regions")
        return high_change_regions

    def second_pass_selection(self, frames, change_map, high_change_regions):
        """
        Second pass: Select frames for analysis
        - All first-pass frames
        - Every 10th frame in high-change regions
        """
        selected_frames = set()

        # Add all first-pass frames
        for entry in change_map:
            selected_frames.add(entry['frame_idx'])

        # Add dense sampling in high-change regions
        for region in high_change_regions:
            start, end = region['start'], region['end']
            for idx in range(start, end, self.second_pass_interval):
                if idx < len(frames):
                    selected_frames.add(idx)

        return sorted(list(selected_frames))

    def generate_analysis_plan(self):
        """
        Generate complete analysis plan for all video folders
        Returns dict with frame selection for each video
        """
        folders = self.get_video_folders()
        analysis_plan = {
            'total_folders': len(folders),
            'folders': {},
            'total_frames_original': 0,
            'total_frames_selected': 0
        }

        for folder in folders:
            print(f"\n\n{'#'*60}")
            print(f"Processing: {folder.name}")
            print(f"{'#'*60}")

            # First pass
            change_map, all_frames = self.first_pass_analysis(folder)

            # Identify high-change regions
            high_change_regions = self.identify_high_change_regions(change_map)

            # Second pass selection
            selected_frames = self.second_pass_selection(
                all_frames, change_map, high_change_regions
            )

            # Store results
            folder_key = folder.name
            analysis_plan['folders'][folder_key] = {
                'total_frames': len(all_frames),
                'selected_frames': selected_frames,
                'num_selected': len(selected_frames),
                'reduction_ratio': 1 - (len(selected_frames) / len(all_frames)),
                'high_change_regions': high_change_regions,
                'frame_paths': [str(all_frames[i]) for i in selected_frames]
            }

            analysis_plan['total_frames_original'] += len(all_frames)
            analysis_plan['total_frames_selected'] += len(selected_frames)

            print(f"\n📊 Summary for {folder.name}:")
            print(f"   Original frames: {len(all_frames)}")
            print(f"   Selected frames: {len(selected_frames)}")
            print(f"   Reduction: {(1 - len(selected_frames)/len(all_frames))*100:.1f}%")

        return analysis_plan

    def save_analysis_plan(self, plan, output_file='analysis_plan.json'):
        """Save analysis plan to JSON file"""
        with open(output_file, 'w') as f:
            json.dump(plan, f, indent=2)
        print(f"\n✅ Analysis plan saved to: {output_file}")

    def print_summary(self, plan):
        """Print overall summary"""
        print(f"\n\n{'='*60}")
        print("OVERALL SUMMARY")
        print(f"{'='*60}")
        print(f"Total videos: {plan['total_folders']}")
        print(f"Original frames: {plan['total_frames_original']:,}")
        print(f"Selected frames: {plan['total_frames_selected']:,}")
        print(f"Overall reduction: {(1 - plan['total_frames_selected']/plan['total_frames_original'])*100:.1f}%")
        print(f"\nEstimated token cost:")
        print(f"  Before: ~{plan['total_frames_original'] * 1600:,} tokens (${plan['total_frames_original'] * 1600 * 3 / 1_000_000:.2f})")
        print(f"  After:  ~{plan['total_frames_selected'] * 1600:,} tokens (${plan['total_frames_selected'] * 1600 * 3 / 1_000_000:.2f})")
        print(f"  Savings: ${(plan['total_frames_original'] - plan['total_frames_selected']) * 1600 * 3 / 1_000_000:.2f}")
        print(f"{'='*60}")


def main():
    analyzer = FrameAnalyzer()

    print("🚀 Starting Intelligent Frame Analysis System")
    print("Strategy: Hybrid Change Detection + Fixed Sampling")

    # Generate analysis plan
    plan = analyzer.generate_analysis_plan()

    # Save plan
    analyzer.save_analysis_plan(plan)

    # Print summary
    analyzer.print_summary(plan)

    print("\n✨ Analysis complete! Ready for frame analysis.")
    print("\nNext steps:")
    print("1. Review analysis_plan.json")
    print("2. Run frame analysis on selected frames")
    print("3. Generate learning summaries")


if __name__ == "__main__":
    main()
