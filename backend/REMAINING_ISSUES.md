# Remaining Issues to Address

**Last Updated:** 2025-11-28
**Status:** 12/15 endpoints working (80%)

---

## ⚠️ Issues to Investigate

### 1. POST /predict - Not Returning JSON Response

**Priority:** Medium
**Status:** Needs Investigation

**Symptoms:**
- Endpoint accepts requests but returns empty response
- No JSON output
- No error message

**Test Case:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"team_strength":85.5,"opponent_strength":78.2,"home_advantage":1}'
```

**Current Behavior:**
- Returns nothing (empty response)

**Possible Causes:**
1. **Response Formatting Issue** - Model returns data but response serialization fails
2. **Model Not Trained** - Requires training data from Knowledge Base
   - Knowledge Base currently empty (no bet history)
   - Training endpoint returns: "No data in Knowledge Base to train on"
3. **Exception Swallowed** - Error happening but not being caught/logged

**Related Code:**
- File: `src/core/model.py` - PredictionModel class
- File: `main.py:163` - POST /predict endpoint
- File: `src/services/knowledge_base.py` - Training data source

**Next Steps:**
1. Check backend logs for errors when calling /predict
2. Add debug logging to model.py predict() method
3. Verify if model needs training first
4. Test with trained model (need to create test bet data)
5. Check response serialization in FastAPI endpoint

**Workaround:**
- None currently - endpoint non-functional

---

## ❌ Missing Data Issues

### 2. NBA Rosters - No Data Available

**Priority:** Low
**Status:** Not Fixable with Current Data

**Missing Data:**
- NBA player rosters (no `nba_rosters.json`)
- NBA player memories (no Kre8VidMems data)
- Only have hardcoded 30 team names

**What We Have:**
- ✅ 30 NBA teams (hardcoded)
- ✅ Small games cache (4KB)
- ✅ DraftKings NBA odds (11 games)

**What We Need:**
- NBA roster data for all 30 teams
- Individual player stats
- Player performance data

**Options to Fix:**
1. **Scrape NBA Data** - Use Firecrawl to scrape rosters from nba.com or espn.com
2. **API Integration** - Use NBA Stats API or similar
3. **Manual Collection** - User provides roster data files
4. **Copy NFL Pattern** - Create similar structure to NFL rosters

**Related Files:**
- `src/services/nba_service.py` - NBA data service
- `src/nba_data/games_cache.json` - Only existing NBA data

**Blocked Endpoints:**
- GET /nba/rosters
- GET /nba/teams/{team_name}/roster
- Any player-specific NBA queries

---

### 3. NBA Players - No Data Available

**Priority:** Low
**Status:** Not Fixable with Current Data

**Missing Data:**
- Individual NBA player data
- Player statistics
- Player memories in Kre8VidMems

**Dependencies:**
- Requires NBA rosters (Issue #2) to be fixed first

**Related Code:**
- Same as Issue #2

---

## 📊 Current System Status

### ✅ Fully Working (12/15 - 80%)

**NFL Services:**
- GET /nfl/teams - 32 teams with divisions
- GET /nfl/players - 768+ players with stats
- GET /nfl/roster/{team_name} - Full team rosters
- GET /nfl/search/teams - Semantic search
- GET /nfl/search/players - Semantic search

**NBA Services (Limited):**
- GET /nba/teams - 30 teams (hardcoded)

**Odds Services:**
- GET /odds/nfl - 27 games cached
- GET /odds/nba - 11 games cached
- GET /odds/history - Historical tracking

**Core Services:**
- GET /health - Backend status
- GET /memories/list - 40+ NFL memories
- POST /memories/search - Semantic search
- GET /portfolio - Knowledge Base
- POST /pipeline/sgp - SGP generation

### ⚠️ Needs Investigation (1/15)
- POST /predict - No response

### ❌ Missing Data (2/15)
- NBA rosters
- NBA players

---

## 💡 Recommendations

### Immediate Action Items:
1. **Debug POST /predict**
   - Add logging to identify issue
   - Test with mock training data
   - Fix response serialization if needed

2. **NBA Data Collection Decision**
   - User to decide: scrape, API, or defer
   - If scraping: use Firecrawl MCP tool
   - If API: evaluate NBA Stats API

### Long-term Improvements:
1. Add comprehensive error logging to all endpoints
2. Create health check for data availability
3. Build data pipeline for automated updates
4. Add data validation on startup

---

## 📝 Notes

**NFL Data Status:** ✅ Complete
- All player stats in Kre8VidMems memories
- Full rosters from ESPN
- Schedule data available
- DraftKings odds working

**NBA Data Status:** ⚠️ Minimal
- Only team names available
- No player data
- No roster data
- Odds working but analysis limited

**OpenAI Integration:** ✅ Ready
- GPT-4o-mini configured
- API key set
- 3 analysis endpoints available
- Not tested (conserving credits)

---

## 🔧 Technical Debt

1. **Remove old migration scripts** - User will delete manually later
2. **Clean up unused scrapers** - `nba_scraper.py` not in use
3. **Audit portfolio.py** - May be obsolete (replaced by knowledge_base.py)
4. **Test OpenAI endpoints** - Need to verify with real API calls

---

**END OF DOCUMENT**
