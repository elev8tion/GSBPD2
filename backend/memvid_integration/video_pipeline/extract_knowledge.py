#!/usr/bin/env python3
"""
Simple script to prepare frame batches for Claude Code analysis
Claude Code will analyze the frames directly through the Read tool
"""

import json
from pathlib import Path

def load_analysis_plan():
    """Load the analysis plan"""
    with open('analysis_plan.json', 'r') as f:
        return json.load(f)

def prepare_batches(batch_size=8):
    """Prepare frame batches for analysis"""
    plan = load_analysis_plan()

    batches = []

    for section_name, section_data in plan['folders'].items():
        frame_paths = section_data['frame_paths']

        # Split into batches
        for i in range(0, len(frame_paths), batch_size):
            batch = frame_paths[i:i+batch_size]
            batches.append({
                'section': section_name,
                'batch_num': (i // batch_size) + 1,
                'frames': batch
            })

    return batches

def main():
    batches = prepare_batches()

    print(f"Total batches to analyze: {len(batches)}")
    print("\nBatch breakdown:")

    current_section = None
    for batch in batches:
        if batch['section'] != current_section:
            current_section = batch['section']
            print(f"\n{current_section}:")
        print(f"  Batch {batch['batch_num']}: {len(batch['frames'])} frames")

    # Save batch info
    with open('batches.json', 'w') as f:
        json.dump(batches, f, indent=2)

    print(f"\n✅ Batch information saved to batches.json")
    print(f"\nReady for Claude Code to analyze!")

if __name__ == "__main__":
    main()
