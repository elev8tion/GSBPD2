"""
Core sports betting analytics modules
Migrated from GSBPD2_NFL system
"""

from src.core.odds_calculator import (
    american_to_decimal,
    decimal_to_american,
    calculate_ev,
    calculate_parlay_odds,
    compare_odds
)

from src.core.correlations import CorrelationAnalyzer

from src.core.feature_engineering import FeatureEngineer

from src.core.model_trainer import ModelTrainer

from src.core.model_predictor import Predictor

from src.core.parlay_builder import ParlayBuilder

from src.core.ev_calculator import EVCalculator

__all__ = [
    'american_to_decimal',
    'decimal_to_american',
    'calculate_ev',
    'calculate_parlay_odds',
    'compare_odds',
    'CorrelationAnalyzer',
    'FeatureEngineer',
    'ModelTrainer',
    'Predictor',
    'ParlayBuilder',
    'EVCalculator'
]
