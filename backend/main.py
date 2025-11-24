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
    game_id: str
    home_team: str
    away_team: str
    bet_type: str # 'Spread', 'Moneyline'
    wager_amount: float
    odds: float
    prediction_used: float
    shap_values: dict = {} # Optional SHAP values
    team_strength: float = 0.0 # Store features for retraining
    opponent_strength: float = 0.0
    home_advantage: int = 0

class ResolveRequest(BaseModel):
    game_id: str
    outcome: str # 'WIN' or 'LOSS'

@app.get("/health")
def health_check():
    return {"status": "healthy", "grok_says": "I'm alive and kicking!"}

@app.get("/games")
def get_upcoming_games():
    return odds_service.get_upcoming_nfl_games()

@app.get("/portfolio")
def get_portfolio():
    return kb_service.get_all_items()

@app.post("/portfolio/bet")
def place_bet(bet: BetRequest):
    return kb_service.place_bet(bet.dict())

@app.post("/portfolio/resolve")
def resolve_bet(resolve: ResolveRequest):
    return kb_service.resolve_bet(resolve.game_id, resolve.outcome)

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
