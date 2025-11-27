#!/usr/bin/env python3
"""
Clean and transform NBA schedule data - Version 2 with proper team name normalization.
"""

import json
from pathlib import Path
from datetime import datetime

# File paths
INPUT_FILE = Path.home() / "Downloads" / "nba_schedule.json"
OUTPUT_FILE = Path(__file__).parent / "nba_data" / "nba_schedule_clean.json"

# Official NBA team name mappings
TEAM_NAME_MAP = {
    # Handle abbreviations and variations
    "LA": "Los Angeles Lakers",
    "Lakers": "Los Angeles Lakers",
    "Los Angeles": "Los Angeles Lakers",  # Default to Lakers
    "LA Clippers": "Los Angeles Clippers",
    "Clippers": "Los Angeles Clippers",

    "New York": "New York Knicks",
    "Knicks": "New York Knicks",

    "Golden State": "Golden State Warriors",
    "Warriors": "Golden State Warriors",

    "San Antonio": "San Antonio Spurs",
    "Spurs": "San Antonio Spurs",

    # Full names (passthrough)
    "Atlanta": "Atlanta Hawks",
    "Atlanta Hawks": "Atlanta Hawks",

    "Boston": "Boston Celtics",
    "Boston Celtics": "Boston Celtics",

    "Brooklyn": "Brooklyn Nets",
    "Brooklyn Nets": "Brooklyn Nets",

    "Charlotte": "Charlotte Hornets",
    "Charlotte Hornets": "Charlotte Hornets",

    "Chicago": "Chicago Bulls",
    "Chicago Bulls": "Chicago Bulls",

    "Cleveland": "Cleveland Cavaliers",
    "Cleveland Cavaliers": "Cleveland Cavaliers",

    "Dallas": "Dallas Mavericks",
    "Dallas Mavericks": "Dallas Mavericks",

    "Denver": "Denver Nuggets",
    "Denver Nuggets": "Denver Nuggets",

    "Detroit": "Detroit Pistons",
    "Detroit Pistons": "Detroit Pistons",

    "Houston": "Houston Rockets",
    "Houston Rockets": "Houston Rockets",

    "Indiana": "Indiana Pacers",
    "Indiana Pacers": "Indiana Pacers",

    "Memphis": "Memphis Grizzlies",
    "Memphis Grizzlies": "Memphis Grizzlies",

    "Miami": "Miami Heat",
    "Miami Heat": "Miami Heat",

    "Milwaukee": "Milwaukee Bucks",
    "Milwaukee Bucks": "Milwaukee Bucks",

    "Minnesota": "Minnesota Timberwolves",
    "Minnesota Timberwolves": "Minnesota Timberwolves",

    "New Orleans": "New Orleans Pelicans",
    "New Orleans Pelicans": "New Orleans Pelicans",

    "Oklahoma City": "Oklahoma City Thunder",
    "Oklahoma City Thunder": "Oklahoma City Thunder",

    "Orlando": "Orlando Magic",
    "Orlando Magic": "Orlando Magic",

    "Philadelphia": "Philadelphia 76ers",
    "Philadelphia 76ers": "Philadelphia 76ers",

    "Phoenix": "Phoenix Suns",
    "Phoenix Suns": "Phoenix Suns",

    "Portland": "Portland Trail Blazers",
    "Portland Trail Blazers": "Portland Trail Blazers",

    "Sacramento": "Sacramento Kings",
    "Sacramento Kings": "Sacramento Kings",

    "Toronto": "Toronto Raptors",
    "Toronto Raptors": "Toronto Raptors",

    "Utah": "Utah Jazz",
    "Utah Jazz": "Utah Jazz",

    "Washington": "Washington Wizards",
    "Washington Wizards": "Washington Wizards",
}

def normalize_team_name(team_name):
    """Normalize team name to official full name."""
    normalized = TEAM_NAME_MAP.get(team_name, team_name)
    if normalized == team_name and team_name not in ["TBD", "Unknown"]:
        print(f"   ⚠️  Unknown team name: {team_name}")
    return normalized

def parse_location(time_or_result):
    """Parse location from time_or_result field."""
    if time_or_result.startswith('@'):
        return time_or_result[1:].strip()
    elif time_or_result.startswith('vs'):
        return time_or_result[2:].strip()
    else:
        return time_or_result.strip()

def clean_schedule_data(input_path, output_path):
    """Clean and transform schedule data with proper deduplication."""
    print(f"📖 Reading schedule from: {input_path}")
    with open(input_path, 'r') as f:
        raw_data = json.load(f)

    print(f"   Total entries: {len(raw_data)}")

    # Track unique games using normalized team names
    games_dict = {}
    skipped = {"playoff": 0, "malformed": 0, "tbd": 0, "unknown_team": 0}

    for entry in raw_data:
        # Skip playoff/play-in games
        if 'round' in entry or 'matchup' in entry:
            skipped["playoff"] += 1
            continue

        # Check required fields
        if 'home_team' not in entry or 'time_or_result' not in entry:
            skipped["malformed"] += 1
            continue

        date = entry['date']
        team_raw = entry['home_team']
        location_str = entry['time_or_result']

        # Skip TBD dates
        if date == "TBD":
            skipped["tbd"] += 1
            continue

        # Skip unknown/TBD teams
        if team_raw in ["TBD", "Unknown", ""]:
            skipped["unknown_team"] += 1
            continue

        # Parse and normalize team names
        team = normalize_team_name(team_raw)
        opponent_raw = parse_location(location_str)
        opponent = normalize_team_name(opponent_raw)

        # Skip if normalization failed
        if opponent in ["TBD", "Unknown"] or team in ["TBD", "Unknown"]:
            skipped["unknown_team"] += 1
            continue

        # Determine home/away
        if location_str.startswith('@'):
            away_team = team
            home_team = opponent
        else:
            away_team = opponent
            home_team = team

        # Create unique game key using SORTED normalized team names and date
        teams_sorted = tuple(sorted([away_team, home_team]))
        game_key = (date, teams_sorted)

        # Only add if not already in dict
        if game_key not in games_dict:
            game_id = f"{date}_{away_team.replace(' ', '-')}_at_{home_team.replace(' ', '-')}"

            games_dict[game_key] = {
                "game_id": game_id,
                "date": date,
                "away_team": away_team,
                "home_team": home_team,
                "game_time": "TBD",
                "venue": home_team,
                "status": "scheduled"
            }

    # Convert to list and sort by date
    cleaned_games = sorted(games_dict.values(), key=lambda x: x['date'])

    print(f"\n📊 Cleaning Results:")
    print(f"   Cleaned games: {len(cleaned_games)}")
    print(f"   Removed duplicates: {len(raw_data) - len(cleaned_games) - sum(skipped.values())}")
    print(f"   Skipped:")
    for reason, count in skipped.items():
        print(f"      {reason}: {count}")

    # Get statistics
    dates = [g['date'] for g in cleaned_games]
    teams = set()
    games_per_team = {}

    for game in cleaned_games:
        for team in [game['away_team'], game['home_team']]:
            teams.add(team)
            games_per_team[team] = games_per_team.get(team, 0) + 1

    print(f"\n   Date range: {min(dates)} to {max(dates)}")
    print(f"   Unique teams: {len(teams)}")
    print(f"   Games per team (avg): {sum(games_per_team.values()) / len(games_per_team):.1f}")

    # Save cleaned data
    print(f"\n💾 Saving cleaned schedule to: {output_path}")
    with open(output_path, 'w') as f:
        json.dump(cleaned_games, f, indent=2)

    # Save statistics
    stats = {
        "total_games": len(cleaned_games),
        "date_range": {"start": min(dates), "end": max(dates)},
        "unique_teams": sorted(list(teams)),
        "games_per_team": games_per_team,
        "skipped": skipped,
        "generated_at": datetime.now().isoformat()
    }

    stats_file = output_path.parent / "nba_schedule_stats.json"
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"   Stats saved to: {stats_file}")
    print(f"\n✅ Schedule cleaning complete!")

    return cleaned_games, stats

if __name__ == "__main__":
    cleaned_games, stats = clean_schedule_data(INPUT_FILE, OUTPUT_FILE)

    print(f"\n📈 Final Summary:")
    print(f"   Total games: {stats['total_games']}")
    print(f"   Teams: {len(stats['unique_teams'])}")
    print(f"   Date range: {stats['date_range']['start']} to {stats['date_range']['end']}")

    # Show games per team
    print(f"\n   Games per team (top 10):")
    sorted_teams = sorted(stats['games_per_team'].items(), key=lambda x: x[1], reverse=True)
    for team, count in sorted_teams[:10]:
        print(f"      {team}: {count}")

    print(f"\n   Sample games:")
    for game in cleaned_games[:5]:
        print(f"      {game['date']}: {game['away_team']} @ {game['home_team']}")
