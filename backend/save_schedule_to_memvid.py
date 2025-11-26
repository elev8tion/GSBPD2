#!/usr/bin/env python3
"""
Save NBA schedule data to Memvid for AI analysis and betting predictions.
Creates markdown files from schedule JSON that can be encoded into Memvid memory.
"""
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Directories
SCHEDULE_DIR = Path(__file__).parent / "memvid_integration" / "scraped" / "nba-schedule"
SCHEDULE_DIR.mkdir(parents=True, exist_ok=True)

# Input file
SCHEDULE_FILE = Path(__file__).parent / "nba_data" / "nba_schedule_clean.json"

def group_games_by_date(games):
    """Group games by date."""
    by_date = defaultdict(list)
    for game in games:
        by_date[game['date']].append(game)
    return dict(sorted(by_date.items()))

def group_games_by_team(games):
    """Group games by team."""
    by_team = defaultdict(list)
    for game in games:
        by_team[game['home_team']].append({**game, 'location': 'home'})
        by_team[game['away_team']].append({**game, 'location': 'away'})
    return by_team

def create_date_markdown(date, games):
    """Create markdown content for a single date's games."""
    md = f"""# NBA Games - {date}

## {len(games)} Games Scheduled

"""
    for game in sorted(games, key=lambda x: x.get('game_time', 'TBD')):
        md += f"""### {game['away_team']} @ {game['home_team']}
- **Game ID**: {game['game_id']}
- **Date**: {game['date']}
- **Time**: {game.get('game_time', 'TBD')}
- **Venue**: {game.get('venue', game['home_team'])}
- **Status**: {game.get('status', 'scheduled')}

"""
    return md

def create_team_schedule_markdown(team, games):
    """Create markdown content for a team's full schedule."""
    home_games = [g for g in games if g['location'] == 'home']
    away_games = [g for g in games if g['location'] == 'away']

    md = f"""# {team} - 2025-26 Season Schedule

## Season Overview
- **Total Games**: {len(games)}
- **Home Games**: {len(home_games)}
- **Away Games**: {len(away_games)}

## Upcoming Games

"""
    for game in sorted(games, key=lambda x: x['date'])[:20]:  # Next 20 games
        location_emoji = "🏠" if game['location'] == 'home' else "✈️"
        opponent = game['home_team'] if game['location'] == 'away' else game['away_team']
        vs_or_at = "vs" if game['location'] == 'home' else "@"

        md += f"""### {location_emoji} {game['date']} - {vs_or_at} {opponent}
- **Game ID**: {game['game_id']}
- **Time**: {game.get('game_time', 'TBD')}
- **Status**: {game.get('status', 'scheduled')}

"""
    return md

def save_schedule_to_memvid():
    """Main function to save schedule data to Memvid format."""
    print(f"📖 Loading schedule from: {SCHEDULE_FILE}")

    if not SCHEDULE_FILE.exists():
        print(f"❌ Schedule file not found: {SCHEDULE_FILE}")
        print(f"   Run clean_nba_schedule_v2.py first")
        return

    with open(SCHEDULE_FILE, 'r') as f:
        games = json.load(f)

    print(f"   Total games loaded: {len(games)}")

    # Create frontmatter timestamp
    scraped_at = datetime.now().isoformat()

    # Save by-date markdown files
    print(f"\n📅 Creating date-based schedule files...")
    games_by_date = group_games_by_date(games)

    date_count = 0
    for date, date_games in games_by_date.items():
        date_slug = date.replace('-', '_')
        filename = f"schedule_{date_slug}.md"
        filepath = SCHEDULE_DIR / filename

        frontmatter = f"""---
source: NBA Schedule
scraped_at: {scraped_at}
category: nba-schedule
date: {date}
total_games: {len(date_games)}
---

"""
        content = create_date_markdown(date, date_games)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter + content)

        date_count += 1

    print(f"   Created {date_count} date files")

    # Save by-team markdown files
    print(f"\n🏀 Creating team schedule files...")
    games_by_team = group_games_by_team(games)

    team_count = 0
    for team, team_games in games_by_team.items():
        team_slug = team.lower().replace(' ', '_').replace("'", "")
        filename = f"team_schedule_{team_slug}.md"
        filepath = SCHEDULE_DIR / filename

        frontmatter = f"""---
source: NBA Schedule
scraped_at: {scraped_at}
category: nba-team-schedules
team: {team}
total_games: {len(team_games)}
home_games: {len([g for g in team_games if g['location'] == 'home'])}
away_games: {len([g for g in team_games if g['location'] == 'away'])}
---

"""
        content = create_team_schedule_markdown(team, team_games)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter + content)

        team_count += 1

    print(f"   Created {team_count} team schedule files")

    print(f"\n✅ Schedule saved to Memvid format!")
    print(f"   Location: {SCHEDULE_DIR}")
    print(f"   Total files: {date_count + team_count}")

    # Summary
    print(f"\n📊 Summary:")
    print(f"   Date files: {date_count} (one per game date)")
    print(f"   Team files: {team_count} (full schedule per team)")
    print(f"   Ready for Memvid encoding")

    print(f"\n🔥 Next step: Encode to Memvid")
    print(f"   cd memvid_integration")
    print(f"   memvid encode scraped/nba-schedule -o ../memories/nba-schedule")

if __name__ == "__main__":
    save_schedule_to_memvid()
