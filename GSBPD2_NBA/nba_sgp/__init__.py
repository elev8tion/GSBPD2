"""
NBA SGP Prediction Engine
A modular package for NBA Same Game Parlay analysis and predictions

Usage:
    # Full pipeline
    from nba_sgp import SGPEngine
    engine = SGPEngine()

    # Individual modules
    from nba_sgp.data import DataDownloader
    from nba_sgp.models import Predictor
    from nba_sgp.parlays import ParlayBuilder
"""

__version__ = "1.0.0"
__author__ = "NBA SGP Engine"

# Import main engine for convenience
from nba_sgp.engine import SGPEngine

__all__ = ['SGPEngine', '__version__']
