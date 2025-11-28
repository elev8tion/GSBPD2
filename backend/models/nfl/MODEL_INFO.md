# NFL SGP Models - Metadata

## Training Date
2025-11-28 10:50:35

## Data Source
- Training data: 2023-2024 NFL seasons
- Total games: 10,745 player-games
- Unique players: 784
- Weeks: 1-18

## Model Files

| Prop Type | File | Size | Best Model | Accuracy | AUC |
|-----------|------|------|------------|----------|-----|
| Passing 250+ | sgp_passing_250+_20251128_105035.pkl | 6.02MB | RandomForest | 0.688 | 0.693 |
| Passing 300+ | sgp_passing_300+_20251128_105035.pkl | 5.02MB | RandomForest | 0.858 | 0.684 |
| Rushing 80+ | sgp_rushing_80+_20251128_105035.pkl | 7.24MB | RandomForest | 0.915 | 0.877 |
| Rushing 100+ | sgp_rushing_100+_20251128_105035.pkl | 5.95MB | RandomForest | 0.952 | 0.882 |
| Receiving 75+ | sgp_receiving_75+_20251128_105035.pkl | 11.25MB | RandomForest | 0.910 | 0.857 |
| Receiving 100+ | sgp_receiving_100+_20251128_105035.pkl | 8.32MB | RandomForest | 0.961 | 0.872 |
| Receptions 5+ | sgp_receptions_5+_20251128_105035.pkl | 14.56MB | RandomForest | 0.870 | 0.868 |
| Anytime TD | sgp_anytime_td_20251128_105035.pkl | 15.53MB | RandomForest | 0.784 | 0.769 |
| Correlations | correlations_20251128_105035.pkl | 0.31KB | N/A | N/A | N/A |

**Total Model Size:** 74.75MB

## Position Distribution (from training data)

| Position | Count | Percentage |
|----------|-------|------------|
| WR | 4,343 | 40.4% |
| RB | 2,688 | 25.0% |
| TE | 2,163 | 20.1% |
| QB | 1,327 | 12.3% |
| FB | 149 | 1.4% |
| Other | 75 | 0.7% |

## Correlations

From correlations.pkl (based on 2024 season data):

| Stack Type | Correlation | Sample Size | Interpretation |
|------------|-------------|-------------|----------------|
| QB-WR Stack | 0.120 | 8,424 games | Moderate positive - QB success helps WR |
| QB-TE Stack | 0.092 | 4,209 games | Weak positive - QB success helps TE |
| QB-RB Receiving | 0.084 | 3,966 games | Weak positive - passing game correlation |
| WR-WR Stack | -0.016 | 11,450 games | Weak negative - competing for targets |
| RB-Team TDs | 0.130 | 2,478 games | Moderate positive - RB TD correlates with team TDs |

### Stack Recommendations
- **Best Stack:** RB-Team TDs (0.130) - strongest correlation
- **QB-WR Stack:** (0.120) - good for same game parlays
- **Avoid:** WR-WR from same team (negative correlation)

## Usage

```python
from src.core.model_predictor import Predictor

predictor = Predictor(models_dir='/Users/kcdacre8tor/GSBPD2/backend/models/nfl')
predictor.load_latest_models()
predictions = predictor.predict_dataframe(player_df)
```

## Model Architecture

Each model file contains:
- 5 trained models (RandomForest, XGBoost, LightGBM, GradientBoosting, NeuralNetwork)
- StandardScaler for feature normalization
- 158 engineered features
- Evaluation metrics (accuracy, AUC, log loss)
- Best model selection based on AUC

**All models selected RandomForest as the best performer**, indicating:
- Strong handling of non-linear relationships
- Good performance on imbalanced datasets
- Robust to overfitting
- Effective feature importance ranking

## Feature Engineering

The models use 158 features including:
- Player historical stats (last 3 games, last 5 games, season averages)
- Rolling averages (passing, rushing, receiving stats)
- Opponent defensive rankings
- Home/away indicators
- Weather conditions
- Days rest
- Divisional game indicators
- Prime time game indicators

## Training Configuration

- Train/test split: 80/20
- Stratified sampling by target variable
- Cross-validation: Time series split (respects temporal order)
- No data leakage: future data excluded from training
- Hyperparameters: Optimized via grid search for each model type

## Model Performance Summary

### High Performers (AUC > 0.85)
- Rushing 100+: 0.882 AUC, 95.2% accuracy
- Rushing 80+: 0.877 AUC, 91.5% accuracy
- Receiving 100+: 0.872 AUC, 96.1% accuracy
- Receptions 5+: 0.868 AUC, 87.0% accuracy
- Receiving 75+: 0.857 AUC, 91.0% accuracy

### Moderate Performers (AUC 0.75-0.85)
- Anytime TD: 0.769 AUC, 78.4% accuracy

### Lower Performers (AUC < 0.75)
- Passing 250+: 0.693 AUC, 68.8% accuracy
- Passing 300+: 0.684 AUC, 85.8% accuracy

**Note:** Passing yards are harder to predict due to higher variance and more external factors (game script, weather, defense strategy).

## Deployment Notes

1. Models are pre-trained and ready for inference
2. Ensure lightgbm, xgboost, and scikit-learn are installed
3. Models expect feature columns in exact order (saved in `feature_cols`)
4. Use StandardScaler from model file for consistent normalization
5. All models trained on 2023-2024 season data (current as of Nov 28, 2025)

## Next Steps

- Re-train models weekly as new game data becomes available
- Monitor model drift using AUC metrics on new predictions
- Consider ensemble methods combining multiple prop types
- Integrate with live odds API for value betting opportunities
