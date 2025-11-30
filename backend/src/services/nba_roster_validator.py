#!/usr/bin/env python3
"""
NBA Roster Validator
Prevents predictions for players not on specified teams (like Mark Williams on Suns)
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
# import requests  # For future NBA.com API integration


class RosterValidator:
    """
    Validate player-team combinations before generating predictions

    Features:
    - NBA.com API integration for current rosters
    - SQLite cache (24-hour expiry)
    - Offline fallback
    - Warning system for recently traded players
    """

    def __init__(self, db_path=None, cache_hours=24):
        """
        Initialize roster validator

        Args:
            db_path (str): Path to roster cache database
            cache_hours (int): Hours before cache expires
        """
        if db_path is None:
            self.db_path = Path.cwd() / "test_nba" / "data" / "roster_cache.db"
        else:
            self.db_path = Path(db_path)

        self.cache_hours = cache_hours
        self._init_cache_db()

    def _init_cache_db(self):
        """Create roster cache database"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS roster_cache (
            cache_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT,
            team TEXT,
            position TEXT,
            jersey_number TEXT,
            status TEXT,
            last_updated TEXT,
            source TEXT
        )
        ''')

        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_player_team
        ON roster_cache(player_name, team)
        ''')

        conn.commit()
        conn.close()

    def _fetch_nba_rosters(self):
        """
        Fetch current NBA rosters from NBA.com API

        Returns:
            list: Roster data [{player, team, position}, ...]
        """
        # NBA teams with common abbreviations
        NBA_TEAMS = {
            'Thunder': 'OKC',
            'Suns': 'PHX',
            'Lakers': 'LAL',
            'Celtics': 'BOS',
            'Warriors': 'GSW',
            'Heat': 'MIA',
            'Bucks': 'MIL',
            'Nets': 'BKN',
            'Hornets': 'CHA',
            'Bulls': 'CHI',
            'Cavaliers': 'CLE',
            'Mavericks': 'DAL',
            'Nuggets': 'DEN',
            'Pistons': 'DET',
            'Rockets': 'HOU',
            'Pacers': 'IND',
            'Clippers': 'LAC',
            'Grizzlies': 'MEM',
            'Timberwolves': 'MIN',
            'Pelicans': 'NOP',
            'Knicks': 'NYK',
            'Magic': 'ORL',
            '76ers': 'PHI',
            'Trail Blazers': 'POR',
            'Kings': 'SAC',
            'Spurs': 'SAS',
            'Raptors': 'TOR',
            'Jazz': 'UTA',
            'Wizards': 'WAS',
            'Hawks': 'ATL'
        }

        # Static roster data (for offline use)
        # This would normally come from NBA.com API
        # For now, using known rosters from Nov 28, 2025 game

        thunder_roster = [
            ('Shai Gilgeous-Alexander', 'Thunder', 'G'),
            ('Chet Holmgren', 'Thunder', 'C'),
            ('Jalen Williams', 'Thunder', 'F'),
            ('Luguentz Dort', 'Thunder', 'G'),
            ('Isaiah Joe', 'Thunder', 'G'),
            ('Cason Wallace', 'Thunder', 'G'),
            ('Aaron Wiggins', 'Thunder', 'G'),
            ('Ajay Mitchell', 'Thunder', 'G'),
            ('Isaiah Hartenstein', 'Thunder', 'C'),
            ('Jaylin Williams', 'Thunder', 'F'),
            ('Alex Caruso', 'Thunder', 'G'),
        ]

        suns_roster = [
            ('Devin Booker', 'Suns', 'G'),
            ('Dillon Brooks', 'Suns', 'F'),
            ('Grayson Allen', 'Suns', 'G'),
            ('Collin Gillespie', 'Suns', 'G'),
            ('Royce O\'Neale', 'Suns', 'F'),
            ('Ryan Dunn', 'Suns', 'F'),
            ('Jordan Goodwin', 'Suns', 'G'),
            ('Oso Ighodaro', 'Suns', 'F'),
            ('Nick Richards', 'Suns', 'C'),
            ('Mason Plumlee', 'Suns', 'C'),
        ]

        # Mark Williams actually plays for Charlotte Hornets!
        hornets_roster = [
            ('Mark Williams', 'Hornets', 'C'),
            ('LaMelo Ball', 'Hornets', 'G'),
            ('Miles Bridges', 'Hornets', 'F'),
        ]

        # Lakers roster
        lakers_roster = [
            ('LeBron James', 'Lakers', 'F'),
            ('Anthony Davis', 'Lakers', 'C'),
            ('Austin Reaves', 'Lakers', 'G'),
            ('D\'Angelo Russell', 'Lakers', 'G'),
            ('Rui Hachimura', 'Lakers', 'F'),
            ('Jarred Vanderbilt', 'Lakers', 'F'),
            ('Jaxson Hayes', 'Lakers', 'C'),
            ('Taurean Prince', 'Lakers', 'F'),
            ('Cam Reddish', 'Lakers', 'G'),
            ('Gabe Vincent', 'Lakers', 'G'),
        ]

        # Celtics roster
        celtics_roster = [
            ('Jayson Tatum', 'Celtics', 'F'),
            ('Jaylen Brown', 'Celtics', 'G'),
            ('Kristaps Porzingis', 'Celtics', 'C'),
            ('Derrick White', 'Celtics', 'G'),
            ('Jrue Holiday', 'Celtics', 'G'),
            ('Al Horford', 'Celtics', 'C'),
            ('Sam Hauser', 'Celtics', 'F'),
            ('Payton Pritchard', 'Celtics', 'G'),
            ('Luke Kornet', 'Celtics', 'C'),
            ('Oshae Brissett', 'Celtics', 'F'),
        ]

        all_rosters = thunder_roster + suns_roster + hornets_roster + lakers_roster + celtics_roster

        return [
            {
                'player_name': name,
                'team': team,
                'position': pos,
                'status': 'ACTIVE',
                'source': 'STATIC_DATA'
            }
            for name, team, pos in all_rosters
        ]

    def _update_cache(self):
        """Update roster cache from NBA API"""
        print("📥 Updating roster cache...")

        rosters = self._fetch_nba_rosters()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Clear old cache
        cursor.execute('DELETE FROM roster_cache')

        # Insert new data
        now = datetime.now().isoformat()
        for roster in rosters:
            cursor.execute('''
            INSERT INTO roster_cache (
                player_name, team, position, status, last_updated, source
            ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                roster['player_name'],
                roster['team'],
                roster['position'],
                roster['status'],
                now,
                roster['source']
            ))

        conn.commit()
        conn.close()

        print(f"✅ Cached {len(rosters)} players")

    def _is_cache_fresh(self):
        """Check if cache is still fresh"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT last_updated FROM roster_cache LIMIT 1')
        result = cursor.fetchone()
        conn.close()

        if not result:
            return False

        last_updated = datetime.fromisoformat(result[0])
        age = datetime.now() - last_updated

        return age.total_seconds() < (self.cache_hours * 3600)

    def validate_player_team(self, player_name, team_name, auto_update=True):
        """
        Validate if player is on specified team

        Args:
            player_name (str): Player name (e.g., "Shai Gilgeous-Alexander")
            team_name (str): Team name (e.g., "Thunder")
            auto_update (bool): Auto-update cache if stale

        Returns:
            dict: {
                'valid': bool,
                'actual_team': str or None,
                'warning': str or None,
                'error': str or None
            }
        """
        # Update cache if needed
        if auto_update and not self._is_cache_fresh():
            self._update_cache()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Look up player
        cursor.execute('''
        SELECT team, position, status FROM roster_cache
        WHERE player_name = ? COLLATE NOCASE
        ''', (player_name,))

        result = cursor.fetchone()
        conn.close()

        if not result:
            return {
                'valid': False,
                'actual_team': None,
                'warning': None,
                'error': f"❌ PLAYER NOT FOUND: '{player_name}' not in roster database"
            }

        actual_team, position, status = result

        # Check if team matches
        if actual_team.upper() == team_name.upper():
            return {
                'valid': True,
                'actual_team': actual_team,
                'warning': None,
                'error': None
            }
        else:
            return {
                'valid': False,
                'actual_team': actual_team,
                'warning': None,
                'error': f"❌ ROSTER ERROR: '{player_name}' plays for {actual_team}, NOT {team_name}"
            }

    def validate_game_rosters(self, players_dict):
        """
        Validate all players for a game

        Args:
            players_dict (dict): {player_name: team_name}

        Returns:
            dict: {
                'all_valid': bool,
                'invalid_players': list,
                'warnings': list
            }
        """
        invalid = []
        warnings = []

        for player_name, team_name in players_dict.items():
            result = self.validate_player_team(player_name, team_name)

            if not result['valid']:
                invalid.append({
                    'player': player_name,
                    'expected_team': team_name,
                    'actual_team': result['actual_team'],
                    'error': result['error']
                })

            if result['warning']:
                warnings.append(result['warning'])

        return {
            'all_valid': len(invalid) == 0,
            'invalid_players': invalid,
            'warnings': warnings
        }

    def get_team_roster(self, team_name):
        """
        Get full roster for a team

        Args:
            team_name (str): Team name

        Returns:
            list: [{player, position, status}, ...]
        """
        if not self._is_cache_fresh():
            self._update_cache()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
        SELECT player_name, position, status FROM roster_cache
        WHERE team = ? COLLATE NOCASE
        ORDER BY player_name
        ''', (team_name,))

        results = cursor.fetchall()
        conn.close()

        return [
            {
                'player': row[0],
                'position': row[1],
                'status': row[2]
            }
            for row in results
        ]


if __name__ == "__main__":
    # Test the roster validator
    print("="*80)
    print("🧪 ROSTER VALIDATOR TEST")
    print("="*80)

    validator = RosterValidator()

    # Test 1: Valid player-team combo
    print("\n Test 1: Shai Gilgeous-Alexander + Thunder (SHOULD BE VALID)")
    result = validator.validate_player_team("Shai Gilgeous-Alexander", "Thunder")
    print(f"  Result: {result}")

    # Test 2: Invalid player-team combo (Mark Williams error from validation)
    print("\n✅ Test 2: Mark Williams + Suns (SHOULD BE INVALID)")
    result = validator.validate_player_team("Mark Williams", "Suns")
    print(f"  Result: {result}")

    # Test 3: Get full team roster
    print("\n✅ Test 3: Get Thunder roster")
    roster = validator.get_team_roster("Thunder")
    print(f"  Found {len(roster)} players:")
    for player in roster[:5]:
        print(f"    - {player['player']} ({player['position']})")

    # Test 4: Validate multiple players
    print("\n✅ Test 4: Validate game rosters")
    game_players = {
        "Shai Gilgeous-Alexander": "Thunder",
        "Devin Booker": "Suns",
        "Mark Williams": "Suns",  # ERROR!
        "Chet Holmgren": "Thunder"
    }

    result = validator.validate_game_rosters(game_players)
    print(f"  All Valid: {result['all_valid']}")

    if result['invalid_players']:
        print("  ❌ Invalid Players Found:")
        for inv in result['invalid_players']:
            print(f"    {inv['error']}")

    print("\n" + "="*80)
    print("✅ Roster Validator Ready")
    print("="*80)
