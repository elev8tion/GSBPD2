#!/usr/bin/env python3
"""
Process all scraped NBA team rosters and append to players.json
"""
import json
from pathlib import Path
from parse_roster_v2 import parse_roster_markdown_v2

# Team data: (team_name, team_abbrev, team_id, markdown_content)
teams_to_parse = []

def load_existing_players():
    """Load existing players from players.json"""
    players_file = Path(__file__).parent / "nba_data" / "players.json"
    if players_file.exists():
        with open(players_file, 'r') as f:
            return json.load(f)
    return []

def save_all_players(all_players):
    """Save all players to players.json"""
    players_file = Path(__file__).parent / "nba_data" / "players.json"
    with open(players_file, 'w') as f:
        json.dump(all_players, f, indent=2)
    print(f"\n✓ Saved {len(all_players)} total players to {players_file}")

def process_all_teams():
    """Parse all teams and append to players.json"""
    # Load existing players
    all_players = load_existing_players()
    existing_count = len(all_players)
    print(f"Loaded {existing_count} existing players")

    # Get existing team IDs to avoid duplicates
    existing_team_ids = set(p['team_id'] for p in all_players)

    new_players_count = 0

    for team_name, team_abbrev, team_id, markdown in teams_to_parse:
        # Skip if team already exists
        if team_id in existing_team_ids:
            print(f"⊘ Skipping {team_name} (already in database)")
            continue

        # Parse team roster
        players = parse_roster_markdown_v2(markdown, team_id, team_name)

        if players:
            print(f"✓ {team_name:<25} - Parsed {len(players)} players")
            all_players.extend(players)
            new_players_count += len(players)
        else:
            print(f"✗ {team_name:<25} - No players found")

    # Save updated players list
    if new_players_count > 0:
        save_all_players(all_players)
        print(f"\n✓ Added {new_players_count} new players")
        print(f"✓ Total players: {len(all_players)}")
    else:
        print("\nNo new players to add")

if __name__ == "__main__":
    # This will be populated by another script
    if not teams_to_parse:
        print("No teams to parse. Please populate teams_to_parse list.")
    else:
        process_all_teams()
