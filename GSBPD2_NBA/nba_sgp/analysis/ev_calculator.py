"""
Expected Value (EV) calculator
Depends only on core.odds module
"""

from nba_sgp.core.odds import calculate_ev, american_to_decimal, decimal_to_american


class EVCalculator:
    """Calculate Expected Value for bets"""

    def __init__(self):
        """Initialize EV calculator"""
        pass

    def calculate_bet_ev(self, our_probability, sportsbook_odds):
        """
        Calculate EV for a single bet

        Args:
            our_probability (float): Our calculated win probability (0.0 to 1.0)
            sportsbook_odds (int): Sportsbook's American odds

        Returns:
            dict: EV results with rating
        """
        ev_percent = calculate_ev(our_probability, sportsbook_odds)

        if ev_percent > 10:
            rating = "🔥 STRONG BET"
        elif ev_percent > 5:
            rating = "✅ GOOD BET"
        elif ev_percent > 0:
            rating = "⚠️ SLIGHT EDGE"
        else:
            rating = "❌ NO VALUE"

        return {
            'our_probability': our_probability,
            'sportsbook_odds': sportsbook_odds,
            'sportsbook_implied_prob': american_to_decimal(sportsbook_odds),
            'ev_percent': ev_percent,
            'is_plus_ev': ev_percent > 0,
            'rating': rating
        }

    def compare_multiple_books(self, our_probability, sportsbook_odds_dict):
        """
        Compare our probability against multiple sportsbooks

        Args:
            our_probability (float): Our calculated probability
            sportsbook_odds_dict (dict): {sportsbook_name: american_odds}

        Returns:
            list: List of EV results sorted by EV
        """
        results = []

        for book_name, odds in sportsbook_odds_dict.items():
            ev_result = self.calculate_bet_ev(our_probability, odds)
            ev_result['sportsbook'] = book_name
            results.append(ev_result)

        # Sort by EV (best first)
        results = sorted(results, key=lambda x: x['ev_percent'], reverse=True)

        return results

    def kelly_criterion(self, our_probability, sportsbook_odds, kelly_fraction=0.25):
        """
        Calculate Kelly Criterion bet sizing

        Args:
            our_probability (float): Our win probability
            sportsbook_odds (int): Sportsbook odds
            kelly_fraction (float): Fraction of Kelly to use (0.25 = quarter Kelly)

        Returns:
            dict: Kelly sizing recommendation
        """
        # Convert odds to decimal payout
        if sportsbook_odds > 0:
            decimal_odds = 1 + (sportsbook_odds / 100)
        else:
            decimal_odds = 1 + (100 / abs(sportsbook_odds))

        # Kelly formula: (bp - q) / b
        # b = decimal odds - 1
        # p = our probability
        # q = 1 - p
        b = decimal_odds - 1
        p = our_probability
        q = 1 - p

        kelly_percentage = (b * p - q) / b

        # Apply fraction
        recommended_percentage = kelly_percentage * kelly_fraction

        # Cap at reasonable maximum
        recommended_percentage = max(0, min(recommended_percentage, 0.05))  # Max 5% of bankroll

        return {
            'full_kelly_percent': kelly_percentage * 100,
            'recommended_percent': recommended_percentage * 100,
            'kelly_fraction_used': kelly_fraction,
            'warning': 'Full Kelly is aggressive - fractional Kelly recommended' if kelly_percentage > 0.05 else None
        }

    def find_arbitrage(self, sportsbook_odds_dict):
        """
        Check for arbitrage opportunities across sportsbooks

        Args:
            sportsbook_odds_dict (dict): {sportsbook_name: {outcome: odds}}

        Returns:
            dict: Arbitrage analysis
        """
        # Simple two-outcome arbitrage check
        # This is a simplified version - real arbitrage requires all outcomes

        if len(sportsbook_odds_dict) < 2:
            return {'is_arb': False, 'reason': 'Need at least 2 sportsbooks'}

        # Get implied probabilities
        implied_probs = {}
        for book, odds in sportsbook_odds_dict.items():
            implied_probs[book] = american_to_decimal(odds)

        # Find best odds for each outcome
        # (This is simplified - real implementation would handle all outcomes)

        return {'is_arb': False, 'reason': 'Not implemented for SGP'}
