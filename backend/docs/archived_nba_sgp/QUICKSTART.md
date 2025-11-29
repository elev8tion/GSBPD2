# 🏀 NBA SGP Engine - Quick Start

## Installation

```bash
cd /Users/kcdacre8tor/Desktop/GSBPD2_NBA
pip install -e .
```

## Basic Usage

### Option 1: Full Pipeline
```python
from nba_sgp import SGPEngine

engine = SGPEngine()
results = engine.full_pipeline(season='2023-24')

# Access results
print(f"Players: {len(results['player_data'])}")
print(f"Parlays: {len(results['parlays'])}")
```

### Option 2: Cherry-Pick Modules

```python
# Just odds calculator
from nba_sgp.core.odds import calculate_ev
ev = calculate_ev(0.40, 150)

# Just download NBA data
from nba_sgp.data import DataDownloader
downloader = DataDownloader()
player_df, sgp_df = downloader.download_all(season='2023-24')

# Just correlations
from nba_sgp.analysis import CorrelationAnalyzer
analyzer = CorrelationAnalyzer()
correlations = analyzer.calculate_all(player_df)

# Just predictions
from nba_sgp.models import Predictor
predictor = Predictor()
predictor.load_latest_models()
predictions = predictor.predict_dataframe(player_df)
```

## NBA Props Available

- Points 25+, 30+
- Rebounds 10+, 12+
- Assists 8+, 10+
- Three-Pointers 3+, 4+
- PRA (Points+Rebounds+Assists) 35+, 40+
- Double-Double, Triple-Double

## NBA Correlations

- Star Player - Team Points: 0.25
- Guard Assists - Team Movement: 0.18
- Center Rebounds - Team Rebounding: 0.22
- Teammate Points: -0.08 (competing for shots)
- Home Court Advantage: 0.12

## Copy to Another Project

```bash
# Copy the nba_sgp folder
cp -r nba_sgp /path/to/other/project/

# Install dependencies
pip install pandas numpy scikit-learn nba_api

# Use it
from nba_sgp.core.odds import calculate_ev
```

## Module Independence

| Module | Use For |
|--------|---------|
| `core.odds` | Odds math only |
| `data.downloader` | Download NBA stats |
| `analysis.correlations` | NBA correlations |
| `models.trainer` | Train ML models |
| `parlays.builder` | Build SGPs |

Same modular design as NFL - works anywhere!
