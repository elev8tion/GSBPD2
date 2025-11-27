"""
NFL Data Service
Handles storing and retrieving NFL data using Kre8VidMems
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Use Kre8VidMems directly - no more FAISS crashes!
from kre8vidmems import Kre8VidMemory
print("✅ NFL Service: Using Kre8VidMems directly (no FAISS!)")

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
        self.data_dir = base_dir / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.rosters_file = self.data_dir / "nfl_rosters.json"

        # Initialize Kre8VidMems retrievers
        self.teams_memory = None
        self.players_memory = None
        self._init_memories()

    def _init_memories(self):
        """Initialize Kre8VidMems memories for NFL data."""
        try:
            # Load NFL teams memory
            if Path("nfl-teams.ann").exists():
                self.teams_memory = Kre8VidMemory.load("nfl-teams")
                print("✓ NFL Teams Kre8VidMems memory loaded")
            else:
                print("⚠ NFL Teams memory not found")

            # Load NFL players memory
            if Path("nfl-players.ann").exists():
                self.players_memory = Kre8VidMemory.load("nfl-players")
                print("✓ NFL Players Kre8VidMems memory loaded")
            else:
                print("⚠ NFL Players memory not found")

        except Exception as e:
            print(f"⚠ Error initializing NFL memories: {e}")
            self.teams_memory = None
            self.players_memory = None

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
        """Get all teams from rosters file or memory"""
        # Try loading from rosters file first
        if self.rosters_file.exists():
            with open(self.rosters_file, 'r') as f:
                data = json.load(f)
                return [{"name": team["team"]} for team in data]

        # Fallback to default teams
        return [
            {
                "team_id": team["id"],
                "name": team["name"],
                "slug": team["slug"],
                "division": team["division"],
                "conference": team["conference"]
            }
            for team in NFL_TEAMS
        ]

    def search_teams(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search teams using Kre8VidMems."""
        if self.teams_memory:
            try:
                results = self.teams_memory.search(query, top_k=top_k)
                teams = []
                for result in results:
                    if isinstance(result, dict):
                        # Extract text from result
                        text = result.get('text', '')
                        try:
                            # Parse the JSON from the text field
                            chunk_data = json.loads(text)
                            metadata = chunk_data.get("metadata", {})
                            teams.append(metadata)
                        except:
                            # If parsing fails, try to extract team info directly
                            pass
                return teams
            except Exception as e:
                print(f"Error searching teams: {e}")

        # Fallback to text search
        return self._fallback_team_search(query)

    def _fallback_team_search(self, query: str) -> List[Dict]:
        """Fallback text search for teams."""
        query_lower = query.lower()
        teams = self.get_all_teams()
        results = []
        for team in teams:
            if query_lower in team.get("name", "").lower():
                results.append(team)
        return results

    def search_players(self, query: str, top_k: int = 10) -> List[Dict]:
        """Search players using Kre8VidMems."""
        if self.players_memory:
            try:
                results = self.players_memory.search(query, top_k=top_k)
                players = []
                for result in results:
                    if isinstance(result, dict):
                        # Extract text from result
                        text = result.get('text', '')
                        try:
                            # Parse the JSON from the text field
                            chunk_data = json.loads(text)
                            metadata = chunk_data.get("metadata", {})
                            players.append(metadata)
                        except:
                            # If parsing fails, try to extract player info directly
                            pass
                return players
            except Exception as e:
                print(f"Error searching players: {e}")

        # Fallback to loading from file
        return self._fallback_player_search(query)

    def _fallback_player_search(self, query: str) -> List[Dict]:
        """Fallback text search for players."""
        if self.rosters_file.exists():
            with open(self.rosters_file, 'r') as f:
                data = json.load(f)
                query_lower = query.lower()
                results = []
                for team in data:
                    for player in team.get("players", []):
                        if (query_lower in player.get("name", "").lower() or
                            query_lower in player.get("position", "").lower()):
                            player_data = player.copy()
                            player_data["team"] = team["team"]
                            results.append(player_data)
                return results[:10]
        return []

    def get_team_roster(self, team_name: str) -> List[Dict]:
        """Get all players for a specific team."""
        # Search for team's players
        results = self.search_players(f"{team_name} roster", top_k=50)
        return results
