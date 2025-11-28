#!/usr/bin/env python3
"""
NFL Team Rushing Stats Pipeline
Loads NFL team rushing statistics into Kre8VidMems memory system
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Any
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.kre8vidmems.kre8vidmems.api.memory import Kre8VidMemory


def format_team_rushing_stats(team: Dict[str, Any]) -> str:
    """Format a team's rushing stats into searchable text."""
    parts = []

    # Team name
    team_name = team.get('team', 'Unknown')
    parts.append(f"Team: {team_name}")
    parts.append(f"NFL 2024 Season Offensive Rushing Statistics")

    # Core rushing stats
    attempts = team.get('attempts', 0)
    yards = team.get('rushing_yards', 0)
    ypc = team.get('yards_per_carry', 0)
    parts.append(f"Rush Attempts: {attempts}")
    parts.append(f"Rushing Yards: {yards:,}")
    parts.append(f"Yards per Carry: {ypc}")

    # Calculate yards per game (assuming ~12 games played so far)
    ypg = yards / 12 if yards > 0 else 0
    parts.append(f"Rushing Yards per Game: {ypg:.1f}")

    # Scoring
    tds = team.get('touchdowns', 0)
    parts.append(f"Rushing Touchdowns: {tds}")

    # Efficiency metrics
    if attempts > 0:
        td_rate = (tds / attempts) * 100
        parts.append(f"TD Rate: {td_rate:.1f}% of attempts")

    # Big plays
    plays_20 = team.get('plays_20_plus', 0)
    plays_40 = team.get('plays_40_plus', 0)
    longest = team.get('longest', 0)
    parts.append(f"20+ Yard Runs: {plays_20}")
    parts.append(f"40+ Yard Runs: {plays_40}")
    parts.append(f"Longest Run: {longest} yards")

    # First downs
    first_downs = team.get('rush_first_downs', 0)
    first_down_pct = team.get('rush_first_down_percentage', 0)
    parts.append(f"Rushing First Downs: {first_downs}")
    parts.append(f"First Down Percentage: {first_down_pct}%")

    # Fumbles
    fumbles = team.get('rush_fumbles', 0)
    parts.append(f"Rushing Fumbles: {fumbles}")

    # Calculate fumble rate
    if attempts > 0:
        fumble_rate = (fumbles / attempts) * 100
        parts.append(f"Fumble Rate: {fumble_rate:.2f}%")

    # Create searchable text
    text = " | ".join(parts)

    # Add searchable terms
    text += f" | {team_name} offensive rushing stats | {team_name} offensive ground game"
    text += f" | {team_name} offensive rushing yards | {team_name} running backs"
    text += f" | {team_name} yards per carry | {team_name} offensive rushing attack"
    text += f" | {team_name} offensive stats | {team_name} offensive performance"

    # Add ranking-related terms
    if yards > 1800:
        text += " | elite rushing offense | dominant ground game | top rushing attack"
    elif yards > 1500:
        text += " | good rushing offense | strong ground game | above average rushing"
    elif yards < 1200:
        text += " | struggling rushing offense | weak ground game | below average rushing"

    if ypc > 4.5:
        text += " | efficient rushing attack | high yards per carry"
    elif ypc < 3.8:
        text += " | inefficient rushing | poor yards per carry"

    if tds > 15:
        text += " | high scoring rushing offense | red zone rushing threat"
    elif tds < 10:
        text += " | low rushing touchdowns | struggling in red zone"

    if fumbles < 3:
        text += " | ball security | protecting the football"
    elif fumbles > 5:
        text += " | fumble issues | ball security problems"

    return text


def process_rushing_stats(stats_path: str) -> List[str]:
    """Process NFL team rushing stats JSON into memory chunks."""
    print(f"Loading rushing stats from: {stats_path}")

    with open(stats_path, 'r') as f:
        data = json.load(f)

    chunks = []

    # Add overall league summary
    summary = []
    summary.append(f"NFL 2024 Season Offensive Rushing Statistics Overview")
    summary.append(f"Total Teams: {data.get('total_teams', 32)}")
    summary.append(f"Conference: {data.get('conference', 'All Teams')}")
    summary.append(f"Stat Type: Offensive {data.get('stat_type', 'Rushing Statistics')}")
    chunks.append(" | ".join(summary))

    # Process each team's stats
    teams = data.get('teams', [])
    print(f"  Processing {len(teams)} teams")

    for team_data in teams:
        chunk = format_team_rushing_stats(team_data)
        chunks.append(chunk)

    # Calculate and add league leaders
    if teams:
        # Most rushing yards
        yards_leader = max(teams, key=lambda x: x.get('rushing_yards', 0))
        chunks.append(f"Rushing Yards Leader: {yards_leader['team']} with {yards_leader['rushing_yards']:,} yards | League leader | Top rushing offense")

        # Most rushing TDs
        td_leader = max(teams, key=lambda x: x.get('touchdowns', 0))
        chunks.append(f"Rushing Touchdowns Leader: {td_leader['team']} with {td_leader['touchdowns']} touchdowns | League leader | Top scoring ground game")

        # Best yards per carry (min 200 attempts)
        eligible_teams = [t for t in teams if t.get('attempts', 0) >= 200]
        if eligible_teams:
            ypc_leader = max(eligible_teams, key=lambda x: x.get('yards_per_carry', 0))
            chunks.append(f"Yards per Carry Leader: {ypc_leader['team']} at {ypc_leader['yards_per_carry']} YPC | Most efficient rushing attack")

        # Fewest fumbles
        fumble_leader = min(teams, key=lambda x: x.get('rush_fumbles', 999))
        chunks.append(f"Fewest Fumbles: {fumble_leader['team']} with {fumble_leader['rush_fumbles']} fumbles | Best ball security")

        # Most explosive plays
        explosive_leader = max(teams, key=lambda x: x.get('plays_20_plus', 0))
        chunks.append(f"Most Explosive Runs (20+): {explosive_leader['team']} with {explosive_leader['plays_20_plus']} big plays | Most explosive ground game")

    return chunks


def main():
    """Main pipeline execution."""
    print("=" * 60)
    print("NFL TEAM RUSHING STATS PIPELINE")
    print("=" * 60)
    print()

    # Paths
    stats_file = "/Users/kcdacre8tor/Downloads/nfl_team_rushing_stats.json"
    memory_dir = "/Users/kcdacre8tor/GSBPD2/backend/data/memories"

    # Check if file exists
    if not os.path.exists(stats_file):
        print(f"❌ Rushing stats file not found: {stats_file}")
        return 1

    print(f"📊 Loading NFL team rushing statistics")
    print()

    # Process stats data
    try:
        chunks = process_rushing_stats(stats_file)
        print(f"\n✅ Processed {len(chunks)} stat records")
    except Exception as e:
        print(f"❌ Error processing stats: {e}")
        return 1

    # Initialize Kre8VidMems
    print("\n🧠 Initializing Kre8VidMems for rushing stats...")
    memory = Kre8VidMemory()

    # Add chunks to memory
    print(f"📝 Adding {len(chunks)} records to memory...")
    start_time = time.time()

    # Add all chunks
    for i, chunk in enumerate(chunks, 1):
        memory.add(chunk)
        if i % 10 == 0:
            print(f"  Added {i}/{len(chunks)} records...")

    # Save the memory
    memory_name = f"{memory_dir}/nfl-rushing-stats"
    memory.save(memory_name)

    elapsed_time = time.time() - start_time
    print(f"\n✅ Successfully loaded rushing stats in {elapsed_time:.2f} seconds")
    print(f"📂 Memory saved to: {memory_name}.*")

    # Display some interesting stats
    print("\n📈 Quick Stats Summary:")
    with open(stats_file, 'r') as f:
        data = json.load(f)
        teams = data.get('teams', [])

        if teams:
            avg_yards = sum(t.get('rushing_yards', 0) for t in teams) / len(teams)
            avg_tds = sum(t.get('touchdowns', 0) for t in teams) / len(teams)
            avg_ypc = sum(t.get('yards_per_carry', 0) for t in teams) / len(teams)
            total_fumbles = sum(t.get('rush_fumbles', 0) for t in teams)

            print(f"   Average Rushing Yards: {avg_yards:,.1f}")
            print(f"   Average Rushing TDs: {avg_tds:.1f}")
            print(f"   Average Yards per Carry: {avg_ypc:.2f}")
            print(f"   Total League Fumbles: {total_fumbles}")

            # Find best and worst rushing teams
            best_team = max(teams, key=lambda x: x.get('rushing_yards', 0))
            worst_team = min(teams, key=lambda x: x.get('rushing_yards', 0))
            print(f"   Best Rushing Team: {best_team['team']} ({best_team['rushing_yards']:,} yards)")
            print(f"   Worst Rushing Team: {worst_team['team']} ({worst_team['rushing_yards']:,} yards)")

    print("\n" + "=" * 60)
    print("✅ NFL RUSHING STATS PIPELINE COMPLETE")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())