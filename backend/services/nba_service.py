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

from models.nba_models import (
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
        self.firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")

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
        """Get all teams from cache"""
        if self.teams_file.exists():
            with open(self.teams_file, 'r') as f:
                return json.load(f)
        return []

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

    def store_in_memvid(self, data: Dict, memory_name: str):
        """Store scraped data in Memvid for semantic search"""
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
