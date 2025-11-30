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
from src.services.nfl_sgp_service import NFLSGPService
from src.services.nba_sgp_service import NBASGPService
from src.services.nba_service import NBADataService
from src.services.nfl_service import NFLDataService
from src.services.draftkings_odds_service import DraftKingsOddsService
from src.services.openai_service import OpenAIInsightsService
from src.services.nba_stats_collector import NBAStatsCollector

# Initialize services
model_service = PredictionModel()
grok_service = GrokInsightGenerator()
data_service = DataService()
odds_service = OddsAPIService()
kb_service = KnowledgeBaseService() # Replaces portfolio_service
nfl_sgp_service = NFLSGPService()
nba_sgp_service = NBASGPService()
nba_service = NBADataService()
nfl_service = NFLDataService()
dk_odds_service = DraftKingsOddsService()
openai_service = OpenAIInsightsService()
nba_stats_collector = NBAStatsCollector()

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
    prediction_margin: float = 0.0  # Default to 0 if not provided
    home_team: str
    away_team: str

@app.post("/pipeline/sgp")
def generate_sgp(request: SGPRequest):
    """Generate SGP picks using NFL SGP Service (deprecated - use /nfl/sgp endpoints)"""
    game_data = {
        "home_team": request.home_team,
        "away_team": request.away_team,
        "spread": 0 # Simplified
    }
    prediction = {"predicted_spread_margin": request.prediction_margin}

    # Legacy endpoint - returns simplified response
    return {
        "status": "deprecated",
        "message": "Use /nfl/sgp/weekly or /nfl/sgp/predictions endpoints",
        "game_data": game_data,
        "prediction": prediction
    }

class IngestRequest(BaseModel):
    file_path: str

@app.post("/pipeline/ingest")
def ingest_video(request: IngestRequest):
    return kb_service.ingest_video(request.file_path)

@app.post("/train")
def train_model(background_tasks: BackgroundTasks):
    # Pull data from Kre8VidMems Knowledge Base
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

# ==================== KRE8VIDMEMS KNOWLEDGE BASE ENDPOINTS ====================

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
    """Search across Kre8VidMems memories for relevant knowledge."""
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
    """List all available Kre8VidMems memories."""
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
    """Delete a Kre8VidMems memory."""
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

# ============ NBA SGP ENDPOINTS ============

class NBATrainRequest(BaseModel):
    season: str = "2023-24"
    force_download: bool = False

class NBAParlayRequest(BaseModel):
    game_id: str
    max_legs: int = 10
    min_ev: float = 0.05

@app.post("/nba/sgp/download")
def download_nba_data(request: NBATrainRequest):
    """Download NBA player data for a season"""
    try:
        result = nba_sgp_service.download_season_data(request.season, request.force_download)
        if result.get("status") == "error":
            raise HTTPException(status_code=500, detail=result.get("message"))
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

@app.post("/nba/sgp/train")
def train_nba_models(request: NBATrainRequest):
    """Train NBA SGP prediction models"""
    try:
        result = nba_sgp_service.train_models(request.season)
        if result.get("status") == "error":
            raise HTTPException(status_code=500, detail=result.get("message"))
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@app.get("/nba/sgp/player/{player_id}/{game_id}")
def get_player_prop_predictions(player_id: str, game_id: str):
    """Get prop predictions for a specific player in a game"""
    try:
        predictions = nba_sgp_service.predict_player_props(player_id, game_id)
        return predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/nba/sgp/parlays")
def build_nba_parlays(request: NBAParlayRequest):
    """Build optimal NBA parlays for a game"""
    try:
        parlays = nba_sgp_service.build_parlays(
            game_id=request.game_id,
            max_legs=request.max_legs,
            min_ev=request.min_ev
        )
        return {
            "game_id": request.game_id,
            "parlays": parlays,
            "total": len(parlays)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/nba/sgp/ev")
def calculate_nba_prop_ev(our_probability: float, sportsbook_odds: int):
    """Calculate expected value for an NBA prop bet"""
    try:
        ev = nba_sgp_service.calculate_ev(our_probability, sportsbook_odds)
        return ev
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/nba/sgp/correlations")
def get_nba_sgp_correlations():
    """Get NBA-specific correlation coefficients for SGP calculations"""
    try:
        return nba_sgp_service.get_correlations()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ NBA STATS DATA ENDPOINTS (New Database) ============

@app.get("/nba/stats/collection-status")
def get_nba_collection_status():
    """Get status of NBA data collection"""
    try:
        status = nba_stats_collector.get_collection_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/nba/stats/players/{player_id}/gamelogs")
def get_player_game_logs(player_id: str, season: str = "2025-26", limit: int = None):
    """Get game logs for a specific player"""
    try:
        import sqlite3
        # Convert season format: "2025-26" -> "22025" (NBA API format)
        season_year = season.split('-')[0]
        nba_api_season = f"2{season_year}"

        conn = sqlite3.connect(nba_stats_collector.stats_db)
        cursor = conn.cursor()

        query = '''
        SELECT game_date, matchup, pts, reb, ast, min, fgm, fga, fg3m, fg3a, ftm, fta
        FROM game_logs
        WHERE player_id = ? AND season_id = ?
        ORDER BY game_date DESC
        '''

        if limit:
            query += f" LIMIT {limit}"

        cursor.execute(query, (player_id, nba_api_season))
        rows = cursor.fetchall()
        conn.close()

        games = []
        for row in rows:
            games.append({
                "game_date": row[0],
                "matchup": row[1],
                "pts": row[2],
                "reb": row[3],
                "ast": row[4],
                "min": row[5],
                "fgm": row[6],
                "fga": row[7],
                "fg3m": row[8],
                "fg3a": row[9],
                "ftm": row[10],
                "fta": row[11]
            })

        return {
            "player_id": player_id,
            "season": season,
            "games": games,
            "total_games": len(games)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/nba/stats/players/{player_id}/averages")
def get_player_season_averages(player_id: str, season: str = "2025-26"):
    """Get season averages for a specific player"""
    try:
        import sqlite3
        # Convert season format: "2025-26" -> "22025" (NBA API format)
        season_year = season.split('-')[0]
        nba_api_season = f"2{season_year}"

        conn = sqlite3.connect(nba_stats_collector.stats_db)
        cursor = conn.cursor()

        cursor.execute('''
        SELECT games_played, mpg, ppg, rpg, apg, spg, bpg, topg, fg_pct, fg3_pct, ft_pct
        FROM season_averages
        WHERE player_id = ? AND season = ?
        ''', (player_id, nba_api_season))

        row = cursor.fetchone()
        conn.close()

        if not row:
            raise HTTPException(status_code=404, detail="Player averages not found")

        return {
            "player_id": player_id,
            "season": season,
            "games_played": row[0],
            "minutes_per_game": round(row[1], 1) if row[1] else 0,
            "points_per_game": round(row[2], 1) if row[2] else 0,
            "rebounds_per_game": round(row[3], 1) if row[3] else 0,
            "assists_per_game": round(row[4], 1) if row[4] else 0,
            "steals_per_game": round(row[5], 1) if row[5] else 0,
            "blocks_per_game": round(row[6], 1) if row[6] else 0,
            "turnovers_per_game": round(row[7], 1) if row[7] else 0,
            "field_goal_pct": round(row[8], 1) if row[8] else 0,
            "three_point_pct": round(row[9], 1) if row[9] else 0,
            "free_throw_pct": round(row[10], 1) if row[10] else 0
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/nba/stats/teams/{team_id}/roster")
def get_team_roster_from_db(team_id: str, season: str = "2025-26"):
    """Get team roster from database"""
    try:
        import sqlite3
        conn = sqlite3.connect(nba_stats_collector.teams_db)
        cursor = conn.cursor()

        cursor.execute('''
        SELECT player_id, full_name, jersey_number, position, height, weight
        FROM rosters
        WHERE team_id = ? AND season = ?
        ORDER BY full_name
        ''', (team_id, season))

        rows = cursor.fetchall()
        conn.close()

        roster = []
        for row in rows:
            roster.append({
                "player_id": row[0],
                "full_name": row[1],
                "jersey_number": row[2],
                "position": row[3],
                "height": row[4],
                "weight": row[5]
            })

        return {
            "team_id": team_id,
            "season": season,
            "roster": roster,
            "total_players": len(roster)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/nba/stats/schedule")
def get_nba_schedule_from_db(date: str = None, limit: int = 100):
    """Get NBA schedule from database"""
    try:
        import sqlite3
        conn = sqlite3.connect(nba_stats_collector.schedule_db)
        cursor = conn.cursor()

        if date:
            cursor.execute('''
            SELECT game_id, game_date, matchup, home_team_name, away_team_name
            FROM schedule
            WHERE game_date = ?
            ORDER BY game_date
            LIMIT ?
            ''', (date, limit))
        else:
            cursor.execute('''
            SELECT game_id, game_date, matchup, home_team_name, away_team_name
            FROM schedule
            ORDER BY game_date DESC
            LIMIT ?
            ''', (limit,))

        rows = cursor.fetchall()
        conn.close()

        games = []
        for row in rows:
            games.append({
                "game_id": row[0],
                "game_date": row[1],
                "matchup": row[2],
                "home_team": row[3],
                "away_team": row[4]
            })

        return {
            "games": games,
            "total": len(games)
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

@app.get("/nfl/player-stats/{player_name}")
def get_nfl_player_stats(player_name: str, week: int = None):
    """Get player stats from nfl_player_stats.db"""
    try:
        stats = nfl_service.get_player_stats(player_name, week)
        return {"player": player_name, "week": week, "stats": stats, "total": len(stats)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get player stats: {str(e)}")

@app.get("/nfl/sgp/{team}/{week}")
def get_nfl_sgp_combinations(team: str, week: int, season: int = 2024):
    """Get SGP combinations from nfl_sgp_combos.db"""
    try:
        combos = nfl_service.get_sgp_combinations(team, week, season)
        return {"team": team, "week": week, "season": season, "combinations": combos, "total": len(combos)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get SGP combinations: {str(e)}")

@app.get("/nfl/team-stats/{team}/{week}")
def get_nfl_team_weekly_stats(team: str, week: int, season: int = 2024):
    """Get aggregated team stats for a week"""
    try:
        stats = nfl_service.get_team_weekly_stats(team, week, season)
        if not stats:
            raise HTTPException(status_code=404, detail=f"No stats found for {team} week {week}")
        return {"team": team, "week": week, "season": season, "stats": stats}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get team stats: {str(e)}")

# ============ NFL SGP SERVICE ENDPOINTS ============

@app.get("/nfl/sgp/weekly/{week}")
def get_weekly_sgp_picks(week: int, season: int = 2024):
    """Generate SGP picks for a specific week using NFL SGP Service"""
    try:
        picks = nfl_sgp_service.generate_weekly_picks(week, season)
        return {
            "week": week,
            "season": season,
            "picks": picks,
            "total": len(picks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate weekly picks: {str(e)}")

@app.get("/nfl/sgp/correlations")
def get_sgp_correlations():
    """Get current SGP correlation coefficients"""
    try:
        correlations = nfl_sgp_service.get_correlations()
        return {
            "correlations": correlations,
            "description": "Correlation coefficients used for SGP fair odds calculations"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get correlations: {str(e)}")

@app.get("/nfl/sgp/predict/{player_name}/{week}")
def predict_player_props(player_name: str, week: int):
    """Predict player props for a specific player and week"""
    try:
        predictions = nfl_sgp_service.predict_player_props(player_name, week)
        if "error" in predictions:
            raise HTTPException(status_code=404, detail=predictions["error"])
        return predictions
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to predict props: {str(e)}")

@app.get("/nfl/sgp/status")
def get_sgp_service_status():
    """Get status of NFL SGP service and loaded models"""
    try:
        status = nfl_sgp_service.get_model_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get service status: {str(e)}")

class EVCalculationRequest(BaseModel):
    our_picks: list
    dk_odds: dict

@app.post("/nfl/sgp/calculate-ev")
def calculate_sgp_ev(request: EVCalculationRequest):
    """Calculate expected value vs DraftKings odds"""
    try:
        ev_picks = nfl_sgp_service.calculate_ev_vs_draftkings(
            request.our_picks,
            request.dk_odds
        )
        return {
            "ev_picks": ev_picks,
            "total_positive_ev": len(ev_picks),
            "best_pick": ev_picks[0] if ev_picks else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate EV: {str(e)}")

# ============ DRAFTKINGS ODDS ENDPOINTS ============

@app.post("/odds/nba/refresh")
def refresh_nba_odds():
    """
    MANUAL REFRESH: Fetch fresh NBA odds from DraftKings via Odds API.
    This uses API credits - only call when user clicks the refresh button!
    """
    try:
        result = dk_odds_service.fetch_nba_odds()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to refresh NBA odds: {str(e)}")

@app.post("/odds/nfl/refresh")
def refresh_nfl_odds():
    """
    MANUAL REFRESH: Fetch fresh NFL odds from DraftKings via Odds API.
    This uses API credits - only call when user clicks the refresh button!
    """
    try:
        result = dk_odds_service.fetch_nfl_odds()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to refresh NFL odds: {str(e)}")

@app.get("/odds/nba")
def get_nba_odds():
    """
    Get cached NBA odds from DraftKings (no API call).
    Returns last fetched data.
    """
    try:
        return dk_odds_service.get_cached_nba_odds()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get NBA odds: {str(e)}")

@app.get("/odds/nfl")
def get_nfl_odds():
    """
    Get cached NFL odds from DraftKings (no API call).
    Returns last fetched data.
    """
    try:
        return dk_odds_service.get_cached_nfl_odds()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get NFL odds: {str(e)}")

@app.get("/odds/history")
def get_odds_history(sport: str = None, game_id: str = None):
    """
    Get historical odds movements.

    Query params:
        sport: Filter by NBA or NFL
        game_id: Filter by specific game ID
    """
    try:
        return dk_odds_service.get_odds_history(sport, game_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get odds history: {str(e)}")

# ============ OPENAI GPT-4O-MINI INSIGHTS ENDPOINTS ============

@app.post("/ai/analyze-game")
def analyze_single_game(game_data: dict):
    """
    Analyze a single game's odds using GPT-4o-mini.

    Request body should contain game data with DraftKings odds.
    """
    try:
        result = openai_service.analyze_game_odds(game_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze game: {str(e)}")

@app.get("/ai/insights/{sport}")
def get_ai_insights(sport: str):
    """
    Get AI-powered betting insights for all games in a sport using GPT-4o-mini.

    Args:
        sport: "nba" or "nfl"

    Returns comprehensive analysis with top betting opportunities.
    """
    try:
        if sport.lower() not in ["nba", "nfl"]:
            raise HTTPException(status_code=400, detail="Sport must be 'nba' or 'nfl'")

        result = openai_service.analyze_multiple_games(sport.lower())
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get AI insights: {str(e)}")

@app.get("/ai/odds-movement/{sport}/{game_id}")
def analyze_odds_movement(sport: str, game_id: str):
    """
    Analyze historical odds movement for a specific game using GPT-4o-mini.

    Args:
        sport: "nba" or "nfl"
        game_id: Game ID to analyze

    Returns analysis of line movements and what they indicate.
    """
    try:
        if sport.lower() not in ["nba", "nfl"]:
            raise HTTPException(status_code=400, detail="Sport must be 'nba' or 'nfl'")

        result = openai_service.compare_odds_movement(sport.lower(), game_id)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze odds movement: {str(e)}")
