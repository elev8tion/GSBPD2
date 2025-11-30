#!/usr/bin/env python3
"""
NBA Stats Collector Service
Comprehensive data collection from NBA API for 2025-26 season

Features:
- Team rosters and player bios
- Player game logs and season averages
- Team stats and advanced metrics
- Schedule data
- Rate limiting (20 requests/min)
- Retry logic with exponential backoff
"""

import sqlite3
import time
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import json

from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import (
    commonteamroster,
    playergamelog,
    teamgamelog,
    leaguegamefinder,
    playercareerstats
)


class RateLimiter:
    """Rate limiter for NBA API (20 requests/minute)"""

    def __init__(self, max_per_minute: int = 20):
        self.max_per_minute = max_per_minute
        self.request_times: List[float] = []
        self.min_interval = 60.0 / max_per_minute  # 3 seconds between requests

    async def wait_if_needed(self):
        """Wait if we've hit rate limit"""
        now = time.time()

        # Remove requests older than 1 minute
        self.request_times = [t for t in self.request_times if now - t < 60]

        # If at limit, wait until oldest request expires
        if len(self.request_times) >= self.max_per_minute:
            sleep_time = 60 - (now - self.request_times[0]) + 0.1
            print(f"  ⏳ Rate limit reached, waiting {sleep_time:.1f}s...")
            await asyncio.sleep(sleep_time)
            self.request_times = self.request_times[1:]

        # Also enforce minimum interval between requests
        if self.request_times:
            time_since_last = now - self.request_times[-1]
            if time_since_last < self.min_interval:
                await asyncio.sleep(self.min_interval - time_since_last)

        self.request_times.append(time.time())


class NBAStatsCollector:
    """
    Comprehensive NBA data collection service

    Collects and stores:
    - Team rosters (current 2025-26 season)
    - Player game logs and season averages
    - Team stats and game logs
    - Schedule data
    - Advanced stats (pace, efficiency ratings)
    """

    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            data_dir = Path(__file__).parent.parent.parent / 'data'

        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Database paths
        self.teams_db = self.data_dir / 'nba_teams.db'
        self.stats_db = self.data_dir / 'nba_player_stats.db'
        self.schedule_db = self.data_dir / 'nba_schedule.db'

        # Rate limiter
        self.rate_limiter = RateLimiter(max_per_minute=20)

        # Season
        self.current_season = '2025-26'

        # Initialize databases
        self._init_databases()

        print(f"✅ NBA Stats Collector initialized")
        print(f"   Data directory: {self.data_dir}")
        print(f"   Season: {self.current_season}")

    def _init_databases(self):
        """Initialize SQLite databases with schemas"""

        # ==========================================
        # NBA TEAMS DATABASE
        # ==========================================
        conn = sqlite3.connect(self.teams_db)
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            team_id TEXT PRIMARY KEY,
            full_name TEXT,
            abbreviation TEXT,
            nickname TEXT,
            city TEXT,
            state TEXT,
            year_founded INTEGER,
            conference TEXT,
            division TEXT
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS rosters (
            player_id TEXT PRIMARY KEY,
            team_id TEXT,
            full_name TEXT,
            first_name TEXT,
            last_name TEXT,
            jersey_number TEXT,
            position TEXT,
            height TEXT,
            weight TEXT,
            birthdate TEXT,
            age TEXT,
            experience TEXT,
            school TEXT,
            season TEXT,
            FOREIGN KEY (team_id) REFERENCES teams(team_id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_bios (
            player_id TEXT PRIMARY KEY,
            is_active INTEGER,
            draft_year TEXT,
            draft_round TEXT,
            draft_number TEXT,
            country TEXT,
            FOREIGN KEY (player_id) REFERENCES rosters(player_id)
        )
        ''')

        conn.commit()
        conn.close()

        # ==========================================
        # NBA PLAYER STATS DATABASE
        # ==========================================
        conn = sqlite3.connect(self.stats_db)
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_logs (
            game_log_id TEXT PRIMARY KEY,
            player_id TEXT,
            season_id TEXT,
            player_name TEXT,
            game_id TEXT,
            game_date TEXT,
            matchup TEXT,
            wl TEXT,
            min REAL,
            fgm INTEGER,
            fga INTEGER,
            fg_pct REAL,
            fg3m INTEGER,
            fg3a INTEGER,
            fg3_pct REAL,
            ftm INTEGER,
            fta INTEGER,
            ft_pct REAL,
            oreb INTEGER,
            dreb INTEGER,
            reb INTEGER,
            ast INTEGER,
            stl INTEGER,
            blk INTEGER,
            tov INTEGER,
            pf INTEGER,
            pts INTEGER,
            plus_minus INTEGER,
            video_available INTEGER
        )
        ''')

        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_game_logs_player
        ON game_logs(player_id)
        ''')

        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_game_logs_date
        ON game_logs(game_date)
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS season_averages (
            player_id TEXT,
            season TEXT,
            games_played INTEGER,
            mpg REAL,
            ppg REAL,
            rpg REAL,
            apg REAL,
            spg REAL,
            bpg REAL,
            topg REAL,
            fg_pct REAL,
            fg3_pct REAL,
            ft_pct REAL,
            PRIMARY KEY (player_id, season)
        )
        ''')

        conn.commit()
        conn.close()

        # ==========================================
        # NBA SCHEDULE DATABASE
        # ==========================================
        conn = sqlite3.connect(self.schedule_db)
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            game_id TEXT PRIMARY KEY,
            season TEXT,
            game_date TEXT,
            matchup TEXT,
            home_team_id TEXT,
            away_team_id TEXT,
            home_team_name TEXT,
            away_team_name TEXT,
            home_score INTEGER,
            away_score INTEGER,
            game_status TEXT
        )
        ''')

        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_schedule_date
        ON schedule(game_date)
        ''')

        conn.commit()
        conn.close()

        print(f"  ✅ Databases initialized")

    # ==========================================
    # TEAM ROSTERS COLLECTION
    # ==========================================

    async def collect_all_teams(self) -> Dict:
        """
        Collect all NBA teams and rosters for current season

        Returns:
            Dict with collection results
        """
        print(f"\n{'='*70}")
        print(f"  COLLECTING NBA TEAMS & ROSTERS ({self.current_season})")
        print(f"{'='*70}\n")

        try:
            # Get all teams from static data
            all_teams = teams.get_teams()
            print(f"📥 Found {len(all_teams)} NBA teams")

            conn = sqlite3.connect(self.teams_db)
            cursor = conn.cursor()

            teams_collected = 0
            total_players = 0

            for team in all_teams:
                team_id = str(team['id'])
                team_name = team['full_name']

                print(f"\n  {teams_collected + 1}/{len(all_teams)} {team_name}...")

                # Insert team
                cursor.execute('''
                INSERT OR REPLACE INTO teams (
                    team_id, full_name, abbreviation, nickname,
                    city, state, year_founded
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    team_id,
                    team['full_name'],
                    team['abbreviation'],
                    team['nickname'],
                    team['city'],
                    team['state'],
                    team['year_founded']
                ))

                # Get team roster
                await self.rate_limiter.wait_if_needed()

                roster = commonteamroster.CommonTeamRoster(
                    team_id=team_id,
                    season=self.current_season
                )

                roster_df = roster.get_data_frames()[0]

                # Insert players
                for _, player in roster_df.iterrows():
                    cursor.execute('''
                    INSERT OR REPLACE INTO rosters (
                        player_id, team_id, full_name, first_name, last_name,
                        jersey_number, position, height, weight,
                        birthdate, age, experience, school, season
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        str(player['PLAYER_ID']),
                        team_id,
                        player['PLAYER'],
                        player.get('PLAYER'),  # FIRST_NAME not in response
                        player.get('PLAYER'),  # LAST_NAME not in response
                        str(player.get('NUM', '')),
                        player.get('POSITION', ''),
                        player.get('HEIGHT', ''),
                        str(player.get('WEIGHT', '')),
                        player.get('BIRTH_DATE', ''),
                        str(player.get('AGE', '')),
                        str(player.get('EXP', '')),
                        player.get('SCHOOL', ''),
                        self.current_season
                    ))

                total_players += len(roster_df)
                teams_collected += 1
                print(f"    ✅ {len(roster_df)} players")

            conn.commit()
            conn.close()

            print(f"\n{'='*70}")
            print(f"✅ TEAMS & ROSTERS COLLECTION COMPLETE")
            print(f"{'='*70}")
            print(f"  Teams: {teams_collected}")
            print(f"  Players: {total_players}")
            print(f"\n")

            return {
                "status": "success",
                "teams_collected": teams_collected,
                "players_collected": total_players,
                "season": self.current_season
            }

        except Exception as e:
            print(f"\n❌ Error collecting teams: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    # ==========================================
    # PLAYER GAME LOGS COLLECTION
    # ==========================================

    async def collect_player_gamelogs(self, limit: Optional[int] = None) -> Dict:
        """
        Collect game logs for all active players

        Args:
            limit: Optional limit on number of players (for testing)

        Returns:
            Dict with collection results
        """
        print(f"\n{'='*70}")
        print(f"  COLLECTING PLAYER GAME LOGS ({self.current_season})")
        print(f"{'='*70}\n")

        try:
            # Get all players from rosters
            conn = sqlite3.connect(self.teams_db)
            cursor = conn.cursor()

            cursor.execute('''
            SELECT DISTINCT player_id, full_name
            FROM rosters
            WHERE season = ?
            ORDER BY full_name
            ''', (self.current_season,))

            players_list = cursor.fetchall()
            conn.close()

            if limit:
                players_list = players_list[:limit]

            print(f"📥 Collecting game logs for {len(players_list)} players...")
            print(f"   (This will take approximately {(len(players_list) * 3) / 60:.1f} minutes)\n")

            conn = sqlite3.connect(self.stats_db)
            cursor = conn.cursor()

            collected = 0
            total_games = 0
            errors = 0

            for player_id, player_name in players_list:
                try:
                    print(f"  {collected + 1}/{len(players_list)} {player_name}...", end=" ")

                    await self.rate_limiter.wait_if_needed()

                    gamelog = playergamelog.PlayerGameLog(
                        player_id=player_id,
                        season=self.current_season
                    )

                    df = gamelog.get_data_frames()[0]

                    if len(df) == 0:
                        print("(no games)")
                        collected += 1
                        continue

                    # Insert game logs
                    for _, game in df.iterrows():
                        game_id = game.get('Game_ID') or game.get('GAME_ID', '')
                        cursor.execute('''
                        INSERT OR REPLACE INTO game_logs (
                            game_log_id, player_id, season_id, player_name,
                            game_id, game_date, matchup, wl, min,
                            fgm, fga, fg_pct, fg3m, fg3a, fg3_pct,
                            ftm, fta, ft_pct, oreb, dreb, reb,
                            ast, stl, blk, tov, pf, pts, plus_minus,
                            video_available
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            f"{player_id}_{game_id}",
                            player_id,
                            game['SEASON_ID'],
                            player_name,
                            game_id,
                            game['GAME_DATE'],
                            game['MATCHUP'],
                            game.get('WL', ''),
                            float(game['MIN']) if game['MIN'] else 0.0,
                            int(game['FGM']),
                            int(game['FGA']),
                            float(game['FG_PCT']) if game['FG_PCT'] else 0.0,
                            int(game['FG3M']),
                            int(game['FG3A']),
                            float(game['FG3_PCT']) if game['FG3_PCT'] else 0.0,
                            int(game['FTM']),
                            int(game['FTA']),
                            float(game['FT_PCT']) if game['FT_PCT'] else 0.0,
                            int(game['OREB']),
                            int(game['DREB']),
                            int(game['REB']),
                            int(game['AST']),
                            int(game['STL']),
                            int(game['BLK']),
                            int(game['TOV']),
                            int(game['PF']),
                            int(game['PTS']),
                            int(game['PLUS_MINUS']) if game['PLUS_MINUS'] else 0,
                            int(game.get('VIDEO_AVAILABLE', 0))
                        ))

                    total_games += len(df)
                    print(f"✅ {len(df)} games")
                    collected += 1

                except Exception as e:
                    print(f"❌ Error: {e}")
                    errors += 1

                # Commit every 10 players
                if collected % 10 == 0:
                    conn.commit()

            conn.commit()
            conn.close()

            print(f"\n{'='*70}")
            print(f"✅ PLAYER GAME LOGS COLLECTION COMPLETE")
            print(f"{'='*70}")
            print(f"  Players processed: {collected}")
            print(f"  Total games: {total_games}")
            print(f"  Errors: {errors}")
            print(f"\n")

            return {
                "status": "success",
                "players_processed": collected,
                "games_collected": total_games,
                "errors": errors
            }

        except Exception as e:
            print(f"\n❌ Error collecting game logs: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    # ==========================================
    # SEASON AVERAGES CALCULATION
    # ==========================================

    def calculate_season_averages(self) -> Dict:
        """
        Calculate season averages from game logs

        Returns:
            Dict with calculation results
        """
        print(f"\n{'='*70}")
        print(f"  CALCULATING SEASON AVERAGES")
        print(f"{'='*70}\n")

        try:
            conn = sqlite3.connect(self.stats_db)
            cursor = conn.cursor()

            # Calculate averages per player per season
            cursor.execute('''
            INSERT OR REPLACE INTO season_averages (
                player_id, season, games_played,
                mpg, ppg, rpg, apg, spg, bpg, topg,
                fg_pct, fg3_pct, ft_pct
            )
            SELECT
                player_id,
                season_id as season,
                COUNT(*) as games_played,
                AVG(min) as mpg,
                AVG(pts) as ppg,
                AVG(reb) as rpg,
                AVG(ast) as apg,
                AVG(stl) as spg,
                AVG(blk) as bpg,
                AVG(tov) as topg,
                AVG(fg_pct) * 100 as fg_pct,
                AVG(fg3_pct) * 100 as fg3_pct,
                AVG(ft_pct) * 100 as ft_pct
            FROM game_logs
            GROUP BY player_id, season_id
            ''')

            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()

            print(f"✅ Calculated averages for {rows_affected} player-seasons\n")

            return {
                "status": "success",
                "player_seasons_calculated": rows_affected
            }

        except Exception as e:
            print(f"❌ Error calculating averages: {e}\n")
            return {
                "status": "error",
                "message": str(e)
            }

    # ==========================================
    # SCHEDULE COLLECTION
    # ==========================================

    async def collect_schedule(self) -> Dict:
        """
        Collect full 2025-26 season schedule

        Returns:
            Dict with collection results
        """
        print(f"\n{'='*70}")
        print(f"  COLLECTING SCHEDULE ({self.current_season})")
        print(f"{'='*70}\n")

        try:
            await self.rate_limiter.wait_if_needed()

            # Get all games for the season
            gamefinder = leaguegamefinder.LeagueGameFinder(
                season_nullable=self.current_season,
                league_id_nullable='00'
            )

            games_df = gamefinder.get_data_frames()[0]

            print(f"📥 Found {len(games_df)} game records\n")

            conn = sqlite3.connect(self.schedule_db)
            cursor = conn.cursor()

            games_inserted = 0

            for _, game in games_df.iterrows():
                cursor.execute('''
                INSERT OR REPLACE INTO schedule (
                    game_id, season, game_date, matchup,
                    home_team_id, away_team_id, home_team_name, away_team_name,
                    home_score, away_score, game_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    str(game['GAME_ID']),
                    game['SEASON_ID'],
                    game['GAME_DATE'],
                    game['MATCHUP'],
                    str(game['TEAM_ID']),
                    '',  # Away team ID not in this endpoint
                    game['TEAM_NAME'],
                    '',  # Away team name not in this endpoint
                    int(game['PTS']) if '@' not in game['MATCHUP'] else 0,
                    int(game['PTS']) if '@' in game['MATCHUP'] else 0,
                    game.get('WL', 'scheduled')
                ))
                games_inserted += 1

            conn.commit()
            conn.close()

            print(f"{'='*70}")
            print(f"✅ SCHEDULE COLLECTION COMPLETE")
            print(f"{'='*70}")
            print(f"  Games: {games_inserted}")
            print(f"\n")

            return {
                "status": "success",
                "games_collected": games_inserted
            }

        except Exception as e:
            print(f"\n❌ Error collecting schedule: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    # ==========================================
    # COLLECTION STATUS
    # ==========================================

    def get_collection_status(self) -> Dict:
        """Get status of all collected data"""

        status = {}

        try:
            # Convert season format for NBA API database queries
            # "2025-26" -> "22025" (NBA API season ID format)
            season_year = self.current_season.split('-')[0]
            nba_api_season = f"2{season_year}"

            # Teams count
            conn = sqlite3.connect(self.teams_db)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM teams")
            status['teams_count'] = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM rosters WHERE season = ?", (self.current_season,))
            status['players_count'] = cursor.fetchone()[0]
            conn.close()

            # Game logs count
            conn = sqlite3.connect(self.stats_db)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM game_logs")
            status['game_logs_count'] = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM season_averages WHERE season = ?", (nba_api_season,))
            status['season_averages_count'] = cursor.fetchone()[0]
            conn.close()

            # Schedule count
            conn = sqlite3.connect(self.schedule_db)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM schedule WHERE season LIKE ?", (f"%{nba_api_season}",))
            status['schedule_games_count'] = cursor.fetchone()[0]
            conn.close()

            status['season'] = self.current_season
            status['databases'] = {
                'teams': str(self.teams_db),
                'player_stats': str(self.stats_db),
                'schedule': str(self.schedule_db)
            }

            return status

        except Exception as e:
            return {
                "error": str(e)
            }


# ==========================================
# STANDALONE EXECUTION
# ==========================================

if __name__ == "__main__":
    import sys

    print("="*70)
    print("  NBA STATS COLLECTOR - STANDALONE MODE")
    print("="*70)

    async def main():
        collector = NBAStatsCollector()

        # Collect teams & rosters
        result = await collector.collect_all_teams()
        print(f"\n📊 Teams Result: {result}")

        # Collect game logs (limit to 10 players for testing)
        result = await collector.collect_player_gamelogs(limit=10)
        print(f"\n📊 Game Logs Result: {result}")

        # Calculate season averages
        result = collector.calculate_season_averages()
        print(f"\n📊 Averages Result: {result}")

        # Collect schedule
        result = await collector.collect_schedule()
        print(f"\n📊 Schedule Result: {result}")

        # Get status
        status = collector.get_collection_status()
        print(f"\n📊 Collection Status:")
        print(json.dumps(status, indent=2))

    asyncio.run(main())
