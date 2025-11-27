#!/usr/bin/env python3
"""
Re-scrape all remaining NBA teams and parse to players.json
Uses Firecrawl cache for fast retrieval, then parses all teams
"""
import json
from pathlib import Path

# Teams that need to be added (all except Lakers and Nets)
TEAMS_TO_ADD = [
    ("New York Knicks", "NYK", "1610612752", "https://www.nba.com/knicks/roster"),
    ("Philadelphia 76ers", "PHI", "1610612755", "https://www.nba.com/sixers/roster"),
    ("Toronto Raptors", "TOR", "1610612761", "https://www.nba.com/raptors/roster"),
    ("Boston Celtics", "BOS", "1610612738", "https://www.nba.com/celtics/roster"),
    ("Chicago Bulls", "CHI", "1610612741", "https://www.nba.com/bulls/roster"),
    ("Cleveland Cavaliers", "CLE", "1610612739", "https://www.nba.com/cavaliers/roster"),
    ("Detroit Pistons", "DET", "1610612765", "https://www.nba.com/pistons/roster"),
    ("Indiana Pacers", "IND", "1610612754", "https://www.nba.com/pacers/roster"),
    ("Milwaukee Bucks", "MIL", "1610612749", "https://www.nba.com/bucks/roster"),
    ("Atlanta Hawks", "ATL", "1610612737", "https://www.nba.com/hawks/roster"),
    ("Charlotte Hornets", "CHA", "1610612766", "https://www.nba.com/hornets/roster"),
    ("Miami Heat", "MIA", "1610612748", "https://www.nba.com/heat/roster"),
    ("Orlando Magic", "ORL", "1610612753", "https://www.nba.com/magic/roster"),
    ("Washington Wizards", "WAS", "1610612764", "https://www.nba.com/wizards/roster"),
    ("Denver Nuggets", "DEN", "1610612743", "https://www.nba.com/nuggets/roster"),
    ("Minnesota Timberwolves", "MIN", "1610612750", "https://www.nba.com/timberwolves/roster"),
    ("Oklahoma City Thunder", "OKC", "1610612760", "https://www.nba.com/thunder/roster"),
    ("Portland Trail Blazers", "POR", "1610612757", "https://www.nba.com/blazers/roster"),
    ("Utah Jazz", "UTA", "1610612762", "https://www.nba.com/jazz/roster"),
    ("Golden State Warriors", "GSW", "1610612744", "https://www.nba.com/warriors/roster"),
    ("LA Clippers", "LAC", "1610612746", "https://www.nba.com/clippers/roster"),
    ("Phoenix Suns", "PHX", "1610612756", "https://www.nba.com/suns/roster"),
    ("Sacramento Kings", "SAC", "1610612758", "https://www.nba.com/kings/roster"),
    ("Dallas Mavericks", "DAL", "1610612742", "https://www.nba.com/mavericks/roster"),
    ("Houston Rockets", "HOU", "1610612745", "https://www.nba.com/rockets/roster"),
    ("Memphis Grizzlies", "MEM", "1610612763", "https://www.nba.com/grizzlies/roster"),
    ("New Orleans Pelicans", "NOP", "1610612740", "https://www.nba.com/pelicans/roster"),
    ("San Antonio Spurs", "SAS", "1610612759", "https://www.nba.com/spurs/roster"),
]

print("=" * 80)
print("RE-SCRAPE AND PARSE ALL REMAINING NBA TEAMS")
print("=" * 80)
print(f"\nTeams to process: {len(TEAMS_TO_ADD)}")
print("\nThis script requires Firecrawl MCP tool access via Claude.")
print("Please run the scraping through Claude Code interface.")
print("\nTeams list:")
for team_name, abbrev, team_id, url in TEAMS_TO_ADD:
    print(f"  - {team_name} ({abbrev})")
