# 🏀 NBA SGP Engine - Complete Package Summary

## ✅ What You Have

A **fully modular NBA SGP prediction engine** - identical architecture to NFL, adapted for basketball.

## 🎯 Key Features

### 1. Same Modular Design as NFL
- Each module works standalone
- Import only what you need
- Zero configuration required
- Works in any project

### 2. NBA-Specific Adaptations

**Props (12 total):**
- Points: 25+, 30+
- Rebounds: 10+, 12+
- Assists: 8+, 10+
- Three-Pointers: 3+, 4+
- PRA (Points+Rebounds+Assists): 35+, 40+
- Double-Double, Triple-Double

**Correlations (5 types):**
- Star Player - Team Points: 0.25
- Guard Assists - Team Movement: 0.18
- Center Rebounds - Team Rebounding: 0.22
- Teammate Points: -0.08 (negative)
- Home Court Advantage: 0.12

**Data Source:**
- Official NBA API via `nba_api` library
- Real player game logs
- Team stats and matchups

### 3. Advanced Features

**156 engineered features:**
- Rolling averages (3, 5, 10 game windows)
- Season-long trends
- Consistency scores
- Home/away tracking
- Days rest between games
- Position-specific metrics

## 📂 Package Structure

```
nba_sgp/
├── core/
│   ├── odds.py          # Same as NFL (pure math)
│   └── config.py        # NBA-specific config
├── data/
│   ├── downloader.py    # NBA API integration
│   └── preprocessor.py  # Basketball feature engineering
├── analysis/
│   ├── correlations.py  # NBA correlations
│   └── ev_calculator.py # Same as NFL
├── models/
│   ├── trainer.py       # Same ML models
│   └── predictor.py     # Load & predict
├── parlays/
│   └── builder.py       # NBA SGP combinations
└── engine.py            # Full pipeline
```

## 🚀 Usage Examples

### Full Pipeline
```python
from nba_sgp import SGPEngine

engine = SGPEngine()
results = engine.full_pipeline(season='2023-24')
```

### Cherry-Pick Modules
```python
# Project A - just odds
from nba_sgp.core.odds import calculate_ev

# Project B - data + analysis
from nba_sgp.data import DataDownloader
from nba_sgp.analysis import CorrelationAnalyzer

# Project C - everything
from nba_sgp import SGPEngine
```

## 📊 What Each Module Does

### `core` - Standalone Utilities
- Odds conversions (American ↔ Decimal)
- EV calculations
- Parlay probability with correlation
- Configuration management

### `data` - NBA Data Pipeline
- Download from official NBA API
- Process player game logs
- Engineer 156 advanced features
- Create prop targets
- Save to SQLite

### `analysis` - Basketball Analytics
- Calculate NBA-specific correlations
- Star player - team scoring correlation
- Guard assists - ball movement
- Position-based correlations
- EV and Kelly Criterion

### `models` - Machine Learning
- Train 6 model types per prop
- RandomForest, XGBoost, LightGBM, etc.
- 12 prop predictions
- Save/load trained models

### `parlays` - SGP Builder
- Build 2+ leg parlays
- Apply NBA correlations
- Calculate fair value odds
- Auto-generate from predictions

## 📥 Installation

```bash
# Core only
pip install -e .

# With ML models
pip install -e .[ml]

# Everything
pip install -e .[full]
```

## 🔧 Dependencies

**Core:**
- pandas, numpy, scikit-learn
- nba_api (official NBA stats)

**Optional:**
- xgboost, lightgbm (better models)
- matplotlib, seaborn (visualization)

## ✅ Tested and Working

All modules independently tested:
- ✅ Core odds calculations
- ✅ NBA configuration
- ✅ Feature engineering
- ✅ EV calculator
- ✅ Parlay builder
- ✅ Full engine

## 🎉 Ready to Use!

Your NBA SGP system is:
- ✅ **Modular** - use what you need
- ✅ **Portable** - works anywhere
- ✅ **NBA-specific** - basketball props & correlations
- ✅ **Production-ready** - tested and working

Same quality as NFL package, adapted for basketball! 🏀
