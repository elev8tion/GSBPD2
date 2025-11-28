"""
Main SGPEngine class - unified interface to all NBA modules
"""

from nba_sgp.core.config import Config
from nba_sgp.data import DataDownloader, FeatureEngineer
from nba_sgp.analysis import CorrelationAnalyzer, EVCalculator
from nba_sgp.models import ModelTrainer, Predictor
from nba_sgp.parlays import ParlayBuilder


class SGPEngine:
    """
    Complete NBA SGP prediction engine
    Unified interface to all functionality
    """

    def __init__(self, base_dir=None):
        """
        Initialize NBA SGP Engine

        Args:
            base_dir (str, optional): Base directory for data/models
        """
        # Initialize config
        self.config = Config(base_dir)

        # Initialize modules
        self.downloader = DataDownloader(self.config.data_dir)
        self.feature_engineer = FeatureEngineer()
        self.correlation_analyzer = CorrelationAnalyzer()
        self.ev_calculator = EVCalculator()
        self.model_trainer = ModelTrainer(self.config.models_dir)
        self.parlay_builder = ParlayBuilder()

        # Data storage
        self.player_data = None
        self.correlations = None
        self.trained_models = None

    def download_data(self, season='2023-24'):
        """
        Download NBA data

        Args:
            season (str): NBA season (e.g., '2023-24')

        Returns:
            tuple: (player_df, sgp_df)
        """
        print("=" * 80)
        print("DOWNLOADING NBA DATA")
        print("=" * 80)

        player_df, sgp_df = self.downloader.download_all(season)
        self.player_data = player_df

        return player_df, sgp_df

    def train_models(self, df=None):
        """
        Train ML models

        Args:
            df (pd.DataFrame, optional): Data to train on. If None, loads from database.

        Returns:
            dict: Trained models
        """
        print("\n" + "=" * 80)
        print("TRAINING NBA MODELS")
        print("=" * 80)

        if df is None:
            import sqlite3
            import pandas as pd
            conn = sqlite3.connect(self.config.db_player_stats)
            df = pd.read_sql_query("SELECT * FROM NBA_Player_Data", conn)
            conn.close()

        # Engineer features
        print("\n1. Engineering features...")
        df = self.feature_engineer.engineer_features(df)
        df = self.feature_engineer.create_prop_targets(df)

        # Calculate correlations
        print("\n2. Calculating NBA correlations...")
        self.correlations = self.correlation_analyzer.calculate_all(df)

        # Get feature columns
        feature_cols = self.feature_engineer.get_feature_columns(df)

        # Train models
        print("\n3. Training models...")
        self.trained_models = self.model_trainer.train_all_props(df, feature_cols)

        # Save models
        self.model_trainer.save_models(self.trained_models, self.correlations)

        return self.trained_models

    def predict(self, df=None):
        """
        Make predictions

        Args:
            df (pd.DataFrame, optional): Data to predict on

        Returns:
            dict: Predictions for all players
        """
        print("\n" + "=" * 80)
        print("MAKING NBA PREDICTIONS")
        print("=" * 80)

        # Load models if not trained
        if not self.predictor.models:
            self.predictor.load_latest_models()

        if df is None:
            import sqlite3
            import pandas as pd
            conn = sqlite3.connect(self.config.db_player_stats)
            df = pd.read_sql_query(
                "SELECT * FROM NBA_Player_Data ORDER BY GAME_NUM DESC LIMIT 1000",
                conn
            )
            conn.close()

        # Engineer features
        df = self.feature_engineer.engineer_features(df)

        # Predict
        predictions = self.predictor.predict_dataframe(df)

        return predictions

    def build_parlays(self, predictions=None, max_legs=10):
        """
        Build NBA SGP parlays

        Args:
            predictions (dict, optional): Player predictions
            max_legs (int): Maximum legs per parlay

        Returns:
            list: List of parlay combinations
        """
        print("\n" + "=" * 80)
        print("BUILDING NBA PARLAYS")
        print("=" * 80)

        if predictions is None:
            predictions = self.predict()

        # Set correlations
        if self.correlations:
            self.parlay_builder.correlations = self.correlations

        # Build parlays
        parlays = self.parlay_builder.build_from_predictions(predictions, max_legs)

        print(f"\n✅ Generated {len(parlays)} NBA parlay combinations")

        return parlays

    def calculate_ev(self, our_probability, sportsbook_odds):
        """
        Calculate EV for a bet

        Args:
            our_probability (float): Our win probability
            sportsbook_odds (int): Sportsbook's American odds

        Returns:
            dict: EV results
        """
        return self.ev_calculator.calculate_bet_ev(our_probability, sportsbook_odds)

    def full_pipeline(self, season='2023-24'):
        """
        Run complete pipeline: download → train → predict → build parlays

        Args:
            season (str): NBA season to download

        Returns:
            dict: All results
        """
        print("=" * 80)
        print("NBA SGP ENGINE - FULL PIPELINE")
        print("=" * 80)

        # 1. Download
        player_df, sgp_df = self.download_data(season)

        # 2. Train
        trained_models = self.train_models(player_df)

        # 3. Predict
        predictions = self.predict()

        # 4. Build parlays
        parlays = self.build_parlays(predictions)

        return {
            'player_data': player_df,
            'sgp_data': sgp_df,
            'trained_models': trained_models,
            'predictions': predictions,
            'parlays': parlays
        }
