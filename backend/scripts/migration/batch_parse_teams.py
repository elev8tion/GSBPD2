#!/usr/bin/env python3
"""
Batch parse and add all remaining NBA teams to players.json
Uses Firecrawl cache for instant retrieval, then parses each team
"""
import json
from pathlib import Path
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

def add_team(all_players, team_name, team_id, markdown):
    """Parse and add a team's roster"""
    # Check if team already exists
    if any(p['team_id'] == team_id for p in all_players):
        return 0

    # Parse the markdown
    new_players = parse_roster_markdown_v2(markdown, team_id, team_name)

    if new_players:
        all_players.extend(new_players)
        return len(new_players)
    return 0

def main():
    """Main processing function"""
    print("=" * 80)
    print("BATCH PARSING NBA TEAMS")
    print("=" * 80)

    all_players = load_players()
    existing_teams = set(p['team_id'] for p in all_players)
    starting_count = len(all_players)

    print(f"\nStarting database: {len(existing_teams)} teams, {starting_count} players")
    print("\nThis script will be called multiple times with markdown data from Firecrawl.")
    print("Each batch will parse teams and append to players.json progressively.\n")

if __name__ == "__main__":
    main()
