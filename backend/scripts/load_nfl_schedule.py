#!/usr/bin/env python3
"""
NFL Schedule Data Pipeline
Loads NFL schedule data into Kre8VidMems memory system
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.kre8vidmems.kre8vidmems.api.memory import Kre8VidMemory


def format_game_info(game: Dict[str, Any], week: int) -> str:
    """Format a single game into searchable text."""
    parts = []

    # Week and date info
    parts.append(f"NFL Week {week} 2024 Season")

    # Game date
    if game.get('date') and game['date'] != 'TBD':
        try:
            date_obj = datetime.strptime(game['date'], '%Y-%m-%d')
            parts.append(f"Date: {date_obj.strftime('%A, %B %d, %Y')}")
        except:
            parts.append(f"Date: {game['date']}")
    else:
        parts.append("Date: TBD")

    # Teams
    away = game.get('away_team', 'TBD')
    home = game.get('home_team', 'TBD')
    parts.append(f"Matchup: {away} at {home}")
    parts.append(f"Away Team: {away}")
    parts.append(f"Home Team: {home}")

    # Time
    game_time = game.get('time', 'TBD')
    parts.append(f"Game Time: {game_time}")

    # Stadium
    stadium = game.get('stadium', 'TBD')
    parts.append(f"Stadium: {stadium}")

    # TV Network
    network = game.get('tv_network', 'TBD')
    parts.append(f"TV Network: {network}")

    # Final score if available
    if 'final_score' in game and game['final_score']:
        score = game['final_score']
        parts.append(f"Final Score: {away} {score.get('away', 0)}, {home} {score.get('home', 0)}")

        # Determine winner
        if score.get('away', 0) > score.get('home', 0):
            parts.append(f"Winner: {away}")
        elif score.get('home', 0) > score.get('away', 0):
            parts.append(f"Winner: {home}")
        else:
            parts.append("Game ended in tie")

    # Game status
    if game.get('status'):
        parts.append(f"Status: {game['status']}")

    # Create searchable text
    text = " | ".join(parts)

    # Add common search terms
    text += f" | NFL game | NFL schedule | {away} vs {home}"
    text += f" | {away} game | {home} game"

    return text


def process_schedule_data(schedule_path: str) -> List[str]:
    """Process NFL schedule JSON into memory chunks."""
    print(f"Loading schedule from: {schedule_path}")

    with open(schedule_path, 'r') as f:
        data = json.load(f)

    chunks = []

    # Process by weeks
    if 'weeks' in data:
        # Master schedule format
        for week_data in data['weeks']:
            week_num = week_data['week']
            print(f"  Processing Week {week_num}: {len(week_data['games'])} games")

            for game in week_data['games']:
                chunk = format_game_info(game, week_num)
                chunks.append(chunk)
    else:
        # Individual week format
        if isinstance(data, list):
            # Assume all games are from the same week (extract from first game)
            week_num = data[0].get('week', 0) if data else 0
            print(f"  Processing {len(data)} games")

            for game in data:
                chunk = format_game_info(game, game.get('week', week_num))
                chunks.append(chunk)

    return chunks


def main():
    """Main pipeline execution."""
    print("=" * 60)
    print("NFL SCHEDULE LOADING PIPELINE")
    print("=" * 60)
    print()

    # Paths
    schedule_dir = "/Users/kcdacre8tor/Downloads/extracted_schedules"
    master_file = os.path.join(schedule_dir, "nfl_2024_master_schedule.json")
    memory_dir = "/Users/kcdacre8tor/GSBPD2/backend/data/memories"

    # Check if master file exists
    if not os.path.exists(master_file):
        print(f"❌ Master schedule not found: {master_file}")
        return 1

    print(f"📊 Loading NFL schedule data from: {schedule_dir}")
    print()

    # Process schedule data
    try:
        chunks = process_schedule_data(master_file)
        print(f"\n✅ Processed {len(chunks)} game records")
    except Exception as e:
        print(f"❌ Error processing schedule: {e}")
        return 1

    # Initialize Kre8VidMems
    print("\n🧠 Initializing Kre8VidMems for NFL schedule...")
    memory = Kre8VidMemory()

    # Add chunks to memory
    print(f"📝 Adding {len(chunks)} game records to memory...")
    start_time = time.time()

    # Add chunks in batches for efficiency
    batch_size = 10
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        for chunk in batch:
            memory.add(chunk)

        # Progress indicator
        progress = min(i + batch_size, len(chunks))
        print(f"  Added {progress}/{len(chunks)} games...")

    # Save the memory
    memory_name = f"{memory_dir}/nfl-schedule"
    memory.save(memory_name)

    elapsed_time = time.time() - start_time
    print(f"\n✅ Successfully loaded NFL schedule in {elapsed_time:.2f} seconds")
    print(f"📂 Memory saved to: {memory_name}.*")

    # Test search
    print("\n🔍 Testing search functionality...")
    test_queries = [
        "Chiefs game week 13",
        "Detroit Lions",
        "Christmas games",
        "Week 15 schedule",
        "Prime Video games"
    ]

    for query in test_queries:
        results = memory.search(query, k=2)
        print(f"\n  Query: '{query}'")
        if results:
            for i, result in enumerate(results[:1], 1):  # Show only top result
                text = result.get('text', '') if isinstance(result, dict) else result
                # Extract key info
                lines = text.split(' | ')
                if len(lines) > 2:
                    print(f"    → {lines[2]}")  # Matchup line
                    if len(lines) > 1:
                        print(f"      {lines[1]}")  # Date line
        else:
            print("    No results found")

    print("\n" + "=" * 60)
    print("✅ NFL SCHEDULE PIPELINE COMPLETE")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())