#!/usr/bin/env python3
"""
NFL Team Offensive Down Conversion Stats Pipeline
Loads NFL team offensive down conversion statistics into Kre8VidMems memory system
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


def format_team_offensive_downs_stats(team: Dict[str, Any]) -> str:
    """Format a team's offensive down conversion stats into searchable text."""
    parts = []

    # Team name
    team_name = team.get('team', 'Unknown')
    parts.append(f"Team: {team_name}")
    parts.append(f"NFL 2024 Season Offensive Down Conversion Statistics")

    # 3rd down offense
    third_attempts = team.get('third_down_attempts', 0)
    third_made = team.get('third_down_made', 0)
    third_pct = team.get('third_down_percentage', 0)
    parts.append(f"3rd Down Conversions: {third_made}/{third_attempts} ({third_pct}%)")

    # 4th down offense
    fourth_attempts = team.get('fourth_down_attempts', 0)
    fourth_made = team.get('fourth_down_made', 0)
    fourth_pct = team.get('fourth_down_percentage', 0)
    parts.append(f"4th Down Conversions: {fourth_made}/{fourth_attempts} ({fourth_pct}%)")

    # First downs
    rec_first = team.get('receiving_first_downs', 0)
    rec_first_pct = team.get('receiving_first_down_percentage', 0)
    rush_first = team.get('rushing_first_downs', 0)
    rush_first_pct = team.get('rushing_first_down_percentage', 0)
    total_first = rec_first + rush_first

    parts.append(f"Total First Downs: {total_first}")
    parts.append(f"Passing First Downs: {rec_first} ({rec_first_pct}% of receptions)")
    parts.append(f"Rushing First Downs: {rush_first} ({rush_first_pct}% of rushes)")

    # Scrimmage plays
    plays = team.get('scrimmage_plays', 0)
    parts.append(f"Total Scrimmage Plays: {plays}")

    # Calculate efficiency
    if plays > 0:
        first_down_rate = (total_first / plays * 100)
        parts.append(f"First Down Rate: {first_down_rate:.1f}% of plays")

    text = " | ".join(parts)

    # Add searchable terms
    text += f" | {team_name} offensive down conversions | {team_name} 3rd down offense"
    text += f" | {team_name} 4th down offense | {team_name} offensive stats"
    text += f" | {team_name} situational offense | {team_name} offense"
    text += f" | {team_name} conversion rate | {team_name} offensive efficiency"
    text += f" | {team_name} moving the chains | {team_name} sustaining drives"

    # Rankings based on performance
    if third_pct > 45:
        text += " | elite 3rd down offense | converting third downs | clutch offense"
        text += " | moving the chains consistently | efficient offense"
    elif third_pct > 40:
        text += " | good 3rd down offense | above average conversions"
    elif third_pct < 35:
        text += " | struggling 3rd down offense | poor conversion rate"
        text += " | offensive inefficiency | can't sustain drives"

    if fourth_pct > 60 and fourth_attempts > 5:
        text += " | aggressive 4th down team | converting 4th downs | analytics-driven"
        text += " | going for it | gutsy play calling"
    elif fourth_pct < 40 and fourth_attempts > 5:
        text += " | poor 4th down conversion | struggling on 4th"

    # First down efficiency
    if rec_first_pct > 60:
        text += " | excellent passing efficiency | moving chains through air"
    if rush_first_pct > 45:
        text += " | strong rushing efficiency | ground game moving chains"

    return text


def process_offensive_downs_stats(stats_path: str) -> List[str]:
    """Process NFL team offensive down conversion stats JSON into memory chunks."""
    print(f"Loading offensive down conversion stats from: {stats_path}")

    with open(stats_path, 'r') as f:
        data = json.load(f)

    chunks = []

    # Add overall league summary
    summary = []
    summary.append(f"NFL 2024 Season Offensive Down Conversion Statistics Overview")
    summary.append(f"Total Teams: {data.get('total_teams', 32)}")
    summary.append(f"Stat Type: {data.get('stat_type', 'Offensive Down Conversions')}")
    summary.append(f"Category: Offensive Statistics")
    chunks.append(" | ".join(summary))

    # Process each team's stats
    teams = data.get('teams', [])
    print(f"  Processing {len(teams)} teams")

    for team_data in teams:
        chunk = format_team_offensive_downs_stats(team_data)
        chunks.append(chunk)

    # Calculate and add league leaders
    if teams:
        # Best 3rd down offense
        third_leader = max(teams, key=lambda x: x.get('third_down_percentage', 0))
        chunks.append(f"Best 3rd Down Offense: {third_leader['team']} converting {third_leader['third_down_percentage']}% | Elite conversion rate | Clutch offense")

        # Best 4th down offense (minimum 5 attempts)
        fourth_candidates = [t for t in teams if t.get('fourth_down_attempts', 0) >= 5]
        if fourth_candidates:
            fourth_leader = max(fourth_candidates, key=lambda x: x.get('fourth_down_percentage', 0))
            chunks.append(f"Best 4th Down Offense: {fourth_leader['team']} converting {fourth_leader['fourth_down_percentage']}% | Aggressive play calling | Analytics-driven")

        # Most total first downs
        first_downs_leader = max(teams, key=lambda x: x.get('receiving_first_downs', 0) + x.get('rushing_first_downs', 0))
        total_fd = first_downs_leader.get('receiving_first_downs', 0) + first_downs_leader.get('rushing_first_downs', 0)
        chunks.append(f"Most First Downs: {first_downs_leader['team']} with {total_fd} | Moving the chains | Sustained drives")

        # Best passing first down percentage
        pass_eff_leader = max(teams, key=lambda x: x.get('receiving_first_down_percentage', 0))
        chunks.append(f"Best Passing Efficiency: {pass_eff_leader['team']} with {pass_eff_leader['receiving_first_down_percentage']}% | Efficient passing attack")

        # Best rushing first down percentage
        rush_eff_leader = max(teams, key=lambda x: x.get('rushing_first_down_percentage', 0))
        chunks.append(f"Best Rushing Efficiency: {rush_eff_leader['team']} with {rush_eff_leader['rushing_first_down_percentage']}% | Dominant ground game")

        # Worst 3rd down offense
        third_worst = min(teams, key=lambda x: x.get('third_down_percentage', 0))
        chunks.append(f"Worst 3rd Down Offense: {third_worst['team']} converting {third_worst['third_down_percentage']}% | Struggling on third down")

    return chunks


def main():
    """Main pipeline execution."""
    print("=" * 60)
    print("NFL TEAM OFFENSIVE DOWN CONVERSION STATS PIPELINE")
    print("=" * 60)
    print()

    # Paths
    stats_file = "/Users/kcdacre8tor/Downloads/nfl_team_offensive_downs_stats.json"
    memory_dir = "/Users/kcdacre8tor/GSBPD2/backend/data/memories"

    # Check if file exists
    if not os.path.exists(stats_file):
        print(f"❌ Offensive down conversion stats file not found: {stats_file}")
        return 1

    print(f"🏈 Loading NFL team offensive down conversion statistics")
    print()

    # Process stats data
    try:
        chunks = process_offensive_downs_stats(stats_file)
        print(f"\n✅ Processed {len(chunks)} stat records")
    except Exception as e:
        print(f"❌ Error processing stats: {e}")
        return 1

    # Initialize Kre8VidMems
    print("\n🧠 Initializing Kre8VidMems for offensive down conversion stats...")
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
    memory_name = f"{memory_dir}/nfl-offensive-downs-stats"
    memory.save(memory_name)

    elapsed_time = time.time() - start_time
    print(f"\n✅ Successfully loaded offensive down conversion stats in {elapsed_time:.2f} seconds")
    print(f"📂 Memory saved to: {memory_name}.*")

    # Display some interesting stats
    print("\n📈 Quick Stats Summary:")
    with open(stats_file, 'r') as f:
        data = json.load(f)
        teams = data.get('teams', [])

        if teams:
            avg_third = sum(t.get('third_down_percentage', 0) for t in teams) / len(teams)
            avg_fourth = sum(t.get('fourth_down_percentage', 0) for t in teams) / len(teams)
            avg_plays = sum(t.get('scrimmage_plays', 0) for t in teams) / len(teams)

            print(f"   Average 3rd Down Conversion: {avg_third:.1f}%")
            print(f"   Average 4th Down Conversion: {avg_fourth:.1f}%")
            print(f"   Average Scrimmage Plays: {avg_plays:.1f}")

            # Find best and worst 3rd down teams
            best_team = max(teams, key=lambda x: x.get('third_down_percentage', 0))
            worst_team = min(teams, key=lambda x: x.get('third_down_percentage', 0))
            print(f"   Best 3rd Down: {best_team['team']} ({best_team['third_down_percentage']}%)")
            print(f"   Worst 3rd Down: {worst_team['team']} ({worst_team['third_down_percentage']}%)")

    print("\n" + "=" * 60)
    print("✅ NFL OFFENSIVE DOWN CONVERSION STATS PIPELINE COMPLETE")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())