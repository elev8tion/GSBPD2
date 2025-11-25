# NBA & NFL Team/Player Data Implementation

## Overview
Complete implementation of NBA and NFL team/player browsing system with live data scraping using Firecrawl.

## Backend Implementation

### Services Created

1. **`backend/services/nba_service.py`**
   - NBADataService class
   - All 30 NBA teams with divisions and conferences
   - Integrates with Firecrawl for live data scraping
   - Caches data in `backend/nba_data/teams.json`
   - Methods:
     - `scrape_all_teams()` - Scrapes NBA.com using Firecrawl
     - `get_all_teams()` - Returns cached team data
     - `get_team_by_id(team_id)` - Get specific team
     - `get_players_by_team(team_id)` - Get team roster

2. **`backend/services/nfl_service.py`**
   - NFLDataService class
   - All 32 NFL teams with divisions and conferences
   - Integrates with Firecrawl for live data scraping
   - Caches data in `backend/nfl_data/teams.json`
   - Same method structure as NBA service

3. **`backend/models/nba_models.py`**
   - Pydantic models for data validation
   - Models:
     - `NBATeam` - Team data with stats
     - `NBAPlayer` - Player profiles
     - `TeamStats` - Detailed statistics
     - `GameSchedule` - Game schedules
     - `TeamMatchup` - Head-to-head analysis
     - `TeamProfile` & `PlayerProfile` - Complete profiles

### API Endpoints

#### NBA Endpoints
- `GET /nba/teams` - Get all NBA teams
- `GET /nba/teams/{team_id}` - Get specific team
- `GET /nba/teams/{team_id}/roster` - Get team roster
- `GET /nba/players` - Get all players
- `POST /nba/scrape` - Trigger fresh data scrape

#### NFL Endpoints
- `GET /nfl/teams` - Get all NFL teams
- `GET /nfl/teams/{team_id}` - Get specific team
- `GET /nfl/teams/{team_id}/roster` - Get team roster
- `GET /nfl/players` - Get all players
- `POST /nfl/scrape` - Trigger fresh data scrape

## Frontend Implementation

### Components Created

1. **`frontend/src/components/Teams.jsx`**
   - Unified component for both NBA and NFL teams
   - Features:
     - Sport switcher (NBA/NFL)
     - Search by team name
     - Filter by conference (Eastern/Western or AFC/NFC)
     - Filter by division (8 NBA divisions or 8 NFL divisions)
     - Grid layout with team cards
     - Shows: Win/Loss record, win %, PPG, RPG, APG
   - Responsive design with hover effects

2. **`frontend/src/components/Players.jsx`**
   - Browse all players from selected sport
   - Features:
     - Sport switcher (NBA/NFL)
     - Search by player name
     - Filter by position (G/F/C for NBA, QB/RB/WR/etc for NFL)
     - Filter by team
     - Shows: Jersey #, stats, height, age, experience
     - Rookie badge for first-year players

### Navigation
Added "Teams" and "Players" tabs to main app navigation in `App.jsx`

## Data Structure

### NBA Team Data
```json
{
  "team_id": "1610612747",
  "name": "Los Angeles Lakers",
  "slug": "lakers",
  "division": "Pacific",
  "conference": "Western",
  "wins": 12,
  "losses": 4,
  "win_percentage": 0.75,
  "ppg": 117.3,
  "rpg": 41.4,
  "apg": 25.8,
  "oppg": 114.6
}
```

### NFL Team Data
```json
{
  "team_id": "KC",
  "name": "Kansas City Chiefs",
  "slug": "kansas-city-chiefs",
  "division": "AFC West",
  "conference": "AFC",
  "wins": 10,
  "losses": 1,
  "ties": 0,
  "win_percentage": 0.909,
  "points_for": 295,
  "points_against": 178
}
```

## Firecrawl Integration

### How It Works
1. Backend calls Firecrawl MCP tool via the scraping functions
2. Firecrawl scrapes NBA.com or NFL.com
3. Data is parsed and stored in JSON files
4. Frontend fetches from local cache via API

### Scraped Data Sources
- **NBA**: https://www.nba.com/teams, https://www.nba.com/stats/team/{id}
- **NFL**: https://www.nfl.com/teams/

## Next Steps

### Immediate
1. ✅ Trigger live scraping for NBA teams using Firecrawl
2. ✅ Trigger live scraping for NFL teams using Firecrawl
3. Process scraped data through Memvid for semantic search
4. Add real player rosters for each team

### Future
1. Build Matchups screen comparing two teams head-to-head
2. Build Team Profile detail pages with:
   - Full roster
   - Recent games
   - Upcoming schedule
   - Betting trends
   - Historical stats
3. Build Player Profile detail pages with:
   - Season stats
   - Career stats
   - Recent game log
   - Injury status
4. Integrate with betting odds API
5. Add real-time game scores

## Usage

### Start the application
```bash
# Backend
cd backend
source ../venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm run dev
```

### Trigger data scraping
```bash
# NBA
curl -X POST http://localhost:8000/nba/scrape

# NFL
curl -X POST http://localhost:8000/nfl/scrape
```

### Browse teams
Navigate to the Teams tab in the UI and toggle between NBA and NFL

## Technologies Used
- **Backend**: Python, FastAPI, Pydantic
- **Frontend**: React, Axios, Tailwind CSS, Lucide Icons
- **Data Scraping**: Firecrawl MCP
- **Semantic Search**: Memvid (planned)
- **Data Storage**: JSON files (temporary), will migrate to database

## Status
✅ Backend services created
✅ API endpoints implemented
✅ Frontend components built
✅ Navigation integrated
✅ Sport switcher working
✅ NFL data structure added
⏳ Live data scraping (ready to trigger)
⏳ Memvid integration
⏳ Detail pages
⏳ Database migration
