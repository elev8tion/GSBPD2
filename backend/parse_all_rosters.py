#!/usr/bin/env python3
"""
Parse all 30 NBA team rosters scraped via Firecrawl
Extracts structured player data and saves to players.json
"""

import sys
import json
import re
from pathlib import Path

sys.path.insert(0, '/Users/kcdacre8tor/GSBPD2/backend')
from services.nba_service import NBA_TEAMS

# This script will be run after Firecrawl scraping is complete
# For now, we'll use the sample data structure and prepare for batch processing

def parse_player_stats(lines, start_idx):
    """Parse player stats from markdown lines"""
    stats = {
        'ppg': 0.0,
        'rpg': 0.0,
        'apg': 0.0,
        'gp': 0
    }

    i = start_idx
    while i < len(lines):
        line = lines[i].strip()

        if line == 'PPG':
            if i + 1 < len(lines):
                try:
                    val = lines[i+1].strip()
                    if val and val != '-':
                        stats['ppg'] = float(val)
                except:
                    pass
                i += 1
        elif line == 'RPG':
            if i + 1 < len(lines):
                try:
                    val = lines[i+1].strip()
                    if val and val != '-':
                        stats['rpg'] = float(val)
                except:
                    pass
                i += 1
        elif line == 'APG':
            if i + 1 < len(lines):
                try:
                    val = lines[i+1].strip()
                    if val and val != '-':
                        stats['apg'] = float(val)
                except:
                    pass
                i += 1
        elif line == 'GP':
            if i + 1 < len(lines):
                try:
                    val = lines[i+1].strip()
                    if val and val != '-':
                        stats['gp'] = int(val)
                except:
                    pass
                i += 1

        i += 1

        # Stop if we've moved too far
        if i > start_idx + 50:
            break

    return stats

def parse_player_from_section(section, team_id, team_name):
    """Parse a single player from a markdown section"""
    try:
        lines = section.strip().split('\n')

        player_data = {
            'team_id': team_id,
            'team_name': team_name,
            'player_id': '',  # Will need to extract from NBA.com data
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

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Skip image markers
            if line.startswith('![') or 'headshot' in line.lower():
                i += 1
                continue

            # Name - typically appears early, capital letters
            if not player_data['name'] and line and not line.startswith('#') and len(line.split()) <= 4:
                # Check if it looks like a name (contains letters, not a stat label)
                if any(c.isalpha() for c in line) and line not in ['Guard', 'Forward', 'Center', 'PPG', 'RPG', 'APG', 'GP', 'Age', 'Years Pro', 'Country']:
                    # Could be first name or full name
                    if i + 1 < len(lines) and len(lines[i+1].split()) <= 2 and any(c.isalpha() for c in lines[i+1]):
                        next_line = lines[i+1].strip()
                        if next_line not in ['Guard', 'Forward', 'Center', 'PPG', 'RPG', 'APG', 'GP']:
                            player_data['name'] = f"{line} {next_line}"
                            i += 1
                    else:
                        player_data['name'] = line

            # Position
            elif 'Guard' in line or 'Forward' in line or 'Center' in line:
                player_data['position'] = line

            # Jersey number
            elif line.isdigit() and len(line) <= 2 and not player_data['jersey_number']:
                player_data['jersey_number'] = line

            # Height (e.g., 6'9")
            elif "'" in line and '"' in line and not player_data['height']:
                player_data['height'] = line

            # Weight (e.g., 250 lbs)
            elif 'lbs' in line.lower() or (line.isdigit() and 150 <= int(line) <= 350):
                player_data['weight'] = line.replace('lbs', '').replace('LBS', '').strip()

            # Age
            elif line == 'Age':
                if i + 1 < len(lines) and lines[i+1].strip().isdigit():
                    player_data['age'] = int(lines[i+1].strip())
                    i += 1

            # Years Pro
            elif line in ['Years Pro', 'YearsPro', 'Experience']:
                if i + 1 < len(lines):
                    val = lines[i+1].strip()
                    if val and val != '-':
                        player_data['years_pro'] = val
                    i += 1

            # Country
            elif line == 'Country':
                if i + 1 < len(lines):
                    val = lines[i+1].strip()
                    if val and val != '-':
                        player_data['country'] = val
                    i += 1

            i += 1

        # Parse stats
        stats = parse_player_stats(lines, 0)
        player_data.update(stats)

        # Only return if we have at least a name
        if player_data['name']:
            return player_data
        return None

    except Exception as e:
        print(f"Error parsing player section: {e}")
        return None

def parse_roster_markdown(markdown_text, team_id, team_name):
    """Parse all players from a team's roster markdown"""
    players = []

    # Split by player sections (look for image markers or player headings)
    sections = re.split(r'!\[.*?headshot.*?\]', markdown_text, flags=re.IGNORECASE)

    for section in sections:
        if section.strip():
            player = parse_player_from_section(section, team_id, team_name)
            if player:
                players.append(player)

    return players

def scrape_all_rosters_with_firecrawl():
    """
    This function would be called to scrape all 30 team rosters using Firecrawl.
    Since scraping was already done in the previous conversation,
    this is a placeholder for the scraping logic.
    """
    print("NOTE: Scraping should be done via Firecrawl MCP tool")
    print("This script expects scraped data to be processed")
    return []

if __name__ == "__main__":
    print("=" * 70)
    print("NBA ROSTER PARSER - ALL 30 TEAMS")
    print("=" * 70)
    print()
    print("This script will parse scraped roster data from Firecrawl")
    print("and populate players.json with structured player data.")
    print()
    print("Teams to process:")
    for i, team in enumerate(NBA_TEAMS, 1):
        print(f"  {i:2d}. {team['name']:<30} ({team['slug']})")
    print()
    print("=" * 70)
    print("Ready to process scraped data")
    print("=" * 70)
