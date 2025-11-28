"""
Model training module
Trains ensemble of ML models for prop predictions
"""

import pandas as pd
import numpy as np
import pickle
from datetime import datetime
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, StackingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, log_loss

try:
    from xgboost import XGBClassifier
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False

try:
    from lightgbm import LGBMClassifier
    HAS_LIGHTGBM = True
except ImportError:
    HAS_LIGHTGBM = False


class ModelTrainer:
    """Train ML models for prop predictions"""

    def __init__(self, models_dir=None):
        """
        Initialize trainer

        Args:
            models_dir (str, optional): Directory to save models
        """
        if models_dir is None:
            self.models_dir = Path.cwd() / 'models'
        else:
            self.models_dir = Path(models_dir)

        self.models_dir.mkdir(parents=True, exist_ok=True)

        self.prop_types = [
            'passing_250+', 'passing_300+',
            'rushing_80+', 'rushing_100+',
            'receiving_75+', 'receiving_100+',
            'anytime_td', 'receptions_5+'
        ]

    def train_prop_model(self, df, prop_type, feature_cols):
        """
        Train ensemble of models for a single prop type

        Args:
            df (pd.DataFrame): Training data with features and target
            prop_type (str): Prop to predict (e.g., 'passing_250+')
            feature_cols (list): List of feature column names

        Returns:
            dict: Trained models and metadata
        """
        print(f"\n{'='*80}")
        print(f"TRAINING: {prop_type}")
        print('='*80)

        # Prepare data
        X = df[feature_cols].fillna(0)
        y = df[prop_type]

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        print(f"  Training: {len(X_train):,} samples ({y_train.mean():.1%} hit rate)")
        print(f"  Testing: {len(X_test):,} samples ({y_test.mean():.1%} hit rate)")

        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Train multiple models
        models = {}
        results = {}

        # RandomForest
        print("\n  Training RandomForest...")
        rf = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, n_jobs=-1)
        rf.fit(X_train, y_train)
        models['RandomForest'] = rf
        results['RandomForest'] = self._evaluate_model(rf, X_test, y_test)

        # XGBoost (if available)
        if HAS_XGBOOST:
            print("  Training XGBoost...")
            xgb = XGBClassifier(n_estimators=200, max_depth=6, random_state=42)
            xgb.fit(X_train, y_train)
            models['XGBoost'] = xgb
            results['XGBoost'] = self._evaluate_model(xgb, X_test, y_test)

        # LightGBM (if available)
        if HAS_LIGHTGBM:
            print("  Training LightGBM...")
            lgbm = LGBMClassifier(n_estimators=200, max_depth=6, random_state=42, verbose=-1)
            lgbm.fit(X_train, y_train)
            models['LightGBM'] = lgbm
            results['LightGBM'] = self._evaluate_model(lgbm, X_test, y_test)

        # GradientBoosting
        print("  Training GradientBoosting...")
        gb = GradientBoostingClassifier(n_estimators=200, max_depth=5, random_state=42)
        gb.fit(X_train, y_train)
        models['GradientBoosting'] = gb
        results['GradientBoosting'] = self._evaluate_model(gb, X_test, y_test)

        # Neural Network
        print("  Training Neural Network...")
        nn = MLPClassifier(hidden_layers=(128, 64, 32), max_iter=500, random_state=42)
        nn.fit(X_train_scaled, y_train)
        models['NeuralNetwork'] = nn
        results['NeuralNetwork'] = self._evaluate_model(nn, X_test_scaled, y_test)

        # Find best model
        best_model_name = max(results, key=lambda k: results[k]['auc'])
        best_model = models[best_model_name]

        print(f"\n  Best Model: {best_model_name} (AUC: {results[best_model_name]['auc']:.3f})")

        return {
            'models': models,
            'best_model': best_model,
            'scaler': scaler,
            'feature_cols': feature_cols,
            'results': results,
            'prop_type': prop_type
        }

    def _evaluate_model(self, model, X_test, y_test):
        """Evaluate model performance"""
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        accuracy = accuracy_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_proba)
        logloss = log_loss(y_test, y_proba)

        print(f"    Accuracy: {accuracy:.3f} | AUC: {auc:.3f} | LogLoss: {logloss:.3f}")

        return {
            'accuracy': accuracy,
            'auc': auc,
            'log_loss': logloss
        }

    def train_all_props(self, df, feature_cols):
        """
        Train models for all prop types

        Args:
            df (pd.DataFrame): Training data
            feature_cols (list): Feature columns

        Returns:
            dict: All trained models
        """
        all_models = {}

        for prop_type in self.prop_types:
            if prop_type in df.columns:
                model_data = self.train_prop_model(df, prop_type, feature_cols)
                all_models[prop_type] = model_data

        return all_models

    def save_models(self, all_models, correlations=None):
        """
        Save all models to disk

        Args:
            all_models (dict): Trained models
            correlations (dict, optional): Correlation values
        """
        print("\n" + "="*80)
        print("SAVING MODELS TO DISK")
        print("="*80)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        for prop_type, model_data in all_models.items():
            filename = f"sgp_{prop_type}_{timestamp}.pkl"
            filepath = self.models_dir / filename

            with open(filepath, 'wb') as f:
                pickle.dump(model_data, f)

            print(f"  ✅ Saved {prop_type} → {filename}")

        # Save correlations
        if correlations:
            corr_file = self.models_dir / f"correlations_{timestamp}.pkl"
            with open(corr_file, 'wb') as f:
                pickle.dump(correlations, f)
            print(f"  ✅ Saved correlations → correlations_{timestamp}.pkl")

        print(f"\n  📁 All models saved in /{self.models_dir.name} directory")
