#!/usr/bin/env python3
"""
Clean and transform NBA schedule data from team-centric format to matchup format.

Input format:
  {"date": "2025-11-25", "away_team": "", "home_team": "Memphis", "time_or_result": "@New Orleans"}

Output format:
  {"date": "2025-11-25", "away_team": "Memphis", "home_team": "New Orleans", "game_time": "TBD", "game_id": "..."}
"""

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# File paths
INPUT_FILE = Path.home() / "Downloads" / "nba_schedule.json"
OUTPUT_FILE = Path(__file__).parent / "nba_data" / "nba_schedule_clean.json"

# Ensure output directory exists
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

def parse_location(time_or_result):
    """
    Parse the time_or_result field to extract opponent location.
    Examples:
      "@Los Angeles" -> "Los Angeles"
      "@New Orleans" -> "New Orleans"
      "vs New York" -> "New York"
    """
    if time_or_result.startswith('@'):
        return time_or_result[1:].strip()
    elif time_or_result.startswith('vs'):
        return time_or_result[2:].strip()
    else:
        return time_or_result.strip()

def normalize_team_name(team_name):
    """
    Normalize team names to full names.
    Examples:
      "LA" -> "Los Angeles Lakers" (or Clippers - need to determine)
      "New York" -> "New York Knicks"
    """
    # Team name mappings
    TEAM_MAP = {
        "LA": "Los Angeles Lakers",  # Default to Lakers
        "LA Clippers": "Los Angeles Clippers",
        "Los Angeles": "Los Angeles Lakers",  # Context-dependent
        "New York": "New York Knicks",
        "Golden State": "Golden State Warriors",
        "San Antonio": "San Antonio Spurs",
        # Add more mappings as needed
    }

    return TEAM_MAP.get(team_name, team_name)

def clean_schedule_data(input_path, output_path):
    """
    Transform team-centric schedule data into matchup format.
    Removes duplicates and creates unique games with home/away teams.
    """
    print(f"📖 Reading schedule from: {input_path}")
    with open(input_path, 'r') as f:
        raw_data = json.load(f)

    print(f"   Total entries: {len(raw_data)}")

    # Use a set to track unique games (date + teams)
    games_dict = {}

    for entry in raw_data:
        # Handle different entry formats (regular season vs playoffs)
        if 'round' in entry or 'matchup' in entry:
            # This is a playoff/play-in game with TBD details - skip for now
            continue

        # Check if entry has required fields
        if 'home_team' not in entry or 'time_or_result' not in entry:
            print(f"   Skipping malformed entry: {entry}")
            continue

        date = entry['date']
        team = entry['home_team']  # Actually the team whose schedule this is
        location_str = entry['time_or_result']

        # Skip TBD dates
        if date == "TBD":
            continue

        # Parse opponent location
        opponent = parse_location(location_str)

        # Determine home/away based on @ symbol
        if location_str.startswith('@'):
            # Team is playing AWAY at opponent's venue
            away_team = team
            home_team = opponent
        else:
            # Team is playing HOME
            away_team = opponent
            home_team = team

        # Create unique game identifier (sorted teams + date to avoid duplicates)
        teams_sorted = tuple(sorted([away_team, home_team]))
        game_key = (date, teams_sorted)

        # Only add if not already in dict
        if game_key not in games_dict:
            game_id = f"{date}_{away_team.replace(' ', '_')}_at_{home_team.replace(' ', '_')}"

            games_dict[game_key] = {
                "game_id": game_id,
                "date": date,
                "away_team": away_team,
                "home_team": home_team,
                "game_time": "TBD",  # No time info in source data
                "venue": home_team,  # Assuming venue is home team's arena
                "status": "scheduled"
            }

    # Convert to list and sort by date
    cleaned_games = sorted(games_dict.values(), key=lambda x: x['date'])

    print(f"   Cleaned games: {len(cleaned_games)}")
    print(f"   Removed duplicates: {len(raw_data) - len(cleaned_games)}")

    # Get date range
    dates = [g['date'] for g in cleaned_games]
    print(f"   Date range: {min(dates)} to {max(dates)}")

    # Show team distribution
    teams = set()
    for game in cleaned_games:
        teams.add(game['away_team'])
        teams.add(game['home_team'])
    print(f"   Unique teams: {len(teams)}")

    # Save cleaned data
    print(f"\n💾 Saving cleaned schedule to: {output_path}")
    with open(output_path, 'w') as f:
        json.dump(cleaned_games, f, indent=2)

    # Also save summary statistics
    stats = {
        "total_games": len(cleaned_games),
        "date_range": {"start": min(dates), "end": max(dates)},
        "unique_teams": sorted(list(teams)),
        "games_per_team": {},
        "generated_at": datetime.now().isoformat()
    }

    # Count games per team
    for game in cleaned_games:
        for team in [game['away_team'], game['home_team']]:
            stats["games_per_team"][team] = stats["games_per_team"].get(team, 0) + 1

    stats_file = output_path.parent / "nba_schedule_stats.json"
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"   Stats saved to: {stats_file}")
    print(f"\n✅ Schedule cleaning complete!")

    return cleaned_games, stats

if __name__ == "__main__":
    cleaned_games, stats = clean_schedule_data(INPUT_FILE, OUTPUT_FILE)

    print(f"\n📊 Summary:")
    print(f"   Total games: {stats['total_games']}")
    print(f"   Teams: {len(stats['unique_teams'])}")
    print(f"   Date range: {stats['date_range']['start']} to {stats['date_range']['end']}")
    print(f"\n   Sample games:")
    for game in cleaned_games[:5]:
        print(f"      {game['date']}: {game['away_team']} @ {game['home_team']}")
