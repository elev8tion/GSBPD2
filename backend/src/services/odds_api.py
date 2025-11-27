import requests
import os
import random
from datetime import datetime, timedelta

class OddsAPIService:
    def __init__(self):
        self.api_key = os.getenv("ODDS_API_KEY")
        self.base_url = "https://api.the-odds-api.com/v4/sports"

    def get_upcoming_nfl_games(self):
        if not self.api_key:
            return self._get_mock_games()

        try:
            response = requests.get(
                f"{self.base_url}/americanfootball_nfl/odds",
                params={
                    "apiKey": self.api_key,
                    "regions": "us",
                    "markets": "h2h,spreads",
                    "oddsFormat": "american"
                }
            )
            response.raise_for_status()
            return self._process_api_response(response.json())
        except Exception as e:
            print(f"Error fetching data from Odds API: {e}")
            return self._get_mock_games()

    def _process_api_response(self, data):
        games = []
        for game in data:
            home_team = game['home_team']
            away_team = game['away_team']
            commence_time = datetime.fromisoformat(game['commence_time'].replace('Z', '+00:00'))
            
            # Simplified logic to extract spread if available
            spread = 0
            # (In a real app, we'd parse the bookmakers data deeply)
            
            games.append({
                "id": game['id'],
                "home_team": home_team,
                "away_team": away_team,
                "commence_time": commence_time.strftime("%Y-%m-%d %H:%M"),
                # Mocking strengths for now as API doesn't give team stats directly
                "home_strength": random.randint(75, 95),
                "away_strength": random.randint(75, 95)
            })
        return games[:5] # Return top 5

    def _get_mock_games(self):
        # Realistic mock data for demo
        today = datetime.now()
        return [
            {
                "id": "mock_1",
                "home_team": "Kansas City Chiefs",
                "away_team": "Buffalo Bills",
                "commence_time": (today + timedelta(days=1)).strftime("%Y-%m-%d 20:15"),
                "home_strength": 94,
                "away_strength": 91
            },
            {
                "id": "mock_2",
                "home_team": "Philadelphia Eagles",
                "away_team": "Dallas Cowboys",
                "commence_time": (today + timedelta(days=2)).strftime("%Y-%m-%d 16:25"),
                "home_strength": 89,
                "away_strength": 87
            },
            {
                "id": "mock_3",
                "home_team": "San Francisco 49ers",
                "away_team": "Baltimore Ravens",
                "commence_time": (today + timedelta(days=3)).strftime("%Y-%m-%d 20:15"),
                "home_strength": 92,
                "away_strength": 93
            }
        ]
