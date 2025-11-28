"""
Configuration management for NBA SGP Engine
Auto-detects paths and creates necessary directories
"""

import os
from pathlib import Path


class Config:
    """
    Configuration manager for NBA SGP Engine
    Automatically sets up directories and paths
    """

    def __init__(self, base_dir=None):
        """
        Initialize configuration

        Args:
            base_dir (str, optional): Base directory for data/models.
                                     Defaults to current working directory.
        """
        # Set base directory
        if base_dir is None:
            self.base_dir = Path.cwd()
        else:
            self.base_dir = Path(base_dir)

        # Define subdirectories
        self.data_dir = self.base_dir / 'data'
        self.models_dir = self.base_dir / 'models'
        self.output_dir = self.base_dir / 'output'

        # Database paths
        self.db_player_stats = self.data_dir / 'NBA_Player_Stats_2024.db'
        self.db_sgp_combos = self.data_dir / 'NBA_SGP_Combos_2024.db'

        # API configuration (optional)
        self.api_key = os.getenv('NBA_SGP_API_KEY', None)

        # Model configuration
        self.model_types = [
            'RandomForest',
            'XGBoost',
            'LightGBM',
            'GradientBoosting',
            'NeuralNetwork',
            'Stacking'
        ]

        # NBA Prop types
        self.prop_types = [
            'points_25+',
            'points_30+',
            'rebounds_10+',
            'rebounds_12+',
            'assists_8+',
            'assists_10+',
            'threes_3+',
            'threes_4+',
            'pra_35+',
            'pra_40+',
            'double_double',
            'triple_double'
        ]

        # NBA-specific correlation defaults
        self.default_correlations = {
            'Star_Team_Points': 0.25,        # Star player points correlate with team total
            'Guard_Team_Assists': 0.18,     # Guard assists correlate with team ball movement
            'Center_Team_Rebounds': 0.22,   # Center rebounds correlate with team rebounding
            'Teammate_Points': -0.08,       # Teammates competing for shots (negative)
            'Home_Performance': 0.12        # Home court advantage correlation
        }

        # Create directories if they don't exist
        self._create_directories()

    def _create_directories(self):
        """Create necessary directories"""
        for directory in [self.data_dir, self.models_dir, self.output_dir]:
            directory.mkdir(parents=True, exist_ok=True)

    def get_model_path(self, prop_type, timestamp=None):
        """
        Get path for a model file

        Args:
            prop_type (str): Type of prop (e.g., 'points_25+')
            timestamp (str, optional): Timestamp string. If None, returns pattern for glob

        Returns:
            Path: Path to model file
        """
        if timestamp:
            return self.models_dir / f'nba_sgp_{prop_type}_{timestamp}.pkl'
        else:
            return self.models_dir / f'nba_sgp_{prop_type}_*.pkl'

    def get_correlation_path(self, timestamp=None):
        """
        Get path for correlations file

        Args:
            timestamp (str, optional): Timestamp string

        Returns:
            Path: Path to correlations file
        """
        if timestamp:
            return self.models_dir / f'correlations_{timestamp}.pkl'
        else:
            return self.models_dir / 'correlations_*.pkl'

    def to_dict(self):
        """Convert config to dictionary"""
        return {
            'base_dir': str(self.base_dir),
            'data_dir': str(self.data_dir),
            'models_dir': str(self.models_dir),
            'output_dir': str(self.output_dir),
            'has_api_key': self.api_key is not None
        }

    def __repr__(self):
        return f"Config(base_dir={self.base_dir})"
