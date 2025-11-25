# KC DaCRE8TOR's Sports Betting Prediction Dashboard (GSBPD)

AI-Powered Sports Betting Intelligence Platform with Advanced Memory Integration

## Features

- **AI Prediction Engine**: XGBoost-powered spread predictions with SHAP explainability
- **Real-time Odds Integration**: Fetches live NFL game data
- **Portfolio Tracking**: Memvid-based betting history with video compression
- **Same Game Parlay (SGP) Engine**: Correlation-based parlay suggestions
- **Video Ingest Pipeline**: Extract game data from screen recordings
- **Knowledge Base**: Stores all game results for continuous learning
- **Visual Database**: Streamlit interface for memory visualization

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
- Python 3.14+
- Node.js 18+
- Homebrew (macOS)

### Setup

1. **Install system dependencies**:
```bash
brew install libomp
```

2. **Backend setup**:
```bash
cd backend
python -m venv ../venv
source ../venv/bin/activate  # On Windows: ..\venv\Scripts\activate
pip install -r requirements.txt
```

3. **Frontend setup**:
```bash
cd frontend
npm install
```

## Running the Application

### Start Backend
```bash
cd backend
../venv/bin/uvicorn main:app --reload --port 8000
```

### Start Frontend
```bash
cd frontend
npm run dev
```

### Start Visual DB (Optional)
```bash
streamlit run visual_db.py
```

## Usage

1. **Dashboard**: View predictions and game insights at `http://localhost:5173`
2. **Pipeline**: Upload screen recordings to extract game data
3. **My Bets**: Track your betting portfolio
4. **Visual DB**: Explore Memvid memory at `http://localhost:8501`

## API Endpoints

- `GET /health` - Health check
- `GET /games` - Fetch upcoming games
- `POST /predict` - Generate prediction
- `POST /pipeline/ingest` - Ingest video file
- `POST /pipeline/sgp` - Generate SGP suggestions
- `GET /portfolio` - Get betting history
- `POST /portfolio/bet` - Place a bet
- `POST /portfolio/resolve` - Resolve bet outcome
- `POST /train` - Retrain model with Knowledge Base data

## License

MIT
