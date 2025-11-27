#!/usr/bin/env python3
"""
Parse all scraped NBA team rosters from the recent scraping session
This includes teams from Mavericks, Rockets, Grizzlies, Pelicans, Spurs, Celtics
and the 22 teams scraped in the previous session
"""
import json
from pathlib import Path
from parse_roster_v2 import parse_roster_markdown_v2

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

# For now, we'll manually mark which teams need parsing
# The Lakers and Nets were already parsed in the previous session
teams_scraped = [
    # Atlantic Division
    ("New York Knicks", "NYK", "1610612752"),
    ("Philadelphia 76ers", "PHI", "1610612755"),
    ("Toronto Raptors", "TOR", "1610612761"),
    ("Boston Celtics", "BOS", "1610612738"),

    # Central Division
    ("Chicago Bulls", "CHI", "1610612741"),
    ("Cleveland Cavaliers", "CLE", "1610612739"),
    ("Detroit Pistons", "DET", "1610612765"),
    ("Indiana Pacers", "IND", "1610612754"),
    ("Milwaukee Bucks", "MIL", "1610612749"),

    # Southeast Division
    ("Atlanta Hawks", "ATL", "1610612737"),
    ("Charlotte Hornets", "CHA", "1610612766"),
    ("Miami Heat", "MIA", "1610612748"),
    ("Orlando Magic", "ORL", "1610612753"),
    ("Washington Wizards", "WAS", "1610612764"),

    # Northwest Division
    ("Denver Nuggets", "DEN", "1610612743"),
    ("Minnesota Timberwolves", "MIN", "1610612750"),
    ("Oklahoma City Thunder", "OKC", "1610612760"),
    ("Portland Trail Blazers", "POR", "1610612757"),
    ("Utah Jazz", "UTA", "1610612762"),

    # Pacific Division
    ("Golden State Warriors", "GSW", "1610612744"),
    ("LA Clippers", "LAC", "1610612746"),
    ("Phoenix Suns", "PHX", "1610612756"),
    ("Sacramento Kings", "SAC", "1610612758"),

    # Southwest Division
    ("Dallas Mavericks", "DAL", "1610612742"),
    ("Houston Rockets", "HOU", "1610612745"),
    ("Memphis Grizzlies", "MEM", "1610612763"),
    ("New Orleans Pelicans", "NOP", "1610612740"),
    ("San Antonio Spurs", "SAS", "1610612759"),
]

print("=" * 80)
print("NBA ROSTER DATA PARSING STATUS")
print("=" * 80)
print("\nNote: This script requires markdown files to be present.")
print("The scraping was completed, but markdown data needs to be saved to files first.")
print("\nTeams that need parsing:")
for team_name, abbrev, team_id in teams_scraped:
    print(f"  - {team_name} ({abbrev})")

print(f"\nTotal teams to parse: {len(teams_scraped)}")
print("\nNext step: Save markdown data to files, then run parsing.")
