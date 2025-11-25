#!/usr/bin/env python3
"""
Build NBA Games Memory
Converts teams.json standings data into markdown for Memvid encoding
"""
import json
from pathlib import Path
from datetime import datetime

# Directory setup
SOURCE_FILE = Path(__file__).parent / "nba_data" / "teams.json"
SCRAPED_DIR = Path(__file__).parent / "memvid_integration" / "scraped" / "nba-games"
SCRAPED_DIR.mkdir(parents=True, exist_ok=True)

def format_team_standings(teams_data):
    """Format team data into structured markdown."""

    # Group teams by conference
    eastern = [t for t in teams_data if t['conference'] == 'Eastern']
    western = [t for t in teams_data if t['conference'] == 'Western']

    # Sort by win percentage
    eastern.sort(key=lambda x: x['win_percentage'], reverse=True)
    western.sort(key=lambda x: x['win_percentage'], reverse=True)

    markdown = "# NBA Team Standings\n\n"
    markdown += f"Last Updated: {datetime.now().strftime('%Y-%m-%d')}\n\n"

    # Eastern Conference
    markdown += "## Eastern Conference\n\n"
    markdown += "| Rank | Team | W-L | Win% | PPG | RPG | APG | OPPG |\n"
    markdown += "|------|------|-----|------|-----|-----|-----|------|\n"

    for i, team in enumerate(eastern, 1):
        markdown += f"| {i} | {team['name']} | {team['wins']}-{team['losses']} | "
        markdown += f"{team['win_percentage']:.3f} | {team['ppg']:.1f} | "
        markdown += f"{team['rpg']:.1f} | {team['apg']:.1f} | {team['oppg']:.1f} |\n"

    markdown += "\n"

    # Western Conference
    markdown += "## Western Conference\n\n"
    markdown += "| Rank | Team | W-L | Win% | PPG | RPG | APG | OPPG |\n"
    markdown += "|------|------|-----|------|-----|-----|-----|------|\n"

    for i, team in enumerate(western, 1):
        markdown += f"| {i} | {team['name']} | {team['wins']}-{team['losses']} | "
        markdown += f"{team['win_percentage']:.3f} | {team['ppg']:.1f} | "
        markdown += f"{team['rpg']:.1f} | {team['apg']:.1f} | {team['oppg']:.1f} |\n"

    return markdown

def format_team_details(team):
    """Format individual team details."""
    markdown = f"# {team['name']} ({team['slug'].upper()})\n\n"
    markdown += f"**Conference:** {team['conference']}  \n"
    markdown += f"**Division:** {team['division']}  \n"
    markdown += f"**Record:** {team['wins']}-{team['losses']} ({team['win_percentage']:.3f})  \n\n"

    markdown += "## Team Statistics\n\n"
    markdown += f"- **Points Per Game (PPG):** {team['ppg']:.1f}\n"
    markdown += f"- **Rebounds Per Game (RPG):** {team['rpg']:.1f}\n"
    markdown += f"- **Assists Per Game (APG):** {team['apg']:.1f}\n"
    markdown += f"- **Opponent PPG:** {team['oppg']:.1f}\n"
    markdown += f"- **Point Differential:** {(team['ppg'] - team['oppg']):.1f}\n\n"

    return markdown

def save_markdown(filename, content, metadata):
    """Save markdown with YAML frontmatter."""
    filepath = SCRAPED_DIR / filename

    header = f"""---
category: nba-games
scraped_at: {datetime.now().isoformat()}
data_type: {metadata.get('data_type', 'standings')}
"""

    if 'team_name' in metadata:
        header += f"team: {metadata['team_name']}\n"
    if 'team_id' in metadata:
        header += f"team_id: {metadata['team_id']}\n"

    header += "---\n\n"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header + content)

    print(f"✓ Saved: {filename}")
    return filepath

def main():
    print("=" * 80)
    print("BUILDING NBA GAMES MEMORY")
    print("=" * 80)
    print(f"\nSource: {SOURCE_FILE}")
    print(f"Target: {SCRAPED_DIR}\n")

    # Load teams data
    with open(SOURCE_FILE, 'r') as f:
        teams_data = json.load(f)

    print(f"Loaded {len(teams_data)} teams\n")

    # 1. Save overall standings
    standings_md = format_team_standings(teams_data)
    save_markdown('nba_standings.md', standings_md, {'data_type': 'standings'})

    # 2. Save individual team details
    for team in teams_data:
        team_md = format_team_details(team)
        filename = f"{team['slug']}_stats.md"
        save_markdown(filename, team_md, {
            'data_type': 'team_stats',
            'team_name': team['name'],
            'team_id': team['team_id']
        })

    print(f"\n✅ Successfully created {len(teams_data) + 1} markdown files")
    print(f"\nNext step:")
    print(f"  python memvid_integration/text_pipeline/encode_to_memvid.py --name nba-games")

if __name__ == "__main__":
    main()
