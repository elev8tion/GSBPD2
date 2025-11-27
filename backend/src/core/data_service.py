import pandas as pd
import random

class DataService:
    def get_mock_training_data(self):
        # Generate synthetic data for training
        data = {
            'team_strength': [random.randint(70, 99) for _ in range(100)],
            'opponent_strength': [random.randint(70, 99) for _ in range(100)],
            'home_advantage': [random.choice([0, 1]) for _ in range(100)],
        }
        
        # Create a target variable with some logic so the model learns something
        # Spread margin = (Team Strength - Opponent Strength) + (Home Advantage * 3) + Noise
        spread_margin = []
        for i in range(100):
            margin = (data['team_strength'][i] - data['opponent_strength'][i]) + (data['home_advantage'][i] * 3) + random.uniform(-5, 5)
            spread_margin.append(margin)
            
        data['spread_margin'] = spread_margin
        return pd.DataFrame(data)
