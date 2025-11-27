from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from src.core.model import PredictionModel
from src.core.grok import GrokInsightGenerator
from src.core.data_service import DataService

app = FastAPI(title="Grok's Sports Betting Prediction Dashboard")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from src.services.odds_api import OddsAPIService
from src.services.knowledge_base import KnowledgeBaseService
from src.services.sgp_engine import SGPEngine
from src.services.nba_service import NBADataService
from src.services.nfl_service import NFLDataService

# Initialize services
model_service = PredictionModel()
grok_service = GrokInsightGenerator()
data_service = DataService()
odds_service = OddsAPIService()
kb_service = KnowledgeBaseService() # Replaces portfolio_service
sgp_engine = SGPEngine()
nba_service = NBADataService()
nfl_service = NFLDataService()

class PredictionRequest(BaseModel):
    team_strength: float
    opponent_strength: float
    home_advantage: int

class PredictionResponse(BaseModel):
    predicted_spread_margin: float
    grok_insight: str
    shap_values: dict

class BetRequest(BaseModel):
    bet_type: str  # 'spread', 'moneyline', 'over_under', 'sgp'
    wager_amount: float
    odds: float = -110  # Default American odds
    game_data: dict = {}  # Game information from frontend
    prediction_used: float = 0.0
    status: str = 'pending'  # 'pending', 'win', 'loss', 'push'
    # Legacy fields for backward compatibility
    game_id: str = None
    home_team: str = None
    away_team: str = None
    shap_values: dict = {}
    team_strength: float = 0.0
    opponent_strength: float = 0.0
    home_advantage: int = 0

class ResolveRequest(BaseModel):
    bet_id: str  # Unique bet identifier
    outcome: str  # 'win', 'loss', or 'push'

@app.get("/health")
def health_check():
    return {"status": "healthy", "kc_dacre8tor_says": "I'm alive and kicking!"}

@app.get("/games")
def get_upcoming_games():
    return odds_service.get_upcoming_nfl_games()

@app.get("/portfolio")
def get_portfolio():
    """Get all bets and observations from portfolio."""
    try:
        return kb_service.get_all_items()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch portfolio: {str(e)}")

@app.post("/portfolio/bet")
def place_bet(bet: BetRequest):
    """Place a new bet."""
    try:
        # Validate wager amount
        if bet.wager_amount <= 0:
            raise HTTPException(status_code=400, detail="Wager amount must be greater than 0")
        if bet.wager_amount > 10000:
            raise HTTPException(status_code=400, detail="Wager amount cannot exceed $10,000")

        # Validate bet type
        valid_bet_types = ['spread', 'moneyline', 'over_under', 'sgp']
        if bet.bet_type.lower() not in valid_bet_types:
            raise HTTPException(status_code=400, detail=f"Invalid bet type. Must be one of: {', '.join(valid_bet_types)}")

        return kb_service.place_bet(bet.dict())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to place bet: {str(e)}")

@app.post("/portfolio/resolve")
def resolve_bet(resolve: ResolveRequest):
    """Resolve a bet outcome (win/loss/push)."""
    try:
        # Validate outcome
        valid_outcomes = ['win', 'loss', 'push']
        if resolve.outcome.lower() not in valid_outcomes:
            raise HTTPException(status_code=400, detail=f"Invalid outcome. Must be one of: {', '.join(valid_outcomes)}")

        result = kb_service.resolve_bet(resolve.bet_id, resolve.outcome)

        if result.get('status') == 'error':
            raise HTTPException(status_code=404, detail=result.get('message'))

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to resolve bet: {str(e)}")

class SGPRequest(BaseModel):
    game_id: str
    prediction_margin: float
    home_team: str
    away_team: str

@app.post("/pipeline/sgp")
def generate_sgp(request: SGPRequest):
    game_data = {
        "home_team": request.home_team,
        "away_team": request.away_team,
        "spread": 0 # Simplified
    }
    prediction = {"predicted_spread_margin": request.prediction_margin}
    return sgp_engine.generate_combinations(game_data, prediction)

class IngestRequest(BaseModel):
    file_path: str

@app.post("/pipeline/ingest")
def ingest_video(request: IngestRequest):
    return kb_service.ingest_video(request.file_path)

@app.post("/train")
def train_model(background_tasks: BackgroundTasks):
    # Pull data from Memvid Knowledge Base
    training_data = kb_service.get_training_data()
    
    if not training_data:
        return {"status": "skipped", "message": "No data in Knowledge Base to train on."}

    # In a real app, we'd merge this with the base dataset
    print(f"Found {len(training_data)} training examples from Knowledge Base.")
    
    background_tasks.add_task(model_service.train, training_data)
    return {"status": "training_started", "message": f"KC DaCRE8TOR is learning from {len(training_data)} past events..."}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    if not model_service.model:
        # Auto-train if no model exists (for demo purposes)
        df = data_service.get_mock_training_data()
        model_service.train(df)
    
    input_data = {
        "team_strength": request.team_strength,
        "opponent_strength": request.opponent_strength,
        "home_advantage": request.home_advantage
    }
    
    prediction, shap_values = model_service.predict(input_data)
    
    if prediction is None:
        raise HTTPException(status_code=500, detail="Model prediction failed")
        
    insight = grok_service.generate_insight(
        prediction, 
        request.team_strength, 
        request.opponent_strength
    )
    
    return {
        "predicted_spread_margin": prediction,
        "grok_insight": insight,
        "shap_values": shap_values or {}
    }

# ==================== NEW MEMVID PIPELINE ENDPOINTS ====================

class MemorySearchRequest(BaseModel):
    query: str
    memories: list = []  # Empty = search all
    top_k: int = 5

class YouTubeIngestRequest(BaseModel):
    url: str
    sport: str = "nfl"  # nfl or nba
    category: str = "highlights"  # highlights, analysis, player-stats

class TextMemoryRequest(BaseModel):
    memory_name: str
    docs_dir: str
    sport: str = "nfl"

@app.post("/memories/search")
def search_memories(request: MemorySearchRequest):
    """Search across memvid memories for relevant knowledge."""
    try:
        # Validate query
        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Search query cannot be empty")

        # Validate top_k
        if request.top_k <= 0 or request.top_k > 20:
            raise HTTPException(status_code=400, detail="top_k must be between 1 and 20")

        result = kb_service.search_memories(
            query=request.query,
            memories=request.memories if request.memories else None,
            top_k=request.top_k
        )

        if result.get('status') == 'error':
            raise HTTPException(status_code=500, detail=result.get('message'))

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/memories/list")
def list_memories():
    """List all available memvid memories."""
    try:
        result = kb_service.list_all_memories()

        if result.get('status') == 'error':
            raise HTTPException(status_code=500, detail=result.get('message'))

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list memories: {str(e)}")

@app.post("/memories/create")
def create_text_memory(request: TextMemoryRequest):
    """Create a new memory from text documents."""
    try:
        # Validate memory name
        if not request.memory_name or len(request.memory_name.strip()) == 0:
            raise HTTPException(status_code=400, detail="Memory name cannot be empty")

        # Validate memory name characters (alphanumeric, hyphens, underscores only)
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', request.memory_name):
            raise HTTPException(
                status_code=400,
                detail="Memory name can only contain letters, numbers, hyphens, and underscores"
            )

        # Validate docs directory
        if not request.docs_dir or len(request.docs_dir.strip()) == 0:
            raise HTTPException(status_code=400, detail="Documents directory cannot be empty")

        from pathlib import Path
        docs_path = Path(request.docs_dir)
        if not docs_path.exists():
            raise HTTPException(status_code=404, detail=f"Directory not found: {request.docs_dir}")
        if not docs_path.is_dir():
            raise HTTPException(status_code=400, detail=f"Path is not a directory: {request.docs_dir}")

        result = kb_service.create_memory_from_text(
            memory_name=request.memory_name,
            docs_dir=request.docs_dir,
            sport=request.sport
        )

        if result.get('status') == 'error':
            raise HTTPException(status_code=500, detail=result.get('message'))

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create memory: {str(e)}")

@app.delete("/memories/{memory_name}")
def delete_memory(memory_name: str):
    """Delete a memvid memory."""
    try:
        # Validate memory name
        if not memory_name or len(memory_name.strip()) == 0:
            raise HTTPException(status_code=400, detail="Memory name cannot be empty")

        result = kb_service.delete_memory(memory_name)

        if result.get('status') == 'error':
            raise HTTPException(status_code=404, detail=result.get('message'))

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete memory: {str(e)}")

@app.post("/pipeline/youtube")
def ingest_youtube(request: YouTubeIngestRequest):
    """Download and process YouTube video (NFL/NBA highlights, analysis, etc.)."""
    return kb_service.ingest_youtube_video(
        url=request.url,
        sport=request.sport,
        category=request.category
    )

# ============ NBA DATA ENDPOINTS ============

@app.get("/nba/teams")
def get_all_nba_teams():
    """Get all NBA teams with current stats"""
    try:
        teams = nba_service.get_all_teams()
        return {"teams": teams, "total": len(teams)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get teams: {str(e)}")

@app.get("/nba/teams/{team_id}")
def get_nba_team(team_id: str):
    """Get specific NBA team by ID"""
    try:
        team = nba_service.get_team_by_id(team_id)
        if not team:
            raise HTTPException(status_code=404, detail=f"Team {team_id} not found")
        return team
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get team: {str(e)}")

@app.get("/nba/teams/{team_id}/roster")
def get_team_roster(team_id: str):
    """Get roster for a specific team"""
    try:
        players = nba_service.get_players_by_team(team_id)
        return {"team_id": team_id, "players": players, "total": len(players)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get roster: {str(e)}")

@app.get("/nba/players")
def get_all_nba_players():
    """Get all NBA players"""
    try:
        players = nba_service.get_all_players()
        return {"players": players, "total": len(players)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get players: {str(e)}")

@app.get("/nba/games")
def get_nba_games():
    """Get upcoming NBA games (cached with 1-hour expiry)"""
    try:
        games = nba_service.get_upcoming_games()
        return {"games": games, "total": len(games)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get games: {str(e)}")

@app.post("/nba/games/refresh")
def refresh_nba_games():
    """Manually refresh NBA games cache from The Odds API"""
    try:
        result = nba_service.refresh_games_cache()
        if result.get("status") == "error":
            raise HTTPException(status_code=500, detail=result.get("message"))
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to refresh games: {str(e)}")

@app.get("/nba/betting-insights")
def get_betting_insights():
    """Get AI-powered betting insights for upcoming NBA games"""
    try:
        games = nba_service.get_upcoming_games()

        insights = []
        for game in games:
            # Calculate implied probability from decimal odds
            home_prob = (1 / game['home_odds'] * 100) if game.get('home_odds') else None
            away_prob = (1 / game['away_odds'] * 100) if game.get('away_odds') else None

            # Determine value bets (where probability suggests better value)
            total_prob = (home_prob + away_prob) if (home_prob and away_prob) else None

            # Get team stats and top players
            home_stats = nba_service.get_team_stats(game['home_team'])
            away_stats = nba_service.get_team_stats(game['away_team'])
            home_top_scorers = nba_service.get_top_players(game['home_team'], 'pts', 3)
            away_top_scorers = nba_service.get_top_players(game['away_team'], 'pts', 3)

            insight = {
                "game_id": game['id'],
                "matchup": f"{game['away_team']} @ {game['home_team']}",
                "commence_time": game['commence_time'],
                "favorite": game['home_team'] if game.get('spread', 0) < 0 else game['away_team'],
                "spread": game.get('spread'),
                "total": game.get('total'),
                "team_stats": {
                    "home": home_stats['stats'] if home_stats else None,
                    "away": away_stats['stats'] if away_stats else None
                },
                "top_players": {
                    "home": [{"name": p['name'], "ppg": p['stats'].get('pts')} for p in home_top_scorers] if home_top_scorers else [],
                    "away": [{"name": p['name'], "ppg": p['stats'].get('pts')} for p in away_top_scorers] if away_top_scorers else []
                },
                "implied_probabilities": {
                    "home": round(home_prob, 2) if home_prob else None,
                    "away": round(away_prob, 2) if away_prob else None
                },
                "betting_analysis": {
                    "spread_line": f"{abs(game.get('spread', 0))} points",
                    "total_line": f"{game.get('total', 0)} points",
                    "over_odds": game.get('over_odds'),
                    "under_odds": game.get('under_odds'),
                    "market_efficiency": round(total_prob, 2) if total_prob else None  # Should be ~200% (includes vig)
                },
                "recommendation": f"Statistical Analysis: {game['home_team']} averages {home_stats['stats'].get('pts', 'N/A')} PPG vs {game['away_team']}'s {away_stats['stats'].get('pts', 'N/A')} PPG" if (home_stats and away_stats) else "Analysis pending"
            }
            insights.append(insight)

        return {
            "insights": insights,
            "total": len(insights),
            "disclaimer": "For entertainment purposes only. Bet responsibly."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get insights: {str(e)}")

@app.get("/nba/rosters")
def get_all_rosters():
    """Get complete roster data for all teams"""
    try:
        rosters = nba_service.get_roster_data()
        return {
            "rosters": rosters,
            "total_teams": len(rosters),
            "total_players": sum(len(t.get('players', [])) for t in rosters)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get rosters: {str(e)}")

@app.get("/nba/teams/{team_name}/stats")
def get_team_statistics(team_name: str):
    """Get statistics for a specific team"""
    try:
        stats = nba_service.get_team_stats(team_name)
        if not stats:
            raise HTTPException(status_code=404, detail=f"Team not found: {team_name}")
        return stats
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get team stats: {str(e)}")

@app.get("/nba/teams/{team_name}/top-players")
def get_team_top_players(team_name: str, stat: str = "pts", limit: int = 10):
    """Get top players for a team by a specific statistic"""
    try:
        players = nba_service.get_top_players(team_name, stat, limit)
        if not players:
            raise HTTPException(status_code=404, detail=f"No players found for team: {team_name}")
        return {
            "team": team_name,
            "stat": stat,
            "players": players,
            "total": len(players)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get top players: {str(e)}")

@app.get("/nba/matchup/{team_a}/{team_b}")
def get_team_matchup(team_a: str, team_b: str):
    """Compare two teams' statistics for matchup analysis"""
    try:
        comparison = nba_service.get_team_comparison(team_a, team_b)
        if "error" in comparison:
            raise HTTPException(status_code=404, detail=comparison["error"])
        return comparison
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get matchup: {str(e)}")

@app.post("/nba/scrape")
def scrape_nba_data():
    """Scrape fresh NBA data from nba.com using Firecrawl"""
    try:
        result = nba_service.scrape_all_teams()
        return {"status": "success", "message": "NBA data scraped successfully", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

# ============================================
# NBA Schedule Endpoints
# ============================================

@app.get("/nba/schedule")
async def get_nba_schedule():
    """Get the full NBA schedule for the season"""
    try:
        schedule = nba_service.get_schedule()
        return {
            "total_games": len(schedule),
            "schedule": schedule
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/nba/schedule/date/{date}")
async def get_games_by_date(date: str):
    """
    Get all games scheduled for a specific date.

    Args:
        date: Date in format YYYY-MM-DD (e.g., 2025-12-25)
    """
    try:
        games = nba_service.get_games_by_date(date)
        return {
            "date": date,
            "games_count": len(games),
            "games": games
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/nba/schedule/team/{team_name}")
async def get_team_schedule(team_name: str):
    """
    Get schedule for a specific team.

    Args:
        team_name: Full team name (e.g., Los Angeles Lakers)
    """
    try:
        games = nba_service.get_team_schedule(team_name)
        return {
            "team": team_name,
            "games_count": len(games),
            "schedule": games
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/nba/schedule/upcoming")
async def get_upcoming_games_schedule(days: int = 7):
    """
    Get games scheduled for the next N days.

    Args:
        days: Number of days to look ahead (default: 7)
    """
    try:
        games = nba_service.get_upcoming_schedule(days)
        return {
            "days_ahead": days,
            "games_count": len(games),
            "games": games
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/nba/schedule/search")
async def search_schedule(q: str):
    """
    Search schedule using semantic search.

    Args:
        q: Search query (e.g., "Lakers games in December")
    """
    try:
        results = nba_service.search_schedule(q)
        return {
            "query": q,
            "results_count": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ NFL DATA ENDPOINTS ============

@app.get("/nfl/teams")
def get_all_nfl_teams():
    """Get all NFL teams with current stats"""
    try:
        teams = nfl_service.get_all_teams()
        return {"teams": teams, "total": len(teams)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get teams: {str(e)}")

@app.get("/nfl/teams/{team_id}")
def get_nfl_team(team_id: str):
    """Get specific NFL team by ID"""
    try:
        team = nfl_service.get_team_by_id(team_id)
        if not team:
            raise HTTPException(status_code=404, detail=f"Team {team_id} not found")
        return team
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get team: {str(e)}")

@app.get("/nfl/teams/{team_id}/roster")
def get_nfl_team_roster(team_id: str):
    """Get roster for a specific NFL team"""
    try:
        players = nfl_service.get_players_by_team(team_id)
        return {"team_id": team_id, "players": players, "total": len(players)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get roster: {str(e)}")

@app.get("/nfl/players")
def get_all_nfl_players():
    """Get all NFL players"""
    try:
        players = nfl_service.get_all_players()
        return {"players": players, "total": len(players)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get players: {str(e)}")

@app.post("/nfl/scrape")
def scrape_nfl_data():
    """Scrape fresh NFL data from nfl.com using Firecrawl"""
    try:
        result = nfl_service.scrape_all_teams()
        return {"status": "success", "message": "NFL data scraped successfully", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

@app.get("/nfl/search/teams")
def search_nfl_teams(query: str, limit: int = 5):
    """Search NFL teams using Kre8VidMems semantic search"""
    try:
        results = nfl_service.search_teams(query, top_k=limit)
        return {"query": query, "results": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/nfl/search/players")
def search_nfl_players(query: str, limit: int = 10):
    """Search NFL players using Kre8VidMems semantic search"""
    try:
        results = nfl_service.search_players(query, top_k=limit)
        return {"query": query, "results": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/nfl/roster/{team_name}")
def get_nfl_team_roster_by_name(team_name: str):
    """Get roster for a team by name using Kre8VidMems search"""
    try:
        players = nfl_service.get_team_roster(team_name)
        return {"team": team_name, "players": players, "total": len(players)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get roster: {str(e)}")
