"""
Load DraftKings NFL Extraction Data into Test System
Processes the comprehensive Bears @ Eagles odds data for testing
"""

import json
import sqlite3
import sys
from pathlib import Path
from datetime import datetime

# Add backend to path
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

# DraftKings data path
DRAFTKINGS_DATA_PATH = Path.home() / "Downloads" / "DraftKings_Odds_Extraction_Results"
MASTER_DB_FILE = DRAFTKINGS_DATA_PATH / "MASTER_Consolidated_Odds_Database_All_5151_Frames.json"

# Backend data paths
NFL_TESTDATA_DB = backend_path / "data" / "nfl_draftkings_testdata.db"


def create_testdata_schema():
    """Create database schema for DraftKings test data"""
    conn = sqlite3.connect(NFL_TESTDATA_DB)
    cursor = conn.cursor()

    # Game lines table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_lines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game TEXT NOT NULL,
            home_team TEXT,
            away_team TEXT,
            spread_home_line REAL,
            spread_home_odds TEXT,
            spread_away_line REAL,
            spread_away_odds TEXT,
            total_line REAL,
            total_over_odds TEXT,
            total_under_odds TEXT,
            moneyline_home TEXT,
            moneyline_away TEXT,
            frame_number INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Player props table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS player_props (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            team TEXT,
            prop_type TEXT NOT NULL,
            stat_context TEXT,
            threshold TEXT,
            odds TEXT,
            frame_number INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Metadata table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS extraction_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_agents INTEGER,
            total_frames INTEGER,
            total_unique_players INTEGER,
            extraction_date DATE,
            data_source TEXT DEFAULT 'DraftKings',
            sport TEXT DEFAULT 'NFL'
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Created test data schema")


def load_game_lines(data: dict):
    """Load game lines from extracted data"""
    conn = sqlite3.connect(NFL_TESTDATA_DB)
    cursor = conn.cursor()

    game_lines = data.get('game_lines_summary', [])
    loaded_count = 0

    for entry in game_lines:
        frame = entry.get('frame')
        lines = entry.get('lines', {})
        game = lines.get('game', 'Unknown')

        spread = lines.get('spread', {})
        total = lines.get('total', {})
        moneyline = lines.get('moneyline', {})

        # Extract spread data (handle both dict and missing data)
        chi_spread = spread.get('chi_bears', {}) if isinstance(spread.get('chi_bears'), dict) else {}
        phi_spread = spread.get('phi_eagles', {}) if isinstance(spread.get('phi_eagles'), dict) else {}

        # Parse line values
        def parse_line(line_str):
            if not line_str:
                return None
            try:
                return float(line_str.replace('+', ''))
            except:
                return None

        cursor.execute("""
            INSERT INTO game_lines (
                game, home_team, away_team,
                spread_home_line, spread_home_odds,
                spread_away_line, spread_away_odds,
                moneyline_home, moneyline_away,
                frame_number
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            game,
            "PHI Eagles",
            "CHI Bears",
            parse_line(phi_spread.get('line')),
            phi_spread.get('odds'),
            parse_line(chi_spread.get('line')),
            chi_spread.get('odds'),
            moneyline.get('phi_eagles') if isinstance(moneyline, dict) else None,
            moneyline.get('chi_bears') if isinstance(moneyline, dict) else None,
            frame
        ))
        loaded_count += 1

    conn.commit()
    conn.close()
    print(f"✅ Loaded {loaded_count} game line entries")
    return loaded_count


def load_player_props(data: dict):
    """Load player props from extracted data"""
    conn = sqlite3.connect(NFL_TESTDATA_DB)
    cursor = conn.cursor()

    all_frames = data.get('all_frames_odds', [])
    loaded_count = 0

    for frame_data in all_frames:
        frame_number = frame_data.get('frame_number')
        player_props = frame_data.get('player_props', [])

        for prop in player_props:
            # Skip if prop is not a dict
            if not isinstance(prop, dict):
                continue

            player = prop.get('player')
            team = prop.get('team')
            prop_type = prop.get('prop_type')
            stat_context = prop.get('stat_context')

            # Each prop can have multiple threshold/odds options
            options = prop.get('options', [])
            if not isinstance(options, list):
                continue

            for option in options:
                # Skip if option is not a dict
                if not isinstance(option, dict):
                    continue

                threshold = option.get('threshold')
                odds = option.get('odds')

                cursor.execute("""
                    INSERT INTO player_props (
                        player_name, team, prop_type, stat_context,
                        threshold, odds, frame_number
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (player, team, prop_type, stat_context, threshold, odds, frame_number))
                loaded_count += 1

    conn.commit()
    conn.close()
    print(f"✅ Loaded {loaded_count} player prop entries")
    return loaded_count


def load_metadata(data: dict):
    """Load extraction metadata"""
    conn = sqlite3.connect(NFL_TESTDATA_DB)
    cursor = conn.cursor()

    meta = data.get('extraction_metadata', {})
    stats = data.get('odds_statistics', {})

    cursor.execute("""
        INSERT INTO extraction_metadata (
            total_agents, total_frames, total_unique_players,
            extraction_date, data_source, sport
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        meta.get('total_agents'),
        meta.get('total_frames'),
        stats.get('total_unique_players'),
        datetime.now().date(),
        'DraftKings',
        'NFL'
    ))

    conn.commit()
    conn.close()
    print("✅ Loaded metadata")


def get_summary_stats():
    """Get summary statistics from loaded data"""
    conn = sqlite3.connect(NFL_TESTDATA_DB)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM game_lines")
    game_lines_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM player_props")
    player_props_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT player_name) FROM player_props")
    unique_players = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT prop_type) FROM player_props")
    unique_prop_types = cursor.fetchone()[0]

    conn.close()

    return {
        "game_lines": game_lines_count,
        "player_props": player_props_count,
        "unique_players": unique_players,
        "unique_prop_types": unique_prop_types
    }


def main():
    print("=" * 60)
    print("DraftKings NFL Test Data Loader")
    print("=" * 60)

    # Check if master database exists
    if not MASTER_DB_FILE.exists():
        print(f"❌ Error: Master database not found at {MASTER_DB_FILE}")
        return

    print(f"📂 Loading from: {MASTER_DB_FILE}")

    # Load JSON data
    with open(MASTER_DB_FILE, 'r') as f:
        data = json.load(f)

    print(f"✅ Loaded master database")

    # Create schema
    create_testdata_schema()

    # Load data
    print("\n" + "=" * 60)
    print("Loading Data")
    print("=" * 60)

    game_lines_count = load_game_lines(data)
    player_props_count = load_player_props(data)
    load_metadata(data)

    # Get summary
    print("\n" + "=" * 60)
    print("Summary Statistics")
    print("=" * 60)

    stats = get_summary_stats()
    print(f"📊 Game Lines: {stats['game_lines']}")
    print(f"📊 Player Props: {stats['player_props']}")
    print(f"👤 Unique Players: {stats['unique_players']}")
    print(f"📈 Unique Prop Types: {stats['unique_prop_types']}")

    print("\n" + "=" * 60)
    print(f"✅ Test data saved to: {NFL_TESTDATA_DB}")
    print("=" * 60)


if __name__ == "__main__":
    main()
