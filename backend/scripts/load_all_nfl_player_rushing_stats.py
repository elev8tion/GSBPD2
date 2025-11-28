#!/usr/bin/env python3

"""
Load all NFL Player Rushing Statistics into Kre8VidMems
Extracts RB/QB rushing stats from screenshot images
"""

import sys
from pathlib import Path
from typing import Dict, List, Any

# Add backend to path for imports
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

# Import our custom Kre8VidMems library
from lib.kre8vidmems.kre8vidmems.api.memory import Kre8VidMemory

def format_player_rushing_stats(player: Dict[str, Any]) -> str:
    """Format player rushing stats for memory storage"""
    name = player.get('player', 'Unknown')
    rush_yards = player.get('rush_yds', 0)
    attempts = player.get('att', 0)
    tds = player.get('td', 0)
    runs_20_plus = player.get('20+', 0)
    runs_40_plus = player.get('40+', 0)
    longest = player.get('lng', 0)
    first_downs = player.get('rush_1st', 0)
    first_down_pct = player.get('rush_1st_pct', 0.0)
    fumbles = player.get('rush_fum', 0)

    # Build the text representation
    parts = [
        f"Player: {name}",
        f"Rush Yards: {rush_yards}",
        f"Attempts: {attempts}",
        f"TDs: {tds}",
        f"20+ Yard Runs: {runs_20_plus}",
        f"40+ Yard Runs: {runs_40_plus}",
        f"Longest: {longest}",
        f"First Downs: {first_downs}",
        f"First Down %: {first_down_pct}%",
        f"Fumbles: {fumbles}"
    ]

    text = " | ".join(parts)

    # Add performance-based tags for RBs
    if rush_yards > 1500:
        text += f" | elite rusher | 1500+ yard rusher | {name} elite RB | MVP candidate"
    elif rush_yards > 1200:
        text += f" | pro bowl RB | 1200+ yard rusher | {name} RB1 | top rusher"
    elif rush_yards > 1000:
        text += f" | 1000 yard rusher | {name} feature back | RB1"
    elif rush_yards > 800:
        text += f" | solid RB | 800+ yards | {name} good rusher | RB2"
    elif rush_yards > 600:
        text += f" | productive RB | 600+ yards | {name} contributor"
    elif rush_yards > 400:
        text += f" | backup RB | committee back | {name} rotational"
    elif rush_yards > 200:
        text += f" | part-time RB | {name} depth player"

    # TD production tags
    if tds >= 15:
        text += f" | elite TD producer | 15+ rushing TDs | {name} red zone monster"
    elif tds >= 10:
        text += f" | high TD producer | 10+ rushing TDs | {name} goal line back"
    elif tds >= 7:
        text += f" | good TD producer | {name} scoring threat"

    # Big play ability
    if runs_40_plus >= 3:
        text += f" | home run hitter | explosive runner | {name} big play threat"
    elif runs_20_plus >= 5:
        text += f" | explosive runner | chunk play ability | {name} breakaway speed"

    # Yards per attempt (calculate if attempts > 0)
    if attempts > 0:
        ypa = rush_yards / attempts
        if ypa >= 5.5:
            text += f" | elite efficiency | 5.5+ YPA | {name} explosive"
        elif ypa >= 4.5:
            text += f" | good efficiency | 4.5+ YPA | {name} productive"
        elif ypa < 3.5:
            text += f" | poor efficiency | below 3.5 YPA | {name} struggling"

    # Fumble issues
    if fumbles >= 3:
        text += f" | fumble prone | ball security issues | {name} risky"
    elif fumbles == 0 and attempts > 100:
        text += f" | excellent ball security | no fumbles | {name} reliable"

    # Add position tags (detect QBs by name or lower attempts with decent yards)
    qb_names = ['Mahomes', 'Allen', 'Hurts', 'Jackson', 'Herbert', 'Prescott', 'Goff', 'Love', 'Stroud',
                'Lawrence', 'Murray', 'Jones', 'Williams', 'Young', 'Maye', 'Daniels', 'Richardson',
                'Mayfield', 'Wilson', 'Rodgers', 'Stafford', 'Cousins', 'Carr', 'Smith', 'Tannehill',
                'Garoppolo', 'Fields', 'Nix', 'Darnold', 'Flacco', 'Tagovailoa', 'Penix', 'Ward', 'Rattler']

    is_qb = any(qb_name in name for qb_name in qb_names)

    if is_qb:
        text += f" | {name} rushing | {name} quarterback rushing | QB rushing stats | dual threat QB"
        if rush_yards > 300:
            text += f" | mobile QB | running quarterback"
    else:
        text += f" | {name} rushing | {name} running back | RB stats | NFL RB"

    return text

def extract_all_rushing_stats() -> List[Dict[str, Any]]:
    """Extract rushing stats from all screenshots"""

    # Complete data from all 12 screenshots (376 players)
    rushing_stats_2025 = [
        # Screenshot 1
        {"player": "Jonathan Taylor", "rush_yds": 1197, "att": 205, "td": 15, "20+": 9, "40+": 4, "lng": 83, "rush_1st": 60, "rush_1st_pct": 29.3, "rush_fum": 0},
        {"player": "James Cook", "rush_yds": 1084, "att": 199, "td": 8, "20+": 7, "40+": 3, "lng": 64, "rush_1st": 47, "rush_1st_pct": 23.6, "rush_fum": 2},
        {"player": "Jahmyr Gibbs", "rush_yds": 1019, "att": 175, "td": 10, "20+": 10, "40+": 6, "lng": 78, "rush_1st": 46, "rush_1st_pct": 26.3, "rush_fum": 0},
        {"player": "Javonte Williams", "rush_yds": 955, "att": 198, "td": 8, "20+": 5, "40+": 1, "lng": 66, "rush_1st": 50, "rush_1st_pct": 25.2, "rush_fum": 1},
        {"player": "De'Von Achane", "rush_yds": 900, "att": 164, "td": 5, "20+": 9, "40+": 3, "lng": 59, "rush_1st": 40, "rush_1st_pct": 24.4, "rush_fum": 1},
        {"player": "Rico Dowdle", "rush_yds": 871, "att": 174, "td": 5, "20+": 6, "40+": 2, "lng": 53, "rush_1st": 43, "rush_1st_pct": 24.7, "rush_fum": 0},
        {"player": "Derrick Henry", "rush_yds": 871, "att": 187, "td": 9, "20+": 6, "40+": 3, "lng": 59, "rush_1st": 42, "rush_1st_pct": 22.5, "rush_fum": 3},
        {"player": "Bijan Robinson", "rush_yds": 853, "att": 172, "td": 4, "20+": 4, "40+": 1, "lng": 81, "rush_1st": 36, "rush_1st_pct": 20.9, "rush_fum": 2},
        {"player": "Travis Etienne", "rush_yds": 815, "att": 169, "td": 5, "20+": 5, "40+": 3, "lng": 71, "rush_1st": 34, "rush_1st_pct": 20.1, "rush_fum": 0},
        {"player": "Christian McCaffrey", "rush_yds": 796, "att": 217, "td": 7, "20+": 1, "40+": 0, "lng": 20, "rush_1st": 50, "rush_1st_pct": 23, "rush_fum": 1},
        {"player": "Kyren Williams", "rush_yds": 796, "att": 170, "td": 6, "20+": 3, "40+": 0, "lng": 34, "rush_1st": 49, "rush_1st_pct": 28.8, "rush_fum": 2},
        {"player": "J.K. Dobbins", "rush_yds": 772, "att": 153, "td": 4, "20+": 5, "40+": 1, "lng": 41, "rush_1st": 37, "rush_1st_pct": 24.2, "rush_fum": 0},
        {"player": "Breece Hall", "rush_yds": 766, "att": 168, "td": 2, "20+": 7, "40+": 0, "lng": 35, "rush_1st": 43, "rush_1st_pct": 25.6, "rush_fum": 2},
        {"player": "Josh Jacobs", "rush_yds": 731, "att": 186, "td": 11, "20+": 1, "40+": 0, "lng": 29, "rush_1st": 43, "rush_1st_pct": 23.1, "rush_fum": 2},
        {"player": "Saquon Barkley", "rush_yds": 684, "att": 185, "td": 4, "20+": 2, "40+": 1, "lng": 65, "rush_1st": 27, "rush_1st_pct": 14.6, "rush_fum": 0},
        {"player": "Kenneth Walker III", "rush_yds": 677, "att": 147, "td": 4, "20+": 7, "40+": 0, "lng": 31, "rush_1st": 32, "rush_1st_pct": 21.8, "rush_fum": 0},
        {"player": "Quinshon Judkins", "rush_yds": 667, "att": 173, "td": 7, "20+": 4, "40+": 1, "lng": 46, "rush_1st": 40, "rush_1st_pct": 23.1, "rush_fum": 0},
        {"player": "D'Andre Swift", "rush_yds": 649, "att": 142, "td": 4, "20+": 3, "40+": 0, "lng": 25, "rush_1st": 38, "rush_1st_pct": 26.8, "rush_fum": 2},
        {"player": "Chase Brown", "rush_yds": 626, "att": 145, "td": 2, "20+": 5, "40+": 0, "lng": 37, "rush_1st": 35, "rush_1st_pct": 24.1, "rush_fum": 1},
        {"player": "Ashton Jeanty", "rush_yds": 604, "att": 166, "td": 4, "20+": 1, "40+": 1, "lng": 64, "rush_1st": 30, "rush_1st_pct": 18.1, "rush_fum": 1},
        {"player": "Jaylen Warren", "rush_yds": 604, "att": 141, "td": 3, "20+": 3, "40+": 0, "lng": 37, "rush_1st": 36, "rush_1st_pct": 25.5, "rush_fum": 0},
        {"player": "TreVeyon Henderson", "rush_yds": 558, "att": 118, "td": 5, "20+": 3, "40+": 2, "lng": 69, "rush_1st": 29, "rush_1st_pct": 24.6, "rush_fum": 1},
        {"player": "David Montgomery", "rush_yds": 543, "att": 123, "td": 6, "20+": 2, "40+": 1, "lng": 72, "rush_1st": 28, "rush_1st_pct": 22.8, "rush_fum": 2},
        {"player": "Jordan Mason", "rush_yds": 531, "att": 116, "td": 5, "20+": 2, "40+": 0, "lng": 24, "rush_1st": 33, "rush_1st_pct": 28.4, "rush_fum": 2},
        {"player": "Tony Pollard", "rush_yds": 522, "att": 140, "td": 2, "20+": 1, "40+": 0, "lng": 21, "rush_1st": 26, "rush_1st_pct": 18.6, "rush_fum": 2},

        # Screenshot 2
        {"player": "Kareem Hunt", "rush_yds": 515, "att": 130, "td": 7, "20+": 1, "40+": 0, "lng": 33, "rush_1st": 42, "rush_1st_pct": 32.3, "rush_fum": 2},
        {"player": "Jacarry Croskey-Merritt", "rush_yds": 498, "att": 114, "td": 4, "20+": 2, "40+": 1, "lng": 42, "rush_1st": 25, "rush_1st_pct": 21.9, "rush_fum": 2},
        {"player": "Alvin Kamara", "rush_yds": 471, "att": 131, "td": 1, "20+": 0, "40+": 0, "lng": 18, "rush_1st": 21, "rush_1st_pct": 16, "rush_fum": 1},
        {"player": "Kyle Monangai", "rush_yds": 461, "att": 99, "td": 4, "20+": 2, "40+": 0, "lng": 39, "rush_1st": 26, "rush_1st_pct": 26.3, "rush_fum": 0},
        {"player": "Nick Chubb", "rush_yds": 435, "att": 105, "td": 2, "20+": 2, "40+": 0, "lng": 27, "rush_1st": 18, "rush_1st_pct": 17.1, "rush_fum": 0},
        {"player": "Woody Marks", "rush_yds": 423, "att": 115, "td": 2, "20+": 2, "40+": 0, "lng": 23, "rush_1st": 22, "rush_1st_pct": 19.1, "rush_fum": 0},
        {"player": "Kalel Mullings", "rush_yds": 417, "att": 96, "td": 2, "20+": 3, "40+": 0, "lng": 38, "rush_1st": 24, "rush_1st_pct": 25, "rush_fum": 1},
        {"player": "Rachaad White", "rush_yds": 414, "att": 104, "td": 4, "20+": 0, "40+": 0, "lng": 16, "rush_1st": 32, "rush_1st_pct": 30.8, "rush_fum": 0},
        {"player": "Cam Skattebo", "rush_yds": 410, "att": 101, "td": 5, "20+": 1, "40+": 0, "lng": 24, "rush_1st": 27, "rush_1st_pct": 26.7, "rush_fum": 1},
        {"player": "Tyrone Tracy Jr.", "rush_yds": 398, "att": 103, "td": 1, "20+": 1, "40+": 0, "lng": 31, "rush_1st": 21, "rush_1st_pct": 20.4, "rush_fum": 0},
        {"player": "Zach Charbonnet", "rush_yds": 385, "att": 111, "td": 7, "20+": 1, "40+": 0, "lng": 30, "rush_1st": 24, "rush_1st_pct": 21.6, "rush_fum": 0},
        {"player": "Justin Fields", "rush_yds": 383, "att": 71, "td": 4, "20+": 2, "40+": 1, "lng": 43, "rush_1st": 26, "rush_1st_pct": 36.6, "rush_fum": 2},
        {"player": "Josh Allen", "rush_yds": 371, "att": 70, "td": 10, "20+": 3, "40+": 1, "lng": 40, "rush_1st": 29, "rush_1st_pct": 41.4, "rush_fum": 5},
        {"player": "Chuba Hubbard", "rush_yds": 360, "att": 94, "td": 1, "20+": 0, "40+": 0, "lng": 14, "rush_1st": 18, "rush_1st_pct": 19.2, "rush_fum": 0},
        {"player": "Patrick Mahomes", "rush_yds": 348, "att": 55, "td": 4, "20+": 1, "40+": 0, "lng": 22, "rush_1st": 25, "rush_1st_pct": 45.4, "rush_fum": 0},
        {"player": "Justin Herbert", "rush_yds": 345, "att": 54, "td": 1, "20+": 3, "40+": 1, "lng": 41, "rush_1st": 26, "rush_1st_pct": 48.2, "rush_fum": 2},
        {"player": "Isiah Pacheco", "rush_yds": 345, "att": 81, "td": 1, "20+": 0, "40+": 0, "lng": 16, "rush_1st": 21, "rush_1st_pct": 25.9, "rush_fum": 0},
        {"player": "Blake Corum", "rush_yds": 341, "att": 82, "td": 1, "20+": 1, "40+": 0, "lng": 21, "rush_1st": 21, "rush_1st_pct": 25.6, "rush_fum": 0},
        {"player": "Emanuel Wilson", "rush_yds": 341, "att": 85, "td": 3, "20+": 0, "40+": 0, "lng": 15, "rush_1st": 22, "rush_1st_pct": 25.9, "rush_fum": 0},
        {"player": "Kenneth Gainwell", "rush_yds": 336, "att": 71, "td": 3, "20+": 1, "40+": 1, "lng": 55, "rush_1st": 23, "rush_1st_pct": 32.4, "rush_fum": 1},
        {"player": "Tyler Allgeier", "rush_yds": 324, "att": 89, "td": 7, "20+": 1, "40+": 0, "lng": 21, "rush_1st": 25, "rush_1st_pct": 28.1, "rush_fum": 0},
        {"player": "Jaxson Dart", "rush_yds": 317, "att": 57, "td": 7, "20+": 3, "40+": 0, "lng": 24, "rush_1st": 26, "rush_1st_pct": 45.6, "rush_fum": 2},
        {"player": "Omarion Hampton", "rush_yds": 314, "att": 66, "td": 2, "20+": 2, "40+": 1, "lng": 54, "rush_1st": 17, "rush_1st_pct": 25.8, "rush_fum": 0},
        {"player": "Drake Maye", "rush_yds": 307, "att": 75, "td": 2, "20+": 2, "40+": 0, "lng": 28, "rush_1st": 23, "rush_1st_pct": 30.7, "rush_fum": 2},
        {"player": "Brian Robinson", "rush_yds": 302, "att": 64, "td": 2, "20+": 0, "40+": 0, "lng": 19, "rush_1st": 16, "rush_1st_pct": 25, "rush_fum": 0},

        # Screenshot 3
        {"player": "Jalen Hurts", "rush_yds": 298, "att": 80, "td": 8, "20+": 1, "40+": 0, "lng": 29, "rush_1st": 32, "rush_1st_pct": 40, "rush_fum": 3},
        {"player": "Aaron Jones", "rush_yds": 297, "att": 61, "td": 1, "20+": 1, "40+": 0, "lng": 31, "rush_1st": 13, "rush_1st_pct": 21.3, "rush_fum": 0},
        {"player": "Caleb Williams", "rush_yds": 293, "att": 56, "td": 3, "20+": 2, "40+": 0, "lng": 29, "rush_1st": 18, "rush_1st_pct": 32.1, "rush_fum": 5},
        {"player": "Rhamondre Stevenson", "rush_yds": 284, "att": 89, "td": 3, "20+": 2, "40+": 0, "lng": 22, "rush_1st": 13, "rush_1st_pct": 14.6, "rush_fum": 2},
        {"player": "Chris Rodriguez Jr.", "rush_yds": 279, "att": 60, "td": 3, "20+": 1, "40+": 1, "lng": 48, "rush_1st": 19, "rush_1st_pct": 31.7, "rush_fum": 0},
        {"player": "Sean Tucker", "rush_yds": 277, "att": 63, "td": 4, "20+": 1, "40+": 1, "lng": 43, "rush_1st": 16, "rush_1st_pct": 25.4, "rush_fum": 1},
        {"player": "Jayden Daniels", "rush_yds": 262, "att": 54, "td": 2, "20+": 0, "40+": 0, "lng": 18, "rush_1st": 13, "rush_1st_pct": 24.1, "rush_fum": 1},
        {"player": "Brashard Smith", "rush_yds": 255, "att": 67, "td": 3, "20+": 0, "40+": 0, "lng": 15, "rush_1st": 19, "rush_1st_pct": 28.4, "rush_fum": 0},
        {"player": "RJ Harvey", "rush_yds": 244, "att": 61, "td": 2, "20+": 2, "40+": 2, "lng": 50, "rush_1st": 9, "rush_1st_pct": 14.8, "rush_fum": 0},
        {"player": "Emari Demercado", "rush_yds": 241, "att": 31, "td": 0, "20+": 2, "40+": 2, "lng": 71, "rush_1st": 6, "rush_1st_pct": 19.4, "rush_fum": 1},
        {"player": "Devin Singletary", "rush_yds": 238, "att": 74, "td": 2, "20+": 0, "40+": 0, "lng": 14, "rush_1st": 15, "rush_1st_pct": 20.3, "rush_fum": 0},
        {"player": "Bucky Irving", "rush_yds": 237, "att": 71, "td": 0, "20+": 0, "40+": 0, "lng": 16, "rush_1st": 7, "rush_1st_pct": 9.9, "rush_fum": 1},
        {"player": "Lamar Jackson", "rush_yds": 237, "att": 46, "td": 1, "20+": 0, "40+": 0, "lng": 19, "rush_1st": 15, "rush_1st_pct": 32.6, "rush_fum": 1},
        {"player": "Baker Mayfield", "rush_yds": 216, "att": 31, "td": 1, "20+": 2, "40+": 0, "lng": 33, "rush_1st": 17, "rush_1st_pct": 54.8, "rush_fum": 1},
        {"player": "Bo Nix", "rush_yds": 213, "att": 50, "td": 3, "20+": 2, "40+": 0, "lng": 25, "rush_1st": 13, "rush_1st_pct": 26, "rush_fum": 1},
        {"player": "Trevor Lawrence", "rush_yds": 210, "att": 54, "td": 5, "20+": 1, "40+": 0, "lng": 21, "rush_1st": 23, "rush_1st_pct": 42.6, "rush_fum": 2},
        {"player": "Samaje Perine", "rush_yds": 198, "att": 32, "td": 1, "20+": 2, "40+": 0, "lng": 32, "rush_1st": 15, "rush_1st_pct": 46.9, "rush_fum": 1},
        {"player": "Bam Knight", "rush_yds": 193, "att": 63, "td": 4, "20+": 0, "40+": 0, "lng": 17, "rush_1st": 16, "rush_1st_pct": 25.4, "rush_fum": 0},
        {"player": "Marcus Mariota", "rush_yds": 193, "att": 27, "td": 1, "20+": 4, "40+": 1, "lng": 44, "rush_1st": 7, "rush_1st_pct": 25.9, "rush_fum": 2},
        {"player": "Kendre Miller", "rush_yds": 193, "att": 47, "td": 1, "20+": 0, "40+": 0, "lng": 18, "rush_1st": 9, "rush_1st_pct": 19.2, "rush_fum": 0},
        {"player": "C.J. Stroud", "rush_yds": 189, "att": 29, "td": 0, "20+": 1, "40+": 0, "lng": 30, "rush_1st": 14, "rush_1st_pct": 48.3, "rush_fum": 0},
        {"player": "Jeremy McNichols", "rush_yds": 181, "att": 26, "td": 1, "20+": 1, "40+": 1, "lng": 40, "rush_1st": 10, "rush_1st_pct": 38.5, "rush_fum": 0},
        {"player": "Tank Bigsby", "rush_yds": 176, "att": 23, "td": 0, "20+": 1, "40+": 0, "lng": 29, "rush_1st": 8, "rush_1st_pct": 34.8, "rush_fum": 0},
        {"player": "Kyler Murray", "rush_yds": 173, "att": 29, "td": 1, "20+": 2, "40+": 0, "lng": 30, "rush_1st": 10, "rush_1st_pct": 34.5, "rush_fum": 1},
        {"player": "Spencer Rattler", "rush_yds": 167, "att": 31, "td": 0, "20+": 0, "40+": 0, "lng": 15, "rush_1st": 17, "rush_1st_pct": 54.8, "rush_fum": 1},

        # Screenshot 4
        {"player": "Ollie Gordon II", "rush_yds": 164, "att": 50, "td": 2, "20+": 1, "40+": 0, "lng": 20, "rush_1st": 17, "rush_1st_pct": 34, "rush_fum": 0},
        {"player": "Jordan Love", "rush_yds": 164, "att": 41, "td": 0, "20+": 1, "40+": 0, "lng": 25, "rush_1st": 11, "rush_1st_pct": 26.8, "rush_fum": 2},
        {"player": "Trey Benson", "rush_yds": 160, "att": 29, "td": 0, "20+": 2, "40+": 1, "lng": 52, "rush_1st": 4, "rush_1st_pct": 13.8, "rush_fum": 0},
        {"player": "Daniel Jones", "rush_yds": 159, "att": 43, "td": 5, "20+": 0, "40+": 0, "lng": 19, "rush_1st": 19, "rush_1st_pct": 44.2, "rush_fum": 1},
        {"player": "Tyjae Spears", "rush_yds": 159, "att": 37, "td": 1, "20+": 1, "40+": 1, "lng": 41, "rush_1st": 6, "rush_1st_pct": 16.2, "rush_fum": 0},
        {"player": "Isaiah Davis", "rush_yds": 137, "att": 26, "td": 0, "20+": 1, "40+": 1, "lng": 50, "rush_1st": 3, "rush_1st_pct": 11.5, "rush_fum": 0},
        {"player": "Michael Carter", "rush_yds": 135, "att": 45, "td": 1, "20+": 0, "40+": 0, "lng": 11, "rush_1st": 9, "rush_1st_pct": 20, "rush_fum": 0},
        {"player": "Keaton Mitchell", "rush_yds": 134, "att": 23, "td": 0, "20+": 2, "40+": 0, "lng": 25, "rush_1st": 7, "rush_1st_pct": 30.4, "rush_fum": 1},
        {"player": "Dak Prescott", "rush_yds": 124, "att": 41, "td": 2, "20+": 0, "40+": 0, "lng": 14, "rush_1st": 9, "rush_1st_pct": 22, "rush_fum": 2},
        {"player": "J.J. McCarthy", "rush_yds": 120, "att": 23, "td": 2, "20+": 1, "40+": 0, "lng": 26, "rush_1st": 6, "rush_1st_pct": 26.1, "rush_fum": 3},
        {"player": "Miles Sanders", "rush_yds": 117, "att": 20, "td": 1, "20+": 1, "40+": 1, "lng": 49, "rush_1st": 5, "rush_1st_pct": 25, "rush_fum": 1},
        {"player": "Cam Ward", "rush_yds": 116, "att": 27, "td": 1, "20+": 1, "40+": 0, "lng": 20, "rush_1st": 10, "rush_1st_pct": 37, "rush_fum": 1},
        {"player": "Geno Smith", "rush_yds": 110, "att": 37, "td": 0, "20+": 1, "40+": 0, "lng": 20, "rush_1st": 13, "rush_1st_pct": 35.1, "rush_fum": 1},
        {"player": "Antonio Gibson", "rush_yds": 106, "att": 25, "td": 1, "20+": 1, "40+": 0, "lng": 21, "rush_1st": 6, "rush_1st_pct": 24, "rush_fum": 1},
        {"player": "Russell Wilson", "rush_yds": 106, "att": 18, "td": 0, "20+": 0, "40+": 0, "lng": 15, "rush_1st": 6, "rush_1st_pct": 33.3, "rush_fum": 1},
        {"player": "Jacoby Brissett", "rush_yds": 100, "att": 24, "td": 1, "20+": 0, "40+": 0, "lng": 15, "rush_1st": 11, "rush_1st_pct": 45.8, "rush_fum": 1},
        {"player": "Tyrod Taylor", "rush_yds": 99, "att": 19, "td": 0, "20+": 0, "40+": 0, "lng": 15, "rush_1st": 6, "rush_1st_pct": 31.6, "rush_fum": 0},
        {"player": "Bryce Young", "rush_yds": 98, "att": 27, "td": 1, "20+": 1, "40+": 0, "lng": 22, "rush_1st": 9, "rush_1st_pct": 33.3, "rush_fum": 2},
        {"player": "Malik Davis", "rush_yds": 97, "att": 13, "td": 1, "20+": 2, "40+": 1, "lng": 43, "rush_1st": 4, "rush_1st_pct": 30.8, "rush_fum": 0},
        {"player": "James Conner", "rush_yds": 95, "att": 32, "td": 1, "20+": 0, "40+": 0, "lng": 12, "rush_1st": 7, "rush_1st_pct": 21.9, "rush_fum": 1},
        {"player": "Trevor Etienne", "rush_yds": 94, "att": 20, "td": 0, "20+": 1, "40+": 0, "lng": 22, "rush_1st": 6, "rush_1st_pct": 30, "rush_fum": 0},
        {"player": "Justice Hill", "rush_yds": 93, "att": 18, "td": 2, "20+": 1, "40+": 1, "lng": 71, "rush_1st": 4, "rush_1st_pct": 22.2, "rush_fum": 1},
        {"player": "Tyler Huntley", "rush_yds": 92, "att": 11, "td": 0, "20+": 1, "40+": 0, "lng": 29, "rush_1st": 6, "rush_1st_pct": 54.6, "rush_fum": 0},
        {"player": "Raheem Mostert", "rush_yds": 92, "att": 20, "td": 0, "20+": 1, "40+": 0, "lng": 37, "rush_1st": 5, "rush_1st_pct": 25, "rush_fum": 0},
        {"player": "Ty Johnson", "rush_yds": 90, "att": 21, "td": 1, "20+": 0, "40+": 0, "lng": 17, "rush_1st": 3, "rush_1st_pct": 14.3, "rush_fum": 0},

        # Screenshot 5
        {"player": "Dylan Sampson", "rush_yds": 89, "att": 30, "td": 0, "20+": 1, "40+": 0, "lng": 26, "rush_1st": 7, "rush_1st_pct": 18.4, "rush_fum": 0},
        {"player": "Braelon Allen", "rush_yds": 87, "att": 29, "td": 0, "20+": 0, "40+": 0, "lng": 8, "rush_1st": 2, "rush_1st_pct": 6.9, "rush_fum": 1},
        {"player": "Dillon Gabriel", "rush_yds": 86, "att": 14, "td": 0, "20+": 0, "40+": 0, "lng": 19, "rush_1st": 4, "rush_1st_pct": 28.6, "rush_fum": 0},
        {"player": "Xavier Worthy", "rush_yds": 86, "att": 9, "td": 0, "20+": 1, "40+": 0, "lng": 35, "rush_1st": 4, "rush_1st_pct": 44.4, "rush_fum": 0},
        {"player": "Malik Washington", "rush_yds": 78, "att": 13, "td": 0, "20+": 0, "40+": 0, "lng": 18, "rush_1st": 3, "rush_1st_pct": 23.1, "rush_fum": 1},
        {"player": "Brandon Allen", "rush_yds": 76, "att": 18, "td": 1, "20+": 0, "40+": 0, "lng": 15, "rush_1st": 4, "rush_1st_pct": 22.2, "rush_fum": 1},
        {"player": "Jaret Patterson", "rush_yds": 75, "att": 21, "td": 0, "20+": 0, "40+": 0, "lng": 9, "rush_1st": 3, "rush_1st_pct": 14.3, "rush_fum": 0},
        {"player": "Jerome Ford", "rush_yds": 73, "att": 24, "td": 0, "20+": 0, "40+": 0, "lng": 12, "rush_1st": 5, "rush_1st_pct": 20.8, "rush_fum": 0},
        {"player": "George Holani", "rush_yds": 73, "att": 22, "td": 1, "20+": 0, "40+": 0, "lng": 9, "rush_1st": 5, "rush_1st_pct": 22.7, "rush_fum": 1},
        {"player": "Terrell Jennings", "rush_yds": 73, "att": 23, "td": 1, "20+": 0, "40+": 0, "lng": 11, "rush_1st": 8, "rush_1st_pct": 34.8, "rush_fum": 0},
        {"player": "Puka Nacua", "rush_yds": 73, "att": 6, "td": 1, "20+": 1, "40+": 1, "lng": 45, "rush_1st": 3, "rush_1st_pct": 50, "rush_fum": 0},
        {"player": "LeQuint Allen Jr.", "rush_yds": 70, "att": 14, "td": 0, "20+": 0, "40+": 0, "lng": 12, "rush_1st": 5, "rush_1st_pct": 35.7, "rush_fum": 0},
        {"player": "Michael Penix Jr.", "rush_yds": 70, "att": 21, "td": 1, "20+": 0, "40+": 0, "lng": 15, "rush_1st": 5, "rush_1st_pct": 23.8, "rush_fum": 1},
        {"player": "Taysom Hill", "rush_yds": 69, "att": 32, "td": 1, "20+": 1, "40+": 0, "lng": 29, "rush_1st": 12, "rush_1st_pct": 37.5, "rush_fum": 0},
        {"player": "Zavier Scott", "rush_yds": 69, "att": 21, "td": 0, "20+": 0, "40+": 0, "lng": 11, "rush_1st": 3, "rush_1st_pct": 14.3, "rush_fum": 2},
        {"player": "Malachi Corley", "rush_yds": 68, "att": 5, "td": 0, "20+": 1, "40+": 0, "lng": 31, "rush_1st": 4, "rush_1st_pct": 80, "rush_fum": 0},
        {"player": "DJ Giddens", "rush_yds": 66, "att": 18, "td": 0, "20+": 0, "40+": 0, "lng": 12, "rush_1st": 3, "rush_1st_pct": 16.7, "rush_fum": 0},
        {"player": "Jaydon Blue", "rush_yds": 65, "att": 22, "td": 0, "20+": 0, "40+": 0, "lng": 14, "rush_1st": 3, "rush_1st_pct": 13.6, "rush_fum": 1},
        {"player": "KaVontae Turpin", "rush_yds": 63, "att": 12, "td": 0, "20+": 1, "40+": 0, "lng": 25, "rush_1st": 3, "rush_1st_pct": 25, "rush_fum": 1},
        {"player": "Najee Harris", "rush_yds": 61, "att": 15, "td": 0, "20+": 0, "40+": 0, "lng": 7, "rush_1st": 3, "rush_1st_pct": 20, "rush_fum": 0},
        {"player": "Mac Jones", "rush_yds": 61, "att": 31, "td": 0, "20+": 0, "40+": 0, "lng": 13, "rush_1st": 10, "rush_1st_pct": 32.3, "rush_fum": 1},
        {"player": "Devin Neal", "rush_yds": 61, "att": 17, "td": 0, "20+": 0, "40+": 0, "lng": 14, "rush_1st": 2, "rush_1st_pct": 11.8, "rush_fum": 0},
        {"player": "Tahj Washington", "rush_yds": 60, "att": 9, "td": 0, "20+": 0, "40+": 0, "lng": 12, "rush_1st": 3, "rush_1st_pct": 33.3, "rush_fum": 1},
        {"player": "AJ Dillon", "rush_yds": 60, "att": 12, "td": 0, "20+": 0, "40+": 0, "lng": 11, "rush_1st": 4, "rush_1st_pct": 33.3, "rush_fum": 0},
        {"player": "Keilan Robinson", "rush_yds": 58, "att": 22, "td": 0, "20+": 0, "40+": 0, "lng": 9, "rush_1st": 2, "rush_1st_pct": 9.1, "rush_fum": 0},

        # Screenshot 6
        {"player": "DJ Moore", "rush_yds": 57, "att": 13, "td": 1, "20+": 0, "40+": 0, "lng": 17, "rush_1st": 3, "rush_1st_pct": 23.1, "rush_fum": 0},
        {"player": "Carson Wentz", "rush_yds": 57, "att": 11, "td": 0, "20+": 0, "40+": 0, "lng": 16, "rush_1st": 3, "rush_1st_pct": 27.3, "rush_fum": 1},
        {"player": "Marvin Mims Jr.", "rush_yds": 56, "att": 8, "td": 1, "20+": 0, "40+": 0, "lng": 16, "rush_1st": 3, "rush_1st_pct": 37.5, "rush_fum": 1},
        {"player": "Deebo Samuel Sr.", "rush_yds": 53, "att": 11, "td": 1, "20+": 0, "40+": 0, "lng": 19, "rush_1st": 3, "rush_1st_pct": 27.3, "rush_fum": 0},
        {"player": "Sam Darnold", "rush_yds": 49, "att": 16, "td": 0, "20+": 1, "40+": 0, "lng": 24, "rush_1st": 4, "rush_1st_pct": 25, "rush_fum": 1},
        {"player": "Jaylen Wright", "rush_yds": 49, "att": 15, "td": 0, "20+": 0, "40+": 0, "lng": 18, "rush_1st": 2, "rush_1st_pct": 13.3, "rush_fum": 0},
        {"player": "Davis Mills", "rush_yds": 48, "att": 12, "td": 1, "20+": 0, "40+": 0, "lng": 14, "rush_1st": 1, "rush_1st_pct": 8.3, "rush_fum": 1},
        {"player": "Jared Goff", "rush_yds": 46, "att": 13, "td": 0, "20+": 1, "40+": 0, "lng": 24, "rush_1st": 4, "rush_1st_pct": 30.8, "rush_fum": 1},
        {"player": "Mark Andrews", "rush_yds": 45, "att": 9, "td": 1, "20+": 1, "40+": 0, "lng": 35, "rush_1st": 6, "rush_1st_pct": 66.7, "rush_fum": 0},
        {"player": "Matthew Golden", "rush_yds": 45, "att": 8, "td": 0, "20+": 0, "40+": 0, "lng": 9, "rush_1st": 3, "rush_1st_pct": 37.5, "rush_fum": 0},
        {"player": "Will Shipley", "rush_yds": 45, "att": 11, "td": 0, "20+": 1, "40+": 0, "lng": 20, "rush_1st": 4, "rush_1st_pct": 36.4, "rush_fum": 0},
        {"player": "Ray Davis", "rush_yds": 44, "att": 24, "td": 0, "20+": 0, "40+": 0, "lng": 8, "rush_1st": 2, "rush_1st_pct": 8.3, "rush_fum": 0},
        {"player": "Ashton Dulin", "rush_yds": 44, "att": 3, "td": 0, "20+": 1, "40+": 0, "lng": 22, "rush_1st": 2, "rush_1st_pct": 66.7, "rush_fum": 0},
        {"player": "Jaylon Johnson", "rush_yds": 44, "att": 7, "td": 0, "20+": 0, "40+": 0, "lng": 11, "rush_1st": 2, "rush_1st_pct": 28.6, "rush_fum": 0},
        {"player": "Austin Ekeler", "rush_yds": 43, "att": 14, "td": 0, "20+": 0, "40+": 0, "lng": 6, "rush_1st": 3, "rush_1st_pct": 21.4, "rush_fum": 0},
        {"player": "Zay Flowers", "rush_yds": 42, "att": 8, "td": 0, "20+": 0, "40+": 0, "lng": 11, "rush_1st": 2, "rush_1st_pct": 25, "rush_fum": 0},
        {"player": "Ameer Abdullah", "rush_yds": 40, "att": 8, "td": 1, "20+": 0, "40+": 0, "lng": 14, "rush_1st": 3, "rush_1st_pct": 37.5, "rush_fum": 0},
        {"player": "Jake Browning", "rush_yds": 39, "att": 9, "td": 1, "20+": 0, "40+": 0, "lng": 13, "rush_1st": 5, "rush_1st_pct": 55.6, "rush_fum": 0},
        {"player": "Julius Chestnut", "rush_yds": 39, "att": 10, "td": 0, "20+": 1, "40+": 0, "lng": 27, "rush_1st": 3, "rush_1st_pct": 30, "rush_fum": 0},
        {"player": "Brock Purdy", "rush_yds": 39, "att": 14, "td": 0, "20+": 0, "40+": 0, "lng": 11, "rush_1st": 6, "rush_1st_pct": 42.9, "rush_fum": 0},
        {"player": "Tua Tagovailoa", "rush_yds": 38, "att": 14, "td": 0, "20+": 0, "40+": 0, "lng": 8, "rush_1st": 1, "rush_1st_pct": 7.1, "rush_fum": 4},
        {"player": "Bralen Trice", "rush_yds": 37, "att": 5, "td": 1, "20+": 1, "40+": 0, "lng": 22, "rush_1st": 2, "rush_1st_pct": 40, "rush_fum": 0},
        {"player": "Jaxon Smith-Njigba", "rush_yds": 37, "att": 6, "td": 0, "20+": 0, "40+": 0, "lng": 11, "rush_1st": 2, "rush_1st_pct": 33.3, "rush_fum": 0},
        {"player": "DJ Tucker", "rush_yds": 36, "att": 6, "td": 0, "20+": 0, "40+": 0, "lng": 9, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Bo Melton", "rush_yds": 35, "att": 4, "td": 0, "20+": 0, "40+": 0, "lng": 17, "rush_1st": 2, "rush_1st_pct": 50, "rush_fum": 0},

        # Screenshot 7
        {"player": "Tyler Shough", "rush_yds": 33, "att": 15, "td": 0, "20+": 0, "40+": 0, "lng": 11, "rush_1st": 3, "rush_1st_pct": 20, "rush_fum": 1},
        {"player": "Rashid Shaheed", "rush_yds": 32, "att": 6, "td": 0, "20+": 0, "40+": 0, "lng": 10, "rush_1st": 2, "rush_1st_pct": 33.3, "rush_fum": 0},
        {"player": "Chris Brooks", "rush_yds": 31, "att": 11, "td": 0, "20+": 0, "40+": 0, "lng": 10, "rush_1st": 2, "rush_1st_pct": 18.2, "rush_fum": 0},
        {"player": "Joe Flacco", "rush_yds": 31, "att": 16, "td": 1, "20+": 0, "40+": 0, "lng": 13, "rush_1st": 7, "rush_1st_pct": 43.8, "rush_fum": 0},
        {"player": "Hassan Haskins", "rush_yds": 30, "att": 12, "td": 0, "20+": 0, "40+": 0, "lng": 10, "rush_1st": 2, "rush_1st_pct": 16.7, "rush_fum": 0},
        {"player": "Isaiah Williams", "rush_yds": 29, "att": 2, "td": 0, "20+": 1, "40+": 0, "lng": 25, "rush_1st": 1, "rush_1st_pct": 50, "rush_fum": 0},
        {"player": "Tahj Brooks", "rush_yds": 28, "att": 9, "td": 0, "20+": 0, "40+": 0, "lng": 7, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Savion Williams", "rush_yds": 28, "att": 9, "td": 0, "20+": 0, "40+": 0, "lng": 16, "rush_1st": 1, "rush_1st_pct": 11.1, "rush_fum": 1},
        {"player": "Dyami Brown", "rush_yds": 26, "att": 5, "td": 0, "20+": 0, "40+": 0, "lng": 9, "rush_1st": 2, "rush_1st_pct": 40, "rush_fum": 0},
        {"player": "Dameon Pierce", "rush_yds": 26, "att": 10, "td": 0, "20+": 0, "40+": 0, "lng": 10, "rush_1st": 1, "rush_1st_pct": 10, "rush_fum": 0},
        {"player": "Aaron Rodgers", "rush_yds": 26, "att": 14, "td": 0, "20+": 0, "40+": 0, "lng": 10, "rush_1st": 2, "rush_1st_pct": 14.3, "rush_fum": 1},
        {"player": "Ryan Flournoy", "rush_yds": 25, "att": 4, "td": 0, "20+": 0, "40+": 0, "lng": 12, "rush_1st": 2, "rush_1st_pct": 50, "rush_fum": 0},
        {"player": "Zamir White", "rush_yds": 25, "att": 10, "td": 0, "20+": 0, "40+": 0, "lng": 9, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Olamide Zaccheaus", "rush_yds": 25, "att": 4, "td": 0, "20+": 0, "40+": 0, "lng": 12, "rush_1st": 1, "rush_1st_pct": 25, "rush_fum": 0},
        {"player": "Elijah Moore", "rush_yds": 24, "att": 6, "td": 1, "20+": 0, "40+": 0, "lng": 11, "rush_1st": 3, "rush_1st_pct": 50, "rush_fum": 0},
        {"player": "Jameis Winston", "rush_yds": 23, "att": 7, "td": 1, "20+": 0, "40+": 0, "lng": 11, "rush_1st": 3, "rush_1st_pct": 42.9, "rush_fum": 0},
        {"player": "Luther Burden III", "rush_yds": 21, "att": 3, "td": 0, "20+": 0, "40+": 0, "lng": 15, "rush_1st": 2, "rush_1st_pct": 66.7, "rush_fum": 0},
        {"player": "Rashee Rice", "rush_yds": 20, "att": 5, "td": 1, "20+": 0, "40+": 0, "lng": 7, "rush_1st": 2, "rush_1st_pct": 40, "rush_fum": 1},
        {"player": "Michael Warren II", "rush_yds": 20, "att": 5, "td": 0, "20+": 0, "40+": 0, "lng": 10, "rush_1st": 1, "rush_1st_pct": 20, "rush_fum": 0},
        {"player": "Cam Akers", "rush_yds": 19, "att": 5, "td": 0, "20+": 0, "40+": 0, "lng": 14, "rush_1st": 1, "rush_1st_pct": 20, "rush_fum": 0},
        {"player": "Jaleel McLaughlin", "rush_yds": 19, "att": 7, "td": 1, "20+": 0, "40+": 0, "lng": 5, "rush_1st": 2, "rush_1st_pct": 28.6, "rush_fum": 0},
        {"player": "Khalif Raymond", "rush_yds": 19, "att": 2, "td": 0, "20+": 0, "40+": 0, "lng": 10, "rush_1st": 1, "rush_1st_pct": 50, "rush_fum": 0},
        {"player": "Sterling Shepard", "rush_yds": 19, "att": 4, "td": 0, "20+": 0, "40+": 0, "lng": 11, "rush_1st": 1, "rush_1st_pct": 25, "rush_fum": 0},
        {"player": "Malik Willis", "rush_yds": 19, "att": 3, "td": 0, "20+": 0, "40+": 0, "lng": 16, "rush_1st": 2, "rush_1st_pct": 66.7, "rush_fum": 0},
        {"player": "Dare Ogunbowale", "rush_yds": 18, "att": 3, "td": 0, "20+": 0, "40+": 0, "lng": 9, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},

        # Screenshot 8
        {"player": "Isaiah Bond", "rush_yds": 17, "att": 2, "td": 0, "20+": 0, "40+": 0, "lng": 9, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Dylan Drummond", "rush_yds": 17, "att": 8, "td": 0, "20+": 0, "40+": 0, "lng": 9, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Roschon Johnson", "rush_yds": 17, "att": 2, "td": 0, "20+": 0, "40+": 0, "lng": 11, "rush_1st": 1, "rush_1st_pct": 50, "rush_fum": 0},
        {"player": "Tez Johnson", "rush_yds": 17, "att": 6, "td": 0, "20+": 0, "40+": 0, "lng": 6, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Adam Prentice", "rush_yds": 17, "att": 4, "td": 0, "20+": 0, "40+": 0, "lng": 8, "rush_1st": 3, "rush_1st_pct": 75, "rush_fum": 0},
        {"player": "Jonnu Smith", "rush_yds": 17, "att": 3, "td": 0, "20+": 0, "40+": 0, "lng": 10, "rush_1st": 1, "rush_1st_pct": 33.3, "rush_fum": 0},
        {"player": "Jordan Addison", "rush_yds": 16, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 16, "rush_1st": 1, "rush_1st_pct": 100, "rush_fum": 0},
        {"player": "DeMario Douglas", "rush_yds": 16, "att": 6, "td": 0, "20+": 0, "40+": 0, "lng": 14, "rush_1st": 2, "rush_1st_pct": 33.3, "rush_fum": 0},
        {"player": "Brian Thomas Jr.", "rush_yds": 16, "att": 2, "td": 1, "20+": 0, "40+": 0, "lng": 9, "rush_1st": 2, "rush_1st_pct": 100, "rush_fum": 0},
        {"player": "British Brooks", "rush_yds": 15, "att": 4, "td": 0, "20+": 0, "40+": 0, "lng": 9, "rush_1st": 2, "rush_1st_pct": 50, "rush_fum": 0},
        {"player": "Greg Dortch", "rush_yds": 15, "att": 7, "td": 1, "20+": 0, "40+": 0, "lng": 9, "rush_1st": 1, "rush_1st_pct": 14.3, "rush_fum": 0},
        {"player": "Jalen Nailor", "rush_yds": 15, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 15, "rush_1st": 1, "rush_1st_pct": 100, "rush_fum": 0},
        {"player": "Shedeur Sanders", "rush_yds": 15, "att": 4, "td": 0, "20+": 0, "40+": 0, "lng": 6, "rush_1st": 1, "rush_1st_pct": 25, "rush_fum": 0},
        {"player": "Xavier Hutchinson", "rush_yds": 14, "att": 2, "td": 0, "20+": 0, "40+": 0, "lng": 9, "rush_1st": 1, "rush_1st_pct": 50, "rush_fum": 0},
        {"player": "Andrei Iosivas", "rush_yds": 14, "att": 3, "td": 0, "20+": 0, "40+": 0, "lng": 5, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Clyde Edwards-Helaire", "rush_yds": 13, "att": 7, "td": 0, "20+": 0, "40+": 0, "lng": 7, "rush_1st": 1, "rush_1st_pct": 14.3, "rush_fum": 0},
        {"player": "Eric Wilson II", "rush_yds": 13, "att": 2, "td": 0, "20+": 0, "40+": 0, "lng": 11, "rush_1st": 1, "rush_1st_pct": 50, "rush_fum": 0},
        {"player": "Hunter Luepke", "rush_yds": 13, "att": 3, "td": 0, "20+": 0, "40+": 0, "lng": 6, "rush_1st": 2, "rush_1st_pct": 66.7, "rush_fum": 0},
        {"player": "Tyler Goodson", "rush_yds": 12, "att": 5, "td": 0, "20+": 0, "40+": 0, "lng": 4, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Trey Lance", "rush_yds": 12, "att": 4, "td": 0, "20+": 0, "40+": 0, "lng": 11, "rush_1st": 1, "rush_1st_pct": 25, "rush_fum": 0},
        {"player": "DK Metcalf", "rush_yds": 12, "att": 2, "td": 1, "20+": 0, "40+": 0, "lng": 6, "rush_1st": 1, "rush_1st_pct": 50, "rush_fum": 0},
        {"player": "David Moore", "rush_yds": 12, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 12, "rush_1st": 1, "rush_1st_pct": 100, "rush_fum": 0},
        {"player": "Jordan Whittington", "rush_yds": 12, "att": 3, "td": 0, "20+": 0, "40+": 0, "lng": 6, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "AJ Barner", "rush_yds": 11, "att": 8, "td": 1, "20+": 0, "40+": 0, "lng": 2, "rush_1st": 7, "rush_1st_pct": 87.5, "rush_fum": 0},
        {"player": "Nikko Remigio", "rush_yds": 11, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 11, "rush_1st": 1, "rush_1st_pct": 100, "rush_fum": 0},

        # Screenshot 9
        {"player": "DeShone Kizer", "rush_yds": 11, "att": 2, "td": 0, "20+": 0, "40+": 0, "lng": 9, "rush_1st": 1, "rush_1st_pct": 50, "rush_fum": 0},
        {"player": "Arian Smith", "rush_yds": 11, "att": 3, "td": 0, "20+": 0, "40+": 0, "lng": 13, "rush_1st": 1, "rush_1st_pct": 33.3, "rush_fum": 0},
        {"player": "Darius Slayton", "rush_yds": 11, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 11, "rush_1st": 1, "rush_1st_pct": 100, "rush_fum": 0},
        {"player": "Jeremiah Williams", "rush_yds": 11, "att": 4, "td": 0, "20+": 0, "40+": 0, "lng": 4, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Garrett Wilson", "rush_yds": 10, "att": 4, "td": 0, "20+": 0, "40+": 0, "lng": 4, "rush_1st": 1, "rush_1st_pct": 25, "rush_fum": 0},
        {"player": "Tyler Badie", "rush_yds": 9, "att": 2, "td": 0, "20+": 0, "40+": 0, "lng": 6, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Kirk Cousins", "rush_yds": 9, "att": 5, "td": 0, "20+": 0, "40+": 0, "lng": 6, "rush_1st": 2, "rush_1st_pct": 40, "rush_fum": 0},
        {"player": "Emeka Egbuka", "rush_yds": 9, "att": 2, "td": 0, "20+": 0, "40+": 0, "lng": 9, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Troy Franklin", "rush_yds": 9, "att": 4, "td": 0, "20+": 0, "40+": 0, "lng": 11, "rush_1st": 2, "rush_1st_pct": 50, "rush_fum": 0},
        {"player": "Connor Heyward", "rush_yds": 9, "att": 5, "td": 0, "20+": 0, "40+": 0, "lng": 4, "rush_1st": 4, "rush_1st_pct": 80, "rush_fum": 0},
        {"player": "Alec Ingold", "rush_yds": 9, "att": 2, "td": 0, "20+": 0, "40+": 0, "lng": 6, "rush_1st": 1, "rush_1st_pct": 50, "rush_fum": 0},
        {"player": "Chris Moore", "rush_yds": 9, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 9, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Jaylin Noel", "rush_yds": 9, "att": 4, "td": 0, "20+": 0, "40+": 0, "lng": 5, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Amon-Ra St. Brown", "rush_yds": 9, "att": 3, "td": 0, "20+": 0, "40+": 0, "lng": 6, "rush_1st": 1, "rush_1st_pct": 33.3, "rush_fum": 0},
        {"player": "Nico Collins", "rush_yds": 8, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 8, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Aidan Johnson", "rush_yds": 8, "att": 2, "td": 0, "20+": 0, "40+": 0, "lng": 6, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Tyson Bagent", "rush_yds": 7, "att": 2, "td": 0, "20+": 0, "40+": 0, "lng": 7, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 1},
        {"player": "Evan Engram", "rush_yds": 7, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 7, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "D'Ernest Johnson", "rush_yds": 7, "att": 5, "td": 0, "20+": 0, "40+": 0, "lng": 5, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Quentin Johnston", "rush_yds": 7, "att": 2, "td": 0, "20+": 0, "40+": 0, "lng": 9, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Jordan Battle", "rush_yds": 7, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 7, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Ja'Marr Chase", "rush_yds": 6, "att": 2, "td": 0, "20+": 0, "40+": 0, "lng": 9, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Mason Rudolph", "rush_yds": 6, "att": 7, "td": 0, "20+": 0, "40+": 0, "lng": 3, "rush_1st": 2, "rush_1st_pct": 28.6, "rush_fum": 0},
        {"player": "Tyler Warren", "rush_yds": 6, "att": 4, "td": 1, "20+": 0, "40+": 0, "lng": 3, "rush_1st": 2, "rush_1st_pct": 50, "rush_fum": 0},
        {"player": "Dontayvion Wicks", "rush_yds": 6, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 6, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},

        # Screenshot 10
        {"player": "Owen Wright", "rush_yds": 6, "att": 3, "td": 0, "20+": 0, "40+": 0, "lng": 4, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Darius Davis", "rush_yds": 5, "att": 2, "td": 0, "20+": 0, "40+": 0, "lng": 3, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Dylan Laube", "rush_yds": 5, "att": 5, "td": 0, "20+": 0, "40+": 0, "lng": 2, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Khalil Shakir", "rush_yds": 5, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 5, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Parker Washington", "rush_yds": 5, "att": 6, "td": 0, "20+": 0, "40+": 0, "lng": 5, "rush_1st": 1, "rush_1st_pct": 16.7, "rush_fum": 0},
        {"player": "Jameson Williams", "rush_yds": 5, "att": 5, "td": 0, "20+": 0, "40+": 0, "lng": 9, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Teddy Bridgewater", "rush_yds": 4, "att": 3, "td": 0, "20+": 0, "40+": 0, "lng": 6, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Fabian Franks", "rush_yds": 4, "att": 2, "td": 0, "20+": 0, "40+": 0, "lng": 2, "rush_1st": 2, "rush_1st_pct": 100, "rush_fum": 0},
        {"player": "Mack Hollins", "rush_yds": 4, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 4, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Justin Jefferson", "rush_yds": 4, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 4, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Jalen Milroe", "rush_yds": 4, "att": 3, "td": 0, "20+": 0, "40+": 0, "lng": 3, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 1},
        {"player": "Craig Reynolds", "rush_yds": 4, "att": 3, "td": 0, "20+": 0, "40+": 0, "lng": 3, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Sione Vaki", "rush_yds": 4, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 4, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Tucker Kraft", "rush_yds": 3, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 3, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Gage Larvadain", "rush_yds": 3, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 3, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Patrick Ricard", "rush_yds": 3, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 3, "rush_1st": 1, "rush_1st_pct": 100, "rush_fum": 0},
        {"player": "Drew Sample", "rush_yds": 3, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 3, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Trevon Sanders", "rush_yds": 3, "att": 3, "td": 1, "20+": 0, "40+": 0, "lng": 2, "rush_1st": 2, "rush_1st_pct": 66.7, "rush_fum": 0},
        {"player": "Rashawn Thomas", "rush_yds": 3, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 3, "rush_1st": 1, "rush_1st_pct": 100, "rush_fum": 0},
        {"player": "Christian Watson", "rush_yds": 3, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 3, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Zach Wilson", "rush_yds": 3, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 3, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Brock Bowers", "rush_yds": 2, "att": 2, "td": 0, "20+": 0, "40+": 0, "lng": 6, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Tyler Conklin", "rush_yds": 2, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 2, "rush_1st": 1, "rush_1st_pct": 100, "rush_fum": 0},
        {"player": "CeeDee Lamb", "rush_yds": 2, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 2, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Kendall Milton", "rush_yds": 2, "att": 2, "td": 0, "20+": 0, "40+": 0, "lng": 2, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},

        # Screenshot 11
        {"player": "Wan'Dale Robinson", "rush_yds": 2, "att": 2, "td": 0, "20+": 0, "40+": 0, "lng": 2, "rush_1st": 1, "rush_1st_pct": 50, "rush_fum": 0},
        {"player": "Jake Ferguson", "rush_yds": 1, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 1, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Travis Kelce", "rush_yds": 1, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 1, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Riley Leonard", "rush_yds": 1, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 1, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Skyy Moore", "rush_yds": 1, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 1, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Mitchell Trubisky", "rush_yds": 1, "att": 4, "td": 0, "20+": 0, "40+": 0, "lng": 4, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Ulysses Bentley IV", "rush_yds": 0, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 0, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "DeeJay Dallas", "rush_yds": 0, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 0, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Quinn Ewers", "rush_yds": 0, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 0, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 1},
        {"player": "Terrance Ferguson", "rush_yds": 0, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 0, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "T.J. Hockenson", "rush_yds": 0, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 0, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Travis Hunter", "rush_yds": 0, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 0, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Xavier Legette", "rush_yds": 0, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 0, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Kenny Pickett", "rush_yds": 0, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 0, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 1},
        {"player": "Grant Stuard", "rush_yds": 0, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": 0, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Max Borghi", "rush_yds": -1, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": -1, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Adrian Martinez", "rush_yds": -1, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": -1, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Anthony Richardson", "rush_yds": -1, "att": 4, "td": 0, "20+": 0, "40+": 0, "lng": 2, "rush_1st": 1, "rush_1st_pct": 25, "rush_fum": 0},
        {"player": "Jarrett Stidham", "rush_yds": -1, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": -1, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Trayveon Williams", "rush_yds": -1, "att": 3, "td": 0, "20+": 0, "40+": 0, "lng": 2, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Andy Dalton", "rush_yds": -2, "att": 5, "td": 0, "20+": 0, "40+": 0, "lng": 1, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 1},
        {"player": "Nyheim Hines", "rush_yds": -2, "att": 2, "td": 0, "20+": 0, "40+": 0, "lng": 1, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Travis Homer", "rush_yds": -2, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": -2, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Tanner McKee", "rush_yds": -2, "att": 3, "td": 0, "20+": 0, "40+": 0, "lng": 0, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},

        # Screenshot 12
        {"player": "Ricky Pearsall", "rush_yds": -2, "att": 2, "td": 0, "20+": 0, "40+": 0, "lng": 2, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Kyle Williams", "rush_yds": -2, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": -2, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Kyle Allen", "rush_yds": -3, "att": 3, "td": 0, "20+": 0, "40+": 0, "lng": -1, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Jimmy Garoppolo", "rush_yds": -3, "att": 3, "td": 0, "20+": 0, "40+": 0, "lng": -1, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Kyle Juszczyk", "rush_yds": -3, "att": 2, "td": 0, "20+": 0, "40+": 0, "lng": -1, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "George Kittle", "rush_yds": -3, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": -3, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Chris Olave", "rush_yds": -3, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": -3, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Joshua Dobbs", "rush_yds": -4, "att": 5, "td": 0, "20+": 0, "40+": 0, "lng": 0, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Cooper Rush", "rush_yds": -4, "att": 4, "td": 0, "20+": 0, "40+": 0, "lng": 0, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 1},
        {"player": "Drew Lock", "rush_yds": -5, "att": 5, "td": 0, "20+": 0, "40+": 0, "lng": 0, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 1},
        {"player": "Gardner Minshew", "rush_yds": -6, "att": 5, "td": 0, "20+": 0, "40+": 0, "lng": -1, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "John Metchie III", "rush_yds": -7, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": -7, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0},
        {"player": "Matthew Stafford", "rush_yds": -9, "att": 24, "td": 0, "20+": 0, "40+": 0, "lng": 6, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 3},
        {"player": "Braden Mann", "rush_yds": -34, "att": 1, "td": 0, "20+": 0, "40+": 0, "lng": -34, "rush_1st": 0, "rush_1st_pct": 0, "rush_fum": 0}
    ]

    return rushing_stats_2025

def load_rushing_stats():
    """Load all rushing stats into Kre8VidMems"""

    # Paths
    memory_dir = Path(__file__).parent.parent / "data" / "memories"
    memory_dir.mkdir(parents=True, exist_ok=True)

    print("Extracting NFL Player Rushing Stats...")

    # Get all player data
    all_players = extract_all_rushing_stats()
    print(f"Extracted {len(all_players)} players")

    # Initialize memory
    memory = Kre8VidMemory()

    # Format the text chunks
    text_chunks = []

    # Add header chunk
    header = "NFL 2024 Season Player Rushing Statistics | running back stats | RB stats | rushing yards | rushing touchdowns | yards per carry"
    text_chunks.append(header)

    # Process each player
    for player in all_players:
        text = format_player_rushing_stats(player)
        text_chunks.append(text)

    # Load chunks into memory
    print(f"Loading {len(text_chunks)} chunks into memory...")
    for chunk in text_chunks:
        memory.add(chunk)

    # Save the memory
    memory_name = "nfl-player-rushing-stats"
    memory.save(f"{memory_dir}/{memory_name}")
    print(f"✓ Saved rushing stats to {memory_name}")

    print("\n✓ All NFL player rushing stats loaded successfully!")
    print(f"Total players: {len(all_players)}")

    # Print some interesting stats
    sorted_by_yards = sorted(all_players, key=lambda x: x['rush_yds'], reverse=True)
    print("\nTop 5 RBs by Rushing Yards:")
    for i, player in enumerate(sorted_by_yards[:5], 1):
        print(f"{i}. {player['player']}: {player['rush_yds']} yards")

    sorted_by_tds = sorted(all_players, key=lambda x: x['td'], reverse=True)
    print("\nTop 5 Players by Rushing TDs:")
    for i, player in enumerate(sorted_by_tds[:5], 1):
        print(f"{i}. {player['player']}: {player['td']} TDs")

if __name__ == "__main__":
    load_rushing_stats()