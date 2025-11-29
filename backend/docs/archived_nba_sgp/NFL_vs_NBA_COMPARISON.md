# 🏈 NFL vs 🏀 NBA SGP Engines - Side-by-Side

## Both Share Same Architecture

| Feature | NFL | NBA |
|---------|-----|-----|
| **Modular Design** | ✅ Yes | ✅ Yes |
| **Standalone Modules** | ✅ Yes | ✅ Yes |
| **Auto-Config** | ✅ Yes | ✅ Yes |
| **ML Models** | 6 types | 6 types |
| **Advanced Features** | 156 | 156 |
| **Correlation Types** | 5 | 5 |

## Sport-Specific Differences

### Props Predicted

**NFL (8 props):**
- Passing 250+, 300+
- Rushing 80+, 100+
- Receiving 75+, 100+
- Anytime TD
- Receptions 5+

**NBA (12 props):**
- Points 25+, 30+
- Rebounds 10+, 12+
- Assists 8+, 10+
- Three-Pointers 3+, 4+
- PRA 35+, 40+
- Double-Double, Triple-Double

### Correlations

**NFL:**
- QB-WR: 0.12
- QB-TE: 0.092
- QB-RB: 0.084
- WR-WR: -0.016
- RB-Team TDs: 0.13

**NBA:**
- Star-Team Points: 0.25
- Guard-Team Assists: 0.18
- Center-Team Rebounds: 0.22
- Teammate Points: -0.08
- Home Court: 0.12

### Data Sources

**NFL:**
- nflverse (GitHub releases)
- CSV/Parquet downloads
- 2023-2024 seasons

**NBA:**
- Official NBA API (nba_api)
- Live player game logs
- 2023-24 season

### Feature Engineering

**NFL-Specific:**
- Position: QB, RB, WR, TE
- Week-based rolling windows
- Rest based on weeks between games

**NBA-Specific:**
- Stats: PTS, REB, AST, 3PM
- Game-based rolling windows
- Days rest between games
- Home/away tracking
- PRA combinations

## Usage - Identical Structure

### NFL
```python
from nfl_sgp import SGPEngine
engine = SGPEngine()
results = engine.full_pipeline(years=[2023, 2024])
```

### NBA
```python
from nba_sgp import SGPEngine
engine = SGPEngine()
results = engine.full_pipeline(season='2023-24')
```

## Module Comparison

| Module | NFL | NBA | Shared? |
|--------|-----|-----|---------|
| `core/odds.py` | ✅ | ✅ | 100% same |
| `core/config.py` | ✅ | ✅ | Adapted |
| `data/downloader.py` | nflverse | NBA API | Different |
| `data/preprocessor.py` | Football stats | Basketball stats | Adapted |
| `analysis/correlations.py` | Football combos | Basketball combos | Adapted |
| `analysis/ev_calculator.py` | ✅ | ✅ | 100% same |
| `models/trainer.py` | ✅ | ✅ | 100% same |
| `models/predictor.py` | ✅ | ✅ | 100% same |
| `parlays/builder.py` | ✅ | ✅ | 95% same |
| `engine.py` | ✅ | ✅ | Adapted |

## Installation

### NFL
```bash
cd GSBPD2_NFL
pip install -e .
```

### NBA
```bash
cd GSBPD2_NBA
pip install -e .
```

## Use Both in Same Project

```python
# Import both!
from nfl_sgp import SGPEngine as NFL_Engine
from nba_sgp import SGPEngine as NBA_Engine

# Use NFL engine
nfl = NFL_Engine(base_dir='./nfl_data')
nfl_results = nfl.full_pipeline()

# Use NBA engine
nba = NBA_Engine(base_dir='./nba_data')
nba_results = nba.full_pipeline()

# Or just cherry-pick from each
from nfl_sgp.core.odds import calculate_ev as nfl_ev
from nba_sgp.core.odds import calculate_ev as nba_ev
```

## Files Created

**Both packages have:**
- `setup.py` - Installation config
- `requirements.txt` - Dependencies
- `README.md` - Documentation
- `QUICKSTART.md` - Quick reference
- `PACKAGE_SUMMARY.md` - Complete overview

## 🎯 Result

Two identical, modular, production-ready SGP engines:
- 🏈 **NFL**: Football props, nflverse data
- 🏀 **NBA**: Basketball props, NBA API data

Both can be:
- ✅ Installed anywhere
- ✅ Used modularly
- ✅ Mixed in same project
- ✅ Zero configuration issues
