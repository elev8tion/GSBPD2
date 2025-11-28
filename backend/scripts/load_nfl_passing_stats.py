#!/usr/bin/env python3
"""
NFL Team Passing Stats Pipeline
Loads NFL team passing statistics into Kre8VidMems memory system
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


def format_team_passing_stats(team: Dict[str, Any]) -> str:
    """Format a team's passing stats into searchable text."""
    parts = []

    # Team name
    team_name = team.get('team', 'Unknown')
    parts.append(f"Team: {team_name}")
    parts.append(f"NFL 2024 Season Offensive Passing Statistics")

    # Core passing stats
    attempts = team.get('attempts', 0)
    completions = team.get('completions', 0)
    comp_pct = team.get('completion_percentage', 0)
    parts.append(f"Pass Attempts: {attempts}")
    parts.append(f"Completions: {completions}")
    parts.append(f"Completion Percentage: {comp_pct}%")

    # Yards and averages
    yards = team.get('passing_yards', 0)
    ypa = team.get('yards_per_attempt', 0)
    parts.append(f"Passing Yards: {yards:,}")
    parts.append(f"Yards per Attempt: {ypa}")

    # Scoring
    tds = team.get('touchdowns', 0)
    ints = team.get('interceptions', 0)
    rating = team.get('passer_rating', 0)
    parts.append(f"Passing Touchdowns: {tds}")
    parts.append(f"Interceptions: {ints}")
    parts.append(f"Passer Rating: {rating}")

    # TD/INT ratio
    if ints > 0:
        td_int_ratio = round(tds / ints, 2)
        parts.append(f"TD/INT Ratio: {td_int_ratio}")

    # First downs
    first_downs = team.get('first_downs', 0)
    first_down_pct = team.get('first_down_percentage', 0)
    parts.append(f"Passing First Downs: {first_downs}")
    parts.append(f"First Down Percentage: {first_down_pct}%")

    # Big plays
    plays_20 = team.get('plays_20_plus', 0)
    plays_40 = team.get('plays_40_plus', 0)
    longest = team.get('longest', 0)
    parts.append(f"20+ Yard Plays: {plays_20}")
    parts.append(f"40+ Yard Plays: {plays_40}")
    parts.append(f"Longest Pass: {longest} yards")

    # Sacks
    sacks = team.get('sacks', 0)
    sack_yards = team.get('sack_yards', 0)
    parts.append(f"Sacks Taken: {sacks}")
    parts.append(f"Sack Yards Lost: {sack_yards}")

    # Create searchable text
    text = " | ".join(parts)

    # Add searchable terms and rankings
    text += f" | {team_name} offensive passing stats | {team_name} offense"
    text += f" | {team_name} offensive passing yards | {team_name} offensive touchdowns"
    text += f" | {team_name} quarterback stats | {team_name} offensive completion percentage"
    text += f" | {team_name} offensive stats | {team_name} offensive performance"

    # Add ranking-related terms for easy searching
    if yards > 3500:
        text += " | top passing offense | elite passing attack"
    elif yards > 3000:
        text += " | good passing offense | above average passing"
    elif yards < 2500:
        text += " | struggling passing offense | below average passing"

    if rating > 100:
        text += " | elite passer rating | excellent quarterback play"
    elif rating > 90:
        text += " | good passer rating | solid quarterback play"
    elif rating < 80:
        text += " | poor passer rating | struggling quarterback play"

    if tds > 25:
        text += " | high scoring passing offense"
    if ints < 10:
        text += " | low interception rate | protecting the ball"
    elif ints > 15:
        text += " | high interception rate | turnover issues"

    return text


def process_passing_stats(stats_path: str) -> List[str]:
    """Process NFL team passing stats JSON into memory chunks."""
    print(f"Loading passing stats from: {stats_path}")

    with open(stats_path, 'r') as f:
        data = json.load(f)

    chunks = []

    # Add overall league summary
    summary = []
    summary.append(f"NFL 2024 Season Offensive Passing Statistics Overview")
    summary.append(f"Total Teams: {data.get('total_teams', 32)}")
    summary.append(f"Conference: {data.get('conference', 'All Teams')}")
    summary.append(f"Stat Type: Offensive {data.get('stat_type', 'Passing Statistics')}")
    chunks.append(" | ".join(summary))

    # Process each team's stats
    teams = data.get('teams', [])
    print(f"  Processing {len(teams)} teams")

    for team_data in teams:
        chunk = format_team_passing_stats(team_data)
        chunks.append(chunk)

    # Calculate and add league leaders
    if teams:
        # Most passing yards
        yards_leader = max(teams, key=lambda x: x.get('passing_yards', 0))
        chunks.append(f"Passing Yards Leader: {yards_leader['team']} with {yards_leader['passing_yards']:,} yards")

        # Most passing TDs
        td_leader = max(teams, key=lambda x: x.get('touchdowns', 0))
        chunks.append(f"Passing Touchdowns Leader: {td_leader['team']} with {td_leader['touchdowns']} touchdowns")

        # Best passer rating
        rating_leader = max(teams, key=lambda x: x.get('passer_rating', 0))
        chunks.append(f"Passer Rating Leader: {rating_leader['team']} with {rating_leader['passer_rating']} rating")

        # Best completion percentage
        comp_leader = max(teams, key=lambda x: x.get('completion_percentage', 0))
        chunks.append(f"Completion Percentage Leader: {comp_leader['team']} at {comp_leader['completion_percentage']}%")

        # Fewest interceptions
        int_leader = min(teams, key=lambda x: x.get('interceptions', 999))
        chunks.append(f"Fewest Interceptions: {int_leader['team']} with {int_leader['interceptions']} interceptions")

    return chunks


def main():
    """Main pipeline execution."""
    print("=" * 60)
    print("NFL TEAM PASSING STATS PIPELINE")
    print("=" * 60)
    print()

    # Paths
    stats_file = "/Users/kcdacre8tor/Downloads/nfl_team_passing_stats.json"
    memory_dir = "/Users/kcdacre8tor/GSBPD2/backend/data/memories"

    # Check if file exists
    if not os.path.exists(stats_file):
        print(f"❌ Passing stats file not found: {stats_file}")
        return 1

    print(f"📊 Loading NFL team passing statistics")
    print()

    # Process stats data
    try:
        chunks = process_passing_stats(stats_file)
        print(f"\n✅ Processed {len(chunks)} stat records")
    except Exception as e:
        print(f"❌ Error processing stats: {e}")
        return 1

    # Initialize Kre8VidMems
    print("\n🧠 Initializing Kre8VidMems for passing stats...")
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
    memory_name = f"{memory_dir}/nfl-passing-stats"
    memory.save(memory_name)

    elapsed_time = time.time() - start_time
    print(f"\n✅ Successfully loaded passing stats in {elapsed_time:.2f} seconds")
    print(f"📂 Memory saved to: {memory_name}.*")

    # Test with sample queries
    print("\n🔍 Testing search functionality...")
    print("   (Note: search() function may need adjustment for this API version)")

    # Display some interesting stats
    print("\n📈 Quick Stats Summary:")
    with open(stats_file, 'r') as f:
        data = json.load(f)
        teams = data.get('teams', [])

        if teams:
            avg_yards = sum(t.get('passing_yards', 0) for t in teams) / len(teams)
            avg_tds = sum(t.get('touchdowns', 0) for t in teams) / len(teams)
            avg_rating = sum(t.get('passer_rating', 0) for t in teams) / len(teams)

            print(f"   Average Passing Yards: {avg_yards:,.1f}")
            print(f"   Average Passing TDs: {avg_tds:.1f}")
            print(f"   Average Passer Rating: {avg_rating:.1f}")

    print("\n" + "=" * 60)
    print("✅ NFL PASSING STATS PIPELINE COMPLETE")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())