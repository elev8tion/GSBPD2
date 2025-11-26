# KC DaCRE8TOR's Sports Betting Prediction Dashboard (GSBPD2)

AI-Powered Sports Betting Intelligence Platform with Advanced Memory Integration

**Version**: 1.2 (NBA Roster Integration Complete)
**Status**: ✅ Core Platform Functional | 🟡 Real Data Integration In Progress

## 🎯 Overview

GSBPD2 is a comprehensive sports betting intelligence platform that combines real-time betting odds, complete team/player data, AI-powered predictions, and advanced memory storage using Memvid video compression. Currently supporting NBA and NFL with full DraftKings odds integration.

## ✨ Key Features

### NBA Integration (Latest)
- **Complete Roster Data**: 30 teams, 524 players with full ESPN statistics
- **DraftKings Betting Lines**: Real-time odds for spreads, totals, and moneylines
- **Team Stats Comparison**: Season averages for points, rebounds, assists, and more
- **Top Players Analysis**: PPG leaders for each matchup
- **Memvid AI Support**: Semantic search across 1.9 MB of compressed team/player data
- **Betting Insights Dashboard**: Enhanced UI showing matchup statistics and key players

### Core Platform Features
- **AI Prediction Engine**: XGBoost-powered spread predictions with SHAP explainability
- **Real-time Odds Integration**: DraftKings odds via The Odds API
- **Portfolio Tracking**: Memvid-based betting history with video compression
- **Same Game Parlay (SGP) Engine**: Correlation-based parlay suggestions
- **Video Ingest Pipeline**: Extract game data from screen recordings (OCR ready)
- **Knowledge Base**: Stores all game results for continuous learning
- **Memory Search**: Semantic search across all stored sports data

## Tech Stack

### Backend
- FastAPI
- XGBoost
- SHAP (Explainability)
- Memvid (Video-based data storage)
- OpenCV (Video processing)

### Frontend
- React + Vite
- Framer Motion
- Recharts
- Lucide Icons

### Visualization
- Streamlit

## Installation

### Prerequisites
- Python 3.12+ (3.14+ recommended)
- Node.js 18+
- Homebrew (macOS) or equivalent package manager
- Git

### Setup

1. **Install system dependencies**:
```bash
brew install libomp
```

2. **Configure Environment**:
```bash
cp .env.example .env
# Edit .env and add your ODDS_API_KEY (get free key at https://the-odds-api.com/)
```

3. **Backend setup**:
```bash
cd backend
python3.12 -m venv ../venv
source ../venv/bin/activate  # On Windows: ..\venv\Scripts\activate
pip install -r requirements.txt
```

4. **Frontend setup**:
```bash
cd frontend
npm install
```

## Running the Application

### Option 1: Quick Start (Recommended)
```bash
# Terminal 1 - Backend
cd backend
./start_server_safe.sh

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Option 2: Manual Start
```bash
# Terminal 1 - Backend
cd backend
source ../venv/bin/activate
python -m uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Access the Application
- **Frontend Dashboard**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)

## 🎮 Usage Guide

### 1. Betting Insights
Navigate to the **Betting Insights** tab to view:
- Real-time DraftKings odds for today's NBA games
- Team stats comparison (PPG, RPG, APG)
- Top scorers for each team
- Implied probabilities and market efficiency metrics

### 2. NBA Teams & Players
- Browse all 30 NBA teams with complete rosters
- View player statistics (points, rebounds, assists, etc.)
- Compare team matchups head-to-head

### 3. Predictions
- Generate AI-powered predictions for upcoming games
- View SHAP explainability charts showing feature importance
- Get confidence scores and recommended bets

### 4. Portfolio Tracking
- Place bets and track outcomes
- View betting history with Memvid compression
- Analyze performance over time

### 5. Same Game Parlays (SGP)
- Get correlation-based parlay suggestions
- View prop odds and combinations
- Optimize for higher payouts

### 6. Memory Search
- Search across all stored sports data using semantic search
- Query team stats, player performance, and betting history
- Powered by Memvid video compression technology

## 🚀 API Endpoints (40+ Total)

### Core Endpoints
- `GET /health` - Health check
- `GET /games` - Fetch upcoming NFL games
- `POST /predict` - Generate AI prediction
- `POST /train` - Retrain ML model

### NBA Endpoints (14 endpoints)
- `GET /nba/betting-insights` - DraftKings odds with team stats & top players
- `GET /nba/games` - Fetch NBA games
- `POST /nba/games/refresh` - Refresh games cache
- `GET /nba/teams` - All NBA teams
- `GET /nba/teams/{id}` - Team by ID
- `GET /nba/teams/{id}/roster` - Team roster
- `GET /nba/teams/{name}/stats` - Team statistics
- `GET /nba/teams/{name}/top-players` - Top players by stat
- `GET /nba/matchup/{team_a}/{team_b}` - Team comparison
- `GET /nba/players` - All players
- `GET /nba/rosters` - Complete roster data (30 teams, 524 players)
- `POST /nba/scrape` - Scrape NBA data

### NFL Endpoints (5 endpoints)
- `GET /nfl/teams` - All NFL teams
- `GET /nfl/teams/{id}` - Team by ID
- `GET /nfl/teams/{id}/roster` - Team roster
- `GET /nfl/players` - All players
- `POST /nfl/scrape` - Scrape NFL data

### Portfolio & Pipeline
- `GET /portfolio` - Get betting history
- `POST /portfolio/bet` - Place a bet
- `POST /portfolio/resolve` - Resolve bet outcome
- `POST /pipeline/ingest` - Video OCR ingestion
- `POST /pipeline/sgp` - Generate SGP suggestions
- `POST /pipeline/youtube` - YouTube video processing

### Memvid Memory
- `POST /memories/search` - Semantic search
- `GET /memories/list` - List all memories
- `POST /memories/create` - Create new memory
- `DELETE /memories/{name}` - Delete memory

**Full API documentation**: http://localhost:8000/docs

## 📊 Project Stats

- **NBA Teams**: 30 teams indexed
- **NBA Players**: 524 players indexed
- **API Endpoints**: 40+ routes
- **Memvid Memories**: 4 active (nba-teams, nba-players, nba-games, portfolio)
- **Total Compressed Data**: ~2.2 MB
- **Backend Code**: ~2,500 lines Python
- **Frontend Code**: ~15,000 lines JSX

## 📚 Documentation

- **[PROJECT_INVENTORY.md](PROJECT_INVENTORY.md)** - Comprehensive project status and inventory
- **[ROADMAP.md](ROADMAP.md)** - Strategic development plan
- **[CURRENT_ARCHITECTURE.md](CURRENT_ARCHITECTURE.md)** - System architecture details
- **[MEMVID_INTEGRATION_COMPLETE.md](backend/MEMVID_INTEGRATION_COMPLETE.md)** - Memvid setup guide
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs (when server running)

## 🐛 Troubleshooting

### macOS Python Crashes
If you experience crashes on macOS, use the safe startup script:
```bash
cd backend
./start_server_safe.sh
```
See `backend/CRASH_FIX_README.md` for details.

### API Key Issues
Ensure your `.env` file has a valid The Odds API key:
```bash
ODDS_API_KEY=your_actual_api_key_here
```
Get a free key at https://the-odds-api.com/ (500 requests/month)

### Memvid Errors
Ensure numpy version is < 2.0.0:
```bash
pip install 'numpy<2.0.0' --force-reinstall
```

## 🤝 Contributing

This is a personal project, but suggestions and feedback are welcome! Please open an issue to discuss proposed changes.

## 📝 Recent Updates

### v1.2 (2025-11-26) - NBA Roster Integration
- ✅ Added complete NBA roster data (30 teams, 524 players)
- ✅ Enhanced betting insights with team stats and top scorers
- ✅ Implemented 4 new roster-focused API endpoints
- ✅ Encoded all roster data to Memvid memories (1.9 MB compressed)
- ✅ Integrated DraftKings odds for NBA games

### v1.1 (2025-11-25) - DraftKings Integration
- ✅ Added DraftKings betting insights infrastructure
- ✅ Implemented comprehensive odds analysis
- ✅ Fixed macOS Python server crashes
- ✅ Reorganized server startup scripts

## 🎯 Next Steps

1. **The Odds API Integration** - Configure API key for real-time odds
2. **Model Persistence** - Save/load trained models
3. **Real OCR Implementation** - Tesseract/EasyOCR for video processing
4. **AI Insights Enhancement** - GPT-4/Claude integration
5. **Production Deployment** - Railway/Vercel deployment

See [ROADMAP.md](ROADMAP.md) for detailed development plan.

## 📧 Contact

Created by **KC DaCRE8TOR**
GitHub: https://github.com/elev8tion/GSBPD2

## 📄 License

MIT
