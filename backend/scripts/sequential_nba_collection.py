#!/usr/bin/env python3
"""
Sequential NBA Data Collection (Reliable Version)

Uses simple sequential processing with proper rate limiting.
Estimated time: ~26 minutes for 526 players at 20 req/min
"""

import sys
import time
import sqlite3
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.nba_stats_collector import NBAStatsCollector
from nba_api.stats.endpoints import playergamelog


def collect_all_game_logs():
    """
    Collect game logs for all players sequentially
    """
    print("=" * 100)
    print("  SEQUENTIAL NBA DATA COLLECTION")
    print("=" * 100)
    print(f"\n🏀 2025-26 NBA Season Data Collection")
    print(f"⏱️  Estimated time: ~26 minutes (526 players at 20 req/min)")
    print(f"📊 Strategy: Sequential processing with rate limiting\n")

    collector = NBAStatsCollector()

    # Get all players
    conn = sqlite3.connect(collector.teams_db)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT DISTINCT player_id, full_name
    FROM rosters
    WHERE season = ?
    ORDER BY full_name
    ''', (collector.current_season,))
    all_players = cursor.fetchall()
    conn.close()

    total_players = len(all_players)
    print(f"✅ Loaded {total_players} players from database\n")
    print("=" * 100)

    # Open stats database for writing
    stats_conn = sqlite3.connect(collector.stats_db)
    stats_cursor = stats_conn.cursor()

    # Track progress
    start_time = time.time()
    collected = 0
    total_games = 0
    errors = []
    no_games = 0

    try:
        for idx, (player_id, player_name) in enumerate(all_players, 1):
            try:
                # Rate limiting - wait 3 seconds between requests (20/min)
                time.sleep(3)

                # Fetch game logs
                gamelog = playergamelog.PlayerGameLog(
                    player_id=player_id,
                    season=collector.current_season
                )

                df = gamelog.get_data_frames()[0]

                if len(df) == 0:
                    no_games += 1
                    status = f"⚠️  No games"
                else:
                    # Insert game logs
                    for _, game in df.iterrows():
                        game_id = game.get('Game_ID') or game.get('GAME_ID', '')
                        stats_cursor.execute('''
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
                    status = f"✅ {len(df)} games"

                    # Commit every 5 players
                    if idx % 5 == 0:
                        stats_conn.commit()

                collected += 1

                # Calculate ETA
                elapsed = time.time() - start_time
                if idx > 0:
                    avg_time_per_player = elapsed / idx
                    players_remaining = total_players - idx
                    eta_seconds = players_remaining * avg_time_per_player
                    eta_minutes = eta_seconds / 60
                    eta_str = f"ETA: {eta_minutes:.1f}min"
                else:
                    eta_str = "ETA: calculating..."

                # Progress output
                print(f"\r[{idx}/{total_players}] {player_name[:40]:40} {status:20} | Total: {total_games:,} games | {eta_str}   ", end="", flush=True)

                # New line every 10 players
                if idx % 10 == 0:
                    print()

            except Exception as e:
                error_msg = str(e)[:100]
                errors.append({'player': player_name, 'error': error_msg})
                print(f"\r[{idx}/{total_players}] {player_name[:40]:40} ❌ ERROR: {error_msg[:50]}   ")

    except KeyboardInterrupt:
        print("\n\n⚠️  Collection interrupted by user")

    finally:
        # Final commit
        stats_conn.commit()
        stats_conn.close()

    print("\n" + "=" * 100)

    # Calculate statistics
    total_time = time.time() - start_time

    print(f"\n✅ COLLECTION COMPLETE in {total_time / 60:.1f} minutes")
    print(f"\n📊 Results:")
    print(f"   Players processed: {collected}")
    print(f"   Games collected: {total_games:,}")
    print(f"   Players with no games: {no_games}")
    print(f"   Errors: {len(errors)}")
    print(f"   Collection rate: {collected / (total_time / 60):.1f} players/min")

    if errors:
        print(f"\n⚠️  Errors encountered ({len(errors)}):")
        for err in errors[:10]:  # Show first 10
            print(f"   {err['player']}: {err['error']}")
        if len(errors) > 10:
            print(f"   ... and {len(errors) - 10} more")

    # Calculate season averages
    print(f"\n📊 Calculating season averages...")
    collector.calculate_season_averages()

    # Collect schedule
    print(f"\n📅 Collecting schedule...")
    import asyncio
    asyncio.run(collector.collect_schedule())

    # Final status
    print("\n" + "=" * 100)
    print("  FINAL COLLECTION STATUS")
    print("=" * 100)

    status = collector.get_collection_status()
    print(f"\n📊 Database Summary:")
    print(f"   Teams: {status.get('teams_count', 0)}")
    print(f"   Players: {status.get('players_count', 0)}")
    print(f"   Game Logs: {status.get('game_logs_count', 0):,}")
    print(f"   Season Averages: {status.get('season_averages_count', 0)}")
    print(f"   Schedule Games: {status.get('schedule_games_count', 0)}")

    print("\n" + "=" * 100)
    print("✅ NBA DATA COLLECTION COMPLETE!")
    print("=" * 100 + "\n")


if __name__ == "__main__":
    collect_all_game_logs()
