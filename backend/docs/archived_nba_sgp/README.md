# 🏀 NBA SGP Engine - Modular Python Package

A fully modular NBA Same Game Parlay prediction engine with ML models, correlation analysis, and EV calculations.

## 🎯 Just Like NFL, But for NBA

Same modular design as the NFL version - use only what you need!

## 📦 Installation

```bash
pip install -e .              # Core only
pip install -e .[ml]          # With ML models
pip install -e .[full]        # Everything
```

## 🏀 NBA Props Supported

- **Points**: 25+, 30+
- **Rebounds**: 10+, 12+
- **Assists**: 8+, 10+
- **Three-Pointers**: 3+, 4+
- **PRA (Points+Rebounds+Assists)**: 35+, 40+
- **Double-Double**: 10+ in any 2 categories
- **Triple-Double**: 10+ in 3 categories

## 🔗 NBA Correlations

- **Star Player - Team Points**: 0.25
- **Guard Assists - Team Ball Movement**: 0.18
- **Center Rebounds - Team Rebounding**: 0.22
- **Teammate Points**: -0.08 (negative - competing for shots)
- **Home Court Advantage**: 0.12

## 🚀 Quick Start

```python
# Full pipeline
from nba_sgp import SGPEngine

engine = SGPEngine()
results = engine.full_pipeline(season='2023-24')

# Just odds calculator
from nba_sgp.core.odds import calculate_ev

ev = calculate_ev(0.40, 150)
print(f"EV: {ev:.2f}%")

# Just download NBA data
from nba_sgp.data import DataDownloader

downloader = DataDownloader()
player_df, sgp_df = downloader.download_all(season='2023-24')
```

## 📂 Same Modular Structure as NFL

```
nba_sgp/
├── core/          # Standalone odds & config
├── data/          # NBA data download (nba_api)
├── analysis/      # Correlations & EV
├── models/        # ML training & prediction
├── parlays/       # SGP combinations
└── engine.py      # Full pipeline
```

## 🎓 Use in Different Projects

**Project A - Just odds:**
```python
from nba_sgp.core.odds import calculate_ev
```

**Project B - Data + correlations:**
```python
from nba_sgp.data import DataDownloader
from nba_sgp.analysis import CorrelationAnalyzer
```

**Project C - Everything:**
```python
from nba_sgp import SGPEngine
```

## 📊 What You Get

- ✅ **12 NBA prop predictions**
- ✅ **6 ML models** per prop
- ✅ **5 NBA-specific correlations**
- ✅ **EV calculator** with Kelly Criterion
- ✅ **156 advanced features**

## 🔧 NBA-Specific Features

- Home/away game tracking
- Days rest between games
- PRA (Points + Rebounds + Assists) combinations
- Double-double & triple-double detection
- Guard vs. Center position-specific features

## 📝 License

MIT License - use however you want!
