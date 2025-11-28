#!/usr/bin/env python3
"""
Load NFL player kickoffs stats from screenshots into Kre8VidMems
"""

import sys
import os
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from lib.kre8vidmems.kre8vidmems.api.memory import Kre8VidMemory

def format_player_kickoffs_stats(player):
    """
    Format kickoffs stats with performance tags
    """
    name = player['name']
    kickoffs = player.get('kickoffs', 0)
    yards = player.get('yards', 0)
    touchbacks = player.get('touchbacks', 0)
    tb_percent = player.get('tb_percent', 0)
    returns = player.get('returns', 0)
    ret_avg = player.get('ret_avg', 0)
    onside_kicks = player.get('onside_kicks', 0)
    onside_rec = player.get('onside_rec', 0)
    out_of_bounds = player.get('out_of_bounds', 0)
    touchdowns = player.get('touchdowns', 0)

    # Performance tags based on stats
    tags = []

    # Elite kickers (60+ kickoffs with 50%+ touchback rate)
    if kickoffs >= 60 and tb_percent >= 50:
        tags.append("elite")
    # Pro Bowl level (50+ kickoffs with 45%+ touchback rate)
    elif kickoffs >= 50 and tb_percent >= 45:
        tags.append("pro bowl")
    # Starter (30+ kickoffs)
    elif kickoffs >= 30:
        tags.append("starter")
    # Backup/situational
    else:
        tags.append("backup")

    # Special teams ace (high touchback percentage)
    if tb_percent >= 55:
        tags.append("touchback specialist")

    # Onside kick specialist
    if onside_kicks >= 3:
        tags.append("onside specialist")

    # Coverage specialist (low return average)
    if returns > 0 and ret_avg < 22:
        tags.append("coverage ace")

    tags_str = ", ".join(tags)

    content = f"""
NFL Player: {name}
Position: Kicker/Special Teams
Stats Type: Kickoffs
Season: 2024

Kickoff Statistics:
- Kickoffs: {kickoffs}
- Total Yards: {yards:,}
- Touchbacks: {touchbacks} ({tb_percent:.1f}%)
- Returns Allowed: {returns}
- Return Average: {ret_avg:.1f} yards
- Onside Kicks: {onside_kicks} (Recovered: {onside_rec})
- Out of Bounds: {out_of_bounds}
- Touchdowns Allowed: {touchdowns}

Performance Tags: {tags_str}
Team Impact: {'High' if kickoffs >= 50 else 'Medium' if kickoffs >= 30 else 'Low'}
"""
    return content.strip()


def main():
    """
    Main function to load all kickoffs stats
    """
    print("Loading NFL player kickoffs stats into Kre8VidMems...")

    # All player data extracted from screenshots
    players_data = [
        # Screenshot 1
        {"name": "Brandon Aubrey", "kickoffs": 71, "yards": 4319, "ret_yards": 1359, "touchbacks": 15, "tb_percent": 21.1, "returns": 54, "ret_avg": 25.2, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 2, "touchdowns": 0},
        {"name": "Jake Bates", "kickoffs": 70, "yards": 4258, "ret_yards": 1416, "touchbacks": 10, "tb_percent": 14.3, "returns": 55, "ret_avg": 25.7, "onside_kicks": 1, "onside_rec": 0, "out_of_bounds": 5, "touchdowns": 0},
        {"name": "Jason Myers", "kickoffs": 67, "yards": 4145, "ret_yards": 1247, "touchbacks": 11, "tb_percent": 16.4, "returns": 54, "ret_avg": 23.1, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 1, "touchdowns": 0},
        {"name": "Arryn Berrios", "kickoffs": 65, "yards": 3868, "ret_yards": 1200, "touchbacks": 12, "tb_percent": 18.5, "returns": 50, "ret_avg": 24, "onside_kicks": 1, "onside_rec": 0, "out_of_bounds": 2, "touchdowns": 0},
        {"name": "Harrison Butker", "kickoffs": 65, "yards": 3926, "ret_yards": 1332, "touchbacks": 10, "tb_percent": 15.4, "returns": 52, "ret_avg": 25.6, "onside_kicks": 1, "onside_rec": 0, "out_of_bounds": 2, "touchdowns": 0},
        {"name": "Tyler Long", "kickoffs": 65, "yards": 3764, "ret_yards": 1349, "touchbacks": 6, "tb_percent": 9.2, "returns": 53, "ret_avg": 25.4, "onside_kicks": 1, "onside_rec": 0, "out_of_bounds": 5, "touchdowns": 0},
        {"name": "Evan McPherson", "kickoffs": 62, "yards": 3758, "ret_yards": 1362, "touchbacks": 9, "tb_percent": 14.5, "returns": 51, "ret_avg": 26.7, "onside_kicks": 2, "onside_rec": 1, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "Matt Prater", "kickoffs": 62, "yards": 3803, "ret_yards": 1417, "touchbacks": 8, "tb_percent": 12.9, "returns": 54, "ret_avg": 26.2, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "Chris Boswell", "kickoffs": 61, "yards": 3643, "ret_yards": 1398, "touchbacks": 3, "tb_percent": 4.9, "returns": 55, "ret_avg": 25.4, "onside_kicks": 2, "onside_rec": 0, "out_of_bounds": 1, "touchdowns": 0},
        {"name": "Cameron Dicker", "kickoffs": 59, "yards": 3667, "ret_yards": 1342, "touchbacks": 10, "tb_percent": 17, "returns": 46, "ret_avg": 29.2, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 3, "touchdowns": 0},
        {"name": "Cam Little", "kickoffs": 58, "yards": 3559, "ret_yards": 1085, "touchbacks": 15, "tb_percent": 25.9, "returns": 40, "ret_avg": 27.1, "onside_kicks": 1, "onside_rec": 0, "out_of_bounds": 2, "touchdowns": 0},
        {"name": "Chad Ryland", "kickoffs": 57, "yards": 3333, "ret_yards": 1207, "touchbacks": 10, "tb_percent": 17.5, "returns": 43, "ret_avg": 28.1, "onside_kicks": 3, "onside_rec": 0, "out_of_bounds": 1, "touchdowns": 0},
        {"name": "Wil Lutz", "kickoffs": 55, "yards": 3467, "ret_yards": 1202, "touchbacks": 13, "tb_percent": 23.6, "returns": 42, "ret_avg": 28.6, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "Chase McLaughlin", "kickoffs": 55, "yards": 3284, "ret_yards": 1369, "touchbacks": 4, "tb_percent": 7.3, "returns": 49, "ret_avg": 27.9, "onside_kicks": 1, "onside_rec": 0, "out_of_bounds": 1, "touchdowns": 0},
        {"name": "Matt Gay", "kickoffs": 53, "yards": 3130, "ret_yards": 837, "touchbacks": 12, "tb_percent": 22.6, "returns": 36, "ret_avg": 23.2, "onside_kicks": 3, "onside_rec": 0, "out_of_bounds": 2, "touchdowns": 0},
        {"name": "Eddy Pineiro", "kickoffs": 53, "yards": 3208, "ret_yards": 1212, "touchbacks": 6, "tb_percent": 11.3, "returns": 47, "ret_avg": 25.8, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "Will Reichard", "kickoffs": 53, "yards": 3183, "ret_yards": 1189, "touchbacks": 6, "tb_percent": 11.3, "returns": 45, "ret_avg": 26.4, "onside_kicks": 1, "onside_rec": 0, "out_of_bounds": 1, "touchdowns": 0},
        {"name": "Jake Elliott", "kickoffs": 52, "yards": 3114, "ret_yards": 1036, "touchbacks": 7, "tb_percent": 13.5, "returns": 44, "ret_avg": 23.6, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 1, "touchdowns": 0},
        {"name": "Riley Patterson", "kickoffs": 51, "yards": 3064, "ret_yards": 1130, "touchbacks": 7, "tb_percent": 13.7, "returns": 43, "ret_avg": 26.3, "onside_kicks": 1, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 1},
        {"name": "Ryan Fitzgerald", "kickoffs": 49, "yards": 2909, "ret_yards": 881, "touchbacks": 8, "tb_percent": 16.3, "returns": 41, "ret_avg": 21.5, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "Cairo Santos", "kickoffs": 49, "yards": 2987, "ret_yards": 1050, "touchbacks": 9, "tb_percent": 18.4, "returns": 38, "ret_avg": 27.6, "onside_kicks": 1, "onside_rec": 0, "out_of_bounds": 1, "touchdowns": 1},
        {"name": "Ka'imi Fairbairn", "kickoffs": 48, "yards": 2987, "ret_yards": 1013, "touchbacks": 10, "tb_percent": 20.8, "returns": 37, "ret_avg": 27.4, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 1, "touchdowns": 0},
        {"name": "Brandon McManus", "kickoffs": 46, "yards": 2905, "ret_yards": 868, "touchbacks": 12, "tb_percent": 26.1, "returns": 34, "ret_avg": 25.5, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "Andre Szmyt", "kickoffs": 44, "yards": 2625, "ret_yards": 1063, "touchbacks": 5, "tb_percent": 11.4, "returns": 38, "ret_avg": 28, "onside_kicks": 1, "onside_rec": 1, "out_of_bounds": 0, "touchdowns": 1},
        {"name": "Daniel Carlson", "kickoffs": 43, "yards": 2543, "ret_yards": 958, "touchbacks": 5, "tb_percent": 11.6, "returns": 35, "ret_avg": 27.4, "onside_kicks": 1, "onside_rec": 0, "out_of_bounds": 2, "touchdowns": 0},
        # Screenshot 2
        {"name": "Blake Grupe", "kickoffs": 43, "yards": 2643, "ret_yards": 900, "touchbacks": 9, "tb_percent": 20.9, "returns": 32, "ret_avg": 28.1, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 2, "touchdowns": 0},
        {"name": "Joey Slye", "kickoffs": 40, "yards": 2485, "ret_yards": 643, "touchbacks": 12, "tb_percent": 30, "returns": 26, "ret_avg": 24.7, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 2, "touchdowns": 0},
        {"name": "Joshua Karty", "kickoffs": 36, "yards": 2146, "ret_yards": 425, "touchbacks": 11, "tb_percent": 30.6, "returns": 24, "ret_avg": 17.7, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 1, "touchdowns": 0},
        {"name": "Bradley Pinion", "kickoffs": 36, "yards": 2200, "ret_yards": 797, "touchbacks": 6, "tb_percent": 16.7, "returns": 29, "ret_avg": 27.5, "onside_kicks": 1, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "Mike Badgley", "kickoffs": 34, "yards": 2052, "ret_yards": 780, "touchbacks": 1, "tb_percent": 2.9, "returns": 32, "ret_avg": 24.4, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 1, "touchdowns": 0},
        {"name": "James Gillan", "kickoffs": 32, "yards": 1830, "ret_yards": 482, "touchbacks": 4, "tb_percent": 12.5, "returns": 22, "ret_avg": 21.9, "onside_kicks": 2, "onside_rec": 0, "out_of_bounds": 4, "touchdowns": 0},
        {"name": "Jack Folk", "kickoffs": 29, "yards": 1601, "ret_yards": 540, "touchbacks": 6, "tb_percent": 20.7, "returns": 19, "ret_avg": 28.4, "onside_kicks": 4, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "Spencer Shrader", "kickoffs": 27, "yards": 1582, "ret_yards": 601, "touchbacks": 2, "tb_percent": 7.4, "returns": 24, "ret_avg": 25, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 1, "touchdowns": 0},
        {"name": "Ethan Evans", "kickoffs": 24, "yards": 1552, "ret_yards": 74, "touchbacks": 21, "tb_percent": 87.5, "returns": 3, "ret_avg": 24.7, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "Austin McNamara", "kickoffs": 22, "yards": 1349, "ret_yards": 467, "touchbacks": 3, "tb_percent": 13.6, "returns": 19, "ret_avg": 24.6, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "Younghoe Koo", "kickoffs": 18, "yards": 1105, "ret_yards": 380, "touchbacks": 3, "tb_percent": 16.7, "returns": 14, "ret_avg": 27.1, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 1, "touchdowns": 0},
        {"name": "Jake Moody", "kickoffs": 17, "yards": 1051, "ret_yards": 302, "touchbacks": 6, "tb_percent": 35.3, "returns": 11, "ret_avg": 27.4, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "Lucas Havrisik", "kickoffs": 16, "yards": 1005, "ret_yards": 286, "touchbacks": 5, "tb_percent": 31.2, "returns": 11, "ret_avg": 26, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "Matthew Wright", "kickoffs": 14, "yards": 861, "ret_yards": 312, "touchbacks": 2, "tb_percent": 14.3, "returns": 12, "ret_avg": 26, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "Graham Gano", "kickoffs": 11, "yards": 663, "ret_yards": 274, "touchbacks": 0, "tb_percent": 0, "returns": 11, "ret_avg": 24.9, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "Cade Gonzalez", "kickoffs": 11, "yards": 686, "ret_yards": 200, "touchbacks": 5, "tb_percent": 45.4, "returns": 6, "ret_avg": 33.3, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "Rigoberto Sanchez", "kickoffs": 8, "yards": 378, "ret_yards": 74, "touchbacks": 2, "tb_percent": 25, "returns": 3, "ret_avg": 24.7, "onside_kicks": 2, "onside_rec": 0, "out_of_bounds": 1, "touchdowns": 0},
        {"name": "Luke McManirney", "kickoffs": 5, "yards": 313, "ret_yards": 73, "touchbacks": 2, "tb_percent": 40, "returns": 3, "ret_avg": 24.3, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "Johnny Hekker", "kickoffs": 3, "yards": 23, "ret_yards": 0, "touchbacks": 0, "tb_percent": 0, "returns": 0, "ret_avg": 0, "onside_kicks": 3, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "Harrison Mavis", "kickoffs": 3, "yards": 195, "ret_yards": 28, "touchbacks": 2, "tb_percent": 66.7, "returns": 1, "ret_avg": 28, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "Thomas Morstead", "kickoffs": 3, "yards": 133, "ret_yards": 25, "touchbacks": 1, "tb_percent": 33.3, "returns": 1, "ret_avg": 25, "onside_kicks": 1, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "Sam Martin", "kickoffs": 2, "yards": 22, "ret_yards": 0, "touchbacks": 0, "tb_percent": 0, "returns": 0, "ret_avg": 0, "onside_kicks": 2, "onside_rec": 1, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "Trey Taylor", "kickoffs": 2, "yards": 122, "ret_yards": 60, "touchbacks": 0, "tb_percent": 0, "returns": 2, "ret_avg": 30, "onside_kicks": 0, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "Corey Bojorquez", "kickoffs": 1, "yards": 9, "ret_yards": 0, "touchbacks": 0, "tb_percent": 0, "returns": 0, "ret_avg": 0, "onside_kicks": 1, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "AJ Cole", "kickoffs": 1, "yards": 18, "ret_yards": 0, "touchbacks": 0, "tb_percent": 0, "returns": 0, "ret_avg": 0, "onside_kicks": 1, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0},
        # Screenshot 3
        {"name": "Ray Davis", "kickoffs": 1, "yards": 9, "ret_yards": 0, "touchbacks": 0, "tb_percent": 0, "returns": 0, "ret_avg": 0, "onside_kicks": 1, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0},
        {"name": "Ryan Rehkow", "kickoffs": 1, "yards": 26, "ret_yards": 0, "touchbacks": 0, "tb_percent": 0, "returns": 0, "ret_avg": 0, "onside_kicks": 1, "onside_rec": 0, "out_of_bounds": 0, "touchdowns": 0}
    ]

    # Initialize memory
    memory = Kre8VidMemory()

    # Stats counters
    total_players = len(players_data)
    elite_count = 0
    pro_bowl_count = 0
    starter_count = 0
    backup_count = 0
    total_kickoffs = 0
    total_touchbacks = 0

    # Process each player
    for player in players_data:
        # Format the player data
        formatted_content = format_player_kickoffs_stats(player)

        # Add to memory
        memory.add(formatted_content)

        # Update stats
        kickoffs = player.get('kickoffs', 0)
        tb_percent = player.get('tb_percent', 0)
        total_kickoffs += kickoffs
        total_touchbacks += player.get('touchbacks', 0)

        # Count performance levels
        if kickoffs >= 60 and tb_percent >= 50:
            elite_count += 1
        elif kickoffs >= 50 and tb_percent >= 45:
            pro_bowl_count += 1
        elif kickoffs >= 30:
            starter_count += 1
        else:
            backup_count += 1

    # Save memory
    memory_path = "data/memories/nfl-player-kickoffs-stats"
    memory.save(memory_path)

    # Print summary
    print(f"\n✅ Successfully loaded {total_players} NFL players' kickoffs stats")
    print(f"\n📊 Summary Statistics:")
    print(f"  Total Players: {total_players}")
    print(f"  Total Kickoffs: {total_kickoffs:,}")
    print(f"  Total Touchbacks: {total_touchbacks:,}")
    print(f"  Average TB%: {(total_touchbacks/total_kickoffs)*100:.1f}%")
    print(f"\n🏆 Performance Breakdown:")
    print(f"  Elite Kickers: {elite_count}")
    print(f"  Pro Bowl Level: {pro_bowl_count}")
    print(f"  Starters: {starter_count}")
    print(f"  Backup/Situational: {backup_count}")
    print(f"\n📁 Memory saved to: {memory_path}")
    print(f"  Files created:")
    print(f"    - {memory_path}.mp4 (QR-encoded data)")
    print(f"    - {memory_path}.ann (Annoy index)")
    print(f"    - {memory_path}.meta (Metadata)")


if __name__ == "__main__":
    main()