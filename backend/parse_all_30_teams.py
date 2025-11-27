#!/usr/bin/env python3
"""
Parse all 30 NBA team rosters from memvid_integration/scraped/nba-players/
and save to nba_data/players.json
"""
import json
import re
from pathlib import Path

SCRAPED_DIR = Path("memvid_integration/scraped/nba-players")
OUTPUT_FILE = Path("nba_data/players.json")

def parse_player_line(line: str, team_name: str, team_id: str) -> dict:
    """Parse a player line from markdown"""
    # Pattern: - Name (#Jersey, Position, Height, Weight, Age XX, X YRS PRO) - Stats
    # Example: - LeBron James (#23, Forward, 6'9", 250 lbs, Age 40, 22 YRS PRO) - 14 PPG, 10 APG, 4.5 RPG

    # Extract basic info
    match = re.match(r'-\s+([^(]+)\s+\(#(\d+),\s+([^,]+),\s+([^,]+),\s+(\d+)\s+lbs,\s+Age\s+(\d+),\s+(\d+|R)\s+YRS?\s+PRO\)', line)
    if not match:
        return None

    name, jersey, position, height, weight, age, experience = match.groups()

    # Extract stats if present
    stats_match = re.search(r'-\s+([\d.]+)\s+PPG,\s+([\d.]+)\s+APG,\s+([\d.]+)\s+RPG', line)
    if stats_match:
        ppg, apg, rpg = stats_match.groups()
    else:
        ppg, apg, rpg = 0.0, 0.0, 0.0

    # Extract GP if present
    gp_match = re.search(r'(\d+)\s+GP', line)
    gp = int(gp_match.group(1)) if gp_match else 0

    return {
        "team_id": team_id,
        "team_name": team_name,
        "player_id": str(hash(f"{name}{team_id}") % 10000000),  # Generate fake ID
        "name": name.strip(),
        "position": position.strip(),
        "jersey_number": jersey,
        "height": height.strip(),
        "weight": weight,
        "age": int(age),
        "experience": experience,
        "country": "USA",  # Default
        "ppg": float(ppg),
        "rpg": float(rpg),
        "apg": float(apg),
        "gp": gp
    }

def parse_team_file(filepath: Path) -> list:
    """Parse a team's markdown file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract team info from frontmatter
    team_match = re.search(r'team:\s+(.+)', content)
    team_id_match = re.search(r'team_id:\s+(\d+)', content)

    if not team_match or not team_id_match:
        return []

    team_name = team_match.group(1).strip()
    team_id = team_id_match.group(1).strip()

    # Parse player lines
    players = []
    for line in content.split('\n'):
        if line.strip().startswith('- ') and '(' in line:
            player = parse_player_line(line, team_name, team_id)
            if player:
                players.append(player)

    return players

def main():
    print("=" * 80)
    print("PARSING ALL 30 NBA TEAM ROSTERS")
    print("=" * 80)

    all_players = []
    team_files = sorted(SCRAPED_DIR.glob("*.md"))

    print(f"\nFound {len(team_files)} team files\n")

    for filepath in team_files:
        players = parse_team_file(filepath)
        if players:
            all_players.extend(players)
            print(f"✓ {filepath.stem:<30} {len(players):2} players")
        else:
            print(f"✗ {filepath.stem:<30} Failed to parse")

    # Save to JSON
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_players, f, indent=2)

    print(f"\n{'=' * 80}")
    print(f"✓ Saved {len(all_players)} total players to {OUTPUT_FILE}")
    print(f"{'=' * 80}")

    # Show team breakdown
    teams = {}
    for player in all_players:
        teams[player['team_name']] = teams.get(player['team_name'], 0) + 1

    print(f"\nTeam breakdown:")
    for team, count in sorted(teams.items()):
        print(f"  {team:<30} {count:2} players")

if __name__ == "__main__":
    main()
