"""
Prediction module - load models and make predictions
"""

import pandas as pd
import numpy as np
import pickle
import glob
from pathlib import Path


class Predictor:
    """Load trained models and make predictions"""

    def __init__(self, models_dir=None):
        """
        Initialize predictor

        Args:
            models_dir (str, optional): Directory with saved models
        """
        if models_dir is None:
            self.models_dir = Path.cwd() / 'models'
        else:
            self.models_dir = Path(models_dir)

        self.models = {}
        self.correlations = {}

    def load_latest_models(self):
        """Load the most recently trained models"""
        print("📦 Loading trained models...")

        model_files = list(self.models_dir.glob('sgp_*.pkl'))

        if not model_files:
            print("  ❌ No models found!")
            return False

        # Extract timestamps
        timestamps = []
        for f in model_files:
            parts = f.stem.split('_')
            if len(parts) >= 3:
                timestamp = f"{parts[-2]}_{parts[-1]}"
                timestamps.append(timestamp)

        latest_timestamp = max(timestamps) if timestamps else None

        if not latest_timestamp:
            print("  ❌ Could not parse model timestamps")
            return False

        print(f"  Loading models from: {latest_timestamp}")

        # Load each prop type
        prop_types = [
            'passing_250+', 'passing_300+',
            'rushing_80+', 'rushing_100+',
            'receiving_75+', 'receiving_100+',
            'anytime_td', 'receptions_5+'
        ]

        for prop in prop_types:
            model_path = self.models_dir / f'sgp_{prop}_{latest_timestamp}.pkl'

            if model_path.exists():
                with open(model_path, 'rb') as f:
                    self.models[prop] = pickle.load(f)
                print(f"  ✅ Loaded: {prop}")

        # Load correlations
        corr_path = self.models_dir / f'correlations_{latest_timestamp}.pkl'
        if corr_path.exists():
            with open(corr_path, 'rb') as f:
                self.correlations = pickle.load(f)
            print(f"  ✅ Loaded correlations")

        print(f"\n  Total models loaded: {len(self.models)}")
        return True

    def predict_single_player(self, player_features):
        """
        Make predictions for a single player

        Args:
            player_features (pd.Series or dict): Player features

        Returns:
            dict: Predictions for all prop types
        """
        if isinstance(player_features, dict):
            player_features = pd.Series(player_features)

        predictions = {}

        for prop_type, model_data in self.models.items():
            best_model = model_data['best_model']
            scaler = model_data['scaler']
            feature_cols = model_data['feature_cols']

            # Extract features
            available_features = [col for col in feature_cols if col in player_features.index]

            if len(available_features) < len(feature_cols) * 0.8:  # Need at least 80% of features
                predictions[prop_type] = {
                    'probability': 0.0,
                    'missing_features': True
                }
                continue

            # Prepare features
            X = player_features[available_features].values.reshape(1, -1)
            X_scaled = scaler.transform(X)

            # Predict
            prob = best_model.predict_proba(X_scaled)[0][1]

            predictions[prop_type] = {
                'probability': prob,
                'missing_features': False
            }

        return predictions

    def predict_dataframe(self, df):
        """
        Make predictions for entire dataframe of players

        Args:
            df (pd.DataFrame): Player features

        Returns:
            dict: {player_name: predictions}
        """
        all_predictions = {}

        for idx, row in df.iterrows():
            player_name = row.get('player_display_name', f'Player_{idx}')
            predictions = self.predict_single_player(row)

            all_predictions[player_name] = {
                'position': row.get('position'),
                'team': row.get('recent_team'),
                'predictions': predictions
            }

        return all_predictions
