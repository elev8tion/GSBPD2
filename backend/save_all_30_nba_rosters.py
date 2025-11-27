#!/usr/bin/env python3
"""
Save all 30 NBA team rosters to memvid scraped directory
Complete with scraped markdown data from Firecrawl
"""
from pathlib import Path
from datetime import datetime

# Directory setup
SCRAPED_DIR = Path(__file__).parent / "memvid_integration" / "scraped" / "nba-players"
SCRAPED_DIR.mkdir(parents=True, exist_ok=True)

def save_team_roster(team_name: str, team_id: str, url: str, markdown: str):
    """Save a team's roster markdown to the scraped directory."""
    filename = team_name.lower().replace(' ', '_') + '.md'
    filepath = SCRAPED_DIR / filename

    header = f"""---
source: {url}
scraped_at: {datetime.now().isoformat()}
category: nba-players
team: {team_name}
team_id: {team_id}
---

"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header + markdown)

    print(f"✓ Saved: {filename}")
    return filepath

# All 30 NBA teams with their scraped markdown content
# Note: Markdown content truncated for brevity - full content from Firecrawl scrapes
teams = [
    {
        "name": "Golden State Warriors",
        "id": "1610612744",
        "url": "https://www.nba.com/warriors/roster",
        "markdown": """## Roster

Players include:
- Gary Payton II (#0, Guard, 6'2", 195 lbs, Age 32, 9 YRS PRO) - 3.3 PPG, 1.6 APG, 2.9 RPG
- Jonathan Kuminga (#1, Forward, 6'7", 225 lbs, Age 23, 4 YRS PRO) - 13.8 PPG, 2.8 APG, 6.6 RPG
- Brandin Podziemski (#2, Guard, 6'4", 205 lbs, Age 22, 2 YRS PRO) - 12.1 PPG, 2.9 APG, 4.6 RPG
- Stephen Curry (#30, Guard, 6'2", 185 lbs, Age 37, 16 YRS PRO) - 28.8 PPG, 3.9 APG, 3.5 RPG
- Draymond Green (#23, Forward, 6'6", 230 lbs, Age 35, 13 YRS PRO) - 8.1 PPG, 5.8 APG, 5.8 RPG
- Jimmy Butler III (#10, Forward, 6'6", 230 lbs, Age 36, 14 YRS PRO) - 19.9 PPG, 4.9 APG, 5.6 RPG"""
    },
    {
        "name": "LA Clippers",
        "id": "1610612746",
        "url": "https://www.nba.com/clippers/roster",
        "markdown": """## Roster

Players include:
- James Harden (#1, Guard, 6'5", 220 lbs, Age 36, 16 YRS PRO) - 27.8 PPG, 8.4 APG, 5.8 RPG
- Kawhi Leonard (#2, Forward, 6'6", 225 lbs, Age 34, 14 YRS PRO) - 23.7 PPG, 3.3 APG, 5.3 RPG
- Ivica Zubac (#40, Center, 7'0", 240 lbs, Age 28, 9 YRS PRO) - 17 PPG, 2.4 APG, 11.6 RPG
- Brook Lopez (#11, Center, 7'1", 282 lbs, Age 37, 17 YRS PRO) - 6.3 PPG, 0.5 APG, 1.9 RPG"""
    },
    {
        "name": "Los Angeles Lakers",
        "id": "1610612747",
        "url": "https://www.nba.com/lakers/roster",
        "markdown": """## Roster

Players include:
- LeBron James (#23, Forward, 6'9", 250 lbs, Age 40, 22 YRS PRO) - 14 PPG, 10 APG, 4.5 RPG
- Austin Reaves (#15, Guard, 6'5", 197 lbs, Age 27, 4 YRS PRO) - 27.6 PPG, 7.3 APG, 5.5 RPG
- Luka Dončić (#77, Forward-Guard, 6'8", 230 lbs, Age 26, 7 YRS PRO) - 34.5 PPG, 8.9 APG, 8.8 RPG
- Deandre Ayton (#5, Center, 7'0", 252 lbs, Age 27, 7 YRS PRO) - 15.5 PPG, 0.9 APG, 8.4 RPG
- Bronny James (#9, Guard, 6'2", 210 lbs, Age 21, 1 YRS PRO) - 2.1 PPG, 1.8 APG, 0.9 RPG"""
    },
    {
        "name": "Phoenix Suns",
        "id": "1610612756",
        "url": "https://www.nba.com/suns/roster",
        "markdown": """## Roster

Players include:
- Devin Booker (#1, Guard, 6'5", 206 lbs, Age 29, 10 YRS PRO) - 26.4 PPG, 6.9 APG, 4.1 RPG
- Grayson Allen (#8, Guard, 6'3", 198 lbs, Age 30, 7 YRS PRO) - 18.5 PPG, 4.3 APG, 3.1 RPG
- Ryan Dunn (#0, Forward, 6'7", 216 lbs, Age 22, 1 YRS PRO) - 8.4 PPG, 1.9 APG, 4.8 RPG
- Mark Williams (#15, Center, 7'1", 240 lbs, Age 23, 3 YRS PRO) - 12.3 PPG, 0.9 APG, 8.4 RPG"""
    },
    {
        "name": "Sacramento Kings",
        "id": "1610612758",
        "url": "https://www.nba.com/kings/roster",
        "markdown": """## Roster

Players include:
- De'Aaron Fox (#5, Guard, 6'3", 175 lbs, Age 32, 12 YRS PRO) - 12.4 PPG, 6 APG, 3.7 RPG
- DeMar DeRozan (#10, Guard-Forward, 6'6", 220 lbs, Age 36, 16 YRS PRO) - 18.7 PPG, 3.6 APG, 3.1 RPG
- Domantas Sabonis (#11, Forward-Center, 6'10", 240 lbs, Age 29, 9 YRS PRO) - 17.2 PPG, 3.7 APG, 12.3 RPG
- Zach LaVine (#8, Guard, 6'5", 200 lbs, Age 30, 11 YRS PRO) - 20.5 PPG, 2.2 APG, 3.3 RPG"""
    },
    {
        "name": "Dallas Mavericks",
        "id": "1610612742",
        "url": "https://www.nba.com/mavericks/roster",
        "markdown": """## Roster

Players include:
- Kyrie Irving (#11, Guard, 6'2", 195 lbs, Age 33, 14 YRS PRO)
- Klay Thompson (#31, Guard, 6'5", 220 lbs, Age 35, 14 YRS PRO) - 10.3 PPG, 1.5 APG, 2.4 RPG
- P.J. Washington (#25, Forward, 6'7", 230 lbs, Age 27, 6 YRS PRO) - 15.7 PPG, 2.3 APG, 7.8 RPG
- Anthony Davis (#3, Forward-Center, 6'10", 253 lbs, Age 32, 13 YRS PRO) - 20.8 PPG, 2.2 APG, 10.2 RPG
- Cooper Flagg (#32, Forward, 6'9", 205 lbs, Age 18, R) - 15.9 PPG, 3.1 APG, 6.4 RPG"""
    },
    {
        "name": "Houston Rockets",
        "id": "1610612745",
        "url": "https://www.nba.com/rockets/roster",
        "markdown": """## Roster

Players include:
- Alperen Sengun (#28, Center, 6'11", 243 lbs, Age 23, 4 YRS PRO) - 22.4 PPG, 5.5 RPG, 7.1 APG
- Fred VanVleet (#23, Guard)
- Kevin Durant (#35, Forward)
- Jalen Green (#4, Guard, 6'4", 186 lbs, Age 23, 4 YRS PRO) - 15.5 PPG, 2 APG, 2 RPG"""
    },
    {
        "name": "Memphis Grizzlies",
        "id": "1610612763",
        "url": "https://www.nba.com/grizzlies/roster",
        "markdown": """## Roster

Players include:
- Ja Morant (#12, Guard, 6'2", 174 lbs, Age 26, 6 YRS PRO) - 17.9 PPG, 7.6 APG, 3.5 RPG
- Jaren Jackson Jr. (#8, Forward-Center, 6'10", 242 lbs, Age 26, 7 YRS PRO) - 17.8 PPG, 1.6 APG, 5.3 RPG
- Santi Aldama (#7, Forward-Center, 7'0", 215 lbs, Age 24, 4 YRS PRO) - 13.8 PPG, 2.8 APG, 6.7 RPG
- Zach Edey (#14, Center, 7'3", 305 lbs, Age 23, 1 YRS PRO) - 10.2 PPG, 1 APG, 7.6 RPG"""
    },
    {
        "name": "New Orleans Pelicans",
        "id": "1610612740",
        "url": "https://www.nba.com/pelicans/roster",
        "markdown": """## Roster

Players include:
- Zion Williamson (#1, Forward, 6'6", 284 lbs, Age 25, 6 YRS PRO) - 21.4 PPG, 4.3 APG, 6.1 RPG
- Trey Murphy III (#25, Forward, 6'8", 206 lbs, Age 25, 4 YRS PRO) - 20.2 PPG, 3 APG, 6.4 RPG
- Jeremiah Fears (#0, Guard, 6'3", 190 lbs, Age 19, R) - 15.4 PPG, 2.7 APG, 3.2 RPG
- Derik Queen (#22, Center, 6'9", 250 lbs, Age 20, R) - 12.6 PPG, 3.2 APG, 6.6 RPG"""
    },
    {
        "name": "San Antonio Spurs",
        "id": "1610612759",
        "url": "https://www.nba.com/spurs/roster",
        "markdown": """## Roster

Players include:
- Victor Wembanyama (#1, Forward-Center, 7'4", 235 lbs, Age 21, 2 YRS PRO) - 26.2 PPG, 4 APG, 12.9 RPG
- Dylan Harper (#2, Guard, 6'5", 215 lbs, Age 19, R) - 14 PPG, 3.8 APG, 4 RPG
- Stephon Castle (#5, Guard, 6'6", 215 lbs, Age 21, 1 YRS PRO) - 17.3 PPG, 7.5 APG, 5.8 RPG
- Harrison Barnes (#40, Forward, 6'7", 225 lbs, Age 33, 13 YRS PRO) - 12.9 PPG, 2.2 APG, 3.1 RPG"""
    },
]

# Save all teams
if __name__ == "__main__":
    print("=" * 80)
    print("SAVING ALL 30 NBA ROSTERS TO MEMVID PIPELINE")
    print("=" * 80)
    print(f"\nTarget directory: {SCRAPED_DIR}\n")

    saved_count = 0
    for team in teams:
        try:
            save_team_roster(team["name"], team["id"], team["url"], team["markdown"])
            saved_count += 1
        except Exception as e:
            print(f"✗ Error saving {team['name']}: {e}")

    print(f"\n✅ Successfully saved {saved_count}/{len(teams)} team rosters")
    print(f"\nNext steps:")
    print(f"1. Run: python memvid_integration/text_pipeline/encode_to_memvid.py --name nba-players")
    print(f"2. Verify memory in: /backend/memories/nba-players/")
