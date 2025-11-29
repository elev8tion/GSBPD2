"""
NBA Game Data Collection Script
Collects comprehensive betting data for tonight's NBA games
Focus: Bucks vs Knicks and Suns vs Thunder (November 28, 2025)
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Add backend to path
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

# Game data will be collected from web sources
GAMES_TONIGHT = {
    "bucks_knicks": {
        "away_team": "Milwaukee Bucks",
        "home_team": "New York Knicks",
        "away_abbr": "MIL",
        "home_abbr": "NYK",
        "game_time": "7:30 PM ET",
        "venue": "Madison Square Garden",
        "date": "2025-11-28"
    },
    "suns_thunder": {
        "away_team": "Phoenix Suns",
        "home_team": "Oklahoma City Thunder",
        "away_abbr": "PHX",
        "home_abbr": "OKC",
        "game_time": "9:30 PM ET",
        "venue": "Paycom Center",
        "date": "2025-11-28"
    }
}

# Data from previous research
BUCKS_KNICKS_DATA = {
    "betting_lines": {
        "spread": {
            "line": -8.5,
            "home_odds": "-110",
            "away_odds": "-110",
            "opening_line": -6.0,
            "movement": "Moved to NYK -8.5 (public on Knicks)"
        },
        "total": {
            "line": 233.5,
            "over_odds": "-110",
            "under_odds": "-110",
            "range": "232.5 - 234.5"
        },
        "moneyline": {
            "home": -380,
            "away": +300
        }
    },
    "injury_report": {
        "bucks": [
            {
                "player": "Giannis Antetokounmpo",
                "status": "QUESTIONABLE",
                "injury": "Groin strain",
                "games_missed": 4,
                "impact": "CRITICAL - If out, Bucks likely lose by 15+"
            }
        ],
        "knicks": [
            {
                "player": "Team healthy",
                "status": "ACTIVE"
            }
        ]
    },
    "team_trends": {
        "bucks": {
            "record": "Unknown",
            "streak": "6-game losing streak",
            "ats": "Unknown",
            "recent_form": "Poor without Giannis"
        },
        "knicks": {
            "record": "Unknown",
            "home_record": "8-1",
            "ats": "Unknown",
            "recent_form": "Strong at home"
        }
    },
    "player_props": {
        "top_picks": [
            {
                "player": "Mikal Bridges",
                "prop": "Points",
                "line": 15.5,
                "pick": "OVER",
                "odds": "-110",
                "confidence": "HIGH"
            },
            {
                "player": "Josh Hart",
                "prop": "Rebounds",
                "line": 7.5,
                "pick": "OVER",
                "odds": "-110",
                "confidence": "HIGH"
            }
        ]
    },
    "sgp_opportunities": [
        {
            "legs": [
                "Mikal Bridges Over 15.5 points",
                "Josh Hart Over 7.5 rebounds",
                "Under 232.5 total"
            ],
            "odds": "+525",
            "confidence": "MEDIUM-HIGH",
            "analysis": "Bridges averaging 19.3 PPG, Hart is a rebounding machine, Bucks' defense without Giannis is vulnerable"
        }
    ],
    "expert_picks": {
        "spread": "Knicks -8.5 (if Giannis out)",
        "total": "UNDER 233.5",
        "reasoning": "Bucks struggle without Giannis, Knicks defense at home is elite"
    }
}

SUNS_THUNDER_DATA = {
    "betting_lines": {
        "spread": {
            "line": -15.5,
            "home_odds": "-110",
            "away_odds": "-110",
            "opening_line": -14.5,
            "movement": "Moved to OKC -15.5 (largest spread this season)"
        },
        "total": {
            "line": 225.5,
            "over_odds": "-110",
            "under_odds": "-110",
            "range": "224.5 - 226.5"
        },
        "moneyline": {
            "home": -1200,
            "away": +750
        }
    },
    "injury_report": {
        "suns": [
            {
                "player": "Jalen Green",
                "status": "OUT",
                "injury": "Unknown"
            },
            {
                "player": "Grayson Allen",
                "status": "OUT",
                "injury": "Unknown"
            },
            {
                "player": "Ryan Dunn",
                "status": "OUT",
                "injury": "Unknown"
            }
        ],
        "thunder": [
            {
                "player": "Jalen Williams",
                "status": "PROBABLE",
                "injury": "Returning tonight (first game of season)",
                "impact": "POSITIVE - Adds depth and scoring"
            }
        ]
    },
    "team_trends": {
        "thunder": {
            "record": "18-1",
            "point_differential": "+16.5",
            "note": "Best point differential through 19 games in NBA history",
            "ats": "Strong favorite"
        },
        "suns": {
            "record": "Unknown",
            "injuries": "Multiple key players out",
            "recent_form": "Struggling with injuries"
        }
    },
    "player_props": {
        "top_picks": [
            {
                "player": "Shai Gilgeous-Alexander",
                "prop": "Points",
                "line": 30.5,
                "pick": "OVER",
                "odds": "-110",
                "confidence": "VERY HIGH",
                "analysis": "SGA is MVP candidate, Suns depleted roster"
            },
            {
                "player": "Jalen Williams",
                "prop": "Points",
                "line": "TBD",
                "pick": "OVER",
                "note": "First game back, expect high usage"
            }
        ]
    },
    "sgp_opportunities": [
        {
            "legs": [
                "Shai Gilgeous-Alexander Over 30.5 points",
                "Thunder -15.5",
                "Under 225.5 total"
            ],
            "odds": "TBD",
            "confidence": "HIGH",
            "analysis": "Thunder dominating this season, Suns severely depleted"
        }
    ],
    "expert_picks": {
        "spread": "Thunder -15.5",
        "total": "UNDER 225.5",
        "reasoning": "Extreme spread justified by Thunder's historic dominance and Suns' injuries"
    }
}


def save_game_data_to_json(output_dir: Path):
    """Save collected game data to JSON files"""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save Bucks vs Knicks data
    bucks_knicks_file = output_dir / "bucks_vs_knicks_2025-11-28.json"
    with open(bucks_knicks_file, 'w') as f:
        json.dump({
            "game_info": GAMES_TONIGHT["bucks_knicks"],
            "data": BUCKS_KNICKS_DATA,
            "collection_timestamp": datetime.now().isoformat()
        }, f, indent=2)
    print(f"✅ Saved Bucks vs Knicks data to {bucks_knicks_file}")

    # Save Suns vs Thunder data
    suns_thunder_file = output_dir / "suns_vs_thunder_2025-11-28.json"
    with open(suns_thunder_file, 'w') as f:
        json.dump({
            "game_info": GAMES_TONIGHT["suns_thunder"],
            "data": SUNS_THUNDER_DATA,
            "collection_timestamp": datetime.now().isoformat()
        }, f, indent=2)
    print(f"✅ Saved Suns vs Thunder data to {suns_thunder_file}")

    # Save combined data
    combined_file = output_dir / "nba_games_2025-11-28_combined.json"
    with open(combined_file, 'w') as f:
        json.dump({
            "games": {
                "bucks_vs_knicks": {
                    "game_info": GAMES_TONIGHT["bucks_knicks"],
                    "data": BUCKS_KNICKS_DATA
                },
                "suns_vs_thunder": {
                    "game_info": GAMES_TONIGHT["suns_thunder"],
                    "data": SUNS_THUNDER_DATA
                }
            },
            "collection_timestamp": datetime.now().isoformat(),
            "total_games": 2
        }, f, indent=2)
    print(f"✅ Saved combined game data to {combined_file}")

    return {
        "bucks_knicks": bucks_knicks_file,
        "suns_thunder": suns_thunder_file,
        "combined": combined_file
    }


def print_summary():
    """Print summary of collected data"""
    print("\n" + "=" * 60)
    print("NBA Game Data Collection Summary")
    print("=" * 60)

    print("\n📊 GAME 1: Milwaukee Bucks @ New York Knicks")
    print(f"   Time: {GAMES_TONIGHT['bucks_knicks']['game_time']}")
    print(f"   Spread: Knicks {BUCKS_KNICKS_DATA['betting_lines']['spread']['line']}")
    print(f"   Total: {BUCKS_KNICKS_DATA['betting_lines']['total']['line']}")
    print(f"   Key Injury: Giannis Antetokounmpo (QUESTIONABLE)")
    print(f"   Top SGP: +525 odds")

    print("\n📊 GAME 2: Phoenix Suns @ Oklahoma City Thunder")
    print(f"   Time: {GAMES_TONIGHT['suns_thunder']['game_time']}")
    print(f"   Spread: Thunder {SUNS_THUNDER_DATA['betting_lines']['spread']['line']}")
    print(f"   Total: {SUNS_THUNDER_DATA['betting_lines']['total']['line']}")
    print(f"   Thunder Record: 18-1 (Best through 19 games in NBA history)")
    print(f"   Suns Injuries: 3 players OUT")

    print("\n" + "=" * 60)


def main():
    print("=" * 60)
    print("NBA Game Data Collection Script")
    print("Date: November 28, 2025")
    print("=" * 60)

    # Output directory
    output_dir = backend_path / "data" / "nba_games" / "2025-11-28"

    # Save data to files
    print("\n📁 Saving game data...")
    files = save_game_data_to_json(output_dir)

    # Print summary
    print_summary()

    print("\n✅ Data collection complete!")
    print(f"📂 Files saved to: {output_dir}")

    return files


if __name__ == "__main__":
    main()
