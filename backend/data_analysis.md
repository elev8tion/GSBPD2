# Data Availability Analysis for Failing Endpoints

## Summary of 5 Failing Endpoints

### 1. ❌ GET /nfl/players - Missing method `get_all_players()`
**Data Available:** ✅ YES
- `data/nfl_rosters.json` - 32 teams with ~24 players each = ~768 players total
- Multiple Kre8VidMems memories with player stats

**Can Fix:** ✅ YES - Add method to load from nfl_rosters.json

---

### 2. ❌ GET /nfl/roster/{team_name} - Returns empty players
**Data Available:** ✅ YES
- `data/nfl_rosters.json` contains full rosters for all 32 teams
- Each team has players array with name, position, number, etc.

**Can Fix:** ✅ YES - Fix roster lookup method to properly load from JSON

---

### 3. ❌ GET /nba/teams - Returns empty teams array
**Data Available:** ⚠️ PARTIAL
- NBA_TEAMS hardcoded in `nba_service.py` (30 teams)
- `src/nba_data/games_cache.json` exists (4KB file)
- NO `nba_rosters.json` found
- NO NBA memories in `data/memories/` (only NFL memories)

**Can Fix:** ✅ YES - Return hardcoded NBA_TEAMS array from service

---

### 4. ❌ POST /predict - No JSON response
**Data Available:** ❌ NO
- Requires trained model
- Knowledge Base is empty (no bet history)
- Training endpoint returns "No data in Knowledge Base to train on"

**Can Fix:** ⚠️ MAYBE - Need to investigate if it's just a response formatting issue or requires training data

---

### 5. ❌ POST /pipeline/sgp - Missing 'prediction_margin' field
**Data Available:** N/A (Schema issue, not data issue)
- This is a request validation error
- Missing required field in SGPRequest model

**Can Fix:** ✅ YES - Update SGP request model or make field optional

---

## What We Have (NFL)

### ✅ Files
- `data/nfl_rosters.json` - 32 teams, ~768 players
- 27 Kre8VidMems memories with comprehensive player stats:
  - Passing stats (team + player)
  - Rushing stats (team + player)
  - Receiving stats (team + player)
  - Defense stats (tackles, interceptions, fumbles, scoring)
  - Special teams (punts, kickoffs, field goals, returns)
  - Schedule data
  - Offensive/defensive downs stats

### ✅ What's Loaded in Memory
- All 40 NFL memories are indexed and searchable
- Semantic search working perfectly
- Team stats available
- Player stats comprehensive

---

## What We DON'T Have (NBA)

### ❌ Missing Files
- No `nba_rosters.json`
- No NBA player memories
- No NBA team memories
- Only `games_cache.json` (4KB - likely just game schedules)

### ⚠️ What Exists
- 30 hardcoded NBA teams in `nba_service.py`
- Small games cache file

---

## What We Previously Deleted (From Earlier Session)

These were identified as safe to delete but NOT YET DELETED:
- `backend/data/rosters/` (empty directory)
- `backend/data/cache/` (empty directory)
- Migration scripts in `backend/scripts/migration/`
- `backend/scrapers/nba_scraper.py`
- `backend/src/services/portfolio.py`
- `backend/lib/kre8vidmems/build/` directory

**NOTE:** These haven't been deleted yet - user said "deal with it later"

---

## Fixable vs Not Fixable

### ✅ Can Fix with Existing Data (3/5)
1. **GET /nfl/players** - Load from nfl_rosters.json
2. **GET /nfl/roster/{team_name}** - Fix roster lookup
3. **GET /nba/teams** - Return hardcoded NBA_TEAMS

### ⚠️ Need Investigation (1/5)
4. **POST /predict** - Check if it's response format or needs training data

### ✅ Simple Schema Fix (1/5)
5. **POST /pipeline/sgp** - Make prediction_margin optional or add default value

---

## Recommendation

**Fix these 4 endpoints now:**
1. Add `get_all_players()` method to NFLDataService
2. Fix `get_roster()` method in NFLDataService
3. Fix `get_all_teams()` method in NBADataService
4. Update SGP request model to fix validation error

**Investigate separately:**
- POST /predict endpoint (may just need response formatting fix)
