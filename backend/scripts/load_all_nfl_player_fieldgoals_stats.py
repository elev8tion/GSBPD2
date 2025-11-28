#!/usr/bin/env python3
"""
Load NFL Player Field Goals Stats from Screenshots into Kre8VidMems
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# Add backend path for imports
backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_path)
sys.path.insert(0, os.path.join(backend_path, 'lib', 'kre8vidmems'))

# Import Kre8VidMems
from lib.kre8vidmems.kre8vidmems.api.memory import Kre8VidMemory

def get_all_fieldgoals_data() -> List[Dict]:
    """Get all field goals data extracted from screenshots"""

    # Data extracted from screenshot-1.png and screenshot-2.png
    players = [
        # Screenshot 1
        {"name": "Cameron Dicker", "fgm": 25, "attempts": 27, "fg_pct": 0.926, "range_1_19": "0/0", "range_20_29": "4/4", "range_30_39": "10/10", "range_40_49": "8/9", "range_50_59": "3/4", "range_60_plus": "0/0", "longest": 59, "blocked": 0},
        {"name": "Ka'imi Fairbairn", "fgm": 25, "attempts": 29, "fg_pct": 0.893, "range_1_19": "0/0", "range_20_29": "4/4", "range_30_39": "8/8", "range_40_49": "8/8", "range_50_59": "5/9", "range_60_plus": "0/0", "longest": 57, "blocked": 0},
        {"name": "Jason Myers", "fgm": 24, "attempts": 29, "fg_pct": 0.828, "range_1_19": "0/0", "range_20_29": "4/4", "range_30_39": "8/9", "range_40_49": "7/8", "range_50_59": "5/7", "range_60_plus": "0/1", "longest": 57, "blocked": 1},
        {"name": "Evan McPherson", "fgm": 23, "attempts": 25, "fg_pct": 0.885, "range_1_19": "0/0", "range_20_29": "4/4", "range_30_39": "6/6", "range_40_49": "9/9", "range_50_59": "3/5", "range_60_plus": "1/2", "longest": 63, "blocked": 0},
        {"name": "Brandon Aubrey", "fgm": 22, "attempts": 24, "fg_pct": 0.917, "range_1_19": "0/0", "range_20_29": "7/7", "range_30_39": "3/3", "range_40_49": "6/6", "range_50_59": "4/5", "range_60_plus": "2/3", "longest": 64, "blocked": 0},
        {"name": "Tyler Lore", "fgm": 22, "attempts": 24, "fg_pct": 0.917, "range_1_19": "0/0", "range_20_29": "7/7", "range_30_39": "7/7", "range_40_49": "7/7", "range_50_59": "1/3", "range_60_plus": "0/0", "longest": 52, "blocked": 0},
        {"name": "Eddy Pineiro", "fgm": 22, "attempts": 22, "fg_pct": 1.000, "range_1_19": "0/0", "range_20_29": "4/4", "range_30_39": "4/4", "range_40_49": "8/8", "range_50_59": "6/6", "range_60_plus": "0/0", "longest": 56, "blocked": 0},
        {"name": "Harrison Butker", "fgm": 21, "attempts": 24, "fg_pct": 0.875, "range_1_19": "1/1", "range_20_29": "7/7", "range_30_39": "7/7", "range_40_49": "3/4", "range_50_59": "3/5", "range_60_plus": "0/0", "longest": 56, "blocked": 0},
        {"name": "Wil Reichard", "fgm": 21, "attempts": 23, "fg_pct": 0.913, "range_1_19": "0/0", "range_20_29": "4/4", "range_30_39": "6/6", "range_40_49": "9/9", "range_50_59": "1/3", "range_60_plus": "1/1", "longest": 62, "blocked": 0},
        {"name": "Nick Folk", "fgm": 20, "attempts": 20, "fg_pct": 1.000, "range_1_19": "0/0", "range_20_29": "4/4", "range_30_39": "5/5", "range_40_49": "6/6", "range_50_59": "5/5", "range_60_plus": "0/0", "longest": 58, "blocked": 0},
        {"name": "Chase McLaughlin", "fgm": 20, "attempts": 24, "fg_pct": 0.833, "range_1_19": "0/0", "range_20_29": "3/3", "range_30_39": "6/7", "range_40_49": "3/6", "range_50_59": "7/7", "range_60_plus": "1/1", "longest": 65, "blocked": 1},
        {"name": "Joey Slye", "fgm": 20, "attempts": 25, "fg_pct": 0.800, "range_1_19": "0/0", "range_20_29": "2/2", "range_30_39": "5/5", "range_40_49": "6/8", "range_50_59": "7/9", "range_60_plus": "0/2", "longest": 57, "blocked": 1},
        {"name": "Andy Berregales", "fgm": 19, "attempts": 21, "fg_pct": 0.905, "range_1_19": "2/2", "range_20_29": "3/3", "range_30_39": "6/6", "range_40_49": "5/7", "range_50_59": "3/3", "range_60_plus": "0/0", "longest": 53, "blocked": 0},
        {"name": "Chris Boswell", "fgm": 19, "attempts": 22, "fg_pct": 0.864, "range_1_19": "0/0", "range_20_29": "2/2", "range_30_39": "2/3", "range_40_49": "8/9", "range_50_59": "6/7", "range_60_plus": "1/1", "longest": 60, "blocked": 1},
        {"name": "Ryan Fitzgerald", "fgm": 18, "attempts": 22, "fg_pct": 0.818, "range_1_19": "0/0", "range_20_29": "5/5", "range_30_39": "6/7", "range_40_49": "5/6", "range_50_59": "2/4", "range_60_plus": "0/0", "longest": 57, "blocked": 1},
        {"name": "Blake Grupe", "fgm": 18, "attempts": 26, "fg_pct": 0.692, "range_1_19": "0/0", "range_20_29": "7/7", "range_30_39": "6/8", "range_40_49": "2/5", "range_50_59": "3/6", "range_60_plus": "0/0", "longest": 54, "blocked": 0},
        {"name": "Cam Little", "fgm": 18, "attempts": 22, "fg_pct": 0.818, "range_1_19": "0/0", "range_20_29": "3/3", "range_30_39": "6/6", "range_40_49": "4/6", "range_50_59": "4/6", "range_60_plus": "1/1", "longest": 68, "blocked": 0},
        {"name": "Wil Lutz", "fgm": 17, "attempts": 20, "fg_pct": 0.850, "range_1_19": "0/0", "range_20_29": "4/4", "range_30_39": "8/8", "range_40_49": "2/3", "range_50_59": "3/5", "range_60_plus": "0/0", "longest": 57, "blocked": 1},
        {"name": "Riley Patterson", "fgm": 17, "attempts": 19, "fg_pct": 0.895, "range_1_19": "0/0", "range_20_29": "3/3", "range_30_39": "5/6", "range_40_49": "9/9", "range_50_59": "0/1", "range_60_plus": "0/0", "longest": 49, "blocked": 0},
        {"name": "Chad Ryland", "fgm": 17, "attempts": 21, "fg_pct": 0.810, "range_1_19": "0/0", "range_20_29": "4/4", "range_30_39": "5/6", "range_40_49": "6/7", "range_50_59": "2/4", "range_60_plus": "0/0", "longest": 57, "blocked": 1},
        {"name": "Cairo Santos", "fgm": 17, "attempts": 21, "fg_pct": 0.810, "range_1_19": "0/0", "range_20_29": "2/2", "range_30_39": "6/6", "range_40_49": "6/8", "range_50_59": "3/5", "range_60_plus": "0/0", "longest": 54, "blocked": 1},
        {"name": "Jake Bates", "fgm": 16, "attempts": 20, "fg_pct": 0.800, "range_1_19": "0/0", "range_20_29": "4/4", "range_30_39": "4/4", "range_40_49": "4/5", "range_50_59": "4/6", "range_60_plus": "0/1", "longest": 59, "blocked": 1},
        {"name": "Daniel Carlson", "fgm": 16, "attempts": 21, "fg_pct": 0.762, "range_1_19": "0/0", "range_20_29": "4/4", "range_30_39": "5/5", "range_40_49": "4/6", "range_50_59": "3/6", "range_60_plus": "0/0", "longest": 54, "blocked": 1},
        {"name": "Andre Szmyt", "fgm": 16, "attempts": 19, "fg_pct": 0.842, "range_1_19": "0/0", "range_20_29": "2/2", "range_30_39": "8/9", "range_40_49": "3/4", "range_50_59": "3/4", "range_60_plus": "0/0", "longest": 55, "blocked": 0},
        {"name": "Matt Gay", "fgm": 15, "attempts": 21, "fg_pct": 0.714, "range_1_19": "0/0", "range_20_29": "3/3", "range_30_39": "2/3", "range_40_49": "6/6", "range_50_59": "4/9", "range_60_plus": "0/0", "longest": 56, "blocked": 0},

        # Screenshot 2
        {"name": "Brandon McManus", "fgm": 15, "attempts": 21, "fg_pct": 0.714, "range_1_19": "0/0", "range_20_29": "4/4", "range_30_39": "6/6", "range_40_49": "3/7", "range_50_59": "2/3", "range_60_plus": "0/1", "longest": 56, "blocked": 1},
        {"name": "Matt Prater", "fgm": 15, "attempts": 17, "fg_pct": 0.882, "range_1_19": "0/0", "range_20_29": "2/2", "range_30_39": "6/7", "range_40_49": "6/6", "range_50_59": "1/2", "range_60_plus": "0/0", "longest": 52, "blocked": 0},
        {"name": "Spencer Shrader", "fgm": 13, "attempts": 14, "fg_pct": 0.929, "range_1_19": "0/0", "range_20_29": "5/5", "range_30_39": "5/5", "range_40_49": "2/2", "range_50_59": "1/2", "range_60_plus": "0/0", "longest": 52, "blocked": 0},
        {"name": "Jake Elliott", "fgm": 11, "attempts": 14, "fg_pct": 0.786, "range_1_19": "0/0", "range_20_29": "1/1", "range_30_39": "4/4", "range_40_49": "3/4", "range_50_59": "3/5", "range_60_plus": "0/0", "longest": 58, "blocked": 0},
        {"name": "John Parker Romo", "fgm": 11, "attempts": 14, "fg_pct": 0.786, "range_1_19": "0/0", "range_20_29": "2/2", "range_30_39": "7/8", "range_40_49": "1/2", "range_50_59": "1/2", "range_60_plus": "0/0", "longest": 54, "blocked": 1},
        {"name": "Joshua Karty", "fgm": 10, "attempts": 15, "fg_pct": 0.667, "range_1_19": "0/0", "range_20_29": "3/4", "range_30_39": "3/5", "range_40_49": "3/4", "range_50_59": "1/2", "range_60_plus": "0/0", "longest": 51, "blocked": 2},
        {"name": "Mike Badgley", "fgm": 9, "attempts": 10, "fg_pct": 0.900, "range_1_19": "0/0", "range_20_29": "1/1", "range_30_39": "3/3", "range_40_49": "3/3", "range_50_59": "2/3", "range_60_plus": "0/0", "longest": 53, "blocked": 0},
        {"name": "Graham Gano", "fgm": 9, "attempts": 10, "fg_pct": 0.900, "range_1_19": "0/0", "range_20_29": "3/3", "range_30_39": "4/4", "range_40_49": "1/2", "range_50_59": "1/1", "range_60_plus": "0/0", "longest": 55, "blocked": 0},
        {"name": "Jake Moody", "fgm": 9, "attempts": 12, "fg_pct": 0.750, "range_1_19": "0/0", "range_20_29": "2/3", "range_30_39": "4/5", "range_40_49": "3/4", "range_50_59": "0/1", "range_60_plus": "0/0", "longest": 48, "blocked": 2},
        {"name": "Zane Gonzalez", "fgm": 6, "attempts": 6, "fg_pct": 1.000, "range_1_19": "0/0", "range_20_29": "0/0", "range_30_39": "0/0", "range_40_49": "3/3", "range_50_59": "3/3", "range_60_plus": "0/0", "longest": 56, "blocked": 0},
        {"name": "Younghoe Koo", "fgm": 6, "attempts": 7, "fg_pct": 0.857, "range_1_19": "1/1", "range_20_29": "1/1", "range_30_39": "2/2", "range_40_49": "2/3", "range_50_59": "0/1", "range_60_plus": "0/0", "longest": 44, "blocked": 0},
        {"name": "Matthew Wright", "fgm": 5, "attempts": 6, "fg_pct": 1.000, "range_1_19": "0/0", "range_20_29": "1/1", "range_30_39": "1/1", "range_40_49": "3/3", "range_50_59": "0/1", "range_60_plus": "0/0", "longest": 46, "blocked": 0},
        {"name": "Lucas Havrisik", "fgm": 4, "attempts": 4, "fg_pct": 1.000, "range_1_19": "0/0", "range_20_29": "0/0", "range_30_39": "2/2", "range_40_49": "1/1", "range_50_59": "0/1", "range_60_plus": "1/1", "longest": 61, "blocked": 0},
        {"name": "Cade McNamara", "fgm": 2, "attempts": 2, "fg_pct": 1.000, "range_1_19": "0/0", "range_20_29": "1/1", "range_30_39": "1/1", "range_40_49": "0/0", "range_50_59": "0/1", "range_60_plus": "0/0", "longest": 31, "blocked": 0},
        {"name": "Harrison Mevis", "fgm": 2, "attempts": 2, "fg_pct": 1.000, "range_1_19": "0/0", "range_20_29": "0/0", "range_30_39": "0/0", "range_40_49": "1/1", "range_50_59": "1/1", "range_60_plus": "0/0", "longest": 52, "blocked": 0},
        {"name": "Gavin Gillan", "fgm": 0, "attempts": 0, "fg_pct": 0.000, "range_1_19": "0/0", "range_20_29": "0/0", "range_30_39": "0/0", "range_40_49": "0/0", "range_50_59": "0/1", "range_60_plus": "0/0", "longest": 0, "blocked": 0},
    ]

    return players

def format_player_fieldgoals_stats(player: Dict) -> tuple:
    """Format player field goals stats with performance tags"""

    # Extract key stats
    name = player.get('name', 'Unknown')
    fgm = int(player.get('fgm', 0))
    attempts = int(player.get('attempts', 0))
    fg_pct = float(player.get('fg_pct', 0))
    longest = int(player.get('longest', 0))
    blocked = int(player.get('blocked', 0))

    # Parse range stats
    ranges = {
        '1-19': player.get('range_1_19', '0/0'),
        '20-29': player.get('range_20_29', '0/0'),
        '30-39': player.get('range_30_39', '0/0'),
        '40-49': player.get('range_40_49', '0/0'),
        '50-59': player.get('range_50_59', '0/0'),
        '60+': player.get('range_60_plus', '0/0')
    }

    # Calculate 50+ yard makes
    fifty_plus_makes = 0
    if '/' in ranges['50-59']:
        fifty_plus_makes += int(ranges['50-59'].split('/')[0])
    if '/' in ranges['60+']:
        sixty_plus_makes = int(ranges['60+'].split('/')[0])
        fifty_plus_makes += sixty_plus_makes

    # Determine performance tags
    tags = []

    # Elite kicker criteria
    if fg_pct >= 0.90 and fgm >= 20:
        tags.append("elite")
    elif fg_pct >= 0.85 and fgm >= 25:
        tags.append("elite")

    # Pro Bowl criteria
    if fg_pct >= 0.85 and fgm >= 20:
        tags.append("pro bowl")

    # Starter criteria
    if fgm >= 15:
        tags.append("starter")
    elif fgm >= 10:
        tags.append("backup")
    else:
        tags.append("reserve")

    # Special tags
    if longest >= 60:
        tags.append("60+ yard club")
    elif longest >= 55:
        tags.append("long range specialist")

    if fifty_plus_makes >= 5:
        tags.append("distance kicker")

    if blocked == 0 and attempts >= 20:
        tags.append("reliable")

    # Perfect accuracy tag
    if fg_pct == 1.0 and attempts >= 10:
        tags.append("perfect season")

    # Format the text chunk
    chunk = f"""
NFL PLAYER: {name}
POSITION: Kicker
2024 FIELD GOALS STATS:
- Field Goals Made: {fgm}/{attempts} ({fg_pct*100:.1f}%)
- Longest: {longest} yards
- Blocked: {blocked}

RANGE BREAKDOWN:
- 1-19 yards: {ranges['1-19']}
- 20-29 yards: {ranges['20-29']}
- 30-39 yards: {ranges['30-39']}
- 40-49 yards: {ranges['40-49']}
- 50-59 yards: {ranges['50-59']}
- 60+ yards: {ranges['60+']}

PERFORMANCE LEVEL: {', '.join(tags).upper()}
"""

    return chunk, tags

def main():
    """Main function to load all field goals stats"""

    print("\n" + "="*60)
    print("NFL PLAYER FIELD GOALS STATS LOADER")
    print("="*60)

    # Get all player data
    all_players = get_all_fieldgoals_data()
    print(f"\nTotal players to load: {len(all_players)}")

    # Initialize Kre8VidMemory
    memory = Kre8VidMemory()

    # Process each player and add to memory
    elite_count = 0
    pro_bowl_count = 0
    starter_count = 0
    total_fgm = 0
    total_attempts = 0
    best_accuracy = 0
    best_kicker = ""
    longest_fg = 0
    longest_kicker = ""
    perfect_kickers = []

    print("\nLoading players into Kre8VidMems...")
    for player in all_players:
        chunk, tags = format_player_fieldgoals_stats(player)

        # Add to memory (metadata is embedded in the chunk text)
        memory.add(chunk)

        # Update summary stats
        if 'elite' in tags:
            elite_count += 1
        if 'pro bowl' in tags:
            pro_bowl_count += 1
        if 'starter' in tags:
            starter_count += 1

        fgm = int(player.get('fgm', 0))
        attempts = int(player.get('attempts', 0))
        fg_pct = float(player.get('fg_pct', 0))
        longest = int(player.get('longest', 0))

        total_fgm += fgm
        total_attempts += attempts

        if fg_pct == 1.0 and attempts >= 10:
            perfect_kickers.append(f"{player.get('name')} ({attempts} att)")

        if fg_pct > best_accuracy and attempts >= 10:
            best_accuracy = fg_pct
            best_kicker = player.get('name')

        if longest > longest_fg:
            longest_fg = longest
            longest_kicker = player.get('name')

        print(f"  Added: {player.get('name')} - {fgm}/{attempts} ({fg_pct*100:.1f}%) - Tags: {', '.join(tags)}")

    # Save the memory
    memory_path = "data/memories/nfl-player-fieldgoals-stats"
    print(f"\nSaving to: {memory_path}")
    memory.save(memory_path)

    # Print summary statistics
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    print(f"Total Kickers Loaded: {len(all_players)}")
    print(f"Elite Kickers: {elite_count}")
    print(f"Pro Bowl Level: {pro_bowl_count}")
    print(f"Starters: {starter_count}")
    print(f"\nLeague Totals:")
    print(f"  Total FG Made: {total_fgm}")
    print(f"  Total Attempts: {total_attempts}")
    if total_attempts > 0:
        print(f"  League Average: {(total_fgm/total_attempts)*100:.1f}%")
    print(f"\nTop Performers:")
    print(f"  Most Accurate: {best_kicker} ({best_accuracy*100:.1f}%)")
    print(f"  Longest FG: {longest_kicker} ({longest_fg} yards)")
    if perfect_kickers:
        print(f"  Perfect Season: {', '.join(perfect_kickers)}")
    print("\n" + "="*60)
    print("FIELD GOALS STATS LOADED SUCCESSFULLY!")
    print("="*60)

if __name__ == "__main__":
    main()