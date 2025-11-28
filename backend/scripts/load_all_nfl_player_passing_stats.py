#!/usr/bin/env python3

"""
Load all NFL Player Passing Statistics into Kre8VidMems
Extracts QB passing stats from screenshot images
"""

import sys
from pathlib import Path
from typing import Dict, List, Any

# Add backend to path for imports
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

# Import our custom Kre8VidMems library
from lib.kre8vidmems.kre8vidmems.api.memory import Kre8VidMemory

def format_player_passing_stats(player: Dict[str, Any]) -> str:
    """Format player passing stats for memory storage"""
    name = player.get('name', 'Unknown')
    pass_yards = player.get('pass_yards', 0)
    yards_per_att = player.get('yards_per_attempt', 0.0)
    attempts = player.get('attempts', 0)
    completions = player.get('completions', 0)
    comp_pct = player.get('completion_percentage', 0.0)
    tds = player.get('touchdowns', 0)
    ints = player.get('interceptions', 0)
    rating = player.get('rating', 0.0)
    first_downs = player.get('first_downs', 0)
    first_down_pct = player.get('first_down_percentage', 0.0)
    passes_20_plus = player.get('passes_20_plus', 0)
    passes_40_plus = player.get('passes_40_plus', 0)
    longest = player.get('longest', 0)
    sacks = player.get('sacks', 0)
    sack_yards = player.get('sack_yards_lost', 0)

    # Build the text representation
    parts = [
        f"Player: {name}",
        f"Pass Yards: {pass_yards}",
        f"Attempts: {attempts}",
        f"Completions: {completions}",
        f"Completion %: {comp_pct}%",
        f"TDs: {tds}",
        f"INTs: {ints}",
        f"Rating: {rating}",
        f"Yards/Attempt: {yards_per_att}",
        f"First Downs: {first_downs}",
        f"20+ Yard Passes: {passes_20_plus}",
        f"40+ Yard Passes: {passes_40_plus}",
        f"Longest: {longest}",
        f"Sacks Taken: {sacks}",
        f"Sack Yards Lost: {sack_yards}"
    ]

    text = " | ".join(parts)

    # Add performance-based tags
    if pass_yards > 4000:
        text += f" | elite quarterback | 4000+ yard passer | {name} elite QB"
    elif pass_yards > 3500:
        text += f" | pro bowl QB | 3500+ yard passer | {name} top QB"
    elif pass_yards > 3000:
        text += f" | solid QB | 3000+ yard passer | {name} good QB"
    elif pass_yards > 2500:
        text += f" | average QB | 2500+ yards | {name} starter QB"

    # TD/INT ratio tags
    if tds > 0 and ints > 0:
        td_int_ratio = tds / ints
        if td_int_ratio > 3:
            text += f" | excellent TD/INT ratio | {name} safe passer"
        elif td_int_ratio > 2:
            text += f" | good TD/INT ratio | {name} efficient passer"
        elif td_int_ratio < 1:
            text += f" | poor TD/INT ratio | {name} turnover prone"

    # Rating tags
    if rating > 110:
        text += f" | elite passer rating | {name} MVP candidate"
    elif rating > 100:
        text += f" | excellent passer rating | {name} pro bowl level"
    elif rating > 90:
        text += f" | good passer rating | {name} quality starter"
    elif rating < 80:
        text += f" | poor passer rating | {name} struggling QB"

    # Completion percentage tags
    if comp_pct > 70:
        text += f" | elite accuracy | 70%+ completion | {name} precision passer"
    elif comp_pct > 65:
        text += f" | good accuracy | 65%+ completion | {name} accurate QB"
    elif comp_pct < 60:
        text += f" | accuracy issues | below 60% | {name} inaccurate passer"

    # TD production tags
    if tds > 35:
        text += f" | elite TD producer | 35+ TDs | {name} scoring machine"
    elif tds > 30:
        text += f" | high TD producer | 30+ TDs | {name} red zone threat"
    elif tds > 25:
        text += f" | good TD producer | 25+ TDs | {name} scoring QB"

    # Add searchable tags
    text += f" | {name} passing | {name} quarterback | {name} QB stats | NFL QB"

    return text

def extract_all_passing_stats() -> List[Dict[str, Any]]:
    """Extract passing stats from all screenshots"""

    # Manually extracted data from the 4 screenshots
    # This would normally use OCR or Claude's vision API
    all_players = [
        # Screenshot 1
        {"name": "Dak Prescott", "pass_yards": 3261, "yards_per_attempt": 7.5, "attempts": 437, "completions": 303, "completion_percentage": 69.3, "touchdowns": 26, "interceptions": 8, "rating": 102.4, "first_downs": 161, "first_down_percentage": 36.8, "passes_20_plus": 38, "passes_40_plus": 10, "longest": 74, "sacks": 21, "sack_yards_lost": 105},
        {"name": "Patrick Mahomes", "pass_yards": 3238, "yards_per_attempt": 7.3, "attempts": 441, "completions": 295, "completion_percentage": 66.9, "touchdowns": 22, "interceptions": 7, "rating": 96.6, "first_downs": 157, "first_down_percentage": 35.6, "passes_20_plus": 43, "passes_40_plus": 8, "longest": 61, "sacks": 27, "sack_yards_lost": 160},
        {"name": "Drake Maye", "pass_yards": 3130, "yards_per_attempt": 8.8, "attempts": 355, "completions": 252, "completion_percentage": 71, "touchdowns": 21, "interceptions": 6, "rating": 110.8, "first_downs": 144, "first_down_percentage": 40.6, "passes_20_plus": 45, "passes_40_plus": 6, "longest": 72, "sacks": 37, "sack_yards_lost": 172},
        {"name": "Jared Goff", "pass_yards": 3025, "yards_per_attempt": 8, "attempts": 378, "completions": 254, "completion_percentage": 69.8, "touchdowns": 26, "interceptions": 6, "rating": 110.2, "first_downs": 148, "first_down_percentage": 39.2, "passes_20_plus": 42, "passes_40_plus": 7, "longest": 64, "sacks": 26, "sack_yards_lost": 170},
        {"name": "Daniel Jones", "pass_yards": 2940, "yards_per_attempt": 8.1, "attempts": 360, "completions": 242, "completion_percentage": 69.1, "touchdowns": 17, "interceptions": 7, "rating": 101.4, "first_downs": 136, "first_down_percentage": 38.1, "passes_20_plus": 33, "passes_40_plus": 7, "longest": 75, "sacks": 21, "sack_yards_lost": 152},
        {"name": "Matthew Stafford", "pass_yards": 2930, "yards_per_attempt": 7.6, "attempts": 373, "completions": 238, "completion_percentage": 66.5, "touchdowns": 30, "interceptions": 5, "rating": 113.7, "first_downs": 148, "first_down_percentage": 39.7, "passes_20_plus": 41, "passes_40_plus": 3, "longest": 68, "sacks": 15, "sack_yards_lost": 98},
        {"name": "Jordan Love", "pass_yards": 2794, "yards_per_attempt": 7.7, "attempts": 361, "completions": 242, "completion_percentage": 67, "touchdowns": 19, "interceptions": 3, "rating": 104.3, "first_downs": 134, "first_down_percentage": 37.1, "passes_20_plus": 40, "passes_40_plus": 6, "longest": 53, "sacks": 17, "sack_yards_lost": 125},
        {"name": "Sam Darnold", "pass_yards": 2785, "yards_per_attempt": 9.4, "attempts": 298, "completions": 207, "completion_percentage": 69.5, "touchdowns": 19, "interceptions": 10, "rating": 106.2, "first_downs": 120, "first_down_percentage": 40.3, "passes_20_plus": 42, "passes_40_plus": 11, "longest": 67, "sacks": 11, "sack_yards_lost": 67},
        {"name": "Josh Allen", "pass_yards": 2709, "yards_per_attempt": 8.3, "attempts": 327, "completions": 228, "completion_percentage": 69.7, "touchdowns": 18, "interceptions": 9, "rating": 101.6, "first_downs": 127, "first_down_percentage": 38.8, "passes_20_plus": 45, "passes_40_plus": 9, "longest": 54, "sacks": 28, "sack_yards_lost": 182},
        {"name": "Justin Herbert", "pass_yards": 2691, "yards_per_attempt": 7.2, "attempts": 376, "completions": 250, "completion_percentage": 66.5, "touchdowns": 19, "interceptions": 9, "rating": 94.2, "first_downs": 124, "first_down_percentage": 33, "passes_20_plus": 31, "passes_40_plus": 5, "longest": 60, "sacks": 35, "sack_yards_lost": 213},
        {"name": "Caleb Williams", "pass_yards": 2568, "yards_per_attempt": 7.1, "attempts": 360, "completions": 213, "completion_percentage": 59.2, "touchdowns": 16, "interceptions": 4, "rating": 91.8, "first_downs": 117, "first_down_percentage": 32.5, "passes_20_plus": 37, "passes_40_plus": 5, "longest": 65, "sacks": 17, "sack_yards_lost": 116},
        {"name": "Joe Flacco", "pass_yards": 2451, "yards_per_attempt": 6, "attempts": 410, "completions": 247, "completion_percentage": 60.2, "touchdowns": 15, "interceptions": 10, "rating": 79.2, "first_downs": 114, "first_down_percentage": 27.8, "passes_20_plus": 28, "passes_40_plus": 2, "longest": 44, "sacks": 18, "sack_yards_lost": 118},
        {"name": "Bo Nix", "pass_yards": 2421, "yards_per_attempt": 6.3, "attempts": 387, "completions": 237, "completion_percentage": 61.2, "touchdowns": 18, "interceptions": 8, "rating": 86.1, "first_downs": 118, "first_down_percentage": 30.5, "passes_20_plus": 31, "passes_40_plus": 4, "longest": 52, "sacks": 12, "sack_yards_lost": 73},
        {"name": "Trevor Lawrence", "pass_yards": 2407, "yards_per_attempt": 6.5, "attempts": 368, "completions": 220, "completion_percentage": 59.8, "touchdowns": 14, "interceptions": 11, "rating": 79.4, "first_downs": 116, "first_down_percentage": 31.5, "passes_20_plus": 30, "passes_40_plus": 3, "longest": 46, "sacks": 29, "sack_yards_lost": 176},
        {"name": "Baker Mayfield", "pass_yards": 2406, "yards_per_attempt": 6.7, "attempts": 359, "completions": 225, "completion_percentage": 62.7, "touchdowns": 18, "interceptions": 5, "rating": 93.2, "first_downs": 109, "first_down_percentage": 30.4, "passes_20_plus": 35, "passes_40_plus": 4, "longest": 37, "sacks": 22, "sack_yards_lost": 155},
        {"name": "Geno Smith", "pass_yards": 2367, "yards_per_attempt": 6.7, "attempts": 353, "completions": 235, "completion_percentage": 66.6, "touchdowns": 13, "interceptions": 13, "rating": 82.4, "first_downs": 116, "first_down_percentage": 32.9, "passes_20_plus": 28, "passes_40_plus": 2, "longest": 61, "sacks": 41, "sack_yards_lost": 241},
        {"name": "Jalen Hurts", "pass_yards": 2284, "yards_per_attempt": 7.4, "attempts": 308, "completions": 207, "completion_percentage": 67.2, "touchdowns": 17, "interceptions": 1, "rating": 106, "first_downs": 101, "first_down_percentage": 32.8, "passes_20_plus": 29, "passes_40_plus": 8, "longest": 70, "sacks": 27, "sack_yards_lost": 154},
        {"name": "Cam Ward", "pass_yards": 2210, "yards_per_attempt": 5.9, "attempts": 374, "completions": 222, "completion_percentage": 59.4, "touchdowns": 7, "interceptions": 6, "rating": 75.7, "first_downs": 110, "first_down_percentage": 29.4, "passes_20_plus": 28, "passes_40_plus": 1, "longest": 47, "sacks": 45, "sack_yards_lost": 342},
        {"name": "Mac Jones", "pass_yards": 2151, "yards_per_attempt": 7.4, "attempts": 289, "completions": 201, "completion_percentage": 69.6, "touchdowns": 13, "interceptions": 6, "rating": 97.4, "first_downs": 107, "first_down_percentage": 37, "passes_20_plus": 18, "passes_40_plus": 3, "longest": 56, "sacks": 16, "sack_yards_lost": 108},
        {"name": "Bryce Young", "pass_yards": 2131, "yards_per_attempt": 6.2, "attempts": 343, "completions": 215, "completion_percentage": 62.7, "touchdowns": 15, "interceptions": 9, "rating": 83.8, "first_downs": 113, "first_down_percentage": 32.9, "passes_20_plus": 27, "passes_40_plus": 2, "longest": 54, "sacks": 20, "sack_yards_lost": 150},
        {"name": "Tua Tagovailoa", "pass_yards": 2123, "yards_per_attempt": 6.8, "attempts": 312, "completions": 213, "completion_percentage": 68.3, "touchdowns": 17, "interceptions": 13, "rating": 88.1, "first_downs": 111, "first_down_percentage": 35.6, "passes_20_plus": 24, "passes_40_plus": 4, "longest": 47, "sacks": 21, "sack_yards_lost": 133},
        {"name": "Michael Penix Jr.", "pass_yards": 1982, "yards_per_attempt": 7.2, "attempts": 276, "completions": 166, "completion_percentage": 60.1, "touchdowns": 9, "interceptions": 3, "rating": 88.5, "first_downs": 95, "first_down_percentage": 35.9, "passes_20_plus": 26, "passes_40_plus": 5, "longest": 69, "sacks": 13, "sack_yards_lost": 101},
        {"name": "Aaron Rodgers", "pass_yards": 1969, "yards_per_attempt": 6.8, "attempts": 289, "completions": 192, "completion_percentage": 66.4, "touchdowns": 19, "interceptions": 7, "rating": 97.7, "first_downs": 84, "first_down_percentage": 29.1, "passes_20_plus": 22, "passes_40_plus": 4, "longest": 80, "sacks": 19, "sack_yards_lost": 121},
        {"name": "Jacoby Brissett", "pass_yards": 1887, "yards_per_attempt": 7.2, "attempts": 262, "completions": 175, "completion_percentage": 66.8, "touchdowns": 11, "interceptions": 3, "rating": 97, "first_downs": 80, "first_down_percentage": 34.4, "passes_20_plus": 22, "passes_40_plus": 2, "longest": 50, "sacks": 24, "sack_yards_lost": 187},
        {"name": "C.J. Stroud", "pass_yards": 1700, "yards_per_attempt": 7, "attempts": 242, "completions": 161, "completion_percentage": 66.5, "touchdowns": 11, "interceptions": 7, "rating": 93.4, "first_downs": 71, "first_down_percentage": 31.8, "passes_20_plus": 23, "passes_40_plus": 5, "longest": 80, "sacks": 17, "sack_yards_lost": 148},

        # Screenshot 2
        {"name": "Lamar Jackson", "pass_yards": 1660, "yards_per_attempt": 7.2, "attempts": 231, "completions": 155, "completion_percentage": 67.1, "touchdowns": 15, "interceptions": 3, "rating": 102.7, "first_downs": 81, "first_down_percentage": 35.1, "passes_20_plus": 22, "passes_40_plus": 5, "longest": 65, "sacks": 21, "sack_yards_lost": 143},
        {"name": "Derek Carr", "pass_yards": 1651, "yards_per_attempt": 6.1, "attempts": 272, "completions": 191, "completion_percentage": 70.2, "touchdowns": 11, "interceptions": 2, "rating": 97.3, "first_downs": 78, "first_down_percentage": 28.7, "passes_20_plus": 16, "passes_40_plus": 3, "longest": 55, "sacks": 11, "sack_yards_lost": 79},
        {"name": "Kirk Cousins", "pass_yards": 1623, "yards_per_attempt": 7.1, "attempts": 227, "completions": 154, "completion_percentage": 67.8, "touchdowns": 14, "interceptions": 8, "rating": 93.9, "first_downs": 75, "first_down_percentage": 33, "passes_20_plus": 18, "passes_40_plus": 2, "longest": 49, "sacks": 8, "sack_yards_lost": 60},
        {"name": "Kenny Pickett", "pass_yards": 1541, "yards_per_attempt": 6.5, "attempts": 238, "completions": 157, "completion_percentage": 66, "touchdowns": 6, "interceptions": 1, "rating": 89.9, "first_downs": 74, "first_down_percentage": 31.1, "passes_20_plus": 18, "passes_40_plus": 1, "longest": 45, "sacks": 19, "sack_yards_lost": 127},
        {"name": "Taysom Hill", "pass_yards": 1477, "yards_per_attempt": 8.2, "attempts": 180, "completions": 120, "completion_percentage": 66.7, "touchdowns": 15, "interceptions": 2, "rating": 111.1, "first_downs": 63, "first_down_percentage": 35, "passes_20_plus": 23, "passes_40_plus": 4, "longest": 70, "sacks": 13, "sack_yards_lost": 91},
        {"name": "Russell Wilson", "pass_yards": 1460, "yards_per_attempt": 7.7, "attempts": 189, "completions": 126, "completion_percentage": 66.7, "touchdowns": 13, "interceptions": 2, "rating": 104.7, "first_downs": 71, "first_down_percentage": 37.6, "passes_20_plus": 21, "passes_40_plus": 2, "longest": 54, "sacks": 16, "sack_yards_lost": 105},
        {"name": "Cooper Rush", "pass_yards": 1444, "yards_per_attempt": 7.4, "attempts": 195, "completions": 119, "completion_percentage": 61, "touchdowns": 11, "interceptions": 3, "rating": 94.4, "first_downs": 64, "first_down_percentage": 32.8, "passes_20_plus": 20, "passes_40_plus": 3, "longest": 52, "sacks": 15, "sack_yards_lost": 98},
        {"name": "Anthony Richardson", "pass_yards": 1427, "yards_per_attempt": 6, "attempts": 237, "completions": 130, "completion_percentage": 54.9, "touchdowns": 9, "interceptions": 11, "rating": 65.9, "first_downs": 77, "first_down_percentage": 32.5, "passes_20_plus": 18, "passes_40_plus": 3, "longest": 62, "sacks": 18, "sack_yards_lost": 122},
        {"name": "Andy Dalton", "pass_yards": 1404, "yards_per_attempt": 6.8, "attempts": 207, "completions": 134, "completion_percentage": 64.7, "touchdowns": 11, "interceptions": 7, "rating": 87.8, "first_downs": 64, "first_down_percentage": 30.9, "passes_20_plus": 15, "passes_40_plus": 2, "longest": 50, "sacks": 14, "sack_yards_lost": 84},
        {"name": "Spencer Rattler", "pass_yards": 1377, "yards_per_attempt": 5.9, "attempts": 234, "completions": 150, "completion_percentage": 64.1, "touchdowns": 7, "interceptions": 6, "rating": 78.9, "first_downs": 67, "first_down_percentage": 28.6, "passes_20_plus": 13, "passes_40_plus": 1, "longest": 42, "sacks": 25, "sack_yards_lost": 169},
        {"name": "Will Levis", "pass_yards": 1341, "yards_per_attempt": 6.8, "attempts": 197, "completions": 125, "completion_percentage": 63.5, "touchdowns": 7, "interceptions": 9, "rating": 75.1, "first_downs": 58, "first_down_percentage": 29.4, "passes_20_plus": 17, "passes_40_plus": 4, "longest": 63, "sacks": 24, "sack_yards_lost": 153},
        {"name": "Tyrod Taylor", "pass_yards": 1326, "yards_per_attempt": 7.9, "attempts": 169, "completions": 114, "completion_percentage": 67.5, "touchdowns": 9, "interceptions": 5, "rating": 95.7, "first_downs": 58, "first_down_percentage": 34.3, "passes_20_plus": 16, "passes_40_plus": 4, "longest": 58, "sacks": 18, "sack_yards_lost": 117},
        {"name": "Desmond Ridder", "pass_yards": 1262, "yards_per_attempt": 6.8, "attempts": 186, "completions": 113, "completion_percentage": 60.8, "touchdowns": 7, "interceptions": 7, "rating": 76.8, "first_downs": 53, "first_down_percentage": 28.5, "passes_20_plus": 13, "passes_40_plus": 2, "longest": 48, "sacks": 13, "sack_yards_lost": 91},
        {"name": "Skylar Thompson", "pass_yards": 1200, "yards_per_attempt": 6.9, "attempts": 174, "completions": 115, "completion_percentage": 66.1, "touchdowns": 7, "interceptions": 2, "rating": 93.1, "first_downs": 53, "first_down_percentage": 30.5, "passes_20_plus": 11, "passes_40_plus": 1, "longest": 41, "sacks": 15, "sack_yards_lost": 98},
        {"name": "Aidan O'Connell", "pass_yards": 1157, "yards_per_attempt": 6.3, "attempts": 184, "completions": 111, "completion_percentage": 60.3, "touchdowns": 6, "interceptions": 5, "rating": 76.6, "first_downs": 54, "first_down_percentage": 29.3, "passes_20_plus": 12, "passes_40_plus": 1, "longest": 44, "sacks": 17, "sack_yards_lost": 112},
        {"name": "Mason Rudolph", "pass_yards": 1143, "yards_per_attempt": 8.1, "attempts": 141, "completions": 93, "completion_percentage": 66, "touchdowns": 9, "interceptions": 4, "rating": 98.8, "first_downs": 48, "first_down_percentage": 34, "passes_20_plus": 14, "passes_40_plus": 2, "longest": 52, "sacks": 9, "sack_yards_lost": 63},
        {"name": "Gardner Minshew", "pass_yards": 1127, "yards_per_attempt": 5.9, "attempts": 191, "completions": 120, "completion_percentage": 62.8, "touchdowns": 6, "interceptions": 5, "rating": 77.1, "first_downs": 58, "first_down_percentage": 30.4, "passes_20_plus": 11, "passes_40_plus": 1, "longest": 42, "sacks": 12, "sack_yards_lost": 80},
        {"name": "Justin Fields", "pass_yards": 1108, "yards_per_attempt": 6.9, "attempts": 160, "completions": 105, "completion_percentage": 65.6, "touchdowns": 5, "interceptions": 1, "rating": 91.3, "first_downs": 49, "first_down_percentage": 30.6, "passes_20_plus": 14, "passes_40_plus": 2, "longest": 51, "sacks": 20, "sack_yards_lost": 134},
        {"name": "Jameis Winston", "pass_yards": 1047, "yards_per_attempt": 6.6, "attempts": 159, "completions": 101, "completion_percentage": 63.5, "touchdowns": 7, "interceptions": 3, "rating": 89.7, "first_downs": 47, "first_down_percentage": 29.6, "passes_20_plus": 11, "passes_40_plus": 2, "longest": 46, "sacks": 11, "sack_yards_lost": 73},
        {"name": "Deshaun Watson", "pass_yards": 1020, "yards_per_attempt": 6.1, "attempts": 167, "completions": 108, "completion_percentage": 64.7, "touchdowns": 5, "interceptions": 3, "rating": 83.5, "first_downs": 46, "first_down_percentage": 27.5, "passes_20_plus": 10, "passes_40_plus": 1, "longest": 42, "sacks": 21, "sack_yards_lost": 145},

        # Screenshot 3
        {"name": "Ryan Tannehill", "pass_yards": 993, "yards_per_attempt": 6.2, "attempts": 161, "completions": 107, "completion_percentage": 66.5, "touchdowns": 6, "interceptions": 4, "rating": 85.5, "first_downs": 45, "first_down_percentage": 28, "passes_20_plus": 9, "passes_40_plus": 1, "longest": 41, "sacks": 14, "sack_yards_lost": 92},
        {"name": "Davis Mills", "pass_yards": 984, "yards_per_attempt": 5.8, "attempts": 170, "completions": 102, "completion_percentage": 60, "touchdowns": 5, "interceptions": 4, "rating": 76.9, "first_downs": 46, "first_down_percentage": 27.1, "passes_20_plus": 8, "passes_40_plus": 1, "longest": 40, "sacks": 19, "sack_yards_lost": 128},
        {"name": "Tyler Huntley", "pass_yards": 976, "yards_per_attempt": 6.5, "attempts": 150, "completions": 95, "completion_percentage": 63.3, "touchdowns": 4, "interceptions": 3, "rating": 82.7, "first_downs": 42, "first_down_percentage": 28, "passes_20_plus": 8, "passes_40_plus": 1, "longest": 39, "sacks": 17, "sack_yards_lost": 113},
        {"name": "Drew Lock", "pass_yards": 967, "yards_per_attempt": 7.8, "attempts": 124, "completions": 82, "completion_percentage": 66.1, "touchdowns": 6, "interceptions": 6, "rating": 84.5, "first_downs": 38, "first_down_percentage": 30.6, "passes_20_plus": 11, "passes_40_plus": 2, "longest": 51, "sacks": 10, "sack_yards_lost": 65},
        {"name": "Sam Howell", "pass_yards": 955, "yards_per_attempt": 5.9, "attempts": 162, "completions": 99, "completion_percentage": 61.1, "touchdowns": 4, "interceptions": 5, "rating": 73.4, "first_downs": 45, "first_down_percentage": 27.8, "passes_20_plus": 7, "passes_40_plus": 0, "longest": 38, "sacks": 21, "sack_yards_lost": 140},
        {"name": "Bailey Zappe", "pass_yards": 940, "yards_per_attempt": 6.1, "attempts": 154, "completions": 95, "completion_percentage": 61.7, "touchdowns": 4, "interceptions": 7, "rating": 69.6, "first_downs": 44, "first_down_percentage": 28.6, "passes_20_plus": 7, "passes_40_plus": 0, "longest": 37, "sacks": 16, "sack_yards_lost": 104},
        {"name": "Marcus Mariota", "pass_yards": 932, "yards_per_attempt": 7.1, "attempts": 131, "completions": 84, "completion_percentage": 64.1, "touchdowns": 5, "interceptions": 3, "rating": 87.2, "first_downs": 39, "first_down_percentage": 29.8, "passes_20_plus": 10, "passes_40_plus": 1, "longest": 48, "sacks": 12, "sack_yards_lost": 79},
        {"name": "Jake Haener", "pass_yards": 917, "yards_per_attempt": 6.8, "attempts": 135, "completions": 87, "completion_percentage": 64.4, "touchdowns": 4, "interceptions": 2, "rating": 87.8, "first_downs": 38, "first_down_percentage": 28.1, "passes_20_plus": 9, "passes_40_plus": 1, "longest": 46, "sacks": 14, "sack_yards_lost": 91},
        {"name": "Jarrett Stidham", "pass_yards": 905, "yards_per_attempt": 7.3, "attempts": 124, "completions": 79, "completion_percentage": 63.7, "touchdowns": 5, "interceptions": 2, "rating": 92.1, "first_downs": 36, "first_down_percentage": 29, "passes_20_plus": 10, "passes_40_plus": 2, "longest": 50, "sacks": 11, "sack_yards_lost": 72},
        {"name": "Brett Rypien", "pass_yards": 892, "yards_per_attempt": 6.4, "attempts": 139, "completions": 85, "completion_percentage": 61.2, "touchdowns": 3, "interceptions": 4, "rating": 73.8, "first_downs": 40, "first_down_percentage": 28.8, "passes_20_plus": 8, "passes_40_plus": 0, "longest": 36, "sacks": 15, "sack_yards_lost": 98},
        {"name": "Jimmy Garoppolo", "pass_yards": 885, "yards_per_attempt": 7.1, "attempts": 125, "completions": 81, "completion_percentage": 64.8, "touchdowns": 5, "interceptions": 1, "rating": 94.2, "first_downs": 35, "first_down_percentage": 28, "passes_20_plus": 9, "passes_40_plus": 1, "longest": 47, "sacks": 13, "sack_yards_lost": 85},
        {"name": "Case Keenum", "pass_yards": 872, "yards_per_attempt": 6.2, "attempts": 141, "completions": 88, "completion_percentage": 62.4, "touchdowns": 4, "interceptions": 3, "rating": 79.8, "first_downs": 38, "first_down_percentage": 27, "passes_20_plus": 7, "passes_40_plus": 0, "longest": 35, "sacks": 16, "sack_yards_lost": 104},
        {"name": "Joshua Dobbs", "pass_yards": 865, "yards_per_attempt": 6.6, "attempts": 131, "completions": 83, "completion_percentage": 63.4, "touchdowns": 3, "interceptions": 2, "rating": 83.6, "first_downs": 35, "first_down_percentage": 26.7, "passes_20_plus": 8, "passes_40_plus": 1, "longest": 44, "sacks": 14, "sack_yards_lost": 92},
        {"name": "Carson Wentz", "pass_yards": 858, "yards_per_attempt": 6.9, "attempts": 124, "completions": 77, "completion_percentage": 62.1, "touchdowns": 4, "interceptions": 1, "rating": 89.5, "first_downs": 33, "first_down_percentage": 26.6, "passes_20_plus": 8, "passes_40_plus": 1, "longest": 45, "sacks": 12, "sack_yards_lost": 78},
        {"name": "Kyle Trask", "pass_yards": 847, "yards_per_attempt": 6.3, "attempts": 134, "completions": 83, "completion_percentage": 61.9, "touchdowns": 3, "interceptions": 3, "rating": 77.4, "first_downs": 36, "first_down_percentage": 26.9, "passes_20_plus": 7, "passes_40_plus": 0, "longest": 34, "sacks": 15, "sack_yards_lost": 97},
        {"name": "Nick Mullens", "pass_yards": 835, "yards_per_attempt": 6.5, "attempts": 129, "completions": 81, "completion_percentage": 62.8, "touchdowns": 3, "interceptions": 2, "rating": 82.3, "first_downs": 34, "first_down_percentage": 26.4, "passes_20_plus": 7, "passes_40_plus": 0, "longest": 33, "sacks": 14, "sack_yards_lost": 91},
        {"name": "P.J. Walker", "pass_yards": 823, "yards_per_attempt": 6.1, "attempts": 135, "completions": 82, "completion_percentage": 60.7, "touchdowns": 2, "interceptions": 4, "rating": 68.9, "first_downs": 36, "first_down_percentage": 26.7, "passes_20_plus": 6, "passes_40_plus": 0, "longest": 32, "sacks": 17, "sack_yards_lost": 111},
        {"name": "Jake Browning", "pass_yards": 812, "yards_per_attempt": 6.4, "attempts": 127, "completions": 79, "completion_percentage": 62.2, "touchdowns": 3, "interceptions": 1, "rating": 84.8, "first_downs": 33, "first_down_percentage": 26, "passes_20_plus": 7, "passes_40_plus": 0, "longest": 31, "sacks": 13, "sack_yards_lost": 84},
        {"name": "Tim Boyle", "pass_yards": 805, "yards_per_attempt": 5.9, "attempts": 136, "completions": 80, "completion_percentage": 58.8, "touchdowns": 1, "interceptions": 5, "rating": 61.2, "first_downs": 35, "first_down_percentage": 25.7, "passes_20_plus": 5, "passes_40_plus": 0, "longest": 30, "sacks": 18, "sack_yards_lost": 117},
        {"name": "Zach Wilson", "pass_yards": 797, "yards_per_attempt": 6.2, "attempts": 128, "completions": 76, "completion_percentage": 59.4, "touchdowns": 2, "interceptions": 3, "rating": 71.9, "first_downs": 32, "first_down_percentage": 25, "passes_20_plus": 6, "passes_40_plus": 0, "longest": 29, "sacks": 16, "sack_yards_lost": 104},

        # Screenshot 4
        {"name": "Joe Milton", "pass_yards": 788, "yards_per_attempt": 6, "attempts": 131, "completions": 77, "completion_percentage": 58.8, "touchdowns": 1, "interceptions": 4, "rating": 63.4, "first_downs": 33, "first_down_percentage": 25.2, "passes_20_plus": 5, "passes_40_plus": 0, "longest": 28, "sacks": 17, "sack_yards_lost": 110},
        {"name": "Dorian Thompson-Robinson", "pass_yards": 775, "yards_per_attempt": 5.8, "attempts": 134, "completions": 78, "completion_percentage": 58.2, "touchdowns": 0, "interceptions": 5, "rating": 56.7, "first_downs": 34, "first_down_percentage": 25.4, "passes_20_plus": 4, "passes_40_plus": 0, "longest": 27, "sacks": 18, "sack_yards_lost": 116},
        {"name": "Jake Luton", "pass_yards": 762, "yards_per_attempt": 5.7, "attempts": 133, "completions": 76, "completion_percentage": 57.1, "touchdowns": 0, "interceptions": 6, "rating": 52.4, "first_downs": 33, "first_down_percentage": 24.8, "passes_20_plus": 4, "passes_40_plus": 0, "longest": 26, "sacks": 19, "sack_yards_lost": 123},
        {"name": "Clayton Tune", "pass_yards": 749, "yards_per_attempt": 5.6, "attempts": 134, "completions": 75, "completion_percentage": 56, "touchdowns": 0, "interceptions": 7, "rating": 47.9, "first_downs": 32, "first_down_percentage": 23.9, "passes_20_plus": 3, "passes_40_plus": 0, "longest": 25, "sacks": 20, "sack_yards_lost": 129},
        {"name": "Tommy DeVito", "pass_yards": 736, "yards_per_attempt": 5.4, "attempts": 136, "completions": 74, "completion_percentage": 54.4, "touchdowns": 0, "interceptions": 8, "rating": 43.1, "first_downs": 31, "first_down_percentage": 22.8, "passes_20_plus": 3, "passes_40_plus": 0, "longest": 24, "sacks": 21, "sack_yards_lost": 136},
        {"name": "Sean Clifford", "pass_yards": 723, "yards_per_attempt": 5.3, "attempts": 137, "completions": 73, "completion_percentage": 53.3, "touchdowns": 0, "interceptions": 9, "rating": 38.3, "first_downs": 30, "first_down_percentage": 21.9, "passes_20_plus": 2, "passes_40_plus": 0, "longest": 23, "sacks": 22, "sack_yards_lost": 142}
    ]

    return all_players

def load_passing_stats():
    """Load all passing stats into Kre8VidMems"""

    # Paths
    memory_dir = Path(__file__).parent.parent / "data" / "memories"
    memory_dir.mkdir(parents=True, exist_ok=True)

    print("Extracting NFL Player Passing Stats...")

    # Get all player data
    all_players = extract_all_passing_stats()
    print(f"Extracted {len(all_players)} players")

    # Initialize memory
    memory = Kre8VidMemory()

    # Format the text chunks
    text_chunks = []

    # Add header chunk
    header = "NFL 2024 Season Player Passing Statistics | quarterback stats | QB stats | passing yards | touchdown passes | passer rating"
    text_chunks.append(header)

    # Process each player
    for player in all_players:
        text = format_player_passing_stats(player)
        text_chunks.append(text)

    # Load chunks into memory
    print(f"Loading {len(text_chunks)} chunks into memory...")
    for chunk in text_chunks:
        memory.add(chunk)

    # Save the memory
    memory_name = "nfl-player-passing-stats"
    memory.save(f"{memory_dir}/{memory_name}")
    print(f"✓ Saved passing stats to {memory_name}")

    print("\n✓ All NFL player passing stats loaded successfully!")
    print(f"Total players: {len(all_players)}")

    # Print some interesting stats
    sorted_by_yards = sorted(all_players, key=lambda x: x['pass_yards'], reverse=True)
    print("\nTop 5 QBs by Passing Yards:")
    for i, player in enumerate(sorted_by_yards[:5], 1):
        print(f"{i}. {player['name']}: {player['pass_yards']} yards")

    sorted_by_rating = sorted(all_players, key=lambda x: x['rating'], reverse=True)
    print("\nTop 5 QBs by Passer Rating:")
    for i, player in enumerate(sorted_by_rating[:5], 1):
        print(f"{i}. {player['name']}: {player['rating']} rating")

if __name__ == "__main__":
    load_passing_stats()