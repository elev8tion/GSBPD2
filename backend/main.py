from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from model import PredictionModel
from grok import GrokInsightGenerator
from data_service import DataService

app = FastAPI(title="Grok's Sports Betting Prediction Dashboard")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from services.odds_api import OddsAPIService
from services.knowledge_base import KnowledgeBaseService
from services.sgp_engine import SGPEngine

# Initialize services
model_service = PredictionModel()
grok_service = GrokInsightGenerator()
data_service = DataService()
odds_service = OddsAPIService()
kb_service = KnowledgeBaseService() # Replaces portfolio_service
sgp_engine = SGPEngine()

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
    return {"status": "healthy", "grok_says": "I'm alive and kicking!"}

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
    return {"status": "training_started", "message": f"Grok is learning from {len(training_data)} past events..."}

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
