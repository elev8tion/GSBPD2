#!/usr/bin/env python3
"""
Load NFL player punting statistics into Kre8VidMems
Extracted from 3 screenshots
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from lib.kre8vidmems.kre8vidmems.api.memory import Kre8VidMemory


def format_player_punting_stats(player: Dict[str, Any]) -> str:
    """Format player punting stats for memory storage with performance tags"""
    name = player.get('player', 'Unknown')
    avg = player.get('avg', 0)
    net_avg = player.get('net_avg', 0)
    punts = player.get('punts', 0)
    yards = player.get('yards', 0)
    longest = player.get('long', 0)
    inside_20 = player.get('in_20', 0)
    touchbacks = player.get('tb', 0)

    # Base stats text
    text = f"NFL Player Punting Stats | {name}"
    text += f" | Average: {avg} yards"
    text += f" | Net Average: {net_avg} yards"
    text += f" | Punts: {punts}"
    text += f" | Total Yards: {yards}"
    text += f" | Longest: {longest}"
    text += f" | Inside 20: {inside_20}"
    text += f" | Touchbacks: {touchbacks}"

    # Performance-based tags for elite punters
    if avg >= 50.0:
        text += f" | elite punter | {name} elite specialist | pro bowl punter | 50+ yard average"
    elif avg >= 48.0:
        text += f" | pro bowl candidate | {name} top punter | excellent hang time"
    elif avg >= 46.0:
        text += f" | quality punter | {name} reliable | good field position"
    elif avg >= 44.0:
        text += f" | solid punter | {name} consistent | field position specialist"

    # Net average excellence
    if net_avg >= 45.0:
        text += f" | elite net average | {name} coffin corner specialist | pinpoint accuracy"
    elif net_avg >= 43.0:
        text += f" | excellent coverage | {name} directional punter | limits returns"
    elif net_avg >= 41.0:
        text += f" | good net punting | {name} solid coverage | controls field position"

    # Inside 20 specialist
    if punts > 30 and inside_20 >= 20:
        text += f" | inside 20 specialist | {name} precision punter | coffin corner expert"
    elif punts > 20 and inside_20 >= 15:
        text += f" | red zone punter | {name} pin deep | field position weapon"
    elif inside_20 >= 10:
        text += f" | good placement | {name} directional kicking | pins opponents"

    # Low touchback ratio (good)
    if punts > 30 and touchbacks <= 3:
        text += f" | touchback avoider | {name} perfect placement | elite control"
    elif punts > 20 and touchbacks <= 2:
        text += f" | excellent control | {name} precision kicker | minimal touchbacks"

    # Big leg (longest punt)
    if longest >= 70:
        text += f" | booming leg | {name} 70+ yard bomb | field flipper | game changer"
    elif longest >= 65:
        text += f" | big leg punter | {name} 65+ yarder | momentum shifter"
    elif longest >= 60:
        text += f" | strong leg | {name} 60+ yard punt | field position flipper"

    return text


# All player data from screenshots
players = [
    # Screenshot 1 - Page 1
    {"player": "Ryan Rehkow", "avg": 52.3, "net_avg": 42.8, "punts": 48, "yards": 2509, "long": 70, "in_20": 17, "tb": 4},
    {"player": "Blake Gillikin", "avg": 51.7, "net_avg": 45.4, "punts": 22, "yards": 1138, "long": 63, "in_20": 8, "tb": 1},
    {"player": "Daniel Whelan", "avg": 51.4, "net_avg": 42.4, "punts": 37, "yards": 1900, "long": 72, "in_20": 12, "tb": 4},
    {"player": "Jordan Stout", "avg": 51.3, "net_avg": 45.5, "punts": 41, "yards": 2103, "long": 74, "in_20": 18, "tb": 7},
    {"player": "Braden Mann", "avg": 50.2, "net_avg": 42.4, "punts": 51, "yards": 2558, "long": 70, "in_20": 15, "tb": 6},
    {"player": "Matt Haack", "avg": 49.8, "net_avg": 42.7, "punts": 6, "yards": 299, "long": 65, "in_20": 4, "tb": 0},
    {"player": "Rigoberto Sanchez", "avg": 49.8, "net_avg": 47.1, "punts": 25, "yards": 1245, "long": 59, "in_20": 14, "tb": 4},
    {"player": "Michael Dickson", "avg": 49.7, "net_avg": 41, "punts": 33, "yards": 1640, "long": 60, "in_20": 12, "tb": 3},
    {"player": "Jake Bailey", "avg": 49.1, "net_avg": 45.7, "punts": 34, "yards": 1669, "long": 64, "in_20": 15, "tb": 2},
    {"player": "J.K. Scott", "avg": 49, "net_avg": 41.7, "punts": 34, "yards": 1667, "long": 60, "in_20": 13, "tb": 3},
    {"player": "Ryan Wright", "avg": 48.8, "net_avg": 44.9, "punts": 45, "yards": 2194, "long": 77, "in_20": 17, "tb": 5},
    {"player": "Tress Way", "avg": 48.5, "net_avg": 45.1, "punts": 34, "yards": 1650, "long": 64, "in_20": 17, "tb": 0},
    {"player": "Tommy Townsend", "avg": 48.4, "net_avg": 40.9, "punts": 48, "yards": 2325, "long": 73, "in_20": 19, "tb": 7},
    {"player": "Tory Taylor", "avg": 48.3, "net_avg": 39.5, "punts": 39, "yards": 1885, "long": 69, "in_20": 12, "tb": 8},
    {"player": "Bryan Anger", "avg": 48.1, "net_avg": 42.5, "punts": 35, "yards": 1685, "long": 62, "in_20": 13, "tb": 1},
    {"player": "Sam Martin", "avg": 48.1, "net_avg": 40, "punts": 41, "yards": 1972, "long": 68, "in_20": 18, "tb": 5},
    {"player": "Jeremy Crawshaw", "avg": 48.1, "net_avg": 41.8, "punts": 57, "yards": 2741, "long": 76, "in_20": 23, "tb": 9},
    {"player": "AJ Cole", "avg": 47.8, "net_avg": 39.9, "punts": 45, "yards": 2056, "long": 64, "in_20": 14, "tb": 10},
    {"player": "Bryce Baringer", "avg": 47.6, "net_avg": 39.6, "punts": 40, "yards": 1902, "long": 73, "in_20": 16, "tb": 3},
    {"player": "Logan Cooke", "avg": 47.2, "net_avg": 43.2, "punts": 37, "yards": 1747, "long": 62, "in_20": 14, "tb": 8},
    {"player": "Matt Araiza", "avg": 46.7, "net_avg": 39.8, "punts": 34, "yards": 1588, "long": 69, "in_20": 16, "tb": 4},
    {"player": "Austin McNamara", "avg": 46.6, "net_avg": 42.8, "punts": 45, "yards": 2098, "long": 64, "in_20": 19, "tb": 1},
    {"player": "Johnny Hekker", "avg": 46.4, "net_avg": 40.1, "punts": 51, "yards": 2365, "long": 65, "in_20": 15, "tb": 3},
    {"player": "Corliss Waitman", "avg": 46.4, "net_avg": 41.9, "punts": 38, "yards": 1762, "long": 67, "in_20": 14, "tb": 3},
    {"player": "Ethan Evans", "avg": 45.9, "net_avg": 39.3, "punts": 35, "yards": 1608, "long": 68, "in_20": 18, "tb": 9},

    # Screenshot 2 & 3 (same data)
    {"player": "Jack Fox", "avg": 45.7, "net_avg": 42.3, "punts": 43, "yards": 1966, "long": 66, "in_20": 23, "tb": 1},
    {"player": "Mitch Wishnowsky", "avg": 45.7, "net_avg": 43.9, "punts": 23, "yards": 1051, "long": 61, "in_20": 12, "tb": 3},
    {"player": "Corey Bojorquez", "avg": 45.6, "net_avg": 37, "punts": 64, "yards": 2870, "long": 67, "in_20": 19, "tb": 11},
    {"player": "Riley Dixon", "avg": 45.2, "net_avg": 40.1, "punts": 46, "yards": 1989, "long": 62, "in_20": 17, "tb": 4},
    {"player": "Thomas Morstead", "avg": 44.8, "net_avg": 36.7, "punts": 33, "yards": 1479, "long": 55, "in_20": 16, "tb": 1},
    {"player": "Bradley Pinion", "avg": 44.8, "net_avg": 40.5, "punts": 43, "yards": 1927, "long": 61, "in_20": 20, "tb": 5},
    {"player": "James Gillan", "avg": 44.1, "net_avg": 39.2, "punts": 45, "yards": 1983, "long": 69, "in_20": 15, "tb": 5},
    {"player": "Cameron Johnston", "avg": 44, "net_avg": 37.9, "punts": 7, "yards": 308, "long": 48, "in_20": 2, "tb": 1},
    {"player": "Kai Kroeger", "avg": 44, "net_avg": 37.1, "punts": 38, "yards": 1626, "long": 61, "in_20": 13, "tb": 5},
    {"player": "Pat O'Donnell", "avg": 42.2, "net_avg": 39.2, "punts": 13, "yards": 506, "long": 49, "in_20": 3, "tb": 1},
    {"player": "Brad Robbins", "avg": 39.5, "net_avg": 38, "punts": 4, "yards": 158, "long": 48, "in_20": 1, "tb": 0},
    {"player": "Daniel Carlson", "avg": 30, "net_avg": 30, "punts": 1, "yards": 30, "long": 30, "in_20": 0, "tb": 1}
]


def main():
    """Load all punting stats into Kre8VidMems"""
    print("Loading NFL Player Punting Stats...")
    print(f"Total punters: {len(players)}")

    # Create memory instance
    memory = Kre8VidMemory()

    # Process all players
    chunks = []
    for player in players:
        chunk = format_player_punting_stats(player)
        chunks.append(chunk)

    # Add summary chunk with top performers
    summary = "NFL Punting Stats Summary 2025"

    # Find top punters by average
    top_avg = sorted(players, key=lambda x: x['avg'], reverse=True)[:10]
    if top_avg:
        summary += "\n\nTop Punters by Average:"
        for p in top_avg[:5]:
            summary += f"\n- {p['player']}: {p['avg']} yards"

    # Find top net average
    top_net = sorted(players, key=lambda x: x['net_avg'], reverse=True)[:10]
    if top_net:
        summary += "\n\nTop Punters by Net Average:"
        for p in top_net[:5]:
            summary += f"\n- {p['player']}: {p['net_avg']} yards"

    # Find inside 20 specialists
    top_in20 = sorted([p for p in players if p['punts'] >= 20],
                      key=lambda x: x['in_20'], reverse=True)[:5]
    if top_in20:
        summary += "\n\nTop Inside 20 Specialists:"
        for p in top_in20:
            summary += f"\n- {p['player']}: {p['in_20']} punts inside 20"

    # Find biggest legs
    top_long = sorted(players, key=lambda x: x['long'], reverse=True)[:5]
    if top_long:
        summary += "\n\nBiggest Leg (Longest Punt):"
        for p in top_long:
            summary += f"\n- {p['player']}: {p['long']} yards"

    chunks.append(summary)

    # Load into memory
    print(f"Loading {len(chunks)} chunks into memory...")
    for i, chunk in enumerate(chunks, 1):
        memory.add(chunk)
        if i % 10 == 0:
            print(f"Added {i} chunks")

    # Save memory
    memory_path = "data/memories/nfl-player-punting-stats"
    memory.save(memory_path)
    print(f"✓ Saved punting stats to {memory_path.split('/')[-1]}")

    # Print statistics
    print(f"\n✓ All NFL player punting stats loaded successfully!")
    print(f"Total punters: {len(players)}")

    # Print top performers
    print(f"\nTop 5 Punters by Average:")
    for i, p in enumerate(top_avg[:5], 1):
        print(f"{i}. {p['player']}: {p['avg']} yards average")

    print(f"\nTop 5 Inside 20 Specialists:")
    for i, p in enumerate(top_in20[:5], 1):
        print(f"{i}. {p['player']}: {p['in_20']} punts inside 20")


if __name__ == "__main__":
    main()