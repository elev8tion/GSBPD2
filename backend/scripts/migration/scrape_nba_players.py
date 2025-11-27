#!/usr/bin/env python3
"""
Scrape NBA player rosters for all 30 teams using Firecrawl
Parses player data from team roster pages and saves to players.json
"""

import sys
import json
import re
from pathlib import Path

sys.path.insert(0, '/Users/kcdacre8tor/GSBPD2/backend')
from services.nba_service import NBA_TEAMS

def parse_player_from_text(text_block, team_id, team_name):
    """Parse a single player's data from text block"""
    try:
        # Extract player info using regex patterns
        lines = text_block.strip().split('\n')

        # Player typically has: Name, Position, Number, Height, Weight, Age, Years Pro, Country, Stats
        player_data = {
            'team_id': team_id,
            'team_name': team_name,
            'name': '',
            'position': '',
            'jersey_number': '',
            'height': '',
            'weight': '',
            'age': 0,
            'years_pro': '',
            'country': '',
            'ppg': 0.0,
            'rpg': 0.0,
            'apg': 0.0,
            'gp': 0
        }

        # Parse each line
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Name (usually first/last name on separate lines or together)
            if not player_data['name'] and line and not line.startswith('!') and len(line.split()) <= 2:
                if i + 1 < len(lines) and len(lines[i+1].split()) <= 2:
                    player_data['name'] = f"{line} {lines[i+1].strip()}"
                    i += 1
                else:
                    player_data['name'] = line

            # Position
            elif 'Guard' in line or 'Forward' in line or 'Center' in line:
                player_data['position'] = line

            # Jersey number (single digit or double digit)
            elif line.isdigit() and len(line) <= 2 and not player_data['jersey_number']:
                player_data['jersey_number'] = line

            # Height (format: 6'7")
            elif "'" in line and '"' in line:
                player_data['height'] = line

            # Weight (format: 220 lbs)
            elif 'lbs' in line:
                player_data['weight'] = line.replace('lbs', '').strip()

            # Age
            elif line == 'Age':
                if i + 1 < len(lines) and lines[i+1].strip().isdigit():
                    player_data['age'] = int(lines[i+1].strip())
                    i += 1

            # Years Pro
            elif line == 'Years Pro':
                if i + 1 < len(lines):
                    player_data['years_pro'] = lines[i+1].strip()
                    i += 1

            # Country
            elif line == 'Country':
                if i + 1 < len(lines):
                    player_data['country'] = lines[i+1].strip()
                    i += 1

            # Stats (PPG, APG, RPG)
            elif line == 'PPG':
                if i + 1 < len(lines):
                    try:
                        val = lines[i+1].strip()
                        if val != '-':
                            player_data['ppg'] = float(val)
                    except:
                        pass
                    i += 1
            elif line == 'APG':
                if i + 1 < len(lines):
                    try:
                        val = lines[i+1].strip()
                        if val != '-':
                            player_data['apg'] = float(val)
                    except:
                        pass
                    i += 1
            elif line == 'RPG':
                if i + 1 < len(lines):
                    try:
                        val = lines[i+1].strip()
                        if val != '-':
                            player_data['rpg'] = float(val)
                    except:
                        pass
                    i += 1
            elif line == 'GP':
                if i + 1 < len(lines):
                    try:
                        val = lines[i+1].strip()
                        if val != '-':
                            player_data['gp'] = int(val)
                    except:
                        pass
                    i += 1

            i += 1

        # Only return if we have at least a name
        if player_data['name']:
            return player_data
        return None

    except Exception as e:
        print(f"Error parsing player: {e}")
        return None

def parse_roster_markdown(markdown, team_id, team_name):
    """Parse all players from roster markdown"""
    players = []

    # Split into sections by player (each player block has their name as header)
    # Look for pattern: Name followed by Position, Number, Stats
    sections = markdown.split('![')

    for section in sections:
        if 'headshot' in section:
            player = parse_player_from_text(section, team_id, team_name)
            if player:
                players.append(player)

    return players

# Manual roster data from Lakers scrape (sample)
MANUAL_ROSTERS = {
    "1610612747": [  # Lakers
        {
            "team_id": "1610612747",
            "team_name": "Los Angeles Lakers",
            "player_id": "2544",
            "name": "LeBron James",
            "position": "Forward",
            "jersey_number": "23",
            "height": "6'9\"",
            "weight": "250",
            "age": 40,
            "years_pro": "22",
            "country": "USA",
            "ppg": 14.0,
            "rpg": 4.5,
            "apg": 10.0,
            "gp": 2
        },
        {
            "team_id": "1610612747",
            "team_name": "Los Angeles Lakers",
            "player_id": "1630559",
            "name": "Austin Reaves",
            "position": "Guard",
            "jersey_number": "15",
            "height": "6'5\"",
            "weight": "197",
            "age": 27,
            "years_pro": "4",
            "country": "USA",
            "ppg": 27.6,
            "rpg": 5.5,
            "apg": 7.3,
            "gp": 13
        },
        {
            "team_id": "1610612747",
            "team_name": "Los Angeles Lakers",
            "player_id": "1629028",
            "name": "Deandre Ayton",
            "position": "Center",
            "jersey_number": "5",
            "height": "7'0\"",
            "weight": "252",
            "age": 27,
            "years_pro": "7",
            "country": "Bahamas",
            "ppg": 15.5,
            "rpg": 8.4,
            "apg": 0.9,
            "gp": 15
        },
        {
            "team_id": "1610612747",
            "team_name": "Los Angeles Lakers",
            "player_id": "1629060",
            "name": "Rui Hachimura",
            "position": "Forward",
            "jersey_number": "28",
            "height": "6'8\"",
            "weight": "230",
            "age": 27,
            "years_pro": "6",
            "country": "Japan",
            "ppg": 15.0,
            "rpg": 3.9,
            "apg": 1.1,
            "gp": 15
        },
        {
            "team_id": "1610612747",
            "team_name": "Los Angeles Lakers",
            "player_id": "1642355",
            "name": "Bronny James",
            "position": "Guard",
            "jersey_number": "9",
            "height": "6'2\"",
            "weight": "210",
            "age": 21,
            "years_pro": "1",
            "country": "USA",
            "ppg": 2.1,
            "rpg": 0.9,
            "apg": 1.8,
            "gp": 10
        },
        {
            "team_id": "1610612747",
            "team_name": "Los Angeles Lakers",
            "player_id": "203935",
            "name": "Marcus Smart",
            "position": "Guard",
            "jersey_number": "36",
            "height": "6'3\"",
            "weight": "220",
            "age": 31,
            "years_pro": "11",
            "country": "USA",
            "ppg": 9.5,
            "rpg": 2.2,
            "apg": 2.9,
            "gp": 13
        },
        {
            "team_id": "1610612747",
            "team_name": "Los Angeles Lakers",
            "player_id": "1631222",
            "name": "Jake LaRavia",
            "position": "Forward",
            "jersey_number": "12",
            "height": "6'7\"",
            "weight": "235",
            "age": 24,
            "years_pro": "3",
            "country": "USA",
            "ppg": 10.3,
            "rpg": 4.3,
            "apg": 2.3,
            "gp": 16
        },
        {
            "team_id": "1610612747",
            "team_name": "Los Angeles Lakers",
            "player_id": "1629216",
            "name": "Gabe Vincent",
            "position": "Guard",
            "jersey_number": "7",
            "height": "6'2\"",
            "weight": "200",
            "age": 29,
            "years_pro": "6",
            "country": "USA",
            "ppg": 4.0,
            "rpg": 0.8,
            "apg": 1.6,
            "gp": 5
        }
    ]
}

if __name__ == "__main__":
    print("=" * 60)
    print("NBA PLAYER ROSTER SCRAPER")
    print("Using Firecrawl MCP to scrape player data from NBA.com")
    print("=" * 60)
    print()

    all_players = []

    # For now, use manual data as a starting point
    # In production, we'd scrape all 30 teams using Firecrawl
    print("Loading player rosters...")
    print()

    for team_id, roster in MANUAL_ROSTERS.items():
        team_info = next((t for t in NBA_TEAMS if t["id"] == team_id), None)
        if team_info:
            print(f"✓ {team_info['name']}: {len(roster)} players")
            all_players.extend(roster)

    print()
    print(f"Total players loaded: {len(all_players)}")
    print()

    # Save to players.json
    base_dir = Path(__file__).parent
    players_file = base_dir / "nba_data" / "players.json"

    with open(players_file, 'w') as f:
        json.dump(all_players, f, indent=2)

    print(f"✓ Player data saved to: {players_file}")
    print()
    print("=" * 60)
    print("NEXT STEPS:")
    print("1. This is sample data for Lakers only")
    print("2. Use Firecrawl MCP to scrape remaining 29 teams")
    print("3. Each team URL: https://www.nba.com/{team_slug}/roster")
    print("=" * 60)
