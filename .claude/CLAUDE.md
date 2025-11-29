# GSBPD2 Project Guidelines

## CRITICAL: Action Restrictions
**DO NOT execute any actions unless explicitly requested by the user.**
- ❌ DO NOT create files without being asked
- ❌ DO NOT run scripts without being asked
- ❌ DO NOT modify code without being asked
- ❌ DO NOT git commit/push without being asked
- ✅ You MAY suggest actions
- ✅ You MAY analyze and explain
- ✅ You MUST wait for user approval before executing

## Core Principles
- Always remember to create pipelines instead of doing things in a non-programmatic way.

## Working in This Codebase - CRITICAL RULES

### 1. ALWAYS Check Existing Infrastructure First
**Before creating anything new:**
1. Check `main.py` for existing API endpoints (`grep "^@app\." backend/main.py`)
2. Check `src/services/` for existing service modules
3. Check `odds_data/` for live odds cache
4. Check `data/memories/` for Kre8VidMems vector storage

**Common mistake:** Creating static JSON files when live API endpoints already exist.

### 2. Understand the Data Flow
```
External APIs → Services → Cache/Storage → FastAPI Endpoints → Frontend
     ↓
DraftKings Odds API → DraftKingsOddsService → odds_data/*.json → /odds/nba, /nba/betting-insights
NBA Stats → NBADataService → data/memories/*.ann (Kre8VidMems) → /nba/* endpoints
NFL Stats → NFLDataService → data/memories/*.ann (Kre8VidMems) → /nfl/* endpoints
```

### 3. How to Add New Data/Features

**DON'T:**
- ❌ Create standalone JSON files in random locations
- ❌ Write research results to static files
- ❌ Build new systems when existing ones already work
- ❌ Suggest "integrating with live APIs" when they're already integrated

**DO:**
- ✅ Use existing service classes (`DraftKingsOddsService`, `NBADataService`, `NFLDataService`)
- ✅ Store data in Kre8VidMems (`data/memories/`) for vector search
- ✅ Cache API responses in `odds_data/` directory
- ✅ Add endpoints to `main.py` if new functionality is needed
- ✅ Check `main.py` to see what endpoints already serve the data

### 4. Quick Reference: What's Already Built

**Odds Integration:**
- `/odds/nba/refresh` - Fetch latest NBA odds from DraftKings
- `/odds/nfl/refresh` - Fetch latest NFL odds from DraftKings
- `/odds/nba` - Get cached NBA odds
- `/odds/nfl` - Get cached NFL odds
- Historical tracking in `odds_data/odds_history.json`

**NBA Features:**
- `/nba/betting-insights` - AI-powered betting insights (uses live odds + stats)
- `/nba/teams` - All NBA teams
- `/nba/games` - Upcoming games
- `/nba/schedule` - Full schedule with date/team filtering
- Kre8VidMems memories for players, games, schedule

**NFL Features:**
- `/nfl/sgp/weekly/{week}` - SGP recommendations by week
- `/nfl/sgp/predict/{player}/{week}` - Player prop predictions
- `/nfl/sgp/correlations` - Stat correlations for SGP building
- SQLite databases: `nfl_player_stats.db`, `nfl_sgp_combos.db`
- Kre8VidMems memories for all player stats

**Knowledge Base:**
- `/memories/search` - Semantic search across all Kre8VidMems
- `/memories/list` - List all available memories
- `/memories/create` - Create new memory from documents

### 5. Before Suggesting New Features

Ask yourself:
1. Does this endpoint already exist in `main.py`?
2. Does this service already exist in `src/services/`?
3. Is this data already cached in `odds_data/` or `data/memories/`?
4. Can I use an existing service instead of creating new code?

### 6. When User Asks for Research/Data Collection

**Correct approach:**
1. Check if live API endpoint exists (`/odds/nba/refresh`, `/nba/betting-insights`)
2. If it exists, tell user to use the endpoint or offer to call it programmatically
3. If storing research insights, use Kre8VidMems memory creation
4. If adding to existing data, extend the appropriate service class

**Wrong approach:**
1. ❌ Writing standalone scripts that dump data to JSON files
2. ❌ Creating "data collection scripts" that duplicate API functionality
3. ❌ Suggesting "integrate with live APIs" when they're already integrated

## Backend Organization (as of 2024-11-27)

### Directory Structure
```
backend/
├── src/                    # Source code
│   ├── core/              # Core application logic
│   │   ├── model.py       # Prediction model
│   │   ├── grok.py        # Grok insight generator
│   │   └── data_service.py # Data service layer
│   ├── services/          # Service modules
│   │   ├── knowledge_base.py # Kre8VidMems knowledge base
│   │   ├── nba_service.py    # NBA data service
│   │   ├── nfl_service.py    # NFL data service
│   │   ├── odds_api.py       # Odds API integration
│   │   ├── portfolio.py      # Portfolio management
│   │   └── sgp_engine.py     # SGP engine
│   └── models/            # Data models
│       └── nba_models.py  # NBA data models
├── data/                  # Data storage
│   ├── memories/          # Kre8VidMems memory files
│   ├── rosters/           # Roster JSON files
│   └── cache/             # Cache storage
├── scripts/               # Utility scripts
│   ├── build/             # Build scripts
│   ├── migration/         # Migration scripts
│   └── testing/           # Test utilities
├── tests/                 # Test files
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
├── lib/                   # External libraries
│   └── kre8vidmems/       # Kre8VidMems package
├── config/                # Configuration files
├── logs/                  # Application logs
├── kre8vid_venv/         # Python virtual environment
└── main.py               # FastAPI application entry
```

### Import Pattern
- `from src.core.{module} import {class}`
- `from src.services.{module} import {class}`
- `from src.models.{module} import {class}`

### Key Technologies
- **Kre8VidMems**: Vector memory storage (no FAISS/Memvid)
- **FastAPI**: REST API framework
- **Python 3.12**: Using kre8vid_venv virtual environment

### Memory Files
Located in `data/memories/`:
- `.mp4` - QR-encoded video storage
- `.ann` - Annoy vector index
- `.meta` - Metadata storage
- `.idx` - Symlink to .ann