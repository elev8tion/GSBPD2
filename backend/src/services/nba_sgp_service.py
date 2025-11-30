"""
NBA Same Game Parlay (SGP) Service
Integrates core modules for NBA SGP prediction and analysis
"""

from pathlib import Path
from typing import List, Dict, Optional
import sqlite3
import pandas as pd
import json

from src.core.odds_calculator import calculate_ev, calculate_parlay_odds, compare_odds
from src.core.correlations import CorrelationAnalyzer
from src.core.feature_engineering import FeatureEngineer
from src.core.model_trainer import ModelTrainer
from src.core.model_predictor import Predictor
from src.core.parlay_builder import ParlayBuilder
from src.core.ev_calculator import EVCalculator

# NBA-specific modules
from src.services.nba_data_downloader import DataDownloader
from src.services.nba_pace_calculator import PaceCalculator
from src.services.nba_uncertainty import UncertaintyQuantifier


class NBASGPService:
    """NBA SGP prediction and analysis service"""

    # NBA prop types
    PROP_TYPES = [
        'points_25+', 'points_30+',
        'rebounds_10+', 'rebounds_12+',
        'assists_8+', 'assists_10+',
        'threes_3+', 'threes_4+',
        'pra_35+', 'pra_40+',
        'double_double', 'triple_double'
    ]

    def __init__(self, base_dir: Optional[Path] = None):
        if base_dir is None:
            base_dir = Path(__file__).parent.parent.parent

        self.base_dir = Path(base_dir)
        self.data_dir = self.base_dir / 'data'
        self.models_dir = self.base_dir / 'models' / 'nba'

        # Create directories if they don't exist
        self.models_dir.mkdir(parents=True, exist_ok=True)

        # Database paths
        self.player_stats_db = self.data_dir / 'nba_player_stats.db'
        self.sgp_combos_db = self.data_dir / 'nba_sgp_combos.db'

        # Initialize core components (reuse from backend)
        self.correlation_analyzer = CorrelationAnalyzer()
        self.feature_engineer = FeatureEngineer()
        self.parlay_builder = ParlayBuilder()
        self.ev_calculator = EVCalculator()

        # NBA-specific components
        self.data_downloader = DataDownloader(data_dir=str(self.data_dir))
        self.pace_calculator = PaceCalculator()
        self.uncertainty_quantifier = UncertaintyQuantifier()

        # Predictor will be initialized when models are available
        self.predictor = None
        if self.models_dir.exists():
            try:
                self.predictor = Predictor(models_dir=str(self.models_dir))
            except Exception as e:
                print(f"⚠️  Could not initialize predictor: {e}")

        # Load correlations if available
        self.loaded_correlations = {}
        self._load_correlations()

    def _load_correlations(self):
        """Load pre-calculated NBA correlations from models directory"""
        correlations_file = self.models_dir / 'correlations.json'

        if correlations_file.exists():
            try:
                with open(correlations_file, 'r') as f:
                    self.loaded_correlations = json.load(f)
                print(f"✅ Loaded NBA correlations: {self.loaded_correlations}")
            except Exception as e:
                print(f"⚠️  Could not load correlations: {e}")
                self._set_default_correlations()
        else:
            self._set_default_correlations()

    def _set_default_correlations(self):
        """Set default NBA correlation values"""
        self.loaded_correlations = {
            'Star_Team_Points': 0.25,       # Star player points ↔ team total
            'Guard_Team_Assists': 0.18,     # Guard assists ↔ team movement
            'Center_Team_Rebounds': 0.22,   # Center rebounds ↔ team rebounds
            'Teammate_Points': -0.08,        # Negative (competing for shots)
            'Home_Performance': 0.12         # Home court advantage
        }
        print(f"✅ Using default NBA correlations: {self.loaded_correlations}")

    def download_season_data(self, season: str = '2023-24', force: bool = False) -> Dict:
        """
        Download NBA data for a season

        Args:
            season: NBA season (e.g., '2023-24')
            force: Force re-download even if data exists

        Returns:
            Dict with download status
        """
        print(f"\n🏀 Downloading NBA data for {season}")

        try:
            player_df, sgp_df = self.data_downloader.download_all(season)

            return {
                "status": "success",
                "season": season,
                "player_games": len(player_df) if player_df is not None else 0,
                "sgp_combos": len(sgp_df) if sgp_df is not None else 0
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def train_models(self, season: str = '2023-24') -> Dict:
        """
        Train NBA SGP models

        Args:
            season: Season to train on

        Returns:
            Dict with training results
        """
        print(f"\n🎯 Training NBA SGP models for {season}")

        if not self.player_stats_db.exists():
            return {
                "status": "error",
                "message": f"Player stats database not found: {self.player_stats_db}. Please download data first."
            }

        try:
            # Load data
            conn = sqlite3.connect(self.player_stats_db)
            df = pd.read_sql_query("SELECT * FROM NBA_Player_Data", conn)
            conn.close()

            # Engineer features
            print("  Engineering features...")
            df = self.feature_engineer.engineer_features(df)

            # Calculate correlations
            print("  Calculating correlations...")
            correlations = self.correlation_analyzer.calculate_all(df)

            # Get feature columns
            feature_cols = self.feature_engineer.get_feature_columns(df)

            # Train models
            print("  Training models...")
            trainer = ModelTrainer(models_dir=str(self.models_dir))
            trained_models = trainer.train_all_props(df, feature_cols)

            # Save models and correlations
            print("  Saving models...")
            trainer.save_models(trained_models, correlations)

            # Update loaded correlations
            self.loaded_correlations = correlations

            return {
                "status": "success",
                "models_trained": len(trained_models),
                "correlations_calculated": len(correlations),
                "prop_types": list(trained_models.keys())
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def predict_player_props(self, player_id: str, game_id: str) -> Dict:
        """
        Get prop predictions for a player in a specific game

        Args:
            player_id: NBA player ID
            game_id: Game ID

        Returns:
            Dict with predictions for all prop types
        """
        if not self.predictor:
            return {
                "status": "error",
                "message": "Models not trained. Please train models first."
            }

        try:
            # Load player game data
            conn = sqlite3.connect(self.player_stats_db)
            query = f"""
                SELECT * FROM NBA_Player_Data
                WHERE PLAYER_ID = '{player_id}'
                ORDER BY GAME_NUM DESC
                LIMIT 20
            """
            df = pd.read_sql_query(query, conn)
            conn.close()

            if df.empty:
                return {
                    "status": "error",
                    "message": f"No data found for player {player_id}"
                }

            # Engineer features
            df = self.feature_engineer.engineer_features(df)

            # Get predictions from models
            predictions = {}
            for prop_type in self.PROP_TYPES:
                try:
                    prob = self.predictor.predict_single(df.iloc[-1:], prop_type)
                    predictions[prop_type] = {
                        "probability": round(prob, 3),
                        "confidence": "pending"  # Add uncertainty quantification later
                    }
                except Exception as e:
                    print(f"⚠️  Could not predict {prop_type}: {e}")
                    predictions[prop_type] = {
                        "probability": None,
                        "error": str(e)
                    }

            return {
                "status": "success",
                "player_id": player_id,
                "game_id": game_id,
                "predictions": predictions
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def build_parlays(self, game_id: str, max_legs: int = 10, min_ev: float = 0.05) -> List[Dict]:
        """
        Build optimal NBA parlays for a game

        Args:
            game_id: Game ID
            max_legs: Max legs per parlay
            min_ev: Minimum expected value threshold

        Returns:
            List of parlay combinations
        """
        try:
            # Load game data and predictions
            # This would use parlay_builder to create optimal combinations
            # Based on correlations and EV thresholds

            parlays = []

            # Placeholder implementation
            # In production, this would:
            # 1. Get all player predictions for the game
            # 2. Use parlay_builder to create combinations
            # 3. Apply correlation adjustments
            # 4. Filter by minimum EV
            # 5. Return top parlays

            return parlays

        except Exception as e:
            print(f"❌ Error building parlays: {e}")
            return []

    def calculate_ev(self, our_probability: float, sportsbook_odds: int) -> Dict:
        """
        Calculate EV for an NBA prop bet

        Args:
            our_probability: Our win probability (0-1)
            sportsbook_odds: American odds

        Returns:
            EV calculation results
        """
        try:
            ev = calculate_ev(our_probability, sportsbook_odds)

            return {
                "our_probability": our_probability,
                "sportsbook_odds": sportsbook_odds,
                "expected_value": round(ev, 4),
                "rating": self._get_ev_rating(ev)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def _get_ev_rating(self, ev: float) -> str:
        """Get rating based on EV"""
        if ev > 0.10:
            return "🔥 STRONG BET"
        elif ev > 0.05:
            return "✅ GOOD BET"
        elif ev > 0:
            return "⚠️  SLIGHT EDGE"
        else:
            return "❌ NO VALUE"

    def get_correlations(self) -> Dict:
        """Get current NBA correlation coefficients"""
        return {
            "correlations": self.loaded_correlations,
            "description": "NBA-specific correlation coefficients for SGP fair odds"
        }
