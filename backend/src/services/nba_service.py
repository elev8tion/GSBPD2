"""
NBA Data Service
Handles scraping, storing, and retrieving NBA data using Firecrawl + Memvid
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import requests
from dotenv import load_dotenv

from src.models.nba_models import (
    NBATeam, NBAPlayer, TeamStats, GameSchedule,
    TeamMatchup, PlayerProfile, TeamProfile
)

load_dotenv()

# NBA Teams Database
NBA_TEAMS = [
    {"id": "1610612738", "name": "Boston Celtics", "slug": "celtics", "division": "Atlantic", "conference": "Eastern"},
    {"id": "1610612751", "name": "Brooklyn Nets", "slug": "nets", "division": "Atlantic", "conference": "Eastern"},
    {"id": "1610612752", "name": "New York Knicks", "slug": "knicks", "division": "Atlantic", "conference": "Eastern"},
    {"id": "1610612755", "name": "Philadelphia 76ers", "slug": "sixers", "division": "Atlantic", "conference": "Eastern"},
    {"id": "1610612761", "name": "Toronto Raptors", "slug": "raptors", "division": "Atlantic", "conference": "Eastern"},
    {"id": "1610612741", "name": "Chicago Bulls", "slug": "bulls", "division": "Central", "conference": "Eastern"},
    {"id": "1610612739", "name": "Cleveland Cavaliers", "slug": "cavaliers", "division": "Central", "conference": "Eastern"},
    {"id": "1610612765", "name": "Detroit Pistons", "slug": "pistons", "division": "Central", "conference": "Eastern"},
    {"id": "1610612754", "name": "Indiana Pacers", "slug": "pacers", "division": "Central", "conference": "Eastern"},
    {"id": "1610612749", "name": "Milwaukee Bucks", "slug": "bucks", "division": "Central", "conference": "Eastern"},
    {"id": "1610612737", "name": "Atlanta Hawks", "slug": "hawks", "division": "Southeast", "conference": "Eastern"},
    {"id": "1610612766", "name": "Charlotte Hornets", "slug": "hornets", "division": "Southeast", "conference": "Eastern"},
    {"id": "1610612748", "name": "Miami Heat", "slug": "heat", "division": "Southeast", "conference": "Eastern"},
    {"id": "1610612753", "name": "Orlando Magic", "slug": "magic", "division": "Southeast", "conference": "Eastern"},
    {"id": "1610612764", "name": "Washington Wizards", "slug": "wizards", "division": "Southeast", "conference": "Eastern"},
    {"id": "1610612743", "name": "Denver Nuggets", "slug": "nuggets", "division": "Northwest", "conference": "Western"},
    {"id": "1610612750", "name": "Minnesota Timberwolves", "slug": "timberwolves", "division": "Northwest", "conference": "Western"},
    {"id": "1610612760", "name": "Oklahoma City Thunder", "slug": "thunder", "division": "Northwest", "conference": "Western"},
    {"id": "1610612757", "name": "Portland Trail Blazers", "slug": "blazers", "division": "Northwest", "conference": "Western"},
    {"id": "1610612762", "name": "Utah Jazz", "slug": "jazz", "division": "Northwest", "conference": "Western"},
    {"id": "1610612744", "name": "Golden State Warriors", "slug": "warriors", "division": "Pacific", "conference": "Western"},
    {"id": "1610612746", "name": "LA Clippers", "slug": "clippers", "division": "Pacific", "conference": "Western"},
    {"id": "1610612747", "name": "Los Angeles Lakers", "slug": "lakers", "division": "Pacific", "conference": "Western"},
    {"id": "1610612756", "name": "Phoenix Suns", "slug": "suns", "division": "Pacific", "conference": "Western"},
    {"id": "1610612758", "name": "Sacramento Kings", "slug": "kings", "division": "Pacific", "conference": "Western"},
    {"id": "1610612742", "name": "Dallas Mavericks", "slug": "mavericks", "division": "Southwest", "conference": "Western"},
    {"id": "1610612745", "name": "Houston Rockets", "slug": "rockets", "division": "Southwest", "conference": "Western"},
    {"id": "1610612763", "name": "Memphis Grizzlies", "slug": "grizzlies", "division": "Southwest", "conference": "Western"},
    {"id": "1610612740", "name": "New Orleans Pelicans", "slug": "pelicans", "division": "Southwest", "conference": "Western"},
    {"id": "1610612759", "name": "San Antonio Spurs", "slug": "spurs", "division": "Southwest", "conference": "Western"},
]

class NBADataService:
    def __init__(self):
        base_dir = Path(__file__).parent.parent
        self.data_dir = base_dir / "nba_data"
        self.data_dir.mkdir(exist_ok=True)
        self.teams_file = self.data_dir / "teams.json"
        self.players_file = self.data_dir / "players.json"
        self.games_cache_file = self.data_dir / "games_cache.json"
        self.rosters_file = self.data_dir / "nba_rosters.json"
        self.schedule_file = self.data_dir / "nba_schedule_clean.json"
        self.firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
        self.odds_api_key = os.getenv("ODDS_API_KEY")

        # Cache expiry time (in seconds) - default 1 hour
        self.cache_expiry = 3600

        # Initialize Kre8VidMems retrievers
        self.memories_dir = base_dir.parent / "data" / "memories"
        self._init_kre8vidmems_retrievers()

    def _init_kre8vidmems_retrievers(self):
        """Initialize Kre8VidMems memories for NBA data"""
        try:
            from kre8vidmems import Kre8VidMemory
            print("✅ NBA Service: Using Kre8VidMems directly (Annoy-based, no FAISS!)")

            # Updated paths to match actual memory files (2025 season)
            # NBA Players memory
            players_path = self.memories_dir / "nba-nba-player-profiles-2025"

            # NBA Teams memory
            teams_path = self.memories_dir / "nba-nba-teams-2025"

            # NBA Schedule memory
            schedule_path = self.memories_dir / "nba-nba-schedule-2025"

            # Load memories
            try:
                self.players_retriever = Kre8VidMemory.load(str(players_path))
                print(f"✓ NBA Players Kre8VidMems memory loaded ({len(self.players_retriever.vector_store.metadata)} chunks)")
            except Exception as e:
                self.players_retriever = None
                print(f"⚠ NBA Players memory not found - using fallback JSON ({e})")

            try:
                self.teams_retriever = Kre8VidMemory.load(str(teams_path))
                print(f"✓ NBA Teams Kre8VidMems memory loaded ({len(self.teams_retriever.vector_store.metadata)} chunks)")
            except Exception as e:
                self.teams_retriever = None
                print(f"⚠ NBA Teams memory not found - using fallback JSON ({e})")

            try:
                self.schedule_retriever = Kre8VidMemory.load(str(schedule_path))
                print(f"✓ NBA Schedule Kre8VidMems memory loaded ({len(self.schedule_retriever.vector_store.metadata)} chunks)")
            except Exception as e:
                self.schedule_retriever = None
                print(f"⚠ NBA Schedule memory not found - using fallback JSON ({e})")

        except ImportError as e:
            print(f"⚠ Kre8VidMems not available - using fallback JSON data ({e})")
            self.players_retriever = None
            self.teams_retriever = None
            self.schedule_retriever = None
        except Exception as e:
            print(f"⚠ Error initializing Kre8VidMems retrievers: {e}")
            self.players_retriever = None
            self.teams_retriever = None
            self.schedule_retriever = None

    def scrape_with_firecrawl(self, url: str) -> str:
        """Use Firecrawl to scrape a URL and return markdown content"""
        if not self.firecrawl_api_key:
            raise Exception("FIRECRAWL_API_KEY not found in environment")

        # For now, return placeholder - will integrate with MCP Firecrawl tool
        return f"Scraped content from {url}"

    def parse_roster_markdown(self, markdown: str, team_id: str, team_name: str) -> List[NBAPlayer]:
        """Parse player roster from markdown table"""
        players = []

        # Extract roster table rows
        lines = markdown.split('\n')
        in_roster_table = False

        for line in lines:
            # Look for roster table header
            if '2025-26 Team Roster' in line or 'Player' in line and 'Pos' in line:
                in_roster_table = True
                continue

            if in_roster_table and line.startswith('['):
                # Parse player row
                # Example: [LeBron James](https://www.nba.com/stats/player/2544/) | #23 | F | 6-9 | 250 lbs | DEC 30, 1984 | 40 | 22 | ...
                match = re.search(r'\[(.*?)\].*?player/(\d+).*?\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*)', line)
                if match:
                    try:
                        player = NBAPlayer(
                            player_id=match.group(2).strip(),
                            name=match.group(1).strip(),
                            team_id=team_id,
                            team_name=team_name,
                            jersey_number=match.group(3).strip().replace('#', ''),
                            position=match.group(4).strip(),
                            height=match.group(5).strip(),
                            weight=match.group(6).strip(),
                            birthdate=match.group(7).strip(),
                            age=int(match.group(8).strip()),
                            experience=match.group(9).strip(),
                            school=match.group(10).strip(),
                            how_acquired=match.group(11).strip() if len(match.groups()) > 10 else ""
                        )
                        players.append(player)
                    except Exception as e:
                        print(f"Error parsing player row: {e}")
                        continue

        return players

    def parse_team_stats_markdown(self, markdown: str, team_id: str, team_name: str) -> NBATeam:
        """Parse team stats from markdown"""
        team_info = next((t for t in NBA_TEAMS if t["id"] == team_id), None)
        if not team_info:
            raise ValueError(f"Team ID {team_id} not found")

        # Extract record (e.g., "12 - 4 | 3rd in Western")
        record_match = re.search(r'(\d+)\s*\\-\s*(\d+)', markdown)
        wins = int(record_match.group(1)) if record_match else 0
        losses = int(record_match.group(2)) if record_match else 0

        # Extract stats
        ppg_match = re.search(r'PPG.*?(\d+\.?\d*)', markdown, re.DOTALL)
        rpg_match = re.search(r'RPG.*?(\d+\.?\d*)', markdown, re.DOTALL)
        apg_match = re.search(r'APG.*?(\d+\.?\d*)', markdown, re.DOTALL)
        oppg_match = re.search(r'OPPG.*?(\d+\.?\d*)', markdown, re.DOTALL)

        team = NBATeam(
            team_id=team_id,
            name=team_name,
            slug=team_info["slug"],
            division=team_info["division"],
            conference=team_info["conference"],
            wins=wins,
            losses=losses,
            win_percentage=wins / (wins + losses) if (wins + losses) > 0 else 0.0,
            ppg=float(ppg_match.group(1)) if ppg_match else 0.0,
            rpg=float(rpg_match.group(1)) if rpg_match else 0.0,
            apg=float(apg_match.group(1)) if apg_match else 0.0,
            oppg=float(oppg_match.group(1)) if oppg_match else 0.0
        )

        return team

    def scrape_all_teams(self) -> Dict:
        """Scrape data for all NBA teams using Firecrawl"""
        print("Starting NBA data scraping with Firecrawl from NBA.com...")
        print("Note: This will be implemented with actual Firecrawl MCP calls")
        print("For now, returning team structure that will be populated by Firecrawl")

        teams = []
        for team_info in NBA_TEAMS:
            team = NBATeam(
                team_id=team_info["id"],
                name=team_info["name"],
                slug=team_info["slug"],
                division=team_info["division"],
                conference=team_info["conference"],
                wins=0,
                losses=0,
                win_percentage=0.0,
                ppg=0.0,
                rpg=0.0,
                apg=0.0,
                oppg=0.0
            )
            teams.append(team.dict())
            print(f"✓ {team_info['name']}")

        # Save to file
        with open(self.teams_file, 'w') as f:
            json.dump(teams, f, indent=2, default=str)

        print(f"\n✓ Created structure for {len(teams)} NBA teams")
        print("Ready for Firecrawl to populate with live data")
        return {"teams": teams, "total": len(teams)}

    def get_all_teams(self) -> List[Dict]:
        """Get all NBA teams from hardcoded database or JSON cache"""
        # Try JSON cache first
        if self.teams_file.exists():
            with open(self.teams_file, 'r') as f:
                teams = json.load(f)
                print(f"✓ Retrieved {len(teams)} teams from JSON cache")
                return teams

        # Fallback to hardcoded NBA_TEAMS
        print(f"✓ Retrieved {len(NBA_TEAMS)} teams from hardcoded database")
        return [
            {
                "team_id": team["id"],
                "name": team["name"],
                "slug": team["slug"],
                "division": team["division"],
                "conference": team["conference"]
            }
            for team in NBA_TEAMS
        ]

    def get_team_by_id(self, team_id: str) -> Optional[Dict]:
        """Get specific team by ID"""
        teams = self.get_all_teams()
        return next((t for t in teams if t["team_id"] == team_id), None)

    def _parse_teams_from_markdown(self, markdown: str) -> List[Dict]:
        """Parse team data from markdown tables"""
        teams = []
        lines = markdown.split('\n')

        for line in lines:
            # Look for table rows with team data
            if '|' in line and not line.startswith('|---'):
                parts = [p.strip() for p in line.split('|') if p.strip()]

                # Skip header rows
                if len(parts) > 2 and not any(header in parts[1] for header in ['Rank', 'Team', 'Conference']):
                    # Try to find team name in NBA_TEAMS
                    team_name = None
                    for part in parts:
                        for team_info in NBA_TEAMS:
                            if team_info["name"] in part:
                                team_name = team_info["name"]
                                break
                        if team_name:
                            break

                    if team_name:
                        team_info = next((t for t in NBA_TEAMS if t["name"] == team_name), None)
                        if team_info:
                            # Extract record (W-L)
                            record_match = re.search(r'(\d+)-(\d+)', line)
                            wins = int(record_match.group(1)) if record_match else 0
                            losses = int(record_match.group(2)) if record_match else 0

                            # Extract stats
                            stats = [p for p in parts if re.match(r'^\d+\.?\d*$', p)]

                            teams.append({
                                "team_id": team_info["id"],
                                "name": team_name,
                                "slug": team_info["slug"],
                                "division": team_info["division"],
                                "conference": team_info["conference"],
                                "wins": wins,
                                "losses": losses,
                                "win_percentage": wins / (wins + losses) if (wins + losses) > 0 else 0.0,
                                "ppg": float(stats[0]) if len(stats) > 0 else 0.0,
                                "rpg": float(stats[1]) if len(stats) > 1 else 0.0,
                                "apg": float(stats[2]) if len(stats) > 2 else 0.0,
                                "oppg": float(stats[3]) if len(stats) > 3 else 0.0,
                                "last_updated": datetime.now().isoformat()
                            })

        return teams

    def get_all_players(self) -> List[Dict]:
        """Get all players from Kre8VidMems or JSON cache fallback"""

        # Try Kre8VidMems first (FIXED: .idx symlinks were missing, now working!)
        if self.players_retriever:
            try:
                # Extract all player data from metadata
                players_data = []

                for meta in self.players_retriever.vector_store.metadata:
                    # Parse player info from text chunk
                    text = meta['text']
                    player = self._parse_player_from_text(text)
                    if player:
                        players_data.append(player)

                print(f"✓ Retrieved {len(players_data)} players from Kre8VidMems")
                return players_data

            except Exception as e:
                print(f"⚠ Error retrieving players from Kre8VidMems: {e}")
                # Fall through to JSON fallback

        # Fallback to JSON file
        if self.players_file.exists():
            with open(self.players_file, 'r') as f:
                players_data = json.load(f)
                print(f"✓ Retrieved {len(players_data)} players from JSON cache")
                return players_data

        print("⚠ No players data available - neither Kre8VidMems nor players.json found")
        return []

    def _parse_player_from_text(self, text: str) -> Optional[Dict]:
        """Parse player data from text chunk"""
        try:
            # Extract player info using regex patterns
            player = {}

            # Player name
            name_match = re.search(r'Player:\s*([^\n]+)', text)
            if name_match:
                player['name'] = name_match.group(1).strip()
            else:
                return None  # Must have a name

            # Position
            pos_match = re.search(r'Position:\s*([^\n]+)', text)
            if pos_match:
                player['position'] = pos_match.group(1).strip()

            # Team ID
            team_match = re.search(r'Team:\s*(\d+)', text)
            if team_match:
                player['team_id'] = team_match.group(1).strip()
                # Map team ID to team name
                team_name = next((t['name'] for t in NBA_TEAMS if t['id'] == player['team_id']), 'Unknown')
                player['team_name'] = team_name

            # Jersey number
            jersey_match = re.search(r'Jersey:\s*#?(\d+)', text)
            if jersey_match:
                player['jersey_number'] = jersey_match.group(1).strip()

            # Height
            height_match = re.search(r'Height:\s*([^\n]+)', text)
            if height_match:
                player['height'] = height_match.group(1).strip()

            # Weight
            weight_match = re.search(r'Weight:\s*(\d+)', text)
            if weight_match:
                player['weight'] = weight_match.group(1).strip()

            # Experience
            exp_match = re.search(r'Experience:\s*([^\n]+)', text)
            if exp_match:
                player['experience'] = exp_match.group(1).strip()

            # School
            school_match = re.search(r'School:\s*([^\n]+)', text)
            if school_match:
                player['school'] = school_match.group(1).strip()

            # Player ID (try multiple patterns)
            id_match = re.search(r'Player ID:\s*(\d+)', text)
            if id_match:
                player['player_id'] = id_match.group(1).strip()
            else:
                # Fallback: try to extract from any number in the text
                id_match = re.search(r'ID:\s*(\d+)', text)
                if id_match:
                    player['player_id'] = id_match.group(1).strip()

            return player if player.get('name') else None

        except Exception as e:
            print(f"⚠ Error parsing player: {e}")
            return None

    def _is_cache_fresh(self) -> bool:
        """Check if games cache is fresh (within expiry time)"""
        if not self.games_cache_file.exists():
            return False

        try:
            with open(self.games_cache_file, 'r') as f:
                cache_data = json.load(f)

            cached_at = datetime.fromisoformat(cache_data.get("cached_at", "1970-01-01T00:00:00"))
            age_seconds = (datetime.now() - cached_at).total_seconds()

            return age_seconds < self.cache_expiry
        except Exception as e:
            print(f"⚠ Error checking cache freshness: {e}")
            return False

    def _load_games_from_cache(self) -> List[Dict]:
        """Load games from cache file"""
        try:
            with open(self.games_cache_file, 'r') as f:
                cache_data = json.load(f)
            return cache_data.get("games", [])
        except Exception as e:
            print(f"⚠ Error loading games from cache: {e}")
            return []

    def _save_games_to_cache(self, games: List[Dict]):
        """Save games to cache file with timestamp"""
        try:
            cache_data = {
                "cached_at": datetime.now().isoformat(),
                "games": games
            }
            with open(self.games_cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
            print(f"✓ Cached {len(games)} NBA games")
        except Exception as e:
            print(f"⚠ Error saving games to cache: {e}")

    def _fetch_games_from_odds_api(self) -> List[Dict]:
        """Fetch games from The Odds API using DraftKings exclusively"""
        if not self.odds_api_key:
            print("⚠ ODDS_API_KEY not configured")
            return []

        try:
            url = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds/"
            params = {
                "apiKey": self.odds_api_key,
                "regions": "us",
                "markets": "h2h,spreads,totals",  # Added totals (over/under)
                "oddsFormat": "decimal",
                "bookmakers": "draftkings"  # Use DraftKings exclusively
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            games_data = response.json()
            games = []

            for game in games_data:
                # Extract betting data from bookmakers
                home_odds = None
                away_odds = None
                spread_line = None
                total_line = None
                over_odds = None
                under_odds = None

                if game.get("bookmakers"):
                    # Get odds from DraftKings
                    bookmaker = game["bookmakers"][0]
                    for market in bookmaker.get("markets", []):
                        if market["key"] == "h2h":
                            # Moneyline odds
                            for outcome in market["outcomes"]:
                                if outcome["name"] == game["home_team"]:
                                    home_odds = outcome["price"]
                                elif outcome["name"] == game["away_team"]:
                                    away_odds = outcome["price"]
                        elif market["key"] == "spreads":
                            # Point spread
                            for outcome in market["outcomes"]:
                                if outcome["name"] == game["home_team"]:
                                    spread_line = outcome.get("point")
                        elif market["key"] == "totals":
                            # Over/Under totals
                            for outcome in market["outcomes"]:
                                if outcome["name"] == "Over":
                                    over_odds = outcome["price"]
                                    total_line = outcome.get("point")
                                elif outcome["name"] == "Under":
                                    under_odds = outcome["price"]

                games.append({
                    "id": game["id"],
                    "home_team": game["home_team"],
                    "away_team": game["away_team"],
                    "commence_time": game["commence_time"],
                    "home_odds": home_odds,
                    "away_odds": away_odds,
                    "spread": spread_line,
                    "total": total_line,
                    "over_odds": over_odds,
                    "under_odds": under_odds,
                    "sport": "NBA",
                    "bookmaker": "DraftKings"
                })

            print(f"✓ Retrieved {len(games)} upcoming NBA games from DraftKings via Odds API")
            return games

        except requests.exceptions.RequestException as e:
            print(f"⚠ Error fetching games from Odds API: {e}")
            return []
        except Exception as e:
            print(f"⚠ Unexpected error getting games: {e}")
            return []

    def get_upcoming_games(self, force_refresh: bool = False) -> List[Dict]:
        """
        Get upcoming NBA games - first from cache, then from Odds API if needed.

        Args:
            force_refresh: If True, bypass cache and fetch fresh data

        Returns:
            List of game dictionaries
        """
        # Check cache first (unless force refresh)
        if not force_refresh and self._is_cache_fresh():
            games = self._load_games_from_cache()
            if games:
                print(f"✓ Loaded {len(games)} NBA games from cache")
                return games

        # Cache miss or stale - fetch from Odds API
        games = self._fetch_games_from_odds_api()

        # Save to cache for next time
        if games:
            self._save_games_to_cache(games)

        return games

    def refresh_games_cache(self) -> Dict:
        """Manually refresh games cache from Odds API"""
        games = self._fetch_games_from_odds_api()
        if games:
            self._save_games_to_cache(games)
            return {
                "status": "success",
                "message": f"Refreshed {len(games)} games from Odds API",
                "games": games
            }
        return {
            "status": "error",
            "message": "Failed to fetch games from Odds API"
        }

    def _parse_players_from_markdown(self, markdown: str, team_id: str) -> List[Dict]:
        """Parse player data from markdown roster"""
        players = []
        lines = markdown.split('\n')

        # Find team name
        team_info = next((t for t in NBA_TEAMS if t["id"] == team_id), None)
        team_name = team_info["name"] if team_info else "Unknown"

        for line in lines:
            # Look for player entries (format: "- Name (#Jersey, Position, Height, Weight, Age, Years Pro) - Stats")
            match = re.search(r'-\s+([\w\s\.]+?)\s+\(#(\d+),\s+([\w-]+),\s+([\d\'"-]+),\s+([\d\s]+lbs),\s+Age\s+(\d+),\s+(\w+)\s+YRS?\s+PRO\)\s+-\s+([\d\.\s]+PPG,\s+[\d\.\s]+APG,\s+[\d\.\s]+RPG)', line)

            if match:
                name = match.group(1).strip()
                jersey = match.group(2).strip()
                position = match.group(3).strip()
                height = match.group(4).strip()
                weight = match.group(5).strip()
                age = match.group(6).strip()
                years_pro = match.group(7).strip()
                stats_str = match.group(8).strip()

                # Parse stats
                stats_match = re.findall(r'([\d\.]+)', stats_str)
                ppg = float(stats_match[0]) if len(stats_match) > 0 else 0.0
                apg = float(stats_match[1]) if len(stats_match) > 1 else 0.0
                rpg = float(stats_match[2]) if len(stats_match) > 2 else 0.0

                players.append({
                    "player_id": f"{team_id}_{jersey}",
                    "name": name,
                    "team_id": team_id,
                    "team_name": team_name,
                    "jersey_number": jersey,
                    "position": position,
                    "height": height,
                    "weight": weight,
                    "age": int(age) if age.isdigit() else 0,
                    "experience": years_pro,
                    "ppg": ppg,
                    "apg": apg,
                    "rpg": rpg
                })

        return players

    def get_players_by_team(self, team_id: str) -> List[Dict]:
        """Get all players for a specific team from Memvid or fallback to JSON"""
        # Try Memvid first
        if self.players_retriever:
            try:
                # Get team name
                team_info = next((t for t in NBA_TEAMS if t["id"] == team_id), None)
                if team_info:
                    results = self.players_retriever.search(f"{team_info['name']} roster", top_k=3)

                    players = []
                    for result in results:
                        players_from_result = self._parse_players_from_markdown(result, team_id)
                        players.extend(players_from_result)

                    if players:
                        print(f"✓ Retrieved {len(players)} players for {team_info['name']} from Memvid")
                        return players
            except Exception as e:
                print(f"⚠ Memvid query failed: {e}, falling back to JSON")

        # Fallback to filtering all players
        all_players = self.get_all_players()
        return [p for p in all_players if p["team_id"] == team_id]

    def store_in_kre8vidmems(self, data: Dict, memory_name: str):
        """Store scraped data in Kre8VidMems for semantic search"""
        from services.knowledge_base import KnowledgeBaseService

        kb = KnowledgeBaseService()

        # Convert data to text chunks
        text_chunks = []
        if "teams" in data:
            for team in data["teams"]:
                chunk = f"""
                Team: {team['name']}
                Division: {team['division']}
                Conference: {team['conference']}
                Record: {team['wins']}-{team['losses']}
                PPG: {team['ppg']}
                """
                text_chunks.append(chunk)

        # Create memory
        docs_dir = self.data_dir / "text_dump"
        docs_dir.mkdir(exist_ok=True)

        for i, chunk in enumerate(text_chunks):
            with open(docs_dir / f"chunk_{i}.txt", 'w') as f:
                f.write(chunk)

        kb.create_memory_from_text(memory_name, str(docs_dir), "nba")
        print(f"✓ Stored in Memvid memory: {memory_name}")

    # ==================== ROSTER DATA METHODS ====================

    def get_roster_data(self) -> List[Dict]:
        """Load complete roster data from nba_rosters.json"""
        if not self.rosters_file.exists():
            print(f"⚠ Roster file not found: {self.rosters_file}")
            return []

        with open(self.rosters_file, 'r') as f:
            return json.load(f)

    def get_team_stats(self, team_name: str) -> Optional[Dict]:
        """Get team statistics by team name"""
        rosters = self.get_roster_data()
        for team in rosters:
            if team['team'].lower() == team_name.lower():
                return {
                    "team": team['team'],
                    "stats": team.get('team_stats', {}),
                    "roster_size": len(team.get('players', []))
                }
        return None

    def get_top_players(self, team_name: str, stat: str = 'pts', limit: int = 3) -> List[Dict]:
        """Get top players for a team by a specific stat"""
        rosters = self.get_roster_data()
        for team in rosters:
            if team['team'].lower() == team_name.lower():
                players = team.get('players', [])
                # Filter players with valid stats and sort
                valid_players = [
                    p for p in players
                    if p.get('stats', {}).get(stat) and p.get('stats', {}).get(stat) != 'N/A'
                ]
                # Convert stat to float for sorting
                for p in valid_players:
                    try:
                        p['_sort_val'] = float(p['stats'][stat])
                    except (ValueError, TypeError):
                        p['_sort_val'] = 0.0

                # Sort and return top players
                top = sorted(valid_players, key=lambda x: x['_sort_val'], reverse=True)[:limit]

                # Clean up temporary sort field
                for p in top:
                    del p['_sort_val']

                return top
        return []

    def get_team_comparison(self, team_a: str, team_b: str) -> Dict:
        """Compare two teams' statistics"""
        stats_a = self.get_team_stats(team_a)
        stats_b = self.get_team_stats(team_b)

        if not stats_a or not stats_b:
            return {"error": "One or both teams not found"}

        comparison = {
            "team_a": {
                "name": stats_a['team'],
                "stats": stats_a['stats']
            },
            "team_b": {
                "name": stats_b['team'],
                "stats": stats_b['stats']
            },
            "differences": {}
        }

        # Calculate differences for key stats
        for stat in ['pts', 'reb', 'ast', 'stl', 'blk']:
            val_a = float(stats_a['stats'].get(stat, 0) or 0)
            val_b = float(stats_b['stats'].get(stat, 0) or 0)
            comparison['differences'][stat] = {
                "advantage": stats_a['team'] if val_a > val_b else stats_b['team'],
                "diff": abs(val_a - val_b)
            }

        return comparison

    # ============================================
    # Schedule Methods
    # ============================================

    def get_schedule(self) -> List[Dict]:
        """
        Get the full NBA schedule for the season.

        Returns:
            List of all scheduled games
        """
        try:
            if self.schedule_file.exists():
                with open(self.schedule_file, 'r') as f:
                    schedule = json.load(f)
                print(f"✓ Loaded {len(schedule)} games from schedule")
                return schedule
            else:
                print("⚠ Schedule file not found")
                return []
        except Exception as e:
            print(f"⚠ Error loading schedule: {e}")
            return []

    def get_games_by_date(self, date: str) -> List[Dict]:
        """
        Get all games scheduled for a specific date.

        Args:
            date: Date in format YYYY-MM-DD

        Returns:
            List of games scheduled for that date
        """
        schedule = self.get_schedule()
        games = [g for g in schedule if g.get('date') == date]
        print(f"✓ Found {len(games)} games on {date}")
        return games

    def get_team_schedule(self, team_name: str) -> List[Dict]:
        """
        Get schedule for a specific team.

        Args:
            team_name: Full team name (e.g., "Los Angeles Lakers")

        Returns:
            List of games for that team (both home and away)
        """
        schedule = self.get_schedule()
        games = [
            g for g in schedule
            if g.get('home_team') == team_name or g.get('away_team') == team_name
        ]
        print(f"✓ Found {len(games)} games for {team_name}")
        return games

    def get_upcoming_schedule(self, days: int = 7) -> List[Dict]:
        """
        Get games scheduled for the next N days.

        Args:
            days: Number of days to look ahead (default: 7)

        Returns:
            List of upcoming games
        """
        from datetime import datetime, timedelta

        schedule = self.get_schedule()
        today = datetime.now().date()
        cutoff = today + timedelta(days=days)

        upcoming = [
            g for g in schedule
            if today <= datetime.fromisoformat(g.get('date')).date() <= cutoff
        ]

        # Sort by date
        upcoming = sorted(upcoming, key=lambda x: x.get('date'))

        print(f"✓ Found {len(upcoming)} games in next {days} days")
        return upcoming

    def search_schedule(self, query: str) -> List[Dict]:
        """
        Search schedule using Memvid semantic search (if available).

        Args:
            query: Search query (e.g., "Lakers games in December")

        Returns:
            List of relevant games from semantic search
        """
        try:
            if self.schedule_retriever:
                results = self.schedule_retriever.query(query, top_k=10)
                print(f"✓ Memvid search returned {len(results)} results")
                return results
            else:
                print("⚠ Schedule Memvid retriever not available - falling back to text search")
                # Fallback to simple text matching
                schedule = self.get_schedule()
                query_lower = query.lower()
                matches = [
                    g for g in schedule
                    if query_lower in g.get('home_team', '').lower()
                    or query_lower in g.get('away_team', '').lower()
                    or query_lower in g.get('date', '').lower()
                ]
                return matches
        except Exception as e:
            print(f"⚠ Error searching schedule: {e}")
            return []
