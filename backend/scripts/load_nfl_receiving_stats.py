#!/usr/bin/env python3
"""
NFL Team Receiving Stats Pipeline
Loads NFL team receiving statistics into Kre8VidMems memory system
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


def format_team_receiving_stats(team: Dict[str, Any]) -> str:
    """Format a team's receiving stats into searchable text."""
    parts = []

    # Team name
    team_name = team.get('team', 'Unknown')
    parts.append(f"Team: {team_name}")
    parts.append(f"NFL 2024 Season Offensive Receiving Statistics")

    # Core receiving stats
    receptions = team.get('receptions', 0)
    yards = team.get('receiving_yards', 0)
    ypr = team.get('yards_per_reception', 0)
    parts.append(f"Receptions: {receptions}")
    parts.append(f"Receiving Yards: {yards:,}")
    parts.append(f"Yards per Reception: {ypr}")

    # Calculate yards per game (assuming ~12 games played so far)
    ypg = yards / 12 if yards > 0 else 0
    parts.append(f"Receiving Yards per Game: {ypg:.1f}")

    # Scoring
    tds = team.get('touchdowns', 0)
    parts.append(f"Receiving Touchdowns: {tds}")

    # TD rate
    if receptions > 0:
        td_rate = (tds / receptions) * 100
        parts.append(f"TD Rate: {td_rate:.1f}% of receptions")

    # Big plays
    plays_20 = team.get('plays_20_plus', 0)
    plays_40 = team.get('plays_40_plus', 0)
    longest = team.get('longest', 0)
    parts.append(f"20+ Yard Receptions: {plays_20}")
    parts.append(f"40+ Yard Receptions: {plays_40}")
    parts.append(f"Longest Reception: {longest} yards")

    # First downs
    first_downs = team.get('receiving_first_downs', 0)
    first_down_pct = team.get('receiving_first_down_percentage', 0)
    parts.append(f"Receiving First Downs: {first_downs}")
    parts.append(f"First Down Percentage: {first_down_pct}%")

    # Fumbles
    fumbles = team.get('receiving_fumbles', 0)
    parts.append(f"Receiving Fumbles: {fumbles}")

    # Calculate fumble rate
    if receptions > 0:
        fumble_rate = (fumbles / receptions) * 100
        parts.append(f"Fumble Rate: {fumble_rate:.2f}%")

    # Create searchable text
    text = " | ".join(parts)

    # Add searchable terms
    text += f" | {team_name} offensive receiving stats | {team_name} offensive passing game"
    text += f" | {team_name} offensive receiving yards | {team_name} wide receivers"
    text += f" | {team_name} yards per catch | {team_name} offensive aerial attack"
    text += f" | {team_name} pass catchers | {team_name} offensive reception yards"
    text += f" | {team_name} offensive stats | {team_name} offensive performance"

    # Add ranking-related terms
    if yards > 3000:
        text += " | elite receiving corps | dominant passing attack | top receiving unit"
    elif yards > 2500:
        text += " | good receiving corps | strong passing game | above average receiving"
    elif yards < 2000:
        text += " | struggling receiving corps | weak passing game | below average receiving"

    if ypr > 12:
        text += " | explosive receiving unit | big play threat | deep passing attack"
    elif ypr < 10:
        text += " | short passing game | possession receivers | conservative passing"

    if tds > 20:
        text += " | high scoring aerial attack | red zone receiving threat"
    elif tds < 10:
        text += " | low receiving touchdowns | struggling in passing game"

    if fumbles < 2:
        text += " | sure-handed receivers | secure ball handling"
    elif fumbles > 4:
        text += " | fumble issues | ball security problems"

    if plays_20 > 35:
        text += " | explosive passing plays | big play receiving threat"
    elif plays_20 < 20:
        text += " | lack of explosive plays | limited big play ability"

    return text


def process_receiving_stats(stats_path: str) -> List[str]:
    """Process NFL team receiving stats JSON into memory chunks."""
    print(f"Loading receiving stats from: {stats_path}")

    with open(stats_path, 'r') as f:
        data = json.load(f)

    chunks = []

    # Add overall league summary
    summary = []
    summary.append(f"NFL 2024 Season Offensive Receiving Statistics Overview")
    summary.append(f"Total Teams: {data.get('total_teams', 32)}")
    summary.append(f"Conference: {data.get('conference', 'All Teams')}")
    summary.append(f"Stat Type: Offensive {data.get('stat_type', 'Receiving Statistics')}")
    chunks.append(" | ".join(summary))

    # Process each team's stats
    teams = data.get('teams', [])
    print(f"  Processing {len(teams)} teams")

    for team_data in teams:
        chunk = format_team_receiving_stats(team_data)
        chunks.append(chunk)

    # Calculate and add league leaders
    if teams:
        # Most receiving yards
        yards_leader = max(teams, key=lambda x: x.get('receiving_yards', 0))
        chunks.append(f"Receiving Yards Leader: {yards_leader['team']} with {yards_leader['receiving_yards']:,} yards | League leader | Top receiving offense")

        # Most receptions
        receptions_leader = max(teams, key=lambda x: x.get('receptions', 0))
        chunks.append(f"Receptions Leader: {receptions_leader['team']} with {receptions_leader['receptions']} receptions | Most catches | Volume passing game")

        # Most receiving TDs
        td_leader = max(teams, key=lambda x: x.get('touchdowns', 0))
        chunks.append(f"Receiving Touchdowns Leader: {td_leader['team']} with {td_leader['touchdowns']} touchdowns | League leader | Top scoring passing attack")

        # Best yards per reception (min 150 receptions)
        eligible_teams = [t for t in teams if t.get('receptions', 0) >= 150]
        if eligible_teams:
            ypr_leader = max(eligible_teams, key=lambda x: x.get('yards_per_reception', 0))
            chunks.append(f"Yards per Reception Leader: {ypr_leader['team']} at {ypr_leader['yards_per_reception']} YPR | Most explosive receiving | Deep threat offense")

        # Fewest fumbles
        fumble_leader = min(teams, key=lambda x: x.get('receiving_fumbles', 999))
        chunks.append(f"Fewest Fumbles: {fumble_leader['team']} with {fumble_leader['receiving_fumbles']} fumbles | Best ball security | Sure-handed receivers")

        # Most explosive plays
        explosive_leader = max(teams, key=lambda x: x.get('plays_20_plus', 0))
        chunks.append(f"Most Explosive Receptions (20+): {explosive_leader['team']} with {explosive_leader['plays_20_plus']} big plays | Most explosive passing game")

        # Most 40+ yard plays
        big_play_leader = max(teams, key=lambda x: x.get('plays_40_plus', 0))
        chunks.append(f"Most Deep Receptions (40+): {big_play_leader['team']} with {big_play_leader['plays_40_plus']} deep plays | Best deep passing attack")

    return chunks


def main():
    """Main pipeline execution."""
    print("=" * 60)
    print("NFL TEAM RECEIVING STATS PIPELINE")
    print("=" * 60)
    print()

    # Paths
    stats_file = "/Users/kcdacre8tor/Downloads/nfl_team_receiving_stats.json"
    memory_dir = "/Users/kcdacre8tor/GSBPD2/backend/data/memories"

    # Check if file exists
    if not os.path.exists(stats_file):
        print(f"❌ Receiving stats file not found: {stats_file}")
        return 1

    print(f"📊 Loading NFL team receiving statistics")
    print()

    # Process stats data
    try:
        chunks = process_receiving_stats(stats_file)
        print(f"\n✅ Processed {len(chunks)} stat records")
    except Exception as e:
        print(f"❌ Error processing stats: {e}")
        return 1

    # Initialize Kre8VidMems
    print("\n🧠 Initializing Kre8VidMems for receiving stats...")
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
    memory_name = f"{memory_dir}/nfl-receiving-stats"
    memory.save(memory_name)

    elapsed_time = time.time() - start_time
    print(f"\n✅ Successfully loaded receiving stats in {elapsed_time:.2f} seconds")
    print(f"📂 Memory saved to: {memory_name}.*")

    # Display some interesting stats
    print("\n📈 Quick Stats Summary:")
    with open(stats_file, 'r') as f:
        data = json.load(f)
        teams = data.get('teams', [])

        if teams:
            avg_yards = sum(t.get('receiving_yards', 0) for t in teams) / len(teams)
            avg_receptions = sum(t.get('receptions', 0) for t in teams) / len(teams)
            avg_tds = sum(t.get('touchdowns', 0) for t in teams) / len(teams)
            avg_ypr = sum(t.get('yards_per_reception', 0) for t in teams) / len(teams)
            total_fumbles = sum(t.get('receiving_fumbles', 0) for t in teams)

            print(f"   Average Receiving Yards: {avg_yards:,.1f}")
            print(f"   Average Receptions: {avg_receptions:.1f}")
            print(f"   Average Receiving TDs: {avg_tds:.1f}")
            print(f"   Average Yards per Reception: {avg_ypr:.2f}")
            print(f"   Total League Fumbles: {total_fumbles}")

            # Find best and worst receiving teams
            best_team = max(teams, key=lambda x: x.get('receiving_yards', 0))
            worst_team = min(teams, key=lambda x: x.get('receiving_yards', 0))
            print(f"   Best Receiving Team: {best_team['team']} ({best_team['receiving_yards']:,} yards)")
            print(f"   Worst Receiving Team: {worst_team['team']} ({worst_team['receiving_yards']:,} yards)")

            # Most explosive team
            explosive_team = max(teams, key=lambda x: x.get('plays_20_plus', 0))
            print(f"   Most Explosive Team: {explosive_team['team']} ({explosive_team['plays_20_plus']} 20+ yard plays)")

    print("\n" + "=" * 60)
    print("✅ NFL RECEIVING STATS PIPELINE COMPLETE")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())