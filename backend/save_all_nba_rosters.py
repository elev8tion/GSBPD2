#!/usr/bin/env python3
"""
Save all 30 NBA team rosters to the memvid scraped directory
"""
from pathlib import Path
from datetime import datetime

# Directory setup
SCRAPED_DIR = Path(__file__).parent / "memvid_integration" / "scraped" / "nba-players"
SCRAPED_DIR.mkdir(parents=True, exist_ok=True)

# All 30 NBA teams with their data
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

def save_team_roster(team_name: str, team_id: str, url: str, markdown: str):
    """Save a team's roster markdown to the scraped directory."""
    # Sanitize filename
    filename = team_name.lower().replace(' ', '_') + '.md'
    filepath = SCRAPED_DIR / filename

    # Create frontmatter
    header = f"""---
source: {url}
scraped_at: {datetime.now().isoformat()}
category: nba-players
team: {team_name}
team_id: {team_id}
---

"""

    # Save file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header + markdown)

    print(f"✓ Saved: {filename}")
    return filepath

def main():
    print("=" * 80)
    print("READY TO SAVE NBA ROSTER DATA")
    print("=" * 80)
    print(f"\nTarget directory: {SCRAPED_DIR}")
    print(f"Total teams to process: {len(NBA_TEAMS)}")
    print("\nNote: Markdown content needs to be provided from Firecrawl scrapes")
    print("\nRun this after scraping is complete to save all data.")

if __name__ == "__main__":
    main()
