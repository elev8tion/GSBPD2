#!/usr/bin/env python3
"""
Complete NBA roster parsing - Final step
All 30 teams have been scraped via Firecrawl.
This script provides the workflow to finalize the database.
"""
import json
from pathlib import Path

def get_current_status():
    """Check current database status"""
    players_file = Path(__file__).parent / "nba_data" / "players.json"

    if not players_file.exists():
        return 0, []

    with open(players_file, 'r') as f:
        players = json.load(f)

    teams = set((p['team_id'], p['team_name']) for p in players)
    return len(players), sorted(teams, key=lambda x: x[1])

# All 30 NBA teams with their IDs
ALL_30_TEAMS = [
    ("1610612747", "Los Angeles Lakers"),
    ("1610612751", "Brooklyn Nets"),
    ("1610612752", "New York Knicks"),
    ("1610612755", "Philadelphia 76ers"),
    ("1610612761", "Toronto Raptors"),
    ("1610612738", "Boston Celtics"),
    ("1610612741", "Chicago Bulls"),
    ("1610612739", "Cleveland Cavaliers"),
    ("1610612765", "Detroit Pistons"),
    ("1610612754", "Indiana Pacers"),
    ("1610612749", "Milwaukee Bucks"),
    ("1610612737", "Atlanta Hawks"),
    ("1610612766", "Charlotte Hornets"),
    ("1610612748", "Miami Heat"),
    ("1610612753", "Orlando Magic"),
    ("1610612764", "Washington Wizards"),
    ("1610612743", "Denver Nuggets"),
    ("1610612750", "Minnesota Timberwolves"),
    ("1610612760", "Oklahoma City Thunder"),
    ("1610612757", "Portland Trail Blazers"),
    ("1610612762", "Utah Jazz"),
    ("1610612744", "Golden State Warriors"),
    ("1610612746", "LA Clippers"),
    ("1610612756", "Phoenix Suns"),
    ("1610612758", "Sacramento Kings"),
    ("1610612742", "Dallas Mavericks"),
    ("1610612745", "Houston Rockets"),
    ("1610612763", "Memphis Grizzlies"),
    ("1610612740", "New Orleans Pelicans"),
    ("1610612759", "San Antonio Spurs"),
]

if __name__ == "__main__":
    total_players, existing_teams = get_current_status()

    print("=" * 80)
    print("NBA ROSTER DATABASE STATUS")
    print("=" * 80)
    print(f"\nCurrent Status:")
    print(f"  Total players in database: {total_players}")
    print(f"  Teams in database: {len(existing_teams)}/30")

    if existing_teams:
        print(f"\nTeams already in database:")
        for team_id, team_name in existing_teams:
            print(f"  ✓ {team_name}")

    # Find missing teams
    existing_ids = set(t[0] for t in existing_teams)
    missing_teams = [(tid, tname) for tid, tname in ALL_30_TEAMS if tid not in existing_ids]

    if missing_teams:
        print(f"\nTeams still needed ({len(missing_teams)}):")
        for team_id, team_name in missing_teams:
            print(f"  - {team_name}")
        print(f"\nNEXT STEPS:")
        print(f"1. All teams have been scraped via Firecrawl (data is cached)")
        print(f"2. Markdown data needs to be saved and parsed")
        print(f"3. Run parsing script to complete database")
    else:
        print(f"\n✓ ALL 30 TEAMS COMPLETE!")
        print(f"✓ Database ready with {total_players} players")
