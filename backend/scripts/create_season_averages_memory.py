#!/usr/bin/env python3
"""
Create NBA Season Averages Memory
"""
import sys
import sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.knowledge_base import KnowledgeBaseService
from src.services.nba_stats_collector import NBAStatsCollector


def main():
    print("Creating NBA Season Averages Memory...")

    collector = NBAStatsCollector()
    kb_service = KnowledgeBaseService()

    temp_docs_dir = Path("./temp_season_averages")
    temp_docs_dir.mkdir(exist_ok=True)

    # Query season averages
    conn = sqlite3.connect(collector.stats_db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = '''
    SELECT player_id, season, games_played, ppg, rpg, apg, spg, bpg, fg_pct, fg3_pct, ft_pct
    FROM season_averages
    WHERE season = '22025'
    ORDER BY ppg DESC
    '''

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    print(f"Found {len(rows)} season averages")

    # Create documents
    for i, row in enumerate(rows):
        row_dict = dict(row)
        doc_content = f"""Player Season Stats
Player ID: {row_dict['player_id']}
Season: {row_dict['season']}
Games: {row_dict['games_played']}
Averages: {row_dict['ppg']:.1f} PPG, {row_dict['rpg']:.1f} RPG, {row_dict['apg']:.1f} APG
Shooting: {row_dict['fg_pct']:.1f}% FG, {row_dict['fg3_pct']:.1f}% 3PT, {row_dict['ft_pct']:.1f}% FT
Defense: {row_dict['spg']:.1f} SPG, {row_dict['bpg']:.1f} BPG
"""
        doc_path = temp_docs_dir / f"doc_{i:05d}.txt"
        with open(doc_path, 'w') as f:
            f.write(doc_content)

    print(f"Created {len(rows)} documents")

    # Create memory
    result = kb_service.create_memory_from_text("nba-season-averages-2025", str(temp_docs_dir), sport="nba")
    print(f"✅ {result['message']}")

    # Cleanup
    import shutil
    shutil.rmtree(temp_docs_dir)
    print("✅ Cleaned up temporary documents")


if __name__ == "__main__":
    main()
