# Core Modules Usage Guide

Quick reference for using the migrated core modules in GSBPD2.

## Import Pattern

All core modules follow this pattern:
```python
from src.core.{module} import {class_or_function}
```

---

## 1. Odds Calculator

**Pure math functions for odds calculations.**

```python
from src.core.odds_calculator import (
    american_to_decimal,
    decimal_to_american,
    calculate_ev,
    calculate_parlay_odds,
    compare_odds
)

# Convert American odds to probability
prob = american_to_decimal(-110)  # 0.524

# Convert probability to American odds
odds = decimal_to_american(0.40)  # +150

# Calculate Expected Value
ev = calculate_ev(our_prob=0.40, sportsbook_odds=200)  # 20.0%

# Calculate parlay odds with correlation
combined_prob, parlay_odds = calculate_parlay_odds(
    individual_probs=[0.40, 0.30],
    correlation=0.12
)

# Compare our fair value to sportsbook
comparison = compare_odds(our_fair_odds=+150, sportsbook_odds=+200)
```

---

## 2. Correlations

**Analyze player performance correlations for SGP.**

```python
from src.core.correlations import CorrelationAnalyzer
import pandas as pd

# Initialize analyzer
analyzer = CorrelationAnalyzer()

# Calculate specific correlation
qb_wr_result = analyzer.calculate_qb_wr_correlation(player_stats_df)
# Returns: {'correlation': 0.12, 'n': 5000}

# Calculate all correlations at once
all_corrs = analyzer.calculate_all(player_stats_df)
# Returns: {'QB_WR': 0.12, 'QB_TE': 0.092, 'RB_Team_TDs': 0.13, 'WR_WR': -0.016}

# Get specific correlation value
qb_wr_corr = analyzer.get_correlation('QB_WR')  # 0.12
```

**Required DataFrame columns:**
- `player_display_name`
- `position` (QB, WR, TE, RB)
- `recent_team`
- `week`
- `season`
- Stat columns: `passing_yards`, `receiving_yards`, `touchdowns`, etc.

---

## 3. Feature Engineering

**Create advanced features from raw player stats.**

```python
from src.core.feature_engineering import FeatureEngineer
import pandas as pd

# Initialize engineer
engineer = FeatureEngineer()

# Engineer advanced features
df_with_features = engineer.engineer_features(player_stats_df)

# Creates features like:
# - passing_yards_roll3_mean (3-game rolling average)
# - passing_yards_roll5_max (5-game peak)
# - passing_yards_trend (improving/declining)
# - passing_yards_consistency (variance-based)
# - games_played, rest_indicator, etc.

# Create prop bet targets
df_with_targets = engineer.create_prop_targets(df_with_features)
# Creates: passing_250+, rushing_100+, receiving_75+, anytime_td, etc.

# Get list of feature columns
feature_cols = engineer.get_feature_columns(df_with_features, exclude_targets=True)
```

**Required DataFrame columns:**
- `player_display_name`
- `season`
- `week`
- Stat columns: `passing_yards`, `rushing_yards`, `receiving_yards`, etc.

---

## 4. Model Trainer

**Train ML models for prop predictions.**

```python
from src.core.model_trainer import ModelTrainer
import pandas as pd

# Initialize trainer (optionally specify models directory)
trainer = ModelTrainer(models_dir='/path/to/models')

# Train model for single prop type
model_data = trainer.train_prop_model(
    df=training_data,
    prop_type='passing_250+',
    feature_cols=feature_column_list
)

# Returns dict with:
# - 'models': all trained models
# - 'best_model': highest AUC model
# - 'scaler': StandardScaler for features
# - 'feature_cols': list of features used
# - 'results': performance metrics

# Train models for all prop types
all_models = trainer.train_all_props(df=training_data, feature_cols=feature_cols)

# Save models to disk
trainer.save_models(all_models, correlations=correlation_dict)
```

**Prop types supported:**
- `passing_250+`, `passing_300+`
- `rushing_80+`, `rushing_100+`
- `receiving_75+`, `receiving_100+`
- `anytime_td`, `receptions_5+`

---

## 5. Model Predictor

**Load trained models and make predictions.**

```python
from src.core.model_predictor import Predictor
import pandas as pd

# Initialize predictor
predictor = Predictor(models_dir='/path/to/models')

# Load latest models
success = predictor.load_latest_models()

# Predict for single player
player_predictions = predictor.predict_single_player(player_features)
# Returns: {'passing_250+': {'probability': 0.42, 'missing_features': False}, ...}

# Predict for entire dataframe
all_predictions = predictor.predict_dataframe(players_df)
# Returns: {
#   'Patrick Mahomes': {
#     'position': 'QB',
#     'team': 'KC',
#     'predictions': {...}
#   },
#   ...
# }
```

---

## 6. Parlay Builder

**Build SGP parlays with correlation adjustments.**

```python
from src.core.parlay_builder import ParlayBuilder

# Initialize builder (optionally provide correlations)
builder = ParlayBuilder(correlations={'QB_WR': 0.12, 'QB_TE': 0.092})

# Build QB-WR stack
parlay = builder.build_qb_wr_stack(qb_prob=0.40, wr_prob=0.30)
# Returns: {
#   'type': '2-leg QB-WR Stack',
#   'individual_probs': [0.40, 0.30],
#   'correlation': 0.12,
#   'combined_probability': 0.134,
#   'fair_odds': '+644'
# }

# Build custom multi-leg parlay
parlay = builder.build_custom_parlay(
    leg_probs=[0.40, 0.30, 0.25],
    correlation=0.08
)

# Build parlays from predictions
parlays = builder.build_from_predictions(
    all_predictions=predictor_results,
    max_legs=3
)
# Returns list of top 50 parlay combinations
```

---

## 7. EV Calculator

**Calculate Expected Value for bets.**

```python
from src.core.ev_calculator import EVCalculator

# Initialize calculator
ev_calc = EVCalculator()

# Calculate EV for single bet
result = ev_calc.calculate_bet_ev(our_probability=0.40, sportsbook_odds=200)
# Returns: {
#   'our_probability': 0.40,
#   'sportsbook_odds': 200,
#   'sportsbook_implied_prob': 0.333,
#   'ev_percent': 20.0,
#   'is_plus_ev': True,
#   'rating': 'STRONG BET'
# }

# Compare multiple sportsbooks
results = ev_calc.compare_multiple_books(
    our_probability=0.40,
    sportsbook_odds_dict={
        'DraftKings': 200,
        'FanDuel': 175,
        'BetMGM': 225
    }
)
# Returns sorted list with best EV first

# Calculate Kelly Criterion sizing
kelly = ev_calc.kelly_criterion(
    our_probability=0.40,
    sportsbook_odds=200,
    kelly_fraction=0.25  # Quarter Kelly
)
# Returns: {
#   'full_kelly_percent': 16.67,
#   'recommended_percent': 4.17,
#   'kelly_fraction_used': 0.25
# }
```

---

## Complete Workflow Example

```python
# 1. Load and engineer features
from src.core.feature_engineering import FeatureEngineer
import pandas as pd

engineer = FeatureEngineer()
raw_data = pd.read_csv('player_stats.csv')
data_with_features = engineer.engineer_features(raw_data)
data_with_targets = engineer.create_prop_targets(data_with_features)
feature_cols = engineer.get_feature_columns(data_with_targets)

# 2. Calculate correlations
from src.core.correlations import CorrelationAnalyzer

analyzer = CorrelationAnalyzer()
correlations = analyzer.calculate_all(data_with_targets)

# 3. Train models
from src.core.model_trainer import ModelTrainer

trainer = ModelTrainer()
models = trainer.train_all_props(data_with_targets, feature_cols)
trainer.save_models(models, correlations)

# 4. Make predictions
from src.core.model_predictor import Predictor

predictor = Predictor()
predictor.load_latest_models()
predictions = predictor.predict_dataframe(this_week_players)

# 5. Build parlays
from src.core.parlay_builder import ParlayBuilder

builder = ParlayBuilder(correlations=correlations)
parlays = builder.build_from_predictions(predictions)

# 6. Calculate EV
from src.core.ev_calculator import EVCalculator

ev_calc = EVCalculator()
for parlay in parlays[:10]:  # Top 10 parlays
    ev_result = ev_calc.calculate_bet_ev(
        our_probability=parlay['combined_probability'],
        sportsbook_odds=+650  # Example sportsbook odds
    )
    print(f"{ev_result['rating']}: {ev_result['ev_percent']:.1f}% EV")
```

---

## Virtual Environment

Always activate the kre8vid_venv before using these modules:

```bash
cd /Users/kcdacre8tor/GSBPD2/backend
source kre8vid_venv/bin/activate
python your_script.py
```

---

## Testing

Run the test suite to verify all modules:

```bash
cd /Users/kcdacre8tor/GSBPD2/backend
source kre8vid_venv/bin/activate
python test_core_modules.py
```

Expected output: `🎉 ALL TESTS PASSED! Core module migration successful!`
