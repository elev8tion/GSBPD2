# GSBPD2 Project Guidelines

## Core Principles
- Always remember to create pipelines instead of doing things in a non-programmatic way.

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