"""
SGP Parlay Builder
Builds multi-leg parlays with correlation adjustments
"""

from nba_sgp.core.odds import calculate_parlay_odds


class ParlayBuilder:
    """Build Same Game Parlays with correlation adjustments"""

    def __init__(self, correlations=None):
        """
        Initialize parlay builder

        Args:
            correlations (dict, optional): Correlation values
        """
        self.correlations = correlations or {
            'QB_WR': 0.12,
            'QB_TE': 0.092,
            'RB_Team_TDs': 0.13,
            'WR_WR': -0.016
        }

    def build_qb_wr_stack(self, qb_prob, wr_prob, correlation=None):
        """
        Build 2-leg QB-WR stack

        Args:
            qb_prob (float): QB passing probability
            wr_prob (float): WR receiving probability
            correlation (float, optional): Custom correlation

        Returns:
            dict: Parlay details
        """
        if correlation is None:
            correlation = self.correlations.get('QB_WR', 0.12)

        combined_prob, american_odds = calculate_parlay_odds([qb_prob, wr_prob], correlation)

        return {
            'type': '2-leg QB-WR Stack',
            'individual_probs': [qb_prob, wr_prob],
            'correlation': correlation,
            'combined_probability': combined_prob,
            'fair_odds': f"+{american_odds}" if american_odds > 0 else str(american_odds)
        }

    def build_custom_parlay(self, leg_probs, correlation=0.0):
        """
        Build custom multi-leg parlay

        Args:
            leg_probs (list): List of individual probabilities
            correlation (float): Average correlation to apply

        Returns:
            dict: Parlay details
        """
        combined_prob, american_odds = calculate_parlay_odds(leg_probs, correlation)

        return {
            'type': f'{len(leg_probs)}-leg Custom Parlay',
            'num_legs': len(leg_probs),
            'individual_probs': leg_probs,
            'correlation': correlation,
            'combined_probability': combined_prob,
            'fair_odds': f"+{american_odds}" if american_odds > 0 else str(american_odds)
        }

    def build_from_predictions(self, all_predictions, max_legs=3):
        """
        Build parlays from player predictions

        Args:
            all_predictions (dict): {player_name: {position, team, predictions}}
            max_legs (int): Maximum legs per parlay

        Returns:
            list: List of parlay combinations
        """
        parlays = []

        # Build QB-WR stacks
        for qb_name, qb_data in all_predictions.items():
            if qb_data['position'] != 'QB':
                continue

            qb_team = qb_data['team']
            qb_prob = qb_data['predictions'].get('passing_250+', {}).get('probability', 0)

            if qb_prob < 0.15:
                continue

            for wr_name, wr_data in all_predictions.items():
                if wr_data['position'] != 'WR' or wr_data['team'] != qb_team:
                    continue

                wr_prob = wr_data['predictions'].get('receiving_75+', {}).get('probability', 0)

                if wr_prob < 0.05:
                    continue

                parlay = self.build_qb_wr_stack(qb_prob, wr_prob)
                parlay['players'] = [qb_name, wr_name]
                parlay['legs'] = [
                    f"{qb_name} Passing 250+",
                    f"{wr_name} Receiving 75+"
                ]
                parlays.append(parlay)

        # Sort by probability
        parlays = sorted(parlays, key=lambda x: x['combined_probability'], reverse=True)

        return parlays[:50]  # Return top 50
