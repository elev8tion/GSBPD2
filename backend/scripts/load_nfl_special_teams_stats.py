#!/usr/bin/env python3

"""
Load all NFL Special Teams Statistics into Kre8VidMems
Processes field goals, kickoffs, punts, and punt returns
"""

import json
from pathlib import Path
import sys

# Add backend to path for imports
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

# Import our custom Kre8VidMems library
from lib.kre8vidmems.kre8vidmems.api.memory import Kre8VidMemory

def load_special_teams_stats():
    """Load all special teams stats from JSON files"""

    # Paths
    data_dir = Path("/Users/kcdacre8tor/Downloads/special_teams")
    memory_dir = Path(__file__).parent.parent / "data" / "memories"
    memory_dir.mkdir(parents=True, exist_ok=True)

    # Files to process with their descriptions
    files_to_process = [
        ("nfl_team_field_goal_stats_verified.json", "Field Goal", "field-goals"),
        ("nfl_team_kickoff_stats.json", "Kickoff", "kickoffs"),
        ("nfl_team_punt_return_stats.json", "Punt Return", "punt-returns"),
        ("nfl_team_punt_stats.json", "Punt", "punts")
    ]

    # Process each special teams category
    for filename, category_name, memory_suffix in files_to_process:
        file_path = data_dir / filename

        if not file_path.exists():
            print(f"Skipping {filename} - file not found")
            continue

        print(f"\nProcessing NFL {category_name} Stats...")

        # Load the JSON data
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Initialize memory
        memory = Kre8VidMemory()

        # Format the text chunks based on category
        text_chunks = []

        # Add header chunk
        header = f"NFL 2024 Season Special Teams - {category_name} Statistics | special teams | {memory_suffix}"
        text_chunks.append(header)

        # Get teams data - handle both direct array and nested structure
        teams_data = data.get('teams', data) if isinstance(data, dict) else data

        # Process each team's stats
        for team in teams_data:
            team_name = team.get('team', 'Unknown')
            parts = [f"Team: {team_name}"]

            # Format stats based on category
            if memory_suffix == "field-goals":
                # Field goal specific stats
                fg_made = team.get('field_goals_made', 0)
                fg_att = team.get('field_goal_attempts', 0)
                fg_pct = team.get('field_goal_percentage', 0)
                fg_long = team.get('longest_field_goal', 0)
                fg_40_49_made = team.get('fg_40_49_made', 0)
                fg_40_49_att = team.get('fg_40_49_attempts', 0)
                fg_50_plus_made = team.get('fg_50_plus_made', 0)
                fg_50_plus_att = team.get('fg_50_plus_attempts', 0)
                xp_made = team.get('extra_points_made', 0)
                xp_att = team.get('extra_points_attempted', 0)

                parts.extend([
                    f"FG Made/Att: {fg_made}/{fg_att}",
                    f"FG%: {fg_pct}%",
                    f"Long: {fg_long}",
                    f"40-49 yards: {fg_40_49_made}/{fg_40_49_att}",
                    f"50+ yards: {fg_50_plus_made}/{fg_50_plus_att}",
                    f"XP Made/Att: {xp_made}/{xp_att}"
                ])

                # Add performance tags
                text = " | ".join(parts)
                if fg_pct >= 90:
                    text += f" | elite kicker | 90%+ FG | {team_name} reliable kicker"
                elif fg_pct >= 85:
                    text += f" | strong kicker | 85%+ FG | {team_name} good kicking"
                elif fg_pct < 75:
                    text += f" | struggling kicker | below 75% FG | {team_name} kicking issues"

                # Add long FG tags
                if fg_long >= 60:
                    text += f" | 60+ yard FG | long range kicker | {team_name} power kicker"
                elif fg_long >= 55:
                    text += f" | 55+ yard FG | strong leg kicker | {team_name} long FG capability"

            elif memory_suffix == "kickoffs":
                # Kickoff specific stats
                kickoffs = team.get('kickoffs', 0)
                touchbacks = team.get('touchbacks', 0)
                tb_pct = team.get('tb_percentage', 0)
                avg_return = team.get('avg_return_yards', 0)
                out_of_bounds = team.get('out_of_bounds', 0)

                parts.extend([
                    f"Kickoffs: {kickoffs}",
                    f"Touchbacks: {touchbacks}",
                    f"TB%: {tb_pct}%",
                    f"Avg Return Allowed: {avg_return}",
                    f"Out of Bounds: {out_of_bounds}"
                ])

                text = " | ".join(parts)
                if tb_pct >= 70:
                    text += f" | strong kickoff | 70%+ touchbacks | {team_name} kickoff specialist"
                elif tb_pct >= 60:
                    text += f" | good kickoff | 60%+ touchbacks | {team_name} solid kickoffs"

                if avg_return <= 20:
                    text += f" | excellent coverage | limiting returns | {team_name} kickoff coverage"

            elif memory_suffix == "punt-returns":
                # Punt return specific stats
                punt_returns = team.get('punt_returns', 0)
                return_yards = team.get('return_yards', 0)
                avg_return = team.get('avg_return', 0)
                long_return = team.get('long_return', 0)
                return_tds = team.get('return_tds', 0)
                fair_catches = team.get('fair_catches', 0)

                parts.extend([
                    f"Returns: {punt_returns}",
                    f"Return Yards: {return_yards}",
                    f"Avg Return: {avg_return}",
                    f"Long: {long_return}",
                    f"Return TDs: {return_tds}",
                    f"Fair Catches: {fair_catches}"
                ])

                text = " | ".join(parts)
                if avg_return >= 12:
                    text += f" | dangerous returner | 12+ avg return | {team_name} return threat"
                elif avg_return >= 10:
                    text += f" | good returner | 10+ avg return | {team_name} solid returns"

                if return_tds > 0:
                    text += f" | return TD threat | {return_tds} return TDs | {team_name} explosive returns"

            elif memory_suffix == "punts":
                # Punt specific stats
                punts = team.get('punts', 0)
                punt_yards = team.get('punt_yards', 0)
                gross_avg = team.get('gross_avg', 0)
                net_avg = team.get('net_avg', 0)
                inside_20 = team.get('inside_20', 0)
                long_punt = team.get('long_punt', 0)
                touchbacks = team.get('touchbacks', 0)

                parts.extend([
                    f"Punts: {punts}",
                    f"Punt Yards: {punt_yards}",
                    f"Gross Avg: {gross_avg}",
                    f"Net Avg: {net_avg}",
                    f"Inside 20: {inside_20}",
                    f"Long: {long_punt}",
                    f"Touchbacks: {touchbacks}"
                ])

                text = " | ".join(parts)
                if gross_avg >= 48:
                    text += f" | elite punter | 48+ gross avg | {team_name} strong punting"
                elif gross_avg >= 46:
                    text += f" | good punter | 46+ gross avg | {team_name} solid punting"

                if net_avg >= 42:
                    text += f" | excellent net | 42+ net avg | {team_name} field position weapon"

                # Inside 20 percentage
                if punts > 0:
                    inside_20_pct = (inside_20 / punts) * 100
                    if inside_20_pct >= 40:
                        text += f" | precision punter | 40%+ inside 20 | {team_name} pin deep"
            else:
                # Generic formatting for any other stats
                text = " | ".join(parts)
                for key, value in team.items():
                    if key != 'team' and value:
                        text += f" | {key}: {value}"

            # Add team name tags for searchability
            text += f" | {team_name} special teams | {team_name} {memory_suffix}"

            text_chunks.append(text)

        # Load chunks into memory
        print(f"Loading {len(text_chunks)} chunks into memory...")
        for chunk in text_chunks:
            memory.add(chunk)

        # Save the memory
        memory_name = f"nfl-special-teams-{memory_suffix}"
        memory.save(f"{memory_dir}/{memory_name}")
        print(f"✓ Saved {category_name} stats to {memory_name}")

    print("\n✓ All NFL special teams stats loaded successfully!")
    print(f"Created memories in: {memory_dir}")
    print("\nMemory files created:")
    print("- nfl-special-teams-field-goals")
    print("- nfl-special-teams-kickoffs")
    print("- nfl-special-teams-punt-returns")
    print("- nfl-special-teams-punts")

if __name__ == "__main__":
    load_special_teams_stats()