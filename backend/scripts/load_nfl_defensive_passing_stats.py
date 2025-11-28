#!/usr/bin/env python3
"""
NFL Team Defensive Passing Stats Pipeline
Loads NFL team defensive passing statistics (opponent passing) into Kre8VidMems memory system
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


def format_team_defensive_passing_stats(team: Dict[str, Any]) -> str:
    """Format a team's defensive passing stats into searchable text."""
    parts = []

    # Team name
    team_name = team.get('team', 'Unknown')
    parts.append(f"Team: {team_name}")
    parts.append(f"NFL 2024 Season Defensive Passing Statistics")
    parts.append(f"Pass Defense | Opponent Passing Stats")

    # Core defensive passing stats (what they allowed)
    attempts_allowed = team.get('attempts', 0)
    completions_allowed = team.get('completions', 0)
    comp_pct_allowed = team.get('completion_percentage', 0)
    parts.append(f"Pass Attempts Allowed: {attempts_allowed}")
    parts.append(f"Completions Allowed: {completions_allowed}")
    parts.append(f"Completion Percentage Allowed: {comp_pct_allowed}%")

    # Yards allowed
    yards_allowed = team.get('passing_yards', 0)
    ypa_allowed = team.get('yards_per_attempt', 0)
    parts.append(f"Passing Yards Allowed: {yards_allowed:,}")
    parts.append(f"Yards per Attempt Allowed: {ypa_allowed}")

    # Calculate yards per game (assuming ~12 games played so far)
    ypg_allowed = yards_allowed / 12 if yards_allowed > 0 else 0
    parts.append(f"Passing Yards Allowed per Game: {ypg_allowed:.1f}")

    # Scoring and turnovers
    tds_allowed = team.get('touchdowns', 0)
    interceptions = team.get('interceptions', 0)  # This is GOOD for defense
    rating_allowed = team.get('passer_rating', 0)
    parts.append(f"Passing TDs Allowed: {tds_allowed}")
    parts.append(f"Interceptions Made: {interceptions}")
    parts.append(f"Passer Rating Allowed: {rating_allowed}")

    # Pass rush (sacks are GOOD for defense)
    sacks = team.get('sacks', 0)
    parts.append(f"Sacks: {sacks}")

    # Calculate sack rate
    if attempts_allowed > 0:
        sack_rate = (sacks / (attempts_allowed + sacks)) * 100
        parts.append(f"Sack Rate: {sack_rate:.1f}%")

    # First downs allowed
    first_downs_allowed = team.get('first_downs', 0)
    first_down_pct_allowed = team.get('first_down_percentage', 0)
    parts.append(f"Passing First Downs Allowed: {first_downs_allowed}")
    parts.append(f"First Down Percentage Allowed: {first_down_pct_allowed}%")

    # Big plays allowed
    plays_20_allowed = team.get('plays_20_plus', 0)
    plays_40_allowed = team.get('plays_40_plus', 0)
    longest_allowed = team.get('longest', 0)
    parts.append(f"20+ Yard Plays Allowed: {plays_20_allowed}")
    parts.append(f"40+ Yard Plays Allowed: {plays_40_allowed}")
    parts.append(f"Longest Pass Allowed: {longest_allowed} yards")

    # Create searchable text
    text = " | ".join(parts)

    # Add searchable terms
    text += f" | {team_name} defensive passing stats | {team_name} pass defense"
    text += f" | {team_name} passing yards allowed | {team_name} defensive performance"
    text += f" | {team_name} pass coverage | {team_name} secondary"
    text += f" | {team_name} defensive stats | {team_name} defense"

    # Add ranking-related terms (inverted from offensive - lower is better)
    if yards_allowed < 2500:
        text += " | elite pass defense | shutdown secondary | top defensive unit"
        text += " | lockdown defense | dominant pass coverage"
    elif yards_allowed < 3000:
        text += " | good pass defense | strong secondary | above average pass defense"
    elif yards_allowed > 3500:
        text += " | struggling pass defense | weak secondary | below average pass defense"
        text += " | porous pass defense | vulnerable secondary"

    if rating_allowed < 80:
        text += " | elite defensive passer rating | excellent pass coverage"
    elif rating_allowed < 90:
        text += " | good defensive passer rating | solid pass coverage"
    elif rating_allowed > 100:
        text += " | poor defensive passer rating | struggling pass coverage"

    if tds_allowed < 15:
        text += " | strong red zone pass defense | limiting passing touchdowns"
    elif tds_allowed > 25:
        text += " | weak red zone pass defense | allowing too many passing touchdowns"

    # Good defensive stats
    if interceptions > 15:
        text += " | ball-hawking defense | high interception rate | turnover machine"
        text += " | opportunistic defense | creating turnovers"
    elif interceptions < 8:
        text += " | low interception rate | not creating turnovers"

    if sacks > 30:
        text += " | elite pass rush | high pressure defense | dominant pass rush"
    elif sacks > 20:
        text += " | good pass rush | solid pressure"
    elif sacks < 15:
        text += " | weak pass rush | low pressure | struggling to get to QB"

    if plays_20_allowed < 25:
        text += " | limiting big plays | bend don't break defense"
    elif plays_20_allowed > 40:
        text += " | allowing too many big plays | explosive plays problem"

    return text


def process_defensive_passing_stats(stats_path: str) -> List[str]:
    """Process NFL team defensive passing stats JSON into memory chunks."""
    print(f"Loading defensive passing stats from: {stats_path}")

    with open(stats_path, 'r') as f:
        data = json.load(f)

    chunks = []

    # Add overall league summary
    summary = []
    summary.append(f"NFL 2024 Season Defensive Passing Statistics Overview")
    summary.append(f"Total Teams: {data.get('total_teams', 32)}")
    summary.append(f"Conference: {data.get('conference', 'All Teams')}")
    summary.append(f"Stat Type: {data.get('stat_type', 'Defensive Passing Statistics')}")
    summary.append(f"Pass Defense Rankings | Opponent Passing Stats")
    chunks.append(" | ".join(summary))

    # Process each team's stats
    teams = data.get('teams', [])
    print(f"  Processing {len(teams)} teams")

    for team_data in teams:
        chunk = format_team_defensive_passing_stats(team_data)
        chunks.append(chunk)

    # Calculate and add league leaders (inverted logic for defense)
    if teams:
        # Best pass defense (fewest yards allowed)
        best_defense = min(teams, key=lambda x: x.get('passing_yards', 999999))
        chunks.append(f"Best Pass Defense: {best_defense['team']} allowing only {best_defense['passing_yards']:,} yards | Elite pass defense | Top defensive unit")

        # Worst pass defense (most yards allowed)
        worst_defense = max(teams, key=lambda x: x.get('passing_yards', 0))
        chunks.append(f"Worst Pass Defense: {worst_defense['team']} allowing {worst_defense['passing_yards']:,} yards | Struggling pass defense")

        # Most interceptions (GOOD for defense)
        int_leader = max(teams, key=lambda x: x.get('interceptions', 0))
        chunks.append(f"Interception Leader: {int_leader['team']} with {int_leader['interceptions']} interceptions | Ball-hawking defense | Turnover leader")

        # Most sacks (GOOD for defense)
        sack_leader = max(teams, key=lambda x: x.get('sacks', 0))
        chunks.append(f"Sack Leader: {sack_leader['team']} with {sack_leader['sacks']} sacks | Elite pass rush | Pressure leader")

        # Best passer rating allowed (lowest is best)
        rating_leader = min(teams, key=lambda x: x.get('passer_rating', 999))
        chunks.append(f"Best Passer Rating Defense: {rating_leader['team']} allowing {rating_leader['passer_rating']} rating | Elite pass coverage")

        # Fewest TDs allowed (GOOD for defense)
        td_leader = min(teams, key=lambda x: x.get('touchdowns', 999))
        chunks.append(f"Fewest Passing TDs Allowed: {td_leader['team']} with {td_leader['touchdowns']} TDs allowed | Red zone defense leader")

        # Fewest big plays allowed
        big_play_leader = min(teams, key=lambda x: x.get('plays_20_plus', 999))
        chunks.append(f"Fewest Big Plays Allowed: {big_play_leader['team']} with {big_play_leader['plays_20_plus']} 20+ yard plays | Limiting explosive plays")

    return chunks


def main():
    """Main pipeline execution."""
    print("=" * 60)
    print("NFL TEAM DEFENSIVE PASSING STATS PIPELINE")
    print("=" * 60)
    print()

    # Paths
    stats_file = "/Users/kcdacre8tor/Downloads/nfl_team_defensive_passing_stats.json"
    memory_dir = "/Users/kcdacre8tor/GSBPD2/backend/data/memories"

    # Check if file exists
    if not os.path.exists(stats_file):
        print(f"❌ Defensive passing stats file not found: {stats_file}")
        return 1

    print(f"🛡️ Loading NFL team defensive passing statistics")
    print()

    # Process stats data
    try:
        chunks = process_defensive_passing_stats(stats_file)
        print(f"\n✅ Processed {len(chunks)} stat records")
    except Exception as e:
        print(f"❌ Error processing stats: {e}")
        return 1

    # Initialize Kre8VidMems
    print("\n🧠 Initializing Kre8VidMems for defensive passing stats...")
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
    memory_name = f"{memory_dir}/nfl-defensive-passing-stats"
    memory.save(memory_name)

    elapsed_time = time.time() - start_time
    print(f"\n✅ Successfully loaded defensive passing stats in {elapsed_time:.2f} seconds")
    print(f"📂 Memory saved to: {memory_name}.*")

    # Display some interesting stats
    print("\n📈 Quick Defensive Stats Summary:")
    with open(stats_file, 'r') as f:
        data = json.load(f)
        teams = data.get('teams', [])

        if teams:
            avg_yards_allowed = sum(t.get('passing_yards', 0) for t in teams) / len(teams)
            avg_tds_allowed = sum(t.get('touchdowns', 0) for t in teams) / len(teams)
            avg_ints = sum(t.get('interceptions', 0) for t in teams) / len(teams)
            avg_sacks = sum(t.get('sacks', 0) for t in teams) / len(teams)
            avg_rating_allowed = sum(t.get('passer_rating', 0) for t in teams) / len(teams)

            print(f"   Average Passing Yards Allowed: {avg_yards_allowed:,.1f}")
            print(f"   Average Passing TDs Allowed: {avg_tds_allowed:.1f}")
            print(f"   Average Interceptions Made: {avg_ints:.1f}")
            print(f"   Average Sacks: {avg_sacks:.1f}")
            print(f"   Average Passer Rating Allowed: {avg_rating_allowed:.1f}")

            # Find best and worst pass defenses
            best_team = min(teams, key=lambda x: x.get('passing_yards', 999999))
            worst_team = max(teams, key=lambda x: x.get('passing_yards', 0))
            print(f"   Best Pass Defense: {best_team['team']} ({best_team['passing_yards']:,} yards allowed)")
            print(f"   Worst Pass Defense: {worst_team['team']} ({worst_team['passing_yards']:,} yards allowed)")

            # Most turnovers created
            turnover_team = max(teams, key=lambda x: x.get('interceptions', 0))
            print(f"   Most Interceptions: {turnover_team['team']} ({turnover_team['interceptions']} INTs)")

            # Best pass rush
            rush_team = max(teams, key=lambda x: x.get('sacks', 0))
            print(f"   Best Pass Rush: {rush_team['team']} ({rush_team['sacks']} sacks)")

    print("\n" + "=" * 60)
    print("✅ NFL DEFENSIVE PASSING STATS PIPELINE COMPLETE")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())