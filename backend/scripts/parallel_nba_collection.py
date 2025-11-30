#!/usr/bin/env python3
"""
Parallel NBA Data Collection with Orchestrated Sub-Agents

Splits the 526 players into multiple batches and collects them in parallel
using coordinated async workers.

Strategy:
- Agent 1-10: Each handles ~53 players (526 / 10 = ~53 per agent)
- Central orchestrator coordinates and aggregates results
- Rate limiting shared across all agents (20 req/min globally)
- Progress tracking and error recovery
"""

import asyncio
import sys
from pathlib import Path
from typing import List, Dict
import time
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.nba_stats_collector import NBAStatsCollector, RateLimiter


class OrchestratedCollectionManager:
    """
    Manages parallel collection across multiple worker agents

    Features:
    - Splits players into batches
    - Coordinates parallel workers
    - Shared rate limiting
    - Progress tracking
    - Error recovery
    """

    def __init__(self, num_workers: int = 10):
        self.num_workers = num_workers
        self.collector = NBAStatsCollector()

        # Shared global rate limiter (20 req/min total across all workers)
        self.global_rate_limiter = RateLimiter(max_per_minute=20)

        # Progress tracking
        self.completed_players = 0
        self.total_games_collected = 0
        self.errors = []
        self.start_time = None

    def split_players_into_batches(self, players: List[tuple], num_batches: int) -> List[List[tuple]]:
        """Split player list into N roughly equal batches"""
        batch_size = len(players) // num_batches
        remainder = len(players) % num_batches

        batches = []
        start_idx = 0

        for i in range(num_batches):
            # Add 1 extra player to first 'remainder' batches
            current_batch_size = batch_size + (1 if i < remainder else 0)
            end_idx = start_idx + current_batch_size
            batches.append(players[start_idx:end_idx])
            start_idx = end_idx

        return batches

    async def worker_agent(self, agent_id: int, player_batch: List[tuple], progress_callback):
        """
        Individual worker agent that collects game logs for a batch of players

        Args:
            agent_id: Worker identifier (1-10)
            player_batch: List of (player_id, player_name) tuples
            progress_callback: Async callback for progress updates
        """
        import sqlite3
        from nba_api.stats.endpoints import playergamelog

        worker_name = f"Agent-{agent_id}"
        collected = 0
        games = 0
        errors = 0

        # Open database connection for this worker
        conn = sqlite3.connect(self.collector.stats_db)
        cursor = conn.cursor()

        try:
            for player_id, player_name in player_batch:
                try:
                    # Use global rate limiter (shared across all workers)
                    await self.global_rate_limiter.wait_if_needed()

                    # Fetch game logs
                    gamelog = playergamelog.PlayerGameLog(
                        player_id=player_id,
                        season=self.collector.current_season
                    )

                    df = gamelog.get_data_frames()[0]

                    if len(df) == 0:
                        collected += 1
                        await progress_callback(worker_name, player_name, 0, "no games")
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

                    games += len(df)
                    collected += 1
                    await progress_callback(worker_name, player_name, len(df), "success")

                    # Commit every 5 players
                    if collected % 5 == 0:
                        conn.commit()

                except Exception as e:
                    errors += 1
                    await progress_callback(worker_name, player_name, 0, f"error: {str(e)[:50]}")
                    self.errors.append({
                        'worker': worker_name,
                        'player': player_name,
                        'error': str(e)
                    })

            # Final commit
            conn.commit()

        finally:
            conn.close()

        return {
            'worker': worker_name,
            'players_processed': collected,
            'games_collected': games,
            'errors': errors
        }

    async def progress_callback(self, worker: str, player: str, games: int, status: str):
        """Handle progress updates from workers"""
        self.completed_players += 1
        self.total_games_collected += games

        # Calculate ETA
        if self.start_time:
            elapsed = time.time() - self.start_time
            players_remaining = 526 - self.completed_players
            if self.completed_players > 0:
                avg_time_per_player = elapsed / self.completed_players
                eta_seconds = players_remaining * avg_time_per_player
                eta_minutes = eta_seconds / 60
                eta_str = f"ETA: {eta_minutes:.1f}min"
            else:
                eta_str = "ETA: calculating..."
        else:
            eta_str = ""

        # Print progress (with carriage return to update same line)
        status_icon = "✅" if status == "success" else "⚠️ " if "no games" in status else "❌"
        print(f"\r{worker}: [{self.completed_players}/526] {player[:30]:30} {status_icon} {games}g | Total: {self.total_games_collected:,} games | {eta_str}   ", end="", flush=True)

        # New line every 10 players
        if self.completed_players % 10 == 0:
            print()

    async def orchestrate_parallel_collection(self):
        """
        Main orchestration method

        Coordinates parallel workers to collect all NBA data
        """
        print("=" * 100)
        print("  ORCHESTRATED PARALLEL NBA DATA COLLECTION")
        print("=" * 100)
        print(f"\n🤖 Initializing {self.num_workers} coordinated sub-agents...")
        print(f"📊 Strategy: Each agent handles ~{526 // self.num_workers} players")
        print(f"⚡ Global rate limit: 20 requests/minute (shared)")
        print(f"⏱️  Estimated time: ~26 minutes\n")

        # Step 1: Get all players
        import sqlite3
        conn = sqlite3.connect(self.collector.teams_db)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT DISTINCT player_id, full_name
        FROM rosters
        WHERE season = ?
        ORDER BY full_name
        ''', (self.collector.current_season,))
        all_players = cursor.fetchall()
        conn.close()

        print(f"✅ Loaded {len(all_players)} players from database\n")

        # Step 2: Split into batches
        player_batches = self.split_players_into_batches(all_players, self.num_workers)

        print(f"📦 Player batches created:")
        for i, batch in enumerate(player_batches, 1):
            print(f"   Agent-{i}: {len(batch)} players")
        print()

        # Step 3: Launch parallel workers
        print(f"🚀 Launching {self.num_workers} parallel workers...\n")
        print("=" * 100)

        self.start_time = time.time()

        # Create tasks for all workers
        tasks = [
            self.worker_agent(i + 1, batch, self.progress_callback)
            for i, batch in enumerate(player_batches)
        ]

        # Run all workers in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)

        print("\n" + "=" * 100)

        # Step 4: Aggregate results
        total_time = time.time() - self.start_time

        print(f"\n✅ ALL WORKERS COMPLETED in {total_time / 60:.1f} minutes")
        print("\n📊 Worker Results:")

        total_processed = 0
        total_games = 0
        total_errors = 0

        for result in results:
            if isinstance(result, dict):
                print(f"   {result['worker']}: {result['players_processed']} players, {result['games_collected']} games, {result['errors']} errors")
                total_processed += result['players_processed']
                total_games += result['games_collected']
                total_errors += result['errors']

        print(f"\n📈 TOTALS:")
        print(f"   Players processed: {total_processed}")
        print(f"   Games collected: {total_games:,}")
        print(f"   Errors: {total_errors}")
        print(f"   Collection rate: {total_processed / (total_time / 60):.1f} players/min")

        # Step 5: Calculate season averages
        print(f"\n📊 Calculating season averages...")
        self.collector.calculate_season_averages()

        # Step 6: Collect schedule
        print(f"\n📅 Collecting schedule...")
        await self.collector.collect_schedule()

        # Step 7: Final status
        print("\n" + "=" * 100)
        print("  FINAL COLLECTION STATUS")
        print("=" * 100)

        status = self.collector.get_collection_status()
        print(f"\n📊 Database Summary:")
        print(f"   Teams: {status.get('teams_count', 0)}")
        print(f"   Players: {status.get('players_count', 0)}")
        print(f"   Game Logs: {status.get('game_logs_count', 0):,}")
        print(f"   Season Averages: {status.get('season_averages_count', 0)}")
        print(f"   Schedule Games: {status.get('schedule_games_count', 0)}")

        if self.errors:
            print(f"\n⚠️  Errors encountered ({len(self.errors)}):")
            for err in self.errors[:10]:  # Show first 10
                print(f"   {err['worker']}: {err['player']} - {err['error'][:60]}")
            if len(self.errors) > 10:
                print(f"   ... and {len(self.errors) - 10} more")

        print("\n" + "=" * 100)
        print("✅ ORCHESTRATED PARALLEL COLLECTION COMPLETE!")
        print("=" * 100 + "\n")

        return {
            'success': True,
            'total_time_minutes': total_time / 60,
            'players_processed': total_processed,
            'games_collected': total_games,
            'errors': total_errors
        }


async def main():
    """Main entry point"""

    # Create orchestrator with 10 worker agents
    manager = OrchestratedCollectionManager(num_workers=10)

    # Run orchestrated parallel collection
    result = await manager.orchestrate_parallel_collection()

    return 0 if result['success'] else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
