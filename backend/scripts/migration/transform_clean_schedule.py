#!/usr/bin/env python3
"""
Transform clean NBA schedule to add game_id and status fields.
Input is already clean - just enriching with metadata.
"""
import json
from pathlib import Path
from datetime import datetime

# File paths
INPUT_FILE = Path(__file__).parent / "nba_data" / "nba_schedule_clean.json"
OUTPUT_FILE = Path(__file__).parent / "nba_data" / "nba_schedule_final.json"

def transform_schedule():
    """Add game_id and status to clean schedule data."""
    print(f"📖 Loading clean schedule from: {INPUT_FILE}")

    with open(INPUT_FILE, 'r') as f:
        games = json.load(f)

    print(f"   Total games: {len(games)}")

    # Transform each game
    transformed = []
    for game in games:
        # Create unique game_id
        date = game['date']
        away = game['away_team'].replace(' ', '-').replace("'", "")
        home = game['home_team'].replace(' ', '-').replace("'", "")
        game_id = f"{date}_{away}_at_{home}"

        # Add fields
        enriched = {
            "game_id": game_id,
            "date": game['date'],
            "away_team": game['away_team'],
            "home_team": game['home_team'],
            "game_time": game.get('time_utc', 'TBD'),
            "venue": game.get('arena', game['home_team']),
            "status": "scheduled"
        }

        transformed.append(enriched)

    # Save transformed data
    print(f"\n💾 Saving transformed schedule to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(transformed, f, indent=2)

    # Also update the original with enriched data
    with open(INPUT_FILE, 'w') as f:
        json.dump(transformed, f, indent=2)

    # Generate stats
    dates = [g['date'] for g in transformed]
    teams = set()
    games_per_team = {}

    for game in transformed:
        for team in [game['away_team'], game['home_team']]:
            teams.add(team)
            games_per_team[team] = games_per_team.get(team, 0) + 1

    stats = {
        "total_games": len(transformed),
        "date_range": {"start": min(dates), "end": max(dates)},
        "unique_teams": sorted(list(teams)),
        "games_per_team": games_per_team,
        "generated_at": datetime.now().isoformat()
    }

    stats_file = INPUT_FILE.parent / "nba_schedule_stats.json"
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"   Stats saved to: {stats_file}")
    print(f"\n✅ Schedule transformation complete!")
    print(f"   Total games: {stats['total_games']}")
    print(f"   Teams: {len(stats['unique_teams'])}")
    print(f"   Date range: {stats['date_range']['start']} to {stats['date_range']['end']}")

    return transformed, stats

if __name__ == "__main__":
    transformed, stats = transform_schedule()

    print(f"\n   Sample transformed games:")
    for game in transformed[:3]:
        print(f"      {game['date']}: {game['away_team']} @ {game['home_team']}")
        print(f"         ID: {game['game_id']}")
        print(f"         Time: {game['game_time']}")
        print(f"         Venue: {game['venue']}")
