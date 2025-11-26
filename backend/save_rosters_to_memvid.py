#!/usr/bin/env python3
"""
Save NBA roster data to Memvid for AI analysis and predictions.
Creates markdown files from roster JSON that can be encoded into Memvid memory.
"""
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Directories
TEAMS_DIR = Path(__file__).parent / "memvid_integration" / "scraped" / "nba-teams"
PLAYERS_DIR = Path(__file__).parent / "memvid_integration" / "scraped" / "nba-players"
TEAMS_DIR.mkdir(parents=True, exist_ok=True)
PLAYERS_DIR.mkdir(parents=True, exist_ok=True)

def create_team_markdown(team: Dict) -> str:
    """Create markdown content for a team's profile and stats"""

    team_name = team['team']
    stats = team.get('team_stats', {})
    players = team.get('players', [])

    # Build roster summary
    roster_summary = "\n".join([
        f"- **{p['name']}** ({p.get('position', 'N/A')}) - "
        f"{p.get('stats', {}).get('pts', 'N/A')} PPG, "
        f"{p.get('stats', {}).get('reb', 'N/A')} RPG, "
        f"{p.get('stats', {}).get('ast', 'N/A')} APG"
        for p in players[:10]  # Top 10 players
    ])

    md = f"""# {team_name}

## Team Overview
- **Roster URL:** {team.get('roster_url', 'N/A')}
- **Stats URL:** {team.get('stats_url', 'N/A')}
- **Total Players:** {len(players)}

## Team Statistics (Season Averages)
- **Games Played:** {stats.get('gp', 'N/A')}
- **Points Per Game:** {stats.get('pts', 'N/A')}
- **Offensive Rebounds:** {stats.get('or', 'N/A')}
- **Defensive Rebounds:** {stats.get('dr', 'N/A')}
- **Total Rebounds:** {stats.get('reb', 'N/A')}
- **Assists:** {stats.get('ast', 'N/A')}
- **Steals:** {stats.get('stl', 'N/A')}
- **Blocks:** {stats.get('blk', 'N/A')}
- **Turnovers:** {stats.get('to', 'N/A')}
- **Personal Fouls:** {stats.get('pf', 'N/A')}
- **Assist/Turnover Ratio:** {stats.get('ast/to', 'N/A')}

## Key Players (Top 10)
{roster_summary}

## Full Roster
Total of {len(players)} players on active roster.

## Analysis Context
The {team_name} average {stats.get('pts', 'N/A')} points per game with {stats.get('reb', 'N/A')} rebounds and {stats.get('ast', 'N/A')} assists.
Their assist-to-turnover ratio of {stats.get('ast/to', 'N/A')} indicates their ball movement and turnover rate.
"""

    return md

def create_player_markdown(player: Dict, team_name: str) -> str:
    """Create markdown content for a player's profile and stats"""

    name = player['name']
    stats = player.get('stats', {})

    md = f"""# {name}

## Player Information
- **Team:** {team_name}
- **Position:** {player.get('position', 'N/A')}
- **Age:** {player.get('age', 'N/A')}
- **Height:** {player.get('height', 'N/A')}
- **Weight:** {player.get('weight', 'N/A')}
- **College:** {player.get('college', 'N/A')}
- **Salary:** {player.get('salary', 'N/A')}
- **Profile URL:** {player.get('link', 'N/A')}

## Season Statistics
- **Games Played:** {stats.get('gp', 'N/A')}
- **Games Started:** {stats.get('gs', 'N/A')}
- **Minutes Per Game:** {stats.get('min', 'N/A')}
- **Points Per Game:** {stats.get('pts', 'N/A')}
- **Offensive Rebounds:** {stats.get('or', 'N/A')}
- **Defensive Rebounds:** {stats.get('dr', 'N/A')}
- **Total Rebounds:** {stats.get('reb', 'N/A')}
- **Assists:** {stats.get('ast', 'N/A')}
- **Steals:** {stats.get('stl', 'N/A')}
- **Blocks:** {stats.get('blk', 'N/A')}
- **Turnovers:** {stats.get('to', 'N/A')}
- **Personal Fouls:** {stats.get('pf', 'N/A')}
- **Assist/Turnover Ratio:** {stats.get('ast/to', 'N/A')}

## Performance Analysis
{name} averages {stats.get('pts', 'N/A')} points, {stats.get('reb', 'N/A')} rebounds, and {stats.get('ast', 'N/A')} assists per game.
Playing {stats.get('min', 'N/A')} minutes per game, they contribute significantly to the {team_name}'s performance.
"""

    return md

def save_team_to_memvid(team: Dict) -> Path:
    """Save a single team's data to Memvid scraped directory"""

    team_name = team['team']
    team_slug = team_name.lower().replace(' ', '_').replace('76ers', 'sixers')

    filename = f"{team_slug}.md"
    filepath = TEAMS_DIR / filename

    # Create frontmatter
    frontmatter = f"""---
source: ESPN
scraped_at: {datetime.now().isoformat()}
category: nba-teams
team: {team_name}
roster_url: {team.get('roster_url', '')}
stats_url: {team.get('stats_url', '')}
total_players: {len(team.get('players', []))}
---

"""

    # Generate content
    content = create_team_markdown(team)

    # Save file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)

    print(f"✓ Saved team: {filename}")
    return filepath

def save_player_to_memvid(player: Dict, team_name: str) -> Path:
    """Save a single player's data to Memvid scraped directory"""

    player_name = player['name']
    player_slug = player_name.lower().replace(' ', '_').replace("'", '').replace('.', '')

    filename = f"{player_slug}_{team_name.lower().replace(' ', '_')}.md"
    filepath = PLAYERS_DIR / filename

    # Create frontmatter
    frontmatter = f"""---
source: ESPN
scraped_at: {datetime.now().isoformat()}
category: nba-players
player: {player_name}
team: {team_name}
position: {player.get('position', '')}
age: {player.get('age', '')}
---

"""

    # Generate content
    content = create_player_markdown(player, team_name)

    # Save file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)

    return filepath

def save_all_rosters_to_memvid(rosters: List[Dict]) -> tuple:
    """Save all rosters to Memvid format"""
    print("=" * 80)
    print("SAVING NBA ROSTERS TO MEMVID")
    print("=" * 80)
    print(f"\nTeams directory: {TEAMS_DIR}")
    print(f"Players directory: {PLAYERS_DIR}")
    print(f"Total teams: {len(rosters)}\n")

    teams_saved = 0
    players_saved = 0

    for team in rosters:
        try:
            # Save team profile
            save_team_to_memvid(team)
            teams_saved += 1

            # Save all players for this team
            team_name = team['team']
            for player in team.get('players', []):
                try:
                    save_player_to_memvid(player, team_name)
                    players_saved += 1
                except Exception as e:
                    print(f"  ✗ Error saving player {player.get('name', 'Unknown')}: {e}")

        except Exception as e:
            print(f"✗ Error saving team {team.get('team', 'Unknown')}: {e}")

    print(f"\n{'=' * 80}")
    print(f"✓ Saved {teams_saved}/{len(rosters)} teams")
    print(f"✓ Saved {players_saved} total players")
    print(f"{'=' * 80}")
    print("\nNext steps:")
    print("1. Encode teams: python memvid_integration/text_pipeline/encode_to_memvid.py --name nba-teams")
    print("2. Encode players: python memvid_integration/text_pipeline/encode_to_memvid.py --name nba-players")
    print("3. These will create Memvid memories for AI-powered roster analysis")

    return teams_saved, players_saved

def load_rosters_from_json() -> List[Dict]:
    """Load rosters from the JSON file"""
    roster_file = Path(__file__).parent / "nba_data" / "nba_rosters.json"

    if not roster_file.exists():
        print("⚠ No roster file found. Expected: backend/nba_data/nba_rosters.json")
        return []

    with open(roster_file, 'r') as f:
        rosters = json.load(f)
        return rosters

def main():
    """Main execution"""
    # Load rosters from JSON
    rosters = load_rosters_from_json()

    if not rosters:
        print("No rosters to save. Exiting.")
        return

    # Save to Memvid format
    save_all_rosters_to_memvid(rosters)

if __name__ == "__main__":
    main()
