#!/usr/bin/env python3
"""
NFL Team Defensive Receiving Stats Pipeline
Loads NFL team defensive receiving statistics (opponent receiving) into Kre8VidMems memory system
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


def format_team_defensive_receiving_stats(team: Dict[str, Any]) -> str:
    """Format a team's defensive receiving stats into searchable text."""
    parts = []

    # Team name
    team_name = team.get('team', 'Unknown')
    parts.append(f"Team: {team_name}")
    parts.append(f"NFL 2024 Season Defensive Receiving Statistics")
    parts.append(f"Receiving Defense | Opponent Receiving Stats")

    # Core defensive receiving stats (what they allowed)
    receptions_allowed = team.get('receptions', 0)
    yards_allowed = team.get('receiving_yards', 0)
    ypr_allowed = team.get('yards_per_reception', 0)
    parts.append(f"Receptions Allowed: {receptions_allowed}")
    parts.append(f"Receiving Yards Allowed: {yards_allowed:,}")
    parts.append(f"Yards per Reception Allowed: {ypr_allowed}")

    # Calculate yards per game (assuming ~12 games played so far)
    ypg_allowed = yards_allowed / 12 if yards_allowed > 0 else 0
    parts.append(f"Receiving Yards Allowed per Game: {ypg_allowed:.1f}")

    # Scoring allowed
    tds_allowed = team.get('touchdowns', 0)
    parts.append(f"Receiving Touchdowns Allowed: {tds_allowed}")

    # TD rate allowed
    if receptions_allowed > 0:
        td_rate = (tds_allowed / receptions_allowed) * 100
        parts.append(f"TD Rate Allowed: {td_rate:.1f}% of receptions")

    # Big plays allowed
    plays_20_allowed = team.get('plays_20_plus', 0)
    plays_40_allowed = team.get('plays_40_plus', 0)
    longest_allowed = team.get('longest', 0)
    parts.append(f"20+ Yard Receptions Allowed: {plays_20_allowed}")
    parts.append(f"40+ Yard Receptions Allowed: {plays_40_allowed}")
    parts.append(f"Longest Reception Allowed: {longest_allowed} yards")

    # First downs allowed
    first_downs_allowed = team.get('receiving_first_downs', 0)
    first_down_pct_allowed = team.get('receiving_first_down_percentage', 0)
    parts.append(f"Receiving First Downs Allowed: {first_downs_allowed}")
    parts.append(f"First Down Percentage Allowed: {first_down_pct_allowed}%")

    # Fumbles recovered (GOOD for defense)
    fumbles_recovered = team.get('receiving_fumbles', 0)
    parts.append(f"Receiving Fumbles Recovered: {fumbles_recovered}")

    # Calculate fumble recovery rate
    if receptions_allowed > 0:
        fumble_rate = (fumbles_recovered / receptions_allowed) * 100
        parts.append(f"Fumble Recovery Rate: {fumble_rate:.2f}%")

    # Create searchable text
    text = " | ".join(parts)

    # Add searchable terms
    text += f" | {team_name} defensive receiving stats | {team_name} receiving defense"
    text += f" | {team_name} receiving yards allowed | {team_name} defensive performance"
    text += f" | {team_name} pass coverage | {team_name} secondary coverage"
    text += f" | {team_name} defensive stats | {team_name} defense"
    text += f" | {team_name} receivers allowed | {team_name} pass defense"

    # Add ranking-related terms (inverted from offensive - lower is better)
    if yards_allowed < 2400:
        text += " | elite receiving defense | shutdown coverage | top defensive secondary"
        text += " | lockdown receivers | dominant pass coverage"
    elif yards_allowed < 2800:
        text += " | good receiving defense | strong coverage | above average receiving defense"
    elif yards_allowed > 3200:
        text += " | struggling receiving defense | weak coverage | below average receiving defense"
        text += " | porous pass defense | vulnerable to receivers"

    if ypr_allowed < 10:
        text += " | limiting yards after catch | tight coverage | sticky defenders"
    elif ypr_allowed > 12:
        text += " | allowing yards after catch | loose coverage | spacing issues"

    if tds_allowed < 15:
        text += " | strong red zone coverage | limiting receiving touchdowns"
    elif tds_allowed > 25:
        text += " | weak red zone coverage | allowing too many receiving touchdowns"

    # Fumbles recovered (GOOD for defense)
    if fumbles_recovered > 3:
        text += " | forcing fumbles | stripping the ball | aggressive defense"
    elif fumbles_recovered < 1:
        text += " | not forcing fumbles | need more aggressive play"

    # Big plays allowed
    if plays_20_allowed < 25:
        text += " | limiting explosive plays | tight coverage downfield"
    elif plays_20_allowed > 40:
        text += " | allowing explosive plays | coverage breakdowns | big play vulnerability"

    if plays_40_allowed < 3:
        text += " | preventing deep plays | excellent deep coverage"
    elif plays_40_allowed > 6:
        text += " | vulnerable to deep plays | deep coverage issues"

    return text


def process_defensive_receiving_stats(stats_path: str) -> List[str]:
    """Process NFL team defensive receiving stats JSON into memory chunks."""
    print(f"Loading defensive receiving stats from: {stats_path}")

    with open(stats_path, 'r') as f:
        data = json.load(f)

    chunks = []

    # Add overall league summary
    summary = []
    summary.append(f"NFL 2024 Season Defensive Receiving Statistics Overview")
    summary.append(f"Total Teams: {data.get('total_teams', 32)}")
    summary.append(f"Conference: {data.get('conference', 'All Teams')}")
    summary.append(f"Stat Type: {data.get('stat_type', 'Defensive Receiving Statistics')}")
    summary.append(f"Receiving Defense Rankings | Opponent Receiving Stats")
    chunks.append(" | ".join(summary))

    # Process each team's stats
    teams = data.get('teams', [])
    print(f"  Processing {len(teams)} teams")

    for team_data in teams:
        chunk = format_team_defensive_receiving_stats(team_data)
        chunks.append(chunk)

    # Calculate and add league leaders (inverted logic for defense)
    if teams:
        # Best receiving defense (fewest yards allowed)
        best_defense = min(teams, key=lambda x: x.get('receiving_yards', 999999))
        chunks.append(f"Best Receiving Defense: {best_defense['team']} allowing only {best_defense['receiving_yards']:,} yards | Elite receiving defense | Top coverage unit")

        # Worst receiving defense (most yards allowed)
        worst_defense = max(teams, key=lambda x: x.get('receiving_yards', 0))
        chunks.append(f"Worst Receiving Defense: {worst_defense['team']} allowing {worst_defense['receiving_yards']:,} yards | Struggling receiving defense")

        # Fewest receptions allowed (GOOD for defense)
        receptions_leader = min(teams, key=lambda x: x.get('receptions', 999))
        chunks.append(f"Fewest Receptions Allowed: {receptions_leader['team']} with {receptions_leader['receptions']} receptions | Tight coverage | Limiting catches")

        # Fewest TDs allowed (GOOD for defense)
        td_leader = min(teams, key=lambda x: x.get('touchdowns', 999))
        chunks.append(f"Fewest Receiving TDs Allowed: {td_leader['team']} with {td_leader['touchdowns']} TDs allowed | Red zone coverage leader")

        # Best yards per reception defense (lowest is best)
        ypr_leader = min(teams, key=lambda x: x.get('yards_per_reception', 999))
        chunks.append(f"Best YPR Defense: {ypr_leader['team']} allowing {ypr_leader['yards_per_reception']} YPR | Limiting yards after catch")

        # Most fumbles recovered (GOOD for defense)
        fumble_leader = max(teams, key=lambda x: x.get('receiving_fumbles', 0))
        chunks.append(f"Most Fumbles Recovered: {fumble_leader['team']} with {fumble_leader['receiving_fumbles']} fumbles | Forcing turnovers | Ball hawks")

        # Fewest explosive plays allowed
        explosive_leader = min(teams, key=lambda x: x.get('plays_20_plus', 999))
        chunks.append(f"Fewest Explosive Plays Allowed: {explosive_leader['team']} with {explosive_leader['plays_20_plus']} 20+ yard plays | Limiting big plays")

        # Fewest deep plays allowed
        deep_leader = min(teams, key=lambda x: x.get('plays_40_plus', 999))
        chunks.append(f"Fewest Deep Plays Allowed: {deep_leader['team']} with {deep_leader['plays_40_plus']} 40+ yard plays | Elite deep coverage")

    return chunks


def main():
    """Main pipeline execution."""
    print("=" * 60)
    print("NFL TEAM DEFENSIVE RECEIVING STATS PIPELINE")
    print("=" * 60)
    print()

    # Paths
    stats_file = "/Users/kcdacre8tor/Downloads/nfl_team_defensive_receiving_stats.json"
    memory_dir = "/Users/kcdacre8tor/GSBPD2/backend/data/memories"

    # Check if file exists
    if not os.path.exists(stats_file):
        print(f"❌ Defensive receiving stats file not found: {stats_file}")
        return 1

    print(f"🛡️ Loading NFL team defensive receiving statistics")
    print()

    # Process stats data
    try:
        chunks = process_defensive_receiving_stats(stats_file)
        print(f"\n✅ Processed {len(chunks)} stat records")
    except Exception as e:
        print(f"❌ Error processing stats: {e}")
        return 1

    # Initialize Kre8VidMems
    print("\n🧠 Initializing Kre8VidMems for defensive receiving stats...")
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
    memory_name = f"{memory_dir}/nfl-defensive-receiving-stats"
    memory.save(memory_name)

    elapsed_time = time.time() - start_time
    print(f"\n✅ Successfully loaded defensive receiving stats in {elapsed_time:.2f} seconds")
    print(f"📂 Memory saved to: {memory_name}.*")

    # Display some interesting stats
    print("\n📈 Quick Defensive Stats Summary:")
    with open(stats_file, 'r') as f:
        data = json.load(f)
        teams = data.get('teams', [])

        if teams:
            avg_yards_allowed = sum(t.get('receiving_yards', 0) for t in teams) / len(teams)
            avg_receptions_allowed = sum(t.get('receptions', 0) for t in teams) / len(teams)
            avg_tds_allowed = sum(t.get('touchdowns', 0) for t in teams) / len(teams)
            avg_ypr_allowed = sum(t.get('yards_per_reception', 0) for t in teams) / len(teams)
            total_fumbles = sum(t.get('receiving_fumbles', 0) for t in teams)

            print(f"   Average Receiving Yards Allowed: {avg_yards_allowed:,.1f}")
            print(f"   Average Receptions Allowed: {avg_receptions_allowed:.1f}")
            print(f"   Average Receiving TDs Allowed: {avg_tds_allowed:.1f}")
            print(f"   Average Yards per Reception Allowed: {avg_ypr_allowed:.2f}")
            print(f"   Total Fumbles Recovered: {total_fumbles}")

            # Find best and worst receiving defenses
            best_team = min(teams, key=lambda x: x.get('receiving_yards', 999999))
            worst_team = max(teams, key=lambda x: x.get('receiving_yards', 0))
            print(f"   Best Receiving Defense: {best_team['team']} ({best_team['receiving_yards']:,} yards allowed)")
            print(f"   Worst Receiving Defense: {worst_team['team']} ({worst_team['receiving_yards']:,} yards allowed)")

            # Most explosive plays allowed
            explosive_team = max(teams, key=lambda x: x.get('plays_20_plus', 0))
            print(f"   Most Explosive Plays Allowed: {explosive_team['team']} ({explosive_team['plays_20_plus']} 20+ yard plays)")

    print("\n" + "=" * 60)
    print("✅ NFL DEFENSIVE RECEIVING STATS PIPELINE COMPLETE")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())