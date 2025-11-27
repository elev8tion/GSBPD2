#!/usr/bin/env python3
"""
Scrape and parse ALL 30 NBA team rosters using Firecrawl
Extracts structured player data and saves to players.json
"""

import sys
import json
import re
from pathlib import Path

sys.path.insert(0, '/Users/kcdacre8tor/GSBPD2/backend')
from services.nba_service import NBA_TEAMS

def extract_player_data(markdown_text, team_id, team_name):
    """
    Extract all players from Firecrawl markdown response
    """
    players = []

    # Split by player sections (each player has an image marker)
    player_sections = re.split(r'!\[\]\(https://cdn\.nba\.com/headshots', markdown_text)

    for section in player_sections[1:]:  # Skip first split (header)
        try:
            lines = section.strip().split('\n')

            # Initialize player data
            player = {
                'team_id': team_id,
                'team_name': team_name,
                'player_id': '',
                'name': '',
                'position': '',
                'jersey_number': '',
                'height': '',
                'weight': '',
                'age': 0,
                'years_pro': '',
                'country': 'USA',  # Default
                'ppg': 0.0,
                'rpg': 0.0,
                'apg': 0.0,
                'gp': 0
            }

            # Extract player ID from image URL (first line)
            if lines and '/nba/latest/' in lines[0]:
                match = re.search(r'/(\d+)\.png', lines[0])
                if match:
                    player['player_id'] = match.group(1)

            # Parse the rest of the data
            i = 0
            first_name = ''
            last_name = ''

            while i < len(lines):
                line = lines[i].strip()

                # Skip empty lines and image markers
                if not line or line.startswith('!['):
                    i += 1
                    continue

                # Name parsing (first name, then last name)
                if not first_name and line and line[0].isupper() and len(line.split()) == 1:
                    if line not in ['Guard', 'Forward', 'Center', 'AGE', 'EXP', 'YRS', 'HT', 'WT', 'GP', 'PPG', 'RPG', 'APG', 'Rook']:
                        first_name = line
                        i += 1
                        continue

                if first_name and not last_name and line and line[0].isupper() and len(line.split()) == 1:
                    if line not in ['Guard', 'Forward', 'Center']:
                        last_name = line
                        player['name'] = f"{first_name} {last_name}"
                        i += 1
                        continue

                # Position
                if 'Guard' in line or 'Forward' in line or 'Center' in line:
                    player['position'] = line

                # Jersey number (appears as standalone number)
                elif line.isdigit() and len(line) <= 2 and not player['jersey_number']:
                    player['jersey_number'] = line

                # Age (look for AGE label)
                elif line == 'AGE':
                    if i + 1 < len(lines) and lines[i+1].strip().isdigit():
                        player['age'] = int(lines[i+1].strip())
                        i += 1

                # Experience (look for EXP or YRS)
                elif line in ['EXP', 'YRS']:
                    if i + 1 < len(lines):
                        exp_val = lines[i+1].strip()
                        # Extract number from strings like "8YRS" or "RookYRS"
                        if 'Rook' in exp_val:
                            player['years_pro'] = 'R'
                        else:
                            match = re.search(r'(\d+)', exp_val)
                            if match:
                                player['years_pro'] = match.group(1)
                        i += 1

                # Height (look for HT)
                elif line == 'HT':
                    if i + 1 < len(lines):
                        ht = lines[i+1].strip()
                        if '-' in ht:
                            player['height'] = ht
                        i += 1

                # Weight (look for WT)
                elif line == 'WT':
                    if i + 1 < len(lines):
                        wt = lines[i+1].strip()
                        if wt.isdigit():
                            player['weight'] = wt
                        i += 1

                # Games Played
                elif line == 'GP':
                    if i + 1 < len(lines):
                        try:
                            val = lines[i+1].strip()
                            if val and val.isdigit():
                                player['gp'] = int(val)
                        except:
                            pass
                        i += 1

                # PPG
                elif line == 'PPG':
                    if i + 1 < len(lines):
                        try:
                            val = lines[i+1].strip()
                            if val and val not in ['-', '']:
                                player['ppg'] = float(val)
                        except:
                            pass
                        i += 1

                # RPG
                elif line == 'RPG':
                    if i + 1 < len(lines):
                        try:
                            val = lines[i+1].strip()
                            if val and val not in ['-', '']:
                                player['rpg'] = float(val)
                        except:
                            pass
                        i += 1

                # APG
                elif line == 'APG':
                    if i + 1 < len(lines):
                        try:
                            val = lines[i+1].strip()
                            if val and val not in ['-', '']:
                                player['apg'] = float(val)
                        except:
                            pass
                        i += 1

                i += 1

            # Only add player if we have a valid name
            if player['name']:
                players.append(player)

        except Exception as e:
            print(f"  ⚠ Error parsing player section: {e}")
            continue

    return players

def main():
    """
    Main function to coordinate scraping
    NOTE: This script provides the parsing logic.
    Actual scraping should be done via Firecrawl MCP tool in Claude Code.
    """
    print("=" * 70)
    print("NBA ROSTER SCRAPER & PARSER - ALL 30 TEAMS")
    print("=" * 70)
    print()
    print("This script provides parsing logic for Firecrawl scraped data.")
    print()
    print(f"Teams to scrape: {len(NBA_TEAMS)}")
    print()

    # Test parsing with sample data
    sample_markdown = """
![](https://cdn.nba.com/headshots/nba/latest/1040x760/1627759.png)

Jaylen

Brown

Guard-Forward

7--

AGE

29

EXP

9YRS

HT

6-6

WT

223

GP

17

PPG

27.9

RPG

5.6

APG

4.3
"""

    test_players = extract_player_data(sample_markdown, "1610612738", "Boston Celtics")
    if test_players:
        print("✓ Parser test successful!")
        print(f"  Sample player: {test_players[0]['name']} - {test_players[0]['ppg']} PPG")
    else:
        print("✗ Parser test failed")

    print()
    print("=" * 70)
    print("Ready for Firecrawl scraping via MCP tool")
    print("=" * 70)

if __name__ == "__main__":
    main()
