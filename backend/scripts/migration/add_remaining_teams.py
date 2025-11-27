#!/usr/bin/env python3
"""
Add all remaining scraped teams to players.json
This script will be manually populated with markdown from Firecrawl scraping results
"""
import json
import sys
from pathlib import Path

# Import the corrected parser
sys.path.insert(0, str(Path(__file__).parent))
from parse_roster_v2 import parse_roster_markdown_v2

def load_players():
    """Load current players from players.json"""
    players_file = Path(__file__).parent / "nba_data" / "players.json"
    if players_file.exists():
        with open(players_file, 'r') as f:
            return json.load(f)
    return []

def save_players(players):
    """Save players to players.json"""
    players_file = Path(__file__).parent / "nba_data" / "players.json"
    with open(players_file, 'w') as f:
        json.dump(players, f, indent=2)
    print(f"\n✓ Saved {len(players)} total players to {players_file}")

def main():
    """Add teams from scraping session"""
    # Load existing players
    all_players = load_players()
    existing_teams = set(p['team_id'] for p in all_players)
    starting_count = len(all_players)

    print(f"Current database: {len(existing_teams)} teams, {starting_count} players")
    print("\nThis script requires markdown data to be embedded.")
    print("Markdown will be added from the Firecrawl scraping results.")

    # Example structure for adding teams:
    # teams_to_add = [
    #     ("Dallas Mavericks", "1610612742", markdown_content),
    #     ("Houston Rockets", "1610612745", markdown_content),
    #     ...
    # ]
    #
    # for team_name, team_id, markdown in teams_to_add:
    #     if team_id not in existing_teams:
    #         players = parse_roster_markdown_v2(markdown, team_id, team_name)
    #         all_players.extend(players)
    #         print(f"✓ Added {team_name}: {len(players)} players")
    #
    # save_players(all_players)

if __name__ == "__main__":
    main()
