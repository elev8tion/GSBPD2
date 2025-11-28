"""
Core utilities - standalone, no dependencies on other modules
"""

from nba_sgp.core.odds import (
    american_to_decimal,
    decimal_to_american,
    calculate_ev,
    calculate_parlay_odds
)
from nba_sgp.core.config import Config

__all__ = [
    'american_to_decimal',
    'decimal_to_american',
    'calculate_ev',
    'calculate_parlay_odds',
    'Config'
]
