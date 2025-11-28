#!/usr/bin/env python3
"""
Load NFL player punt return statistics into Kre8VidMems
Extracted from 4 screenshots
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from lib.kre8vidmems.kre8vidmems.api.memory import Kre8VidMemory


def format_player_punt_return_stats(player: Dict[str, Any]) -> str:
    """Format player punt return stats for memory storage with performance tags"""
    name = player.get('player', 'Unknown')
    avg = player.get('avg', 0.0)
    ret = player.get('ret', 0)
    yds = player.get('yds', 0)
    td = player.get('td', 0)
    twenty_plus = player.get('20+', 0)
    forty_plus = player.get('40+', 0)
    long = player.get('long', 0)
    fc = player.get('fc', 0)
    fum = player.get('fum', 0)

    # Base stats text
    text = f"NFL Player Punt Return Stats | {name}"
    text += f" | Average: {avg} yards"
    text += f" | Returns: {ret}"
    text += f" | Total Yards: {yds}"
    text += f" | Touchdowns: {td}"
    text += f" | 20+ Yard Returns: {twenty_plus}"
    text += f" | 40+ Yard Returns: {forty_plus}"
    text += f" | Longest Return: {long} yards"
    text += f" | Fair Catches: {fc}"
    text += f" | Fumbles: {fum}"

    # Performance-based tags for punt returners
    if avg >= 15:
        text += f" | elite returner | {name} explosive player | game breaker | pro bowl return specialist"
    elif avg >= 12:
        text += f" | dangerous returner | {name} field position weapon | impact player"
    elif avg >= 10:
        text += f" | solid returner | {name} reliable hands | good field position"
    elif avg >= 8:
        text += f" | average returner | {name} steady contributor"

    # TD scorer tags
    if td >= 2:
        text += f" | touchdown machine | {name} return touchdown specialist | elite scorer"
    elif td >= 1:
        text += f" | touchdown threat | {name} scoring ability | game changer"

    # Big play ability
    if forty_plus >= 2:
        text += f" | big play specialist | {name} explosive returns | home run hitter"
    elif twenty_plus >= 4:
        text += f" | chunk play returner | {name} field flipper | momentum shifter"

    # Volume tags
    if ret >= 20:
        text += f" | primary returner | {name} high volume | trusted hands"
    elif ret >= 10:
        text += f" | regular returner | {name} consistent opportunities"

    # Ball security
    if ret >= 10 and fum == 0:
        text += f" | sure hands | {name} ball security | no fumbles | reliable"
    elif fum >= 2:
        text += f" | fumble prone | {name} ball security issues"

    # Special teams value
    if avg >= 10 and ret >= 15:
        text += f" | special teams ace | {name} all-pro candidate | elite special teamer"
    elif avg >= 8 and ret >= 10:
        text += f" | special teams starter | {name} valuable contributor"

    return text


# All player data extracted from screenshots
players = [
    # Screenshot 1
    {"player": "Dalanius Blitz", "avg": 23.8, "ret": 12, "yds": 285, "td": 2, "20+": 4, "40+": 2, "long": 90, "fc": 18, "fum": 1},
    {"player": "Tom Kennedy", "avg": 21, "ret": 1, "yds": 21, "td": 0, "20+": 1, "40+": 0, "long": 21, "fc": 0, "fum": 0},
    {"player": "Tyreek Hill", "avg": 19, "ret": 1, "yds": 19, "td": 0, "20+": 0, "40+": 0, "long": 19, "fc": 0, "fum": 0},
    {"player": "Parker Washington", "avg": 17.2, "ret": 18, "yds": 309, "td": 2, "20+": 3, "40+": 3, "long": 87, "fc": 8, "fum": 1},
    {"player": "Marvin Mims Jr.", "avg": 15.3, "ret": 22, "yds": 336, "td": 0, "20+": 5, "40+": 1, "long": 70, "fc": 14, "fum": 1},
    {"player": "Tory Horton", "avg": 14.9, "ret": 16, "yds": 238, "td": 1, "20+": 2, "40+": 1, "long": 95, "fc": 9, "fum": 0},
    {"player": "Malik Washington", "avg": 14.8, "ret": 14, "yds": 207, "td": 1, "20+": 2, "40+": 1, "long": 74, "fc": 5, "fum": 0},
    {"player": "Marcus Jones", "avg": 14.6, "ret": 16, "yds": 234, "td": 1, "20+": 2, "40+": 2, "long": 87, "fc": 15, "fum": 1},
    {"player": "LaJohnay Wester", "avg": 14.4, "ret": 12, "yds": 173, "td": 0, "20+": 2, "40+": 0, "long": 35, "fc": 4, "fum": 1},
    {"player": "Greg Dortch", "avg": 13.8, "ret": 13, "yds": 179, "td": 0, "20+": 3, "40+": 1, "long": 40, "fc": 4, "fum": 0},
    {"player": "Kameron Johnson", "avg": 13, "ret": 18, "yds": 234, "td": 0, "20+": 3, "40+": 2, "long": 54, "fc": 10, "fum": 0},
    {"player": "Isaiah Williams", "avg": 12.7, "ret": 22, "yds": 280, "td": 1, "20+": 2, "40+": 1, "long": 74, "fc": 7, "fum": 0},
    {"player": "Rashid Shaheed", "avg": 12.6, "ret": 15, "yds": 189, "td": 0, "20+": 3, "40+": 1, "long": 40, "fc": 16, "fum": 0},
    {"player": "Jaylin Lane", "avg": 12.4, "ret": 18, "yds": 223, "td": 1, "20+": 2, "40+": 1, "long": 90, "fc": 6, "fum": 2},
    {"player": "Anthony Gould", "avg": 11.7, "ret": 10, "yds": 117, "td": 0, "20+": 2, "40+": 0, "long": 21, "fc": 6, "fum": 0},
    {"player": "Xavier Gipson", "avg": 10.8, "ret": 8, "yds": 86, "td": 0, "20+": 0, "40+": 0, "long": 19, "fc": 8, "fum": 2},
    {"player": "Kage Lervedah", "avg": 10.7, "ret": 13, "yds": 139, "td": 0, "20+": 1, "40+": 1, "long": 44, "fc": 9, "fum": 0},
    {"player": "Kaylin Noel", "avg": 10.6, "ret": 23, "yds": 244, "td": 0, "20+": 3, "40+": 2, "long": 53, "fc": 11, "fum": 0},
    {"player": "Jayden Reed", "avg": 10.5, "ret": 2, "yds": 21, "td": 0, "20+": 1, "40+": 0, "long": 20, "fc": 0, "fum": 0},
    {"player": "Myles Price", "avg": 10.3, "ret": 27, "yds": 278, "td": 0, "20+": 4, "40+": 1, "long": 43, "fc": 8, "fum": 2},
    {"player": "Skyy Moore", "avg": 10.3, "ret": 18, "yds": 185, "td": 0, "20+": 1, "40+": 0, "long": 27, "fc": 5, "fum": 1},
    {"player": "Avery Williams", "avg": 10.2, "ret": 4, "yds": 41, "td": 0, "20+": 0, "40+": 0, "long": 17, "fc": 0, "fum": 0},
    {"player": "Devin Duvernay", "avg": 10.2, "ret": 15, "yds": 153, "td": 0, "20+": 1, "40+": 0, "long": 22, "fc": 10, "fum": 0},
    {"player": "Ja'Shawn Williams", "avg": 10.2, "ret": 11, "yds": 112, "td": 0, "20+": 0, "40+": 0, "long": 17, "fc": 4, "fum": 1},
    {"player": "Ladd McConkey", "avg": 10, "ret": 1, "yds": 10, "td": 0, "20+": 0, "40+": 0, "long": 10, "fc": 3, "fum": 0},

    # Screenshot 2
    {"player": "Mitchell Tinsley", "avg": 10, "ret": 1, "yds": 10, "td": 0, "20+": 0, "40+": 0, "long": 10, "fc": 1, "fum": 0},
    {"player": "Charlie Jones", "avg": 9.8, "ret": 12, "yds": 117, "td": 0, "20+": 1, "40+": 0, "long": 23, "fc": 12, "fum": 0},
    {"player": "Jahan Dotson", "avg": 9.6, "ret": 5, "yds": 48, "td": 0, "20+": 0, "40+": 0, "long": 16, "fc": 12, "fum": 0},
    {"player": "DeAndre Carter", "avg": 9.3, "ret": 6, "yds": 56, "td": 0, "20+": 0, "40+": 0, "long": 15, "fc": 5, "fum": 1},
    {"player": "Darnell Agnew", "avg": 9.2, "ret": 11, "yds": 101, "td": 0, "20+": 0, "40+": 0, "long": 17, "fc": 7, "fum": 1},
    {"player": "Josh Downs", "avg": 9.2, "ret": 6, "yds": 55, "td": 0, "20+": 1, "40+": 0, "long": 24, "fc": 3, "fum": 1},
    {"player": "Jalen Cropper", "avg": 9, "ret": 3, "yds": 27, "td": 0, "20+": 0, "40+": 0, "long": 10, "fc": 3, "fum": 1},
    {"player": "Gunner Olszewski", "avg": 8.7, "ret": 19, "yds": 164, "td": 0, "20+": 1, "40+": 0, "long": 21, "fc": 12, "fum": 0},
    {"player": "Braxton Berrios", "avg": 8.3, "ret": 3, "yds": 25, "td": 0, "20+": 0, "40+": 0, "long": 10, "fc": 0, "fum": 0},
    {"player": "Calvin Austin III", "avg": 8, "ret": 6, "yds": 48, "td": 0, "20+": 0, "40+": 0, "long": 12, "fc": 3, "fum": 0},
    {"player": "Byron Williams", "avg": 8, "ret": 1, "yds": 8, "td": 0, "20+": 0, "40+": 0, "long": 8, "fc": 3, "fum": 0},
    {"player": "Xavier Smith", "avg": 7.9, "ret": 18, "yds": 142, "td": 0, "20+": 1, "40+": 0, "long": 20, "fc": 10, "fum": 0},
    {"player": "Alex Bachman", "avg": 7.3, "ret": 10, "yds": 73, "td": 0, "20+": 1, "40+": 0, "long": 25, "fc": 8, "fum": 0},
    {"player": "Kalif Raymond", "avg": 7.3, "ret": 20, "yds": 146, "td": 1, "20+": 1, "40+": 1, "long": 65, "fc": 12, "fum": 0},
    {"player": "Nikko Remigio", "avg": 7.3, "ret": 22, "yds": 160, "td": 0, "20+": 2, "40+": 0, "long": 25, "fc": 7, "fum": 1},
    {"player": "Darius Davis", "avg": 7.2, "ret": 8, "yds": 58, "td": 0, "20+": 1, "40+": 0, "long": 33, "fc": 14, "fum": 0},
    {"player": "Tahreek Gill", "avg": 7.2, "ret": 5, "yds": 36, "td": 0, "20+": 0, "40+": 0, "long": 11, "fc": 0, "fum": 0},
    {"player": "Tris Tucker", "avg": 7, "ret": 7, "yds": 49, "td": 0, "20+": 0, "40+": 0, "long": 15, "fc": 4, "fum": 0},
    {"player": "KaVontae Turpin", "avg": 6.9, "ret": 8, "yds": 55, "td": 0, "20+": 0, "40+": 0, "long": 19, "fc": 8, "fum": 0},
    {"player": "Trevor Etienne", "avg": 6.9, "ret": 14, "yds": 96, "td": 0, "20+": 0, "40+": 0, "long": 15, "fc": 4, "fum": 1},
    {"player": "Hunter Renfrow", "avg": 6.5, "ret": 2, "yds": 13, "td": 0, "20+": 0, "40+": 0, "long": 13, "fc": 2, "fum": 0},
    {"player": "Romeo Doubs", "avg": 6.2, "ret": 14, "yds": 87, "td": 0, "20+": 0, "40+": 0, "long": 16, "fc": 2, "fum": 0},
    {"player": "Ireon Coleman", "avg": 6, "ret": 1, "yds": 6, "td": 0, "20+": 0, "40+": 0, "long": 6, "fc": 0, "fum": 0},
    {"player": "Michael Bandy", "avg": 5.8, "ret": 5, "yds": 29, "td": 0, "20+": 0, "40+": 0, "long": 12, "fc": 3, "fum": 1},
    {"player": "Brandon Codrington", "avg": 5.8, "ret": 10, "yds": 58, "td": 0, "20+": 0, "40+": 0, "long": 15, "fc": 4, "fum": 1},

    # Screenshot 3 (and duplicate in screenshot 4)
    {"player": "Khalil Shakir", "avg": 5, "ret": 10, "yds": 50, "td": 0, "20+": 0, "40+": 0, "long": 11, "fc": 6, "fum": 0},
    {"player": "Matthew Golden", "avg": 4.7, "ret": 6, "yds": 28, "td": 0, "20+": 0, "40+": 0, "long": 11, "fc": 2, "fum": 0},
    {"player": "Isaiah Bond", "avg": 4.5, "ret": 2, "yds": 9, "td": 0, "20+": 0, "40+": 0, "long": 9, "fc": 1, "fum": 0},
    {"player": "Dante Pettis", "avg": 3.6, "ret": 5, "yds": 18, "td": 0, "20+": 0, "40+": 0, "long": 11, "fc": 2, "fum": 0},
    {"player": "Mason Kinsey", "avg": 1, "ret": 1, "yds": 1, "td": 0, "20+": 0, "40+": 0, "long": 1, "fc": 0, "fum": 0},
    {"player": "Keisean Nixon", "avg": 1, "ret": 3, "yds": 3, "td": 0, "20+": 0, "40+": 0, "long": 3, "fc": 1, "fum": 1},
    {"player": "Mike Ford", "avg": 0, "ret": 1, "yds": 0, "td": 0, "20+": 0, "40+": 0, "long": 0, "fc": 0, "fum": 0},
    {"player": "Marcola Hardiman", "avg": 0, "ret": 1, "yds": 0, "td": 0, "20+": 0, "40+": 0, "long": 0, "fc": 0, "fum": 1},
    {"player": "Quan Hart", "avg": 0, "ret": 1, "yds": 0, "td": 0, "20+": 0, "40+": 0, "long": 0, "fc": 0, "fum": 0},
    {"player": "Ray-Ray McCloud", "avg": 0, "ret": 2, "yds": 0, "td": 0, "20+": 0, "40+": 0, "long": 0, "fc": 2, "fum": 0},
    {"player": "David Moore", "avg": 0, "ret": 1, "yds": 0, "td": 0, "20+": 0, "40+": 0, "long": 0, "fc": 1, "fum": 0},
    {"player": "Mike Sainristil", "avg": 0, "ret": 1, "yds": 0, "td": 0, "20+": 0, "40+": 0, "long": 0, "fc": 0, "fum": 1},
]

def main():
    """Load all punt return stats into Kre8VidMems"""
    print("Loading NFL Player Punt Return Stats...")
    print(f"Total players: {len(players)}")

    # Create memory instance
    memory = Kre8VidMemory()

    # Process all players
    chunks = []
    for player in players:
        chunk = format_player_punt_return_stats(player)
        chunks.append(chunk)

    # Add summary chunk with top performers
    summary = "NFL Punt Return Stats Summary 2025"

    # Find top average returners
    top_avg = sorted([p for p in players if p['ret'] >= 5], key=lambda x: x['avg'], reverse=True)[:10]
    if top_avg:
        summary += "\n\nTop Punt Returners by Average (min 5 returns):"
        for p in top_avg:
            summary += f"\n- {p['player']}: {p['avg']} avg ({p['ret']} returns, {p['td']} TDs)"

    # Find touchdown scorers
    td_scorers = sorted([p for p in players if p['td'] > 0], key=lambda x: x['td'], reverse=True)
    if td_scorers:
        summary += "\n\nPunt Return TD Scorers:"
        for p in td_scorers:
            summary += f"\n- {p['player']}: {p['td']} TDs ({p['avg']} avg)"

    # Find most returns
    high_volume = sorted([p for p in players if p['ret'] > 0], key=lambda x: x['ret'], reverse=True)[:5]
    if high_volume:
        summary += "\n\nMost Punt Returns:"
        for p in high_volume:
            summary += f"\n- {p['player']}: {p['ret']} returns ({p['yds']} yards)"

    # Find longest returns
    longest = sorted([p for p in players if p['long'] > 0], key=lambda x: x['long'], reverse=True)[:5]
    if longest:
        summary += "\n\nLongest Punt Returns:"
        for p in longest:
            summary += f"\n- {p['player']}: {p['long']} yards"

    chunks.append(summary)

    # Load into memory
    print(f"Loading {len(chunks)} chunks into memory...")
    for i, chunk in enumerate(chunks, 1):
        memory.add(chunk)
        if i % 20 == 0:
            print(f"Added {i} chunks (Total: {i})")

    # Save memory
    memory_path = "data/memories/nfl-player-punt-returns-stats"
    memory.save(memory_path)
    print(f"✓ Saved punt return stats to {memory_path.split('/')[-1]}")

    # Print statistics
    print(f"\n✓ All NFL player punt return stats loaded successfully!")
    print(f"Total players: {len(players)}")
    print(f"\nPlayers with TD returns: {sum(1 for p in players if p['td'] > 0)}")
    print(f"Players with 15+ yard average (min 5 returns): {sum(1 for p in players if p['avg'] >= 15 and p['ret'] >= 5)}")
    print(f"Players with 20+ returns: {sum(1 for p in players if p['ret'] >= 20)}")
    print(f"Players with fumbles: {sum(1 for p in players if p['fum'] > 0)}")

    # Print top performers
    if top_avg:
        print(f"\nTop 5 Punt Returners by Average (min 5 returns):")
        for i, p in enumerate(top_avg[:5], 1):
            print(f"{i}. {p['player']}: {p['avg']} yards/return ({p['ret']} returns, {p['td']} TDs)")

    if td_scorers:
        print(f"\nAll Punt Return TD Scorers:")
        for i, p in enumerate(td_scorers, 1):
            print(f"{i}. {p['player']}: {p['td']} TDs")


if __name__ == "__main__":
    main()