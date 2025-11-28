#!/usr/bin/env python3
"""
NFL Team All Defensive Stats Pipeline
Loads all NFL team defensive statistics into Kre8VidMems memory system
Includes: Down conversions, Fumbles, Interceptions, Scoring defense, Tackles
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


def format_down_conversion_stats(team: Dict[str, Any]) -> str:
    """Format down conversion defense stats."""
    parts = []

    team_name = team.get('team', 'Unknown')
    parts.append(f"Team: {team_name}")
    parts.append(f"NFL 2024 Defensive Down Conversion Stats")

    # 3rd down defense
    third_attempts = team.get('third_down_attempts', 0)
    third_made = team.get('third_down_made', 0)
    third_pct = (third_made / third_attempts * 100) if third_attempts > 0 else 0
    parts.append(f"3rd Downs Allowed: {third_made}/{third_attempts} ({third_pct:.1f}%)")

    # 4th down defense
    fourth_attempts = team.get('fourth_down_attempts', 0)
    fourth_made = team.get('fourth_down_made', 0)
    fourth_pct = (fourth_made / fourth_attempts * 100) if fourth_attempts > 0 else 0
    parts.append(f"4th Downs Allowed: {fourth_made}/{fourth_attempts} ({fourth_pct:.1f}%)")

    # First downs allowed
    rec_first = team.get('receiving_first_downs', 0)
    rush_first = team.get('rushing_first_downs', 0)
    total_first = rec_first + rush_first
    parts.append(f"Total First Downs Allowed: {total_first}")
    parts.append(f"Passing First Downs Allowed: {rec_first}")
    parts.append(f"Rushing First Downs Allowed: {rush_first}")

    text = " | ".join(parts)

    # Add searchable terms
    text += f" | {team_name} defensive down conversions | {team_name} 3rd down defense"
    text += f" | {team_name} 4th down defense | {team_name} defensive stats"
    text += f" | {team_name} situational defense | {team_name} defense"

    # Rankings
    if third_pct < 35:
        text += " | elite 3rd down defense | getting off the field | clutch defense"
    elif third_pct > 45:
        text += " | struggling 3rd down defense | can't get off field"

    if fourth_pct < 40 and fourth_attempts > 5:
        text += " | strong 4th down defense | red zone stops"

    return text


def format_fumble_stats(team: Dict[str, Any]) -> str:
    """Format defensive fumble stats."""
    parts = []

    team_name = team.get('team', 'Unknown')
    parts.append(f"Team: {team_name}")
    parts.append(f"NFL 2024 Defensive Fumble Statistics")

    forced = team.get('forced_fumbles', 0)
    recovered = team.get('fumble_recoveries', 0)
    tds = team.get('fumble_return_touchdowns', 0)

    parts.append(f"Forced Fumbles: {forced}")
    parts.append(f"Fumble Recoveries: {recovered}")
    parts.append(f"Fumble Return TDs: {tds}")

    # Recovery rate
    if forced > 0:
        recovery_rate = (recovered / forced * 100)
        parts.append(f"Recovery Rate: {recovery_rate:.1f}%")

    text = " | ".join(parts)

    # Add searchable terms
    text += f" | {team_name} defensive fumbles | {team_name} forced fumbles"
    text += f" | {team_name} fumble recoveries | {team_name} defensive turnovers"
    text += f" | {team_name} defensive stats | {team_name} defense"

    # Rankings
    if forced > 12:
        text += " | ball-hawking defense | forcing turnovers | strip sack specialists"
    elif forced < 6:
        text += " | not forcing fumbles | need more aggressive play"

    if tds > 1:
        text += " | scoring on defense | defensive touchdowns"

    return text


def format_interception_stats(team: Dict[str, Any]) -> str:
    """Format defensive interception stats."""
    parts = []

    team_name = team.get('team', 'Unknown')
    parts.append(f"Team: {team_name}")
    parts.append(f"NFL 2024 Defensive Interception Statistics")

    ints = team.get('interceptions', 0)
    tds = team.get('interception_return_touchdowns', 0)
    yards = team.get('interception_return_yards', 0)
    longest = team.get('longest', 0)

    parts.append(f"Interceptions: {ints}")
    parts.append(f"INT Return TDs: {tds}")
    parts.append(f"INT Return Yards: {yards}")
    parts.append(f"Longest Return: {longest} yards")

    # Average return
    if ints > 0:
        avg_return = yards / ints
        parts.append(f"Average Return: {avg_return:.1f} yards")
        td_rate = (tds / ints * 100)
        parts.append(f"INT TD Rate: {td_rate:.1f}%")

    text = " | ".join(parts)

    # Add searchable terms
    text += f" | {team_name} interceptions | {team_name} picks | {team_name} INTs"
    text += f" | {team_name} defensive turnovers | {team_name} secondary"
    text += f" | {team_name} defensive stats | {team_name} defense"

    # Rankings
    if ints > 15:
        text += " | ball-hawking secondary | turnover machine | elite ball skills"
        text += " | no-fly zone | shutdown secondary"
    elif ints < 8:
        text += " | low interception rate | not creating turnovers"

    if tds > 2:
        text += " | pick-six threat | scoring defense"

    return text


def format_scoring_defense_stats(team: Dict[str, Any]) -> str:
    """Format defensive scoring stats."""
    parts = []

    team_name = team.get('team', 'Unknown')
    parts.append(f"Team: {team_name}")
    parts.append(f"NFL 2024 Defensive Scoring Statistics")

    fumble_tds = team.get('fumble_return_touchdowns', 0)
    int_tds = team.get('interception_return_touchdowns', 0)
    safeties = team.get('safeties', 0)
    total_def_tds = fumble_tds + int_tds

    parts.append(f"Total Defensive TDs: {total_def_tds}")
    parts.append(f"Fumble Return TDs: {fumble_tds}")
    parts.append(f"INT Return TDs: {int_tds}")
    parts.append(f"Safeties: {safeties}")

    # Calculate defensive points scored
    def_points = (total_def_tds * 6) + (safeties * 2)
    parts.append(f"Defensive Points Scored: {def_points}")

    text = " | ".join(parts)

    # Add searchable terms
    text += f" | {team_name} defensive scoring | {team_name} defensive touchdowns"
    text += f" | {team_name} scoring defense | {team_name} defensive points"
    text += f" | {team_name} defensive stats | {team_name} defense"

    # Rankings
    if total_def_tds > 3:
        text += " | scoring defense | defensive playmakers | game-changing defense"

    if safeties > 1:
        text += " | creating safeties | dominant pass rush"

    return text


def format_tackle_stats(team: Dict[str, Any]) -> str:
    """Format defensive tackle stats."""
    parts = []

    team_name = team.get('team', 'Unknown')
    parts.append(f"Team: {team_name}")
    parts.append(f"NFL 2024 Defensive Tackle Statistics")

    sacks = team.get('sacks', 0)
    combined = team.get('combined_tackles', 0)
    solo = team.get('solo_tackles', 0)
    assisted = team.get('assisted_tackles', 0)

    parts.append(f"Sacks: {sacks}")
    parts.append(f"Combined Tackles: {combined}")
    parts.append(f"Solo Tackles: {solo}")
    parts.append(f"Assisted Tackles: {assisted}")

    # Tackle efficiency
    if combined > 0:
        solo_pct = (solo / combined * 100)
        parts.append(f"Solo Tackle Rate: {solo_pct:.1f}%")

    # Sacks per game (assuming ~12 games)
    spg = sacks / 12
    parts.append(f"Sacks per Game: {spg:.1f}")

    text = " | ".join(parts)

    # Add searchable terms
    text += f" | {team_name} defensive tackles | {team_name} sacks | {team_name} tackles"
    text += f" | {team_name} pass rush | {team_name} run defense"
    text += f" | {team_name} defensive stats | {team_name} defense"

    # Rankings
    if sacks > 35:
        text += " | elite pass rush | dominant defensive line | quarterback nightmare"
    elif sacks < 20:
        text += " | weak pass rush | struggling to pressure QB"

    if solo > 500:
        text += " | sure tackling | disciplined defense | gap sound"

    return text


def process_defensive_file(file_path: str, stat_type: str) -> List[str]:
    """Process a single defensive stats file."""
    print(f"  Processing {stat_type} from: {os.path.basename(file_path)}")

    with open(file_path, 'r') as f:
        data = json.load(f)

    chunks = []

    # Add summary
    summary = []
    summary.append(f"NFL 2024 {stat_type} Overview")
    summary.append(f"Total Teams: {data.get('total_teams', 32)}")
    summary.append(f"Stat Type: {data.get('stat_type', stat_type)}")
    chunks.append(" | ".join(summary))

    # Process each team
    teams = data.get('teams', [])

    for team_data in teams:
        if stat_type == "Down Conversion Defense":
            chunk = format_down_conversion_stats(team_data)
        elif stat_type == "Fumble Defense":
            chunk = format_fumble_stats(team_data)
        elif stat_type == "Interception Defense":
            chunk = format_interception_stats(team_data)
        elif stat_type == "Scoring Defense":
            chunk = format_scoring_defense_stats(team_data)
        elif stat_type == "Tackle Defense":
            chunk = format_tackle_stats(team_data)
        else:
            continue
        chunks.append(chunk)

    # Add league leaders based on stat type
    if teams and stat_type == "Down Conversion Defense":
        # Best 3rd down defense (lowest percentage)
        valid_teams = [t for t in teams if t.get('third_down_attempts', 0) > 50]
        if valid_teams:
            best = min(valid_teams, key=lambda x: x.get('third_down_made', 999) / max(x.get('third_down_attempts', 1), 1))
            pct = (best.get('third_down_made', 0) / max(best.get('third_down_attempts', 1), 1)) * 100
            chunks.append(f"Best 3rd Down Defense: {best['team']} allowing {pct:.1f}% | Elite situational defense")

    elif teams and stat_type == "Fumble Defense":
        # Most forced fumbles
        leader = max(teams, key=lambda x: x.get('forced_fumbles', 0))
        chunks.append(f"Forced Fumbles Leader: {leader['team']} with {leader['forced_fumbles']} | Ball-hawking defense")

    elif teams and stat_type == "Interception Defense":
        # Most interceptions
        leader = max(teams, key=lambda x: x.get('interceptions', 0))
        chunks.append(f"Interception Leader: {leader['team']} with {leader['interceptions']} INTs | Ball-hawking secondary")

    elif teams and stat_type == "Scoring Defense":
        # Most defensive TDs
        teams_with_tds = [(t, t.get('fumble_return_touchdowns', 0) + t.get('interception_return_touchdowns', 0)) for t in teams]
        leader = max(teams_with_tds, key=lambda x: x[1])
        chunks.append(f"Defensive TD Leader: {leader[0]['team']} with {leader[1]} TDs | Scoring defense")

    elif teams and stat_type == "Tackle Defense":
        # Most sacks
        leader = max(teams, key=lambda x: x.get('sacks', 0))
        chunks.append(f"Sack Leader: {leader['team']} with {leader['sacks']} sacks | Elite pass rush")

    return chunks


def main():
    """Main pipeline execution."""
    print("=" * 60)
    print("NFL ALL DEFENSIVE STATS PIPELINE")
    print("=" * 60)
    print()

    # Define files and their types
    stats_dir = "/Users/kcdacre8tor/Downloads/nfl_defensive_team_stats"
    memory_dir = "/Users/kcdacre8tor/GSBPD2/backend/data/memories"

    files_to_process = [
        ("nfl_team_defensive_down_conversion_stats.json", "Down Conversion Defense", "down-conversion"),
        ("nfl_team_defensive_fumble_stats.json", "Fumble Defense", "fumbles"),
        ("nfl_team_defensive_interception_stats.json", "Interception Defense", "interceptions"),
        ("nfl_team_defensive_scoring_stats.json", "Scoring Defense", "scoring"),
        ("nfl_team_defensive_tackle_stats.json", "Tackle Defense", "tackles")
    ]

    print(f"🛡️ Loading NFL team defensive statistics from:")
    print(f"   {stats_dir}")
    print()

    total_start = time.time()

    for file_name, stat_type, memory_suffix in files_to_process:
        file_path = os.path.join(stats_dir, file_name)

        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            continue

        print(f"\n📊 Processing {stat_type}...")

        try:
            # Process the file
            chunks = process_defensive_file(file_path, stat_type)
            print(f"   ✅ Processed {len(chunks)} records")

            # Initialize memory for this stat type
            memory = Kre8VidMemory()

            # Add chunks to memory
            print(f"   📝 Adding to memory...")
            for chunk in chunks:
                memory.add(chunk)

            # Save the memory
            memory_name = f"{memory_dir}/nfl-defensive-{memory_suffix}-stats"
            memory.save(memory_name)
            print(f"   📂 Saved to: {memory_name}.*")

        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue

    total_elapsed = time.time() - total_start

    print("\n" + "=" * 60)
    print(f"✅ ALL DEFENSIVE STATS PIPELINE COMPLETE")
    print(f"⏱️  Total time: {total_elapsed:.2f} seconds")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())