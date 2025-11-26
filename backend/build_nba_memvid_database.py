#!/usr/bin/env python3
"""
Build NBA Memvid Database - Complete Pipeline
Scrapes all 30 NBA teams → Parses data → Stores in Memvid
"""
import json
from pathlib import Path
from parse_roster_v2 import parse_roster_markdown_v2

# All 30 NBA teams
NBA_TEAMS = [
    ("Boston Celtics", "1610612738", "https://www.nba.com/celtics/roster"),
    ("Brooklyn Nets", "1610612751", "https://www.nba.com/nets/roster"),
    ("New York Knicks", "1610612752", "https://www.nba.com/knicks/roster"),
    ("Philadelphia 76ers", "1610612755", "https://www.nba.com/sixers/roster"),
    ("Toronto Raptors", "1610612761", "https://www.nba.com/raptors/roster"),
    ("Chicago Bulls", "1610612741", "https://www.nba.com/bulls/roster"),
    ("Cleveland Cavaliers", "1610612739", "https://www.nba.com/cavaliers/roster"),
    ("Detroit Pistons", "1610612765", "https://www.nba.com/pistons/roster"),
    ("Indiana Pacers", "1610612754", "https://www.nba.com/pacers/roster"),
    ("Milwaukee Bucks", "1610612749", "https://www.nba.com/bucks/roster"),
    ("Atlanta Hawks", "1610612737", "https://www.nba.com/hawks/roster"),
    ("Charlotte Hornets", "1610612766", "https://www.nba.com/hornets/roster"),
    ("Miami Heat", "1610612748", "https://www.nba.com/heat/roster"),
    ("Orlando Magic", "1610612753", "https://www.nba.com/magic/roster"),
    ("Washington Wizards", "1610612764", "https://www.nba.com/wizards/roster"),
    ("Denver Nuggets", "1610612743", "https://www.nba.com/nuggets/roster"),
    ("Minnesota Timberwolves", "1610612750", "https://www.nba.com/timberwolves/roster"),
    ("Oklahoma City Thunder", "1610612760", "https://www.nba.com/thunder/roster"),
    ("Portland Trail Blazers", "1610612757", "https://www.nba.com/blazers/roster"),
    ("Utah Jazz", "1610612762", "https://www.nba.com/jazz/roster"),
    ("Golden State Warriors", "1610612744", "https://www.nba.com/warriors/roster"),
    ("LA Clippers", "1610612746", "https://www.nba.com/clippers/roster"),
    ("Los Angeles Lakers", "1610612747", "https://www.nba.com/lakers/roster"),
    ("Phoenix Suns", "1610612756", "https://www.nba.com/suns/roster"),
    ("Sacramento Kings", "1610612758", "https://www.nba.com/kings/roster"),
    ("Dallas Mavericks", "1610612742", "https://www.nba.com/mavericks/roster"),
    ("Houston Rockets", "1610612745", "https://www.nba.com/rockets/roster"),
    ("Memphis Grizzlies", "1610612763", "https://www.nba.com/grizzlies/roster"),
    ("New Orleans Pelicans", "1610612740", "https://www.nba.com/pelicans/roster"),
    ("San Antonio Spurs", "1610612759", "https://www.nba.com/spurs/roster"),
]

def convert_player_to_text(player: dict) -> str:
    """Convert player dict to text format for Memvid"""
    return f"""
PLAYER: {player['name']}
TEAM: {player['team_name']} (ID: {player['team_id']})
POSITION: {player['position']}
JERSEY: #{player['jersey_number']}
HEIGHT: {player['height']}
WEIGHT: {player['weight']}
AGE: {player['age']}
EXPERIENCE: {player['experience']} years
COUNTRY: {player['country']}
STATS (Current Season):
  - Games Played: {player['gp']}
  - PPG: {player['ppg']}
  - RPG: {player['rpg']}
  - APG: {player['apg']}
PLAYER_ID: {player['player_id']}
"""

def main():
    print("=" * 80)
    print("NBA MEMVID DATABASE BUILDER")
    print("=" * 80)
    print("\nThis script will:")
    print("  1. Scrape all 30 NBA team rosters using Firecrawl")
    print("  2. Parse player data from markdown")
    print("  3. Convert to text format for Memvid")
    print("  4. Create nba-players memory")
    print("\nNote: Firecrawl scraping will be done via Claude Code with Firecrawl MCP tool")
    print("\nTeams to scrape:")
    for i, (name, team_id, url) in enumerate(NBA_TEAMS, 1):
        print(f"  {i}. {name}")

    print(f"\nTotal: {len(NBA_TEAMS)} teams")
    print("\nReady to start scraping...")

if __name__ == "__main__":
    main()
