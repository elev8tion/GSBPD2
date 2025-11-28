#!/usr/bin/env python3
"""
Load NFL Player Interception Stats into Kre8VidMems Database
Extracts data from screenshots and categorizes players by performance
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from lib.kre8vidmems.kre8vidmems.api.memory import Kre8VidMemory

def get_all_player_data() -> List[Dict[str, Any]]:
    """Get all player interception data - extracted from screenshots"""

    # Complete data extracted from all 7 screenshots
    all_players = [
        # Screenshot 1 - Top interceptors (5, 4, 3 INTs)
        {"player_name": "Kevin Byard", "interceptions": 5, "int_touchdowns": 0, "int_yards": 70, "longest_int": 35},
        {"player_name": "Jaycee Horn", "interceptions": 5, "int_touchdowns": 0, "int_yards": 46, "longest_int": 22},
        {"player_name": "Nathakoa Wright", "interceptions": 5, "int_touchdowns": 1, "int_yards": 118, "longest_int": 74},
        {"player_name": "Galen Bullock", "interceptions": 4, "int_touchdowns": 0, "int_yards": 40, "longest_int": 29},
        {"player_name": "Tremaine Edmunds", "interceptions": 4, "int_touchdowns": 0, "int_yards": 10, "longest_int": 10},
        {"player_name": "Devin Lloyd", "interceptions": 4, "int_touchdowns": 1, "int_yards": 129, "longest_int": 99},
        {"player_name": "Cody Barton", "interceptions": 3, "int_touchdowns": 1, "int_yards": 25, "longest_int": 24},
        {"player_name": "Jordan Battle", "interceptions": 3, "int_touchdowns": 0, "int_yards": 6, "longest_int": 4},
        {"player_name": "Cole Bishop", "interceptions": 3, "int_touchdowns": 0, "int_yards": 16, "longest_int": 12},
        {"player_name": "Darnel Dean", "interceptions": 3, "int_touchdowns": 1, "int_yards": 74, "longest_int": 55},
        {"player_name": "Calais Durant", "interceptions": 3, "int_touchdowns": 1, "int_yards": 60, "longest_int": 50},
        {"player_name": "Emmanuel Forbes", "interceptions": 3, "int_touchdowns": 0, "int_yards": 43, "longest_int": 31},
        {"player_name": "Quinta Jackson", "interceptions": 3, "int_touchdowns": 0, "int_yards": 21, "longest_int": 21},
        {"player_name": "Ernest Jones", "interceptions": 3, "int_touchdowns": 0, "int_yards": 59, "longest_int": 29},
        {"player_name": "Marcus Jones", "interceptions": 3, "int_touchdowns": 1, "int_yards": 65, "longest_int": 33},
        {"player_name": "Kerby Joseph", "interceptions": 3, "int_touchdowns": 0, "int_yards": 1, "longest_int": 1},
        {"player_name": "Lassih Latu", "interceptions": 3, "int_touchdowns": 0, "int_yards": 9, "longest_int": 6},
        {"player_name": "Jalen Pitre", "interceptions": 3, "int_touchdowns": 0, "int_yards": 20, "longest_int": 12},
        {"player_name": "Mike Sainristil", "interceptions": 3, "int_touchdowns": 0, "int_yards": 23, "longest_int": 23},
        {"player_name": "Derek Stingley Jr.", "interceptions": 3, "int_touchdowns": 0, "int_yards": 37, "longest_int": 20},
        {"player_name": "Xavier Watts", "interceptions": 3, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Nate Wiggins", "interceptions": 3, "int_touchdowns": 0, "int_yards": 84, "longest_int": 61},
        {"player_name": "Ryan Williams", "interceptions": 3, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Jessie Bates", "interceptions": 2, "int_touchdowns": 0, "int_yards": 20, "longest_int": 17},
        {"player_name": "Maliki Blackmon", "interceptions": 2, "int_touchdowns": 0, "int_yards": 41, "longest_int": 32},

        # Screenshot 2 - 2 INTs players
        {"player_name": "Ji'Ayir Brown", "interceptions": 2, "int_touchdowns": 0, "int_yards": 4, "longest_int": 4},
        {"player_name": "Coby Bryant", "interceptions": 2, "int_touchdowns": 0, "int_yards": 43, "longest_int": 28},
        {"player_name": "Denzel Burke", "interceptions": 2, "int_touchdowns": 0, "int_yards": 4, "longest_int": 4},
        {"player_name": "Camryn Bynum", "interceptions": 2, "int_touchdowns": 0, "int_yards": 14, "longest_int": 14},
        {"player_name": "Kam Curl", "interceptions": 2, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Maxwell Hairston", "interceptions": 2, "int_touchdowns": 0, "int_yards": 1, "longest_int": 1},
        {"player_name": "Jaylinn Hawkins", "interceptions": 2, "int_touchdowns": 0, "int_yards": 1, "longest_int": 1},
        {"player_name": "Ronnie Hickman Jr.", "interceptions": 2, "int_touchdowns": 0, "int_yards": 31, "longest_int": 16},
        {"player_name": "Mike Jackson", "interceptions": 2, "int_touchdowns": 0, "int_yards": 54, "longest_int": 54},
        {"player_name": "Tony Jefferson", "interceptions": 2, "int_touchdowns": 0, "int_yards": 2, "longest_int": 2},
        {"player_name": "Antonio Johnson", "interceptions": 2, "int_touchdowns": 0, "int_yards": 44, "longest_int": 44},
        {"player_name": "Kyu Blu Kelly", "interceptions": 2, "int_touchdowns": 0, "int_yards": 26, "longest_int": 26},
        {"player_name": "Darnon Kandeck", "interceptions": 2, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Kamren Kinchens", "interceptions": 2, "int_touchdowns": 0, "int_yards": 53, "longest_int": 31},
        {"player_name": "Demetrius Knight Jr.", "interceptions": 2, "int_touchdowns": 0, "int_yards": 39, "longest_int": 39},
        {"player_name": "Kemon Lassiter", "interceptions": 2, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Commodore Lenoir", "interceptions": 2, "int_touchdowns": 0, "int_yards": 90, "longest_int": 64},
        {"player_name": "Jourdan Lewis", "interceptions": 2, "int_touchdowns": 0, "int_yards": 6, "longest_int": 6},
        {"player_name": "Xavier McKinney", "interceptions": 2, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Kool-Aid McKinstry", "interceptions": 2, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Josh Metellus", "interceptions": 2, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "B.J. Mickens", "interceptions": 2, "int_touchdowns": 0, "int_yards": 25, "longest_int": 15},
        {"player_name": "Andrew Mukuba", "interceptions": 2, "int_touchdowns": 0, "int_yards": 41, "longest_int": 41},
        {"player_name": "Andru Phillips", "interceptions": 2, "int_touchdowns": 0, "int_yards": 56, "longest_int": 56},
        {"player_name": "Isaiah Pola-Mao", "interceptions": 2, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},

        # Screenshot 3 - 2 and 1 INTs players
        {"player_name": "Keenan Schwesinger", "interceptions": 2, "int_touchdowns": 0, "int_yards": 16, "longest_int": 9},
        {"player_name": "Robert Spillane", "interceptions": 2, "int_touchdowns": 0, "int_yards": 70, "longest_int": 37},
        {"player_name": "Malaki Starks", "interceptions": 2, "int_touchdowns": 0, "int_yards": 9, "longest_int": 9},
        {"player_name": "Daron Stone", "interceptions": 2, "int_touchdowns": 1, "int_yards": 57, "longest_int": 52},
        {"player_name": "Dashon Taylor-Demerson", "interceptions": 2, "int_touchdowns": 0, "int_yards": 18, "longest_int": 18},
        {"player_name": "Domdos Tillman", "interceptions": 2, "int_touchdowns": 0, "int_yards": 59, "longest_int": 36},
        {"player_name": "DJ Turner II", "interceptions": 2, "int_touchdowns": 0, "int_yards": 7, "longest_int": 7},
        {"player_name": "Jaylen Watson", "interceptions": 2, "int_touchdowns": 0, "int_yards": 14, "longest_int": 14},
        {"player_name": "Donovan Wilson", "interceptions": 2, "int_touchdowns": 0, "int_yards": 21, "longest_int": 21},
        {"player_name": "Alex Anzalone", "interceptions": 1, "int_touchdowns": 0, "int_yards": 14, "longest_int": 14},
        {"player_name": "Terron Arnold", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Budda Baker", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Jahdae Barron", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Zack Baun", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Mathoppes Bell", "interceptions": 1, "int_touchdowns": 0, "int_yards": 24, "longest_int": 24},
        {"player_name": "Terrel Bernard", "interceptions": 1, "int_touchdowns": 0, "int_yards": 24, "longest_int": 24},
        {"player_name": "DaRon Bland", "interceptions": 1, "int_touchdowns": 1, "int_yards": 68, "longest_int": 68},
        {"player_name": "Reed Blankenship", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Billy Bowman Jr.", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Tykevius Bridges", "interceptions": 1, "int_touchdowns": 0, "int_yards": 7, "longest_int": 7},
        {"player_name": "Jaquan Brisker", "interceptions": 1, "int_touchdowns": 0, "int_yards": 32, "longest_int": 32},
        {"player_name": "Montaric Brown", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Baron Browning", "interceptions": 1, "int_touchdowns": 0, "int_yards": 4, "longest_int": 4},
        {"player_name": "Deion Bush", "interceptions": 1, "int_touchdowns": 1, "int_yards": 23, "longest_int": 23},
        {"player_name": "Shaud Campbell", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},

        # Screenshot 4 - 1 INT players
        {"player_name": "Tyson Campbell", "interceptions": 1, "int_touchdowns": 1, "int_yards": 34, "longest_int": 34},
        {"player_name": "Lan Chenal", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Jack Cochrane", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Maro Crosby", "interceptions": 1, "int_touchdowns": 0, "int_yards": 19, "longest_int": 19},
        {"player_name": "Nick Cross", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Michael Davis", "interceptions": 1, "int_touchdowns": 0, "int_yards": 10, "longest_int": 10},
        {"player_name": "Lacorrie Davis", "interceptions": 1, "int_touchdowns": 0, "int_yards": 3, "longest_int": 3},
        {"player_name": "Akeem Davis-Gaither", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Cooper DeJean", "interceptions": 1, "int_touchdowns": 0, "int_yards": 21, "longest_int": 21},
        {"player_name": "Grant Delpit", "interceptions": 1, "int_touchdowns": 0, "int_yards": 25, "longest_int": 25},
        {"player_name": "Ja'Wrcus Dennis", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Kyle Dugger", "interceptions": 1, "int_touchdowns": 1, "int_yards": 73, "longest_int": 73},
        {"player_name": "Brandin Echols", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "DeShon Elliott", "interceptions": 1, "int_touchdowns": 0, "int_yards": 4, "longest_int": 4},
        {"player_name": "Kaidon Eliss", "interceptions": 1, "int_touchdowns": 0, "int_yards": 16, "longest_int": 16},
        {"player_name": "A.J. Espensa", "interceptions": 1, "int_touchdowns": 0, "int_yards": 24, "longest_int": 24},
        {"player_name": "Minkah Fitzpatrick", "interceptions": 1, "int_touchdowns": 0, "int_yards": 7, "longest_int": 7},
        {"player_name": "Cortale Flott", "interceptions": 1, "int_touchdowns": 0, "int_yards": 68, "longest_int": 68},
        {"player_name": "Dee Alford", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Thomas Harper", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Daiyan Henley", "interceptions": 1, "int_touchdowns": 0, "int_yards": 8, "longest_int": 8},
        {"player_name": "Nick Herbig", "interceptions": 1, "int_touchdowns": 0, "int_yards": 41, "longest_int": 41},
        {"player_name": "Daxton Hill", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Jevon Holland", "interceptions": 1, "int_touchdowns": 0, "int_yards": 3, "longest_int": 3},
        {"player_name": "Marlon Humphrey", "interceptions": 1, "int_touchdowns": 0, "int_yards": 27, "longest_int": 27},

        # Screenshot 5 - 1 INT players continued
        {"player_name": "Jalyx Hunt", "interceptions": 1, "int_touchdowns": 1, "int_yards": 42, "longest_int": 42},
        {"player_name": "Darian James", "interceptions": 1, "int_touchdowns": 0, "int_yards": 21, "longest_int": 21},
        {"player_name": "Hayshawn Jenkins", "interceptions": 1, "int_touchdowns": 0, "int_yards": 9, "longest_int": 9},
        {"player_name": "Josh Jobe", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Brandon Jones", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Zack Jones", "interceptions": 1, "int_touchdowns": 0, "int_yards": 7, "longest_int": 7},
        {"player_name": "Daman Jones", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Quentin Lake", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Chris Lammons", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Marshon Lattimore", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Dexter Lawrence", "interceptions": 1, "int_touchdowns": 0, "int_yards": 37, "longest_int": 37},
        {"player_name": "DeAngelo Malone", "interceptions": 1, "int_touchdowns": 0, "int_yards": 6, "longest_int": 6},
        {"player_name": "Mario Mapu", "interceptions": 1, "int_touchdowns": 0, "int_yards": 20, "longest_int": 20},
        {"player_name": "Arthur Maulet", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Roger McCreary", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Isaiah McDuffie", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Trent McDuffie", "interceptions": 1, "int_touchdowns": 0, "int_yards": 2, "longest_int": 2},
        {"player_name": "Ja'Quan McMillian", "interceptions": 1, "int_touchdowns": 0, "int_yards": 16, "longest_int": 16},
        {"player_name": "Realu Mckimovau", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Tai'von Moehring", "interceptions": 1, "int_touchdowns": 0, "int_yards": 36, "longest_int": 36},
        {"player_name": "Kenny Moore II", "interceptions": 1, "int_touchdowns": 1, "int_yards": 32, "longest_int": 32},
        {"player_name": "Eric Murray", "interceptions": 1, "int_touchdowns": 0, "int_yards": 12, "longest_int": 12},
        {"player_name": "Malik Mustapha", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Anthony Nelson", "interceptions": 1, "int_touchdowns": 1, "int_yards": 3, "longest_int": 3},
        {"player_name": "Ty Okada", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},

        # Screenshot 6 - 1 INT players continued
        {"player_name": "Foyc Okudum", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Jacob Parish", "interceptions": 1, "int_touchdowns": 0, "int_yards": 3, "longest_int": 3},
        {"player_name": "Avery Porter Jr.", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Jaden Ramsey", "interceptions": 1, "int_touchdowns": 0, "int_yards": 2, "longest_int": 2},
        {"player_name": "D.J. Reed", "interceptions": 1, "int_touchdowns": 0, "int_yards": 34, "longest_int": 34},
        {"player_name": "Justin Reid", "interceptions": 1, "int_touchdowns": 1, "int_yards": 49, "longest_int": 49},
        {"player_name": "Quincy Riley", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Amik Robertson", "interceptions": 1, "int_touchdowns": 0, "int_yards": 2, "longest_int": 2},
        {"player_name": "Isaiah Rodgers", "interceptions": 1, "int_touchdowns": 1, "int_yards": 87, "longest_int": 87},
        {"player_name": "Christian Roland-Wallace", "interceptions": 1, "int_touchdowns": 0, "int_yards": 23, "longest_int": 23},
        {"player_name": "Jamar Seeker", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Jack Sawyer", "interceptions": 1, "int_touchdowns": 0, "int_yards": 4, "longest_int": 4},
        {"player_name": "Tyrlen Smith", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Chan Smith-Wade", "interceptions": 1, "int_touchdowns": 1, "int_yards": 11, "longest_int": 11},
        {"player_name": "Charles Snowden", "interceptions": 1, "int_touchdowns": 0, "int_yards": 18, "longest_int": 18},
        {"player_name": "Tyrque Stevenson", "interceptions": 1, "int_touchdowns": 0, "int_yards": 3, "longest_int": 3},
        {"player_name": "Oliver Stewart", "interceptions": 1, "int_touchdowns": 0, "int_yards": 3, "longest_int": 3},
        {"player_name": "Benjamin St-Juste", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Justin Strnad", "interceptions": 1, "int_touchdowns": 0, "int_yards": 21, "longest_int": 21},
        {"player_name": "T.J. Tampa", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Alontae Taylor", "interceptions": 1, "int_touchdowns": 0, "int_yards": 11, "longest_int": 11},
        {"player_name": "Kindle Vildor", "interceptions": 1, "int_touchdowns": 0, "int_yards": 13, "longest_int": 13},
        {"player_name": "Bobby Wagner", "interceptions": 1, "int_touchdowns": 0, "int_yards": 1, "longest_int": 1},
        {"player_name": "Denzal Ward", "interceptions": 1, "int_touchdowns": 0, "int_yards": 13, "longest_int": 13},
        {"player_name": "T.J. Watt", "interceptions": 1, "int_touchdowns": 0, "int_yards": 13, "longest_int": 13},

        # Screenshot 7 - Final 1 INT players
        {"player_name": "Daron White", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Darious Williams", "interceptions": 1, "int_touchdowns": 0, "int_yards": 18, "longest_int": 18},
        {"player_name": "Garrett Williams", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Mark Wilson", "interceptions": 1, "int_touchdowns": 0, "int_yards": 9, "longest_int": 9},
        {"player_name": "Payton Wilson", "interceptions": 1, "int_touchdowns": 0, "int_yards": 17, "longest_int": 17},
        {"player_name": "Antoine Winfield Jr.", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Andrew Wingard", "interceptions": 1, "int_touchdowns": 0, "int_yards": 39, "longest_int": 39},
        {"player_name": "D.J. Wonnum", "interceptions": 1, "int_touchdowns": 0, "int_yards": 0, "longest_int": 0},
        {"player_name": "Xavier Woods", "interceptions": 1, "int_touchdowns": 0, "int_yards": 16, "longest_int": 16},
    ]

    return all_players

def format_player_interceptions_stats(player: Dict[str, Any]) -> str:
    """Format player interception stats with performance tags"""

    ints = player.get('interceptions', 0)
    int_tds = player.get('int_touchdowns', 0)
    int_yards = player.get('int_yards', 0)
    longest = player.get('longest_int', 0)

    # Calculate performance level based on interceptions
    if ints >= 8:
        performance_tag = "elite"
        performance_desc = "Elite NFL Defensive Back"
    elif ints >= 5:
        performance_tag = "pro_bowl"
        performance_desc = "Pro Bowl Level Defensive Back"
    elif ints >= 3:
        performance_tag = "starter"
        performance_desc = "Starting NFL Defensive Back"
    elif ints >= 2:
        performance_tag = "contributor"
        performance_desc = "Contributing Defensive Back"
    else:
        performance_tag = "depth"
        performance_desc = "Depth Player"

    # Calculate yards per interception
    yards_per_int = round(int_yards / ints, 1) if ints > 0 else 0

    # Calculate TD rate
    td_rate = round((int_tds / ints) * 100, 1) if ints > 0 else 0

    # Build the formatted text
    text_parts = [
        f"NFL Player: {player['player_name']}",
        f"Position: Defensive Back",
        f"Performance Level: {performance_desc}",
        f"",
        f"2024 Interception Statistics:",
        f"- Interceptions: {ints}",
        f"- Interception Touchdowns: {int_tds}",
        f"- Interception Return Yards: {int_yards}",
        f"- Longest Return: {longest} yards",
        f"- Yards Per Return: {yards_per_int}",
        f"- Touchdown Rate: {td_rate}%",
        f"",
        f"Tags: #{performance_tag} #nfl #interceptions #defense #{player['player_name'].replace(' ', '_').lower()}"
    ]

    # Add special achievements
    achievements = []
    if ints >= 8:
        achievements.append("DPOY Candidate")
    if int_tds >= 2:
        achievements.append("Pick-Six Specialist")
    if longest >= 80:
        achievements.append("Big Play Threat")
    if yards_per_int >= 25 and ints >= 3:
        achievements.append("Elite Return Ability")

    if achievements:
        text_parts.append(f"Special Achievements: {', '.join(achievements)}")

    return '\n'.join(text_parts)

def main():
    """Main function to load all interception stats"""

    print("=" * 60)
    print("NFL Player Interception Stats Loader")
    print("=" * 60)

    # Get all player data (extracted from screenshots)
    print("\nExtracting player data from screenshots...")
    all_players = get_all_player_data()

    print(f"\n{'-' * 40}")
    print(f"Total players extracted: {len(all_players)}")

    # Sort players by interceptions (descending)
    all_players.sort(key=lambda x: x.get('interceptions', 0), reverse=True)

    # Initialize Kre8VidMemory
    memory = Kre8VidMemory()

    # Format and add all player data
    print("\nAdding players to Kre8VidMems database...")

    stats_summary = {
        'elite': 0,
        'pro_bowl': 0,
        'starter': 0,
        'contributor': 0,
        'depth': 0,
        'total_ints': 0,
        'total_tds': 0,
        'total_yards': 0
    }

    for player in all_players:
        # Format the player data
        formatted_text = format_player_interceptions_stats(player)

        # Add to memory (metadata is included in the formatted text)
        memory.add(formatted_text)

        # Update stats summary
        ints = player.get('interceptions', 0)
        if ints >= 8:
            stats_summary['elite'] += 1
        elif ints >= 5:
            stats_summary['pro_bowl'] += 1
        elif ints >= 3:
            stats_summary['starter'] += 1
        elif ints >= 2:
            stats_summary['contributor'] += 1
        else:
            stats_summary['depth'] += 1

        stats_summary['total_ints'] += player.get('interceptions', 0)
        stats_summary['total_tds'] += player.get('int_touchdowns', 0)
        stats_summary['total_yards'] += player.get('int_yards', 0)

    # Save the memory
    memory_name = "nfl-player-interceptions-stats"
    save_path = f"data/memories/{memory_name}"
    memory.save(save_path)

    print(f"\n✓ Successfully saved to: {save_path}")

    # Print summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    print(f"Total Players: {len(all_players)}")
    print(f"\nPerformance Breakdown:")
    print(f"  Elite (8+ INTs):        {stats_summary['elite']} players")
    print(f"  Pro Bowl (5-7 INTs):    {stats_summary['pro_bowl']} players")
    print(f"  Starter (3-4 INTs):     {stats_summary['starter']} players")
    print(f"  Contributor (2 INTs):   {stats_summary['contributor']} players")
    print(f"  Depth (0-1 INTs):       {stats_summary['depth']} players")

    print(f"\nAggregate Stats:")
    print(f"  Total Interceptions:    {stats_summary['total_ints']}")
    print(f"  Total INT Touchdowns:   {stats_summary['total_tds']}")
    print(f"  Total INT Yards:        {stats_summary['total_yards']}")

    if all_players:
        print(f"\nTop 5 Players by Interceptions:")
        for i, player in enumerate(all_players[:5], 1):
            print(f"  {i}. {player['player_name']}: {player.get('interceptions', 0)} INTs")

    print("\n" + "=" * 60)
    print("✓ Data successfully loaded into Kre8VidMems!")
    print("=" * 60)

if __name__ == "__main__":
    main()