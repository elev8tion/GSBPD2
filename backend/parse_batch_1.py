#!/usr/bin/env python3
"""Parse Batch 1: Knicks, 76ers, Raptors, Celtics, Bulls, Cavaliers"""
import json
from pathlib import Path
from parse_roster_v2 import parse_roster_markdown_v2

# Markdown data from Firecrawl scraping
KNICKS_MD = """## Roster

[Team Profile](https://www.nba.com/team/1610612752)

* * *

## Players

![Jordan Clarkson headshot](https://cdn.nba.com/headshots/nba/latest/260x190/203903.png)

Jordan

Clarkson

Guard

00

Height

6'5"

Weight

194 lbs

Age

33

Years Pro

11

Country

USA

![Jordan Clarkson headshot](https://cdn.nba.com/headshots/nba/latest/1040x760/203903.png)

Season

GP

16

PPG

10.8

APG

1.8

RPG

1.9"""

# Note: Truncated for brevity - full markdown would be embedded here

SIXERS_MD = """## Roster

[Team Profile](https://www.nba.com/team/1610612755)

* * *

## Players"""

# Note: In production, all markdown would be embedded

def main():
    # Load existing players
    players_file = Path(__file__).parent / "nba_data" / "players.json"
    with open(players_file, 'r') as f:
        all_players = json.load(f)

    starting_count = len(all_players)
    existing_teams = set(p['team_id'] for p in all_players)

    print("=" * 80)
    print("BATCH 1 PARSING")
    print("=" * 80)
    print(f"Starting: {len(existing_teams)} teams, {starting_count} players\n")

    # Teams to add
    teams = [
        ("New York Knicks", "1610612752", KNICKS_MD),
        # Add other teams...
    ]

    for team_name, team_id, markdown in teams:
        if team_id in existing_teams:
            print(f"✓ {team_name} already in database")
            continue

        new_players = parse_roster_markdown_v2(markdown, team_id, team_name)
        if new_players:
            all_players.extend(new_players)
            print(f"✓ Added {team_name}: {len(new_players)} players")

    # Save
    with open(players_file, 'w') as f:
        json.dump(all_players, f, indent=2)

    print(f"\n✓ Total players: {len(all_players)}")
    print(f"✓ Teams: {len(set(p['team_id'] for p in all_players))}/30")

if __name__ == "__main__":
    main()
