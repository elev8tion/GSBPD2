#!/usr/bin/env python3
"""
NBA Data Collection Script
Collects all NBA data for 2025-26 season

Usage:
    python scripts/collect_nba_data.py [--full | --teams-only | --gamelogs-only | --schedule-only]

Options:
    --full: Collect everything (teams, game logs, schedule) [DEFAULT]
    --teams-only: Only collect teams and rosters
    --gamelogs-only: Only collect player game logs
    --schedule-only: Only collect schedule
    --limit N: Limit game logs to N players (for testing)
"""

import asyncio
import sys
import argparse
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.nba_stats_collector import NBAStatsCollector


async def main():
    parser = argparse.ArgumentParser(description='Collect NBA data for 2025-26 season')
    parser.add_argument('--full', action='store_true', help='Collect everything (default)')
    parser.add_argument('--teams-only', action='store_true', help='Only collect teams/rosters')
    parser.add_argument('--gamelogs-only', action='store_true', help='Only collect game logs')
    parser.add_argument('--schedule-only', action='store_true', help='Only collect schedule')
    parser.add_argument('--limit', type=int, help='Limit game logs to N players')

    args = parser.parse_args()

    # Default to full collection
    collect_teams = args.full or args.teams_only or (not any([args.teams_only, args.gamelogs_only, args.schedule_only]))
    collect_gamelogs = args.full or args.gamelogs_only or (not any([args.teams_only, args.gamelogs_only, args.schedule_only]))
    collect_schedule = args.full or args.schedule_only or (not any([args.teams_only, args.gamelogs_only, args.schedule_only]))

    print("="*80)
    print("  NBA DATA COLLECTION - 2025-26 SEASON")
    print("="*80)
    print(f"\n📋 Collection Plan:")
    print(f"  {'✅' if collect_teams else '❌'} Teams & Rosters")
    print(f"  {'✅' if collect_gamelogs else '❌'} Player Game Logs{f' (limit: {args.limit})' if args.limit else ''}")
    print(f"  {'✅' if collect_schedule else '❌'} Schedule")
    print()

    collector = NBAStatsCollector()

    # PHASE 1: Collect teams and rosters
    if collect_teams:
        result = await collector.collect_all_teams()
        if result['status'] != 'success':
            print(f"\n❌ Failed to collect teams: {result.get('message')}")
            return 1

    # PHASE 2: Collect player game logs
    if collect_gamelogs:
        result = await collector.collect_player_gamelogs(limit=args.limit)
        if result['status'] != 'success':
            print(f"\n❌ Failed to collect game logs: {result.get('message')}")
            return 1

        # Calculate season averages
        print("\n")
        result = collector.calculate_season_averages()
        if result['status'] != 'success':
            print(f"\n❌ Failed to calculate averages: {result.get('message')}")
            return 1

    # PHASE 3: Collect schedule
    if collect_schedule:
        result = await collector.collect_schedule()
        if result['status'] != 'success':
            print(f"\n❌ Failed to collect schedule: {result.get('message')}")
            return 1

    # Final status
    print("\n" + "="*80)
    print("  FINAL COLLECTION STATUS")
    print("="*80)

    status = collector.get_collection_status()
    print(f"\n📊 Collection Summary:")
    print(f"  Teams: {status.get('teams_count', 0)}")
    print(f"  Players: {status.get('players_count', 0)}")
    print(f"  Game Logs: {status.get('game_logs_count', 0):,}")
    print(f"  Season Averages: {status.get('season_averages_count', 0)}")
    print(f"  Schedule Games: {status.get('schedule_games_count', 0)}")
    print(f"\n💾 Databases:")
    for name, path in status.get('databases', {}).items():
        print(f"  {name}: {path}")

    print("\n" + "="*80)
    print("✅ NBA DATA COLLECTION COMPLETE!")
    print("="*80 + "\n")

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
