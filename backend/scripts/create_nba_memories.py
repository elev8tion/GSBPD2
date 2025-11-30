#!/usr/bin/env python3
"""
Create Kre8VidMems Memories from NBA Data

Creates 5 semantic search memories:
1. nba-teams-2025 - Team rosters and info
2. nba-player-gamelogs-2025 - Player game logs
3. nba-player-profiles-2025 - Player bios and career stats
4. nba-schedule-2025 - Season schedule
5. nba-season-averages-2025 - Player season averages

Usage:
    python scripts/create_nba_memories.py
"""

import sys
import sqlite3
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.knowledge_base import KnowledgeBaseService
from src.services.nba_stats_collector import NBAStatsCollector


def create_temp_docs_from_db(db_path: Path, query: str, output_dir: Path, doc_formatter) -> int:
    """
    Create temporary text documents from database query results

    Args:
        db_path: Path to SQLite database
        query: SQL query to run
        output_dir: Directory to save documents
        doc_formatter: Function to format each row as a document

    Returns:
        Number of documents created
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Access columns by name
    cursor = conn.cursor()

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    for i, row in enumerate(rows):
        doc_content = doc_formatter(dict(row))
        doc_path = output_dir / f"doc_{i:05d}.txt"
        with open(doc_path, 'w') as f:
            f.write(doc_content)

    return len(rows)


def main():
    print("="*80)
    print("  NBA KRE8VIDMEMS MEMORY CREATION")
    print("="*80)
    print()

    collector = NBAStatsCollector()
    kb_service = KnowledgeBaseService()

    temp_docs_dir = Path("./temp_nba_docs")
    temp_docs_dir.mkdir(exist_ok=True)

    # ==========================================
    # MEMORY 1: NBA Teams & Rosters
    # ==========================================
    print("\n📦 Memory 1: NBA Teams & Rosters")
    print("-" * 80)

    teams_dir = temp_docs_dir / "teams"

    def format_team_roster(row):
        return f"""NBA Team: {row['full_name']}
City: {row['city']}
Conference: {row.get('conference', 'Unknown')}
Player: {row['player_name']}
Position: {row['position']}
Jersey: #{row['jersey_number']}
Height: {row['height']}
Weight: {row['weight']}
"""

    query = '''
    SELECT
        t.full_name, t.city, t.conference,
        r.full_name as player_name, r.position, r.jersey_number, r.height, r.weight
    FROM teams t
    JOIN rosters r ON t.team_id = r.team_id
    WHERE r.season = '2025-26'
    ORDER BY t.full_name, r.full_name
    '''

    num_docs = create_temp_docs_from_db(collector.teams_db, query, teams_dir, format_team_roster)
    print(f"  Created {num_docs} roster documents")

    result = kb_service.create_memory_from_text("nba-teams-2025", str(teams_dir), sport="nba")
    print(f"  {result['message']}")

    # ==========================================
    # MEMORY 2: Player Game Logs
    # ==========================================
    print("\n📊 Memory 2: Player Game Logs")
    print("-" * 80)

    gamelogs_dir = temp_docs_dir / "gamelogs"

    def format_gamelog(row):
        return f"""Player: {row['player_name']}
Game: {row['matchup']} on {row['game_date']}
Stats: {row['pts']} PTS, {row['reb']} REB, {row['ast']} AST
Minutes: {row['min']}
Shooting: {row['fgm']}/{row['fga']} FG, {row['fg3m']}/{row['fg3a']} 3PT, {row['ftm']}/{row['fta']} FT
Defense: {row['stl']} STL, {row['blk']} BLK
"""

    query = '''
    SELECT player_name, game_date, matchup, pts, reb, ast, min,
           fgm, fga, fg3m, fg3a, ftm, fta, stl, blk
    FROM game_logs
    ORDER BY game_date DESC
    LIMIT 5000
    '''

    num_docs = create_temp_docs_from_db(collector.stats_db, query, gamelogs_dir, format_gamelog)
    print(f"  Created {num_docs} game log documents")

    result = kb_service.create_memory_from_text("nba-player-gamelogs-2025", str(gamelogs_dir), sport="nba")
    print(f"  {result['message']}")

    # ==========================================
    # MEMORY 3: Player Profiles
    # ==========================================
    print("\n👤 Memory 3: Player Profiles")
    print("-" * 80)

    profiles_dir = temp_docs_dir / "profiles"

    def format_profile(row):
        return f"""Player: {row['full_name']}
Position: {row['position']}
Team: {row.get('team_id', 'Unknown')}
Height: {row['height']}
Weight: {row['weight']}
Experience: {row.get('experience', 'Unknown')} years
School: {row.get('school', 'Unknown')}
Jersey: #{row['jersey_number']}
"""

    query = '''
    SELECT full_name, position, team_id, height, weight, experience, school, jersey_number
    FROM rosters
    WHERE season = '2025-26'
    ORDER BY full_name
    '''

    num_docs = create_temp_docs_from_db(collector.teams_db, query, profiles_dir, format_profile)
    print(f"  Created {num_docs} player profile documents")

    result = kb_service.create_memory_from_text("nba-player-profiles-2025", str(profiles_dir), sport="nba")
    print(f"  {result['message']}")

    # ==========================================
    # MEMORY 4: Season Schedule
    # ==========================================
    print("\n📅 Memory 4: Season Schedule")
    print("-" * 80)

    schedule_dir = temp_docs_dir / "schedule"

    def format_schedule(row):
        return f"""NBA Game on {row['game_date']}
Matchup: {row['matchup']}
Home Team: {row.get('home_team_name', 'Unknown')}
Away Team: {row.get('away_team_name', 'Unknown')}
Game ID: {row['game_id']}
"""

    query = '''
    SELECT game_id, game_date, matchup, home_team_name, away_team_name
    FROM schedule
    ORDER BY game_date DESC
    LIMIT 2000
    '''

    num_docs = create_temp_docs_from_db(collector.schedule_db, query, schedule_dir, format_schedule)
    print(f"  Created {num_docs} schedule documents")

    result = kb_service.create_memory_from_text("nba-schedule-2025", str(schedule_dir), sport="nba")
    print(f"  {result['message']}")

    # ==========================================
    # MEMORY 5: Season Averages
    # ==========================================
    print("\n📈 Memory 5: Season Averages")
    print("-" * 80)

    averages_dir = temp_docs_dir / "averages"

    def format_averages(row):
        return f"""Player Season Stats
Player ID: {row['player_id']}
Season: {row['season']}
Games: {row['games_played']}
Averages: {row['ppg']:.1f} PPG, {row['rpg']:.1f} RPG, {row['apg']:.1f} APG
Shooting: {row['fg_pct']:.1f}% FG, {row['fg3_pct']:.1f}% 3PT, {row['ft_pct']:.1f}% FT
Defense: {row['spg']:.1f} SPG, {row['bpg']:.1f} BPG
"""

    query = '''
    SELECT player_id, season, games_played, ppg, rpg, apg, spg, bpg, fg_pct, fg3_pct, ft_pct
    FROM season_averages
    WHERE season LIKE '%2025-26%'
    ORDER BY ppg DESC
    '''

    num_docs = create_temp_docs_from_db(collector.stats_db, query, averages_dir, format_averages)
    print(f"  Created {num_docs} season averages documents")

    result = kb_service.create_memory_from_text("nba-season-averages-2025", str(averages_dir), sport="nba")
    print(f"  {result['message']}")

    # ==========================================
    # CLEANUP
    # ==========================================
    print("\n🧹 Cleanup")
    print("-" * 80)

    import shutil
    shutil.rmtree(temp_docs_dir)
    print("  Removed temporary documents")

    # ==========================================
    # SUMMARY
    # ==========================================
    print("\n" + "="*80)
    print("  MEMORY CREATION COMPLETE")
    print("="*80)
    print("\n✅ Created 5 NBA Kre8VidMems memories:")
    print("   1. nba-teams-2025")
    print("   2. nba-player-gamelogs-2025")
    print("   3. nba-player-profiles-2025")
    print("   4. nba-schedule-2025")
    print("   5. nba-season-averages-2025")
    print("\n💡 Use /memories/search endpoint to query these memories")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
