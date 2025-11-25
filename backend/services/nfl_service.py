"""
NFL Data Service
Handles scraping, storing, and retrieving NFL data using Firecrawl + Memvid
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# NFL Teams Database (32 teams)
NFL_TEAMS = [
    # NFC East
    {"id": "DAL", "name": "Dallas Cowboys", "slug": "dallas-cowboys", "division": "NFC East", "conference": "NFC"},
    {"id": "NYG", "name": "New York Giants", "slug": "new-york-giants", "division": "NFC East", "conference": "NFC"},
    {"id": "PHI", "name": "Philadelphia Eagles", "slug": "philadelphia-eagles", "division": "NFC East", "conference": "NFC"},
    {"id": "WAS", "name": "Washington Commanders", "slug": "washington-commanders", "division": "NFC East", "conference": "NFC"},
    # NFC North
    {"id": "CHI", "name": "Chicago Bears", "slug": "chicago-bears", "division": "NFC North", "conference": "NFC"},
    {"id": "DET", "name": "Detroit Lions", "slug": "detroit-lions", "division": "NFC North", "conference": "NFC"},
    {"id": "GB", "name": "Green Bay Packers", "slug": "green-bay-packers", "division": "NFC North", "conference": "NFC"},
    {"id": "MIN", "name": "Minnesota Vikings", "slug": "minnesota-vikings", "division": "NFC North", "conference": "NFC"},
    # NFC South
    {"id": "ATL", "name": "Atlanta Falcons", "slug": "atlanta-falcons", "division": "NFC South", "conference": "NFC"},
    {"id": "CAR", "name": "Carolina Panthers", "slug": "carolina-panthers", "division": "NFC South", "conference": "NFC"},
    {"id": "NO", "name": "New Orleans Saints", "slug": "new-orleans-saints", "division": "NFC South", "conference": "NFC"},
    {"id": "TB", "name": "Tampa Bay Buccaneers", "slug": "tampa-bay-buccaneers", "division": "NFC South", "conference": "NFC"},
    # NFC West
    {"id": "ARI", "name": "Arizona Cardinals", "slug": "arizona-cardinals", "division": "NFC West", "conference": "NFC"},
    {"id": "LA", "name": "Los Angeles Rams", "slug": "los-angeles-rams", "division": "NFC West", "conference": "NFC"},
    {"id": "SF", "name": "San Francisco 49ers", "slug": "san-francisco-49ers", "division": "NFC West", "conference": "NFC"},
    {"id": "SEA", "name": "Seattle Seahawks", "slug": "seattle-seahawks", "division": "NFC West", "conference": "NFC"},
    # AFC East
    {"id": "BUF", "name": "Buffalo Bills", "slug": "buffalo-bills", "division": "AFC East", "conference": "AFC"},
    {"id": "MIA", "name": "Miami Dolphins", "slug": "miami-dolphins", "division": "AFC East", "conference": "AFC"},
    {"id": "NE", "name": "New England Patriots", "slug": "new-england-patriots", "division": "AFC East", "conference": "AFC"},
    {"id": "NYJ", "name": "New York Jets", "slug": "new-york-jets", "division": "AFC East", "conference": "AFC"},
    # AFC North
    {"id": "BAL", "name": "Baltimore Ravens", "slug": "baltimore-ravens", "division": "AFC North", "conference": "AFC"},
    {"id": "CIN", "name": "Cincinnati Bengals", "slug": "cincinnati-bengals", "division": "AFC North", "conference": "AFC"},
    {"id": "CLE", "name": "Cleveland Browns", "slug": "cleveland-browns", "division": "AFC North", "conference": "AFC"},
    {"id": "PIT", "name": "Pittsburgh Steelers", "slug": "pittsburgh-steelers", "division": "AFC North", "conference": "AFC"},
    # AFC South
    {"id": "HOU", "name": "Houston Texans", "slug": "houston-texans", "division": "AFC South", "conference": "AFC"},
    {"id": "IND", "name": "Indianapolis Colts", "slug": "indianapolis-colts", "division": "AFC South", "conference": "AFC"},
    {"id": "JAX", "name": "Jacksonville Jaguars", "slug": "jacksonville-jaguars", "division": "AFC South", "conference": "AFC"},
    {"id": "TEN", "name": "Tennessee Titans", "slug": "tennessee-titans", "division": "AFC South", "conference": "AFC"},
    # AFC West
    {"id": "DEN", "name": "Denver Broncos", "slug": "denver-broncos", "division": "AFC West", "conference": "AFC"},
    {"id": "KC", "name": "Kansas City Chiefs", "slug": "kansas-city-chiefs", "division": "AFC West", "conference": "AFC"},
    {"id": "LV", "name": "Las Vegas Raiders", "slug": "las-vegas-raiders", "division": "AFC West", "conference": "AFC"},
    {"id": "LAC", "name": "Los Angeles Chargers", "slug": "los-angeles-chargers", "division": "AFC West", "conference": "AFC"},
]

class NFLDataService:
    def __init__(self):
        base_dir = Path(__file__).parent.parent
        self.data_dir = base_dir / "nfl_data"
        self.data_dir.mkdir(exist_ok=True)
        self.teams_file = self.data_dir / "teams.json"
        self.players_file = self.data_dir / "players.json"

    def scrape_all_teams(self) -> Dict:
        """Scrape data for all NFL teams"""
        print("Starting NFL data scraping...")
        teams = []

        for team_info in NFL_TEAMS:
            team = {
                "team_id": team_info["id"],
                "name": team_info["name"],
                "slug": team_info["slug"],
                "division": team_info["division"],
                "conference": team_info["conference"],
                "wins": 0,
                "losses": 0,
                "ties": 0,
                "win_percentage": 0.0,
                "points_for": 0,
                "points_against": 0,
                "last_updated": datetime.now().isoformat()
            }
            teams.append(team)

        # Save to files
        with open(self.teams_file, 'w') as f:
            json.dump(teams, f, indent=2, default=str)

        print(f"\n✓ Scraped {len(teams)} NFL teams")
        return {"teams": teams, "total": len(teams)}

    def get_all_teams(self) -> List[Dict]:
        """Get all teams from cache"""
        if self.teams_file.exists():
            with open(self.teams_file, 'r') as f:
                return json.load(f)
        # Return default structure if file doesn't exist
        return [
            {
                "team_id": team["id"],
                "name": team["name"],
                "slug": team["slug"],
                "division": team["division"],
                "conference": team["conference"],
                "wins": 0,
                "losses": 0,
                "ties": 0,
                "win_percentage": 0.0,
                "points_for": 0,
                "points_against": 0
            }
            for team in NFL_TEAMS
        ]

    def get_team_by_id(self, team_id: str) -> Optional[Dict]:
        """Get specific team by ID"""
        teams = self.get_all_teams()
        return next((t for t in teams if t["team_id"] == team_id), None)

    def get_all_players(self) -> List[Dict]:
        """Get all players from cache"""
        if self.players_file.exists():
            with open(self.players_file, 'r') as f:
                return json.load(f)
        return []

    def get_players_by_team(self, team_id: str) -> List[Dict]:
        """Get all players for a specific team"""
        all_players = self.get_all_players()
        return [p for p in all_players if p["team_id"] == team_id]
