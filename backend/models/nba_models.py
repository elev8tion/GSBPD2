"""
NBA Data Models
Database schema for teams, players, stats, and matchups
"""

from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field

class NBATeam(BaseModel):
    """NBA Team Model"""
    team_id: str
    name: str
    slug: str
    division: str
    conference: str  # Eastern or Western
    logo_url: Optional[str] = None
    wins: int = 0
    losses: int = 0
    win_percentage: float = 0.0
    ppg: float = 0.0  # Points per game
    rpg: float = 0.0  # Rebounds per game
    apg: float = 0.0  # Assists per game
    oppg: float = 0.0  # Opponent points per game
    last_updated: datetime = Field(default_factory=datetime.now)

class NBAPlayer(BaseModel):
    """NBA Player Model"""
    player_id: str
    name: str
    team_id: str
    team_name: str
    jersey_number: str
    position: str  # G, F, C, G-F, F-C
    height: str  # e.g., "6-8"
    weight: str  # e.g., "230 lbs"
    birthdate: str
    age: int
    experience: str  # e.g., "7" or "R" for rookie
    school: str
    how_acquired: str
    # Stats
    ppg: float = 0.0
    rpg: float = 0.0
    apg: float = 0.0
    fg_percentage: float = 0.0
    three_pt_percentage: float = 0.0
    ft_percentage: float = 0.0
    last_updated: datetime = Field(default_factory=datetime.now)

class TeamStats(BaseModel):
    """Detailed Team Statistics"""
    team_id: str
    season: str  # e.g., "2024-25"
    games_played: int
    wins: int
    losses: int
    # Offensive stats
    ppg: float
    fg_percentage: float
    three_pt_percentage: float
    ft_percentage: float
    rpg: float
    apg: float
    spg: float  # Steals per game
    bpg: float  # Blocks per game
    tpg: float  # Turnovers per game
    # Defensive stats
    oppg: float
    opp_fg_percentage: float
    last_updated: datetime = Field(default_factory=datetime.now)

class GameSchedule(BaseModel):
    """NBA Game Schedule"""
    game_id: str
    home_team_id: str
    away_team_id: str
    home_team_name: str
    away_team_name: str
    game_date: datetime
    game_time: str
    venue: str
    status: str  # SCHEDULED, LIVE, FINAL
    # Scores (if game is completed)
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    last_updated: datetime = Field(default_factory=datetime.now)

class TeamMatchup(BaseModel):
    """Head-to-head team matchup analysis"""
    matchup_id: str
    team_a_id: str
    team_b_id: str
    team_a_name: str
    team_b_name: str
    # Historical stats
    total_games: int
    team_a_wins: int
    team_b_wins: int
    avg_total_score: float
    # Recent form
    team_a_last_5: str  # e.g., "W-L-W-W-L"
    team_b_last_5: str
    # Betting insights
    team_a_cover_rate: float  # % of games team A covered spread
    team_b_cover_rate: float
    over_under_trend: str  # "OVER", "UNDER", "MIXED"
    last_updated: datetime = Field(default_factory=datetime.now)

class PlayerProfile(BaseModel):
    """Complete player profile with stats and history"""
    player: NBAPlayer
    season_stats: Dict[str, float]  # Current season averages
    career_stats: Dict[str, float]  # Career averages
    recent_games: List[Dict]  # Last 5-10 games
    injury_status: Optional[str] = None
    notes: Optional[str] = None

class TeamProfile(BaseModel):
    """Complete team profile with roster and stats"""
    team: NBATeam
    roster: List[NBAPlayer]
    stats: TeamStats
    upcoming_games: List[GameSchedule]
    recent_results: List[GameSchedule]
    key_matchups: List[TeamMatchup]
    strengths: List[str] = []
    weaknesses: List[str] = []
    betting_trends: Dict[str, str] = {}
