#!/usr/bin/env python3
"""Add Dallas Mavericks to players.json"""
import json
from pathlib import Path
from parse_roster_v2 import parse_roster_markdown_v2

# Mavericks markdown from Firecrawl scraping
MAVERICKS_MD = """## Roster

[Team Profile](https://www.nba.com/team/1610612742)

* * *

## Players

![Danté Exum headshot](https://cdn.nba.com/headshots/nba/latest/260x190/203957.png)

Danté

Exum

Guard

0

Height

6'5"

Weight

214 lbs

Age

30

Years Pro

9

Country

Australia

![Danté Exum headshot](https://cdn.nba.com/headshots/nba/latest/1040x760/203957.png)

Season

GP

-

PPG

-

APG

-

RPG

-

Height

6'5"

Weight

214 lbs

Age

30

Years Pro

9

Country

Australia

[Bio](https://www.nba.com/player/203957/dant%C3%A9-exum/bio) [Shop](https://mavsshop.com/collections/dante-exum)

![Max Christie headshot](https://cdn.nba.com/headshots/nba/latest/260x190/1631108.png)

Max

Christie

Guard

00

Height

6'5"

Weight

190 lbs

Age

22

Years Pro

3

Country

USA

![Max Christie headshot](https://cdn.nba.com/headshots/nba/latest/1040x760/1631108.png)

Season

GP

19

PPG

12.8

APG

2.2

RPG

3.6"""

# Continue with all Mavericks players...

def main():
    # Load existing players
    players_file = Path(__file__).parent / "nba_data" / "players.json"
    with open(players_file, 'r') as f:
        all_players = json.load(f)

    # Check if Mavericks already added
    if any(p['team_id'] == '1610612742' for p in all_players):
        print("✗ Mavericks already in database")
        return

    # Parse Mavericks
    mavs_players = parse_roster_markdown_v2(MAVERICKS_MD, "1610612742", "Dallas Mavericks")

    if mavs_players:
        all_players.extend(mavs_players)
        with open(players_file, 'w') as f:
            json.dump(all_players, f, indent=2)
        print(f"✓ Added Dallas Mavericks: {len(mavs_players)} players")
        print(f"✓ Total players: {len(all_players)}")
    else:
        print("✗ Failed to parse Mavericks")

if __name__ == "__main__":
    main()
