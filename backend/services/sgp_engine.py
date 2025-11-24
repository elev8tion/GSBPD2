import itertools
from typing import List, Dict

class SGPEngine:
    def __init__(self):
        # Correlation matrix (Mocked for now)
        # Positive correlation: If A happens, B is more likely
        self.correlations = {
            "favorite_cover": ["qb_passing_yards_over", "wr_receiving_yards_over"],
            "underdog_cover": ["rb_rushing_yards_over", "game_total_under"],
            "total_over": ["qb_passing_yards_over", "both_teams_score_20"],
            "total_under": ["defense_sacks_over", "rb_rushing_attempts_over"]
        }

    def calculate_parlay_odds(self, legs: List[Dict]) -> float:
        """
        Calculates the combined odds for a parlay.
        Simple multiplication of decimal odds for uncorrelated events.
        For SGP, real books use complex correlation models. 
        We will apply a 'correlation penalty' to simulate realistic pricing.
        """
        combined_odds = 1.0
        for leg in legs:
            combined_odds *= leg['odds']
        
        # Apply a correlation adjustment (reduction in payout for correlated events)
        # E.g., Chiefs Win + Mahomes 2+ TDs is correlated, so payout is less than pure multiplication
        correlation_penalty = 0.9 ** (len(legs) - 1)
        
        return round(combined_odds * correlation_penalty, 2)

    def generate_combinations(self, game_data: Dict, prediction: Dict) -> List[Dict]:
        """
        Generates valid SGP combinations based on the AI's prediction.
        """
        suggestions = []
        
        # Base leg: The AI's main prediction
        base_leg = {
            "type": "Spread",
            "selection": game_data['home_team'] if prediction['predicted_spread_margin'] > 0 else game_data['away_team'],
            "odds": 1.91
        }
        
        # Determine context
        context = "favorite_cover" if prediction['predicted_spread_margin'] > game_data.get('spread', 0) else "underdog_cover"
        
        # Find correlated props
        correlated_props = self.correlations.get(context, [])
        
        # Generate 2-leg and 3-leg parlays
        for prop in correlated_props:
            # 2-Leg SGP
            leg2 = self._create_mock_prop(prop, game_data)
            suggestions.append({
                "name": f"Smart SGP: {base_leg['selection']} + {leg2['name']}",
                "legs": [base_leg, leg2],
                "total_odds": self.calculate_parlay_odds([base_leg, leg2]),
                "reasoning": f"Since we predict {base_leg['selection']} to cover, {leg2['name']} is highly correlated."
            })
            
            # 3-Leg SGP (Try to find another prop)
            if len(correlated_props) > 1:
                other_prop = [p for p in correlated_props if p != prop][0]
                leg3 = self._create_mock_prop(other_prop, game_data)
                suggestions.append({
                    "name": f"Mega SGP: {base_leg['selection']} + {leg2['name']} + {leg3['name']}",
                    "legs": [base_leg, leg2, leg3],
                    "total_odds": self.calculate_parlay_odds([base_leg, leg2, leg3]),
                    "reasoning": "High risk, high reward combination based on game script analysis."
                })
                
        return suggestions[:3] # Return top 3 suggestions

    def _create_mock_prop(self, prop_type: str, game_data: Dict) -> Dict:
        """
        Helper to create mock prop bets.
        """
        if prop_type == "qb_passing_yards_over":
            return {"type": "Player Prop", "name": "QB 250+ Pass Yds", "odds": 1.85}
        elif prop_type == "wr_receiving_yards_over":
            return {"type": "Player Prop", "name": "WR1 80+ Rec Yds", "odds": 1.95}
        elif prop_type == "rb_rushing_yards_over":
            return {"type": "Player Prop", "name": "RB 75+ Rush Yds", "odds": 1.90}
        elif prop_type == "game_total_under":
            return {"type": "Total", "name": "Under 45.5 Pts", "odds": 1.91}
        elif prop_type == "both_teams_score_20":
            return {"type": "Game Prop", "name": "Both Teams 20+ Pts", "odds": 2.10}
        else:
            return {"type": "Prop", "name": "Generic Prop", "odds": 1.91}
