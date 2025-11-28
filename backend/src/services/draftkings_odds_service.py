"""
DraftKings Odds Service
Fetches and caches betting data from The Odds API (DraftKings only)
For NBA and NFL - Manual refresh only to conserve API credits
"""

import json
import os
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class DraftKingsOddsService:
    def __init__(self):
        base_dir = Path(__file__).parent.parent.parent  # backend/
        self.data_dir = base_dir / "odds_data"
        self.data_dir.mkdir(exist_ok=True)

        # Cache files
        self.nba_cache = self.data_dir / "nba_draftkings_odds.json"
        self.nfl_cache = self.data_dir / "nfl_draftkings_odds.json"
        self.history_file = self.data_dir / "odds_history.json"

        self.api_key = os.getenv("ODDS_API_KEY")
        self.base_url = "https://api.the-odds-api.com/v4"

        # DraftKings only
        self.bookmaker = "draftkings"

        # All available markets
        self.markets = "h2h,spreads,totals"

    def fetch_nba_odds(self) -> Dict:
        """
        Manually fetch NBA odds from DraftKings via Odds API.
        Only call this when user clicks refresh button.
        """
        try:
            url = f"{self.base_url}/sports/basketball_nba/odds/"
            params = {
                "apiKey": self.api_key,
                "regions": "us",
                "markets": self.markets,
                "bookmakers": self.bookmaker,
                "oddsFormat": "decimal"
            }

            print(f"🔄 Fetching NBA odds from DraftKings via Odds API...")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            games = response.json()

            # Extract DraftKings data
            processed_games = self._process_games(games, "NBA")

            # Save to cache
            cache_data = {
                "sport": "NBA",
                "fetched_at": datetime.now().isoformat(),
                "games_count": len(processed_games),
                "games": processed_games
            }

            with open(self.nba_cache, 'w') as f:
                json.dump(cache_data, f, indent=2)

            # Save to historical tracking
            self._save_to_history(processed_games, "NBA")

            print(f"✅ Cached {len(processed_games)} NBA games from DraftKings")

            return {
                "status": "success",
                "sport": "NBA",
                "games_count": len(processed_games),
                "fetched_at": cache_data["fetched_at"],
                "games": processed_games
            }

        except requests.RequestException as e:
            print(f"❌ Failed to fetch NBA odds: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to fetch NBA odds: {str(e)}"
            }

    def fetch_nfl_odds(self) -> Dict:
        """
        Manually fetch NFL odds from DraftKings via Odds API.
        Only call this when user clicks refresh button.
        """
        try:
            url = f"{self.base_url}/sports/americanfootball_nfl/odds/"
            params = {
                "apiKey": self.api_key,
                "regions": "us",
                "markets": self.markets,
                "bookmakers": self.bookmaker,
                "oddsFormat": "decimal"
            }

            print(f"🔄 Fetching NFL odds from DraftKings via Odds API...")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            games = response.json()

            # Extract DraftKings data
            processed_games = self._process_games(games, "NFL")

            # Save to cache
            cache_data = {
                "sport": "NFL",
                "fetched_at": datetime.now().isoformat(),
                "games_count": len(processed_games),
                "games": processed_games
            }

            with open(self.nfl_cache, 'w') as f:
                json.dump(cache_data, f, indent=2)

            # Save to historical tracking
            self._save_to_history(processed_games, "NFL")

            print(f"✅ Cached {len(processed_games)} NFL games from DraftKings")

            return {
                "status": "success",
                "sport": "NFL",
                "games_count": len(processed_games),
                "fetched_at": cache_data["fetched_at"],
                "games": processed_games
            }

        except requests.RequestException as e:
            print(f"❌ Failed to fetch NFL odds: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to fetch NFL odds: {str(e)}"
            }

    def _process_games(self, games: List[Dict], sport: str) -> List[Dict]:
        """
        Extract all DraftKings data from API response.
        """
        processed = []

        for game in games:
            # Find DraftKings bookmaker
            dk_data = None
            for bookmaker in game.get("bookmakers", []):
                if bookmaker.get("key") == "draftkings":
                    dk_data = bookmaker
                    break

            if not dk_data:
                continue  # Skip if no DraftKings data

            # Extract all markets
            markets_data = {}
            for market in dk_data.get("markets", []):
                market_key = market["key"]
                outcomes = market.get("outcomes", [])

                if market_key == "h2h":
                    # Moneyline
                    markets_data["moneyline"] = {
                        "home": next((o["price"] for o in outcomes if o["name"] == game["home_team"]), None),
                        "away": next((o["price"] for o in outcomes if o["name"] == game["away_team"]), None),
                        "last_update": market.get("last_update")
                    }

                elif market_key == "spreads":
                    # Point spreads
                    home_spread = next((o for o in outcomes if o["name"] == game["home_team"]), None)
                    away_spread = next((o for o in outcomes if o["name"] == game["away_team"]), None)

                    markets_data["spreads"] = {
                        "home": {
                            "point": home_spread.get("point") if home_spread else None,
                            "price": home_spread.get("price") if home_spread else None
                        },
                        "away": {
                            "point": away_spread.get("point") if away_spread else None,
                            "price": away_spread.get("price") if away_spread else None
                        },
                        "last_update": market.get("last_update")
                    }

                elif market_key == "totals":
                    # Over/Under
                    over = next((o for o in outcomes if o["name"] == "Over"), None)
                    under = next((o for o in outcomes if o["name"] == "Under"), None)

                    markets_data["totals"] = {
                        "over": {
                            "point": over.get("point") if over else None,
                            "price": over.get("price") if over else None
                        },
                        "under": {
                            "point": under.get("point") if under else None,
                            "price": under.get("price") if under else None
                        },
                        "last_update": market.get("last_update")
                    }

            processed.append({
                "game_id": game["id"],
                "sport": sport,
                "home_team": game["home_team"],
                "away_team": game["away_team"],
                "commence_time": game["commence_time"],
                "bookmaker": "DraftKings",
                "bookmaker_last_update": dk_data.get("last_update"),
                "markets": markets_data
            })

        return processed

    def _save_to_history(self, games: List[Dict], sport: str):
        """
        Save odds snapshot to historical tracking.
        Keeps a timeline of how odds moved over time.
        """
        # Load existing history
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                history = json.load(f)
        else:
            history = []

        # Add new snapshot
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "sport": sport,
            "games": games
        }

        history.append(snapshot)

        # Keep last 100 snapshots per sport to avoid huge files
        sport_snapshots = [h for h in history if h["sport"] == sport]
        if len(sport_snapshots) > 100:
            # Remove oldest snapshots for this sport
            other_sport_snapshots = [h for h in history if h["sport"] != sport]
            history = other_sport_snapshots + sport_snapshots[-100:]

        # Save
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)

    def get_cached_nba_odds(self) -> Dict:
        """Get cached NBA odds (no API call)"""
        if not self.nba_cache.exists():
            return {
                "status": "empty",
                "message": "No cached NBA odds. Click 'Refresh NBA Odds' to fetch.",
                "games": []
            }

        with open(self.nba_cache, 'r') as f:
            data = json.load(f)

        return {
            "status": "success",
            "cached": True,
            **data
        }

    def get_cached_nfl_odds(self) -> Dict:
        """Get cached NFL odds (no API call)"""
        if not self.nfl_cache.exists():
            return {
                "status": "empty",
                "message": "No cached NFL odds. Click 'Refresh NFL Odds' to fetch.",
                "games": []
            }

        with open(self.nfl_cache, 'r') as f:
            data = json.load(f)

        return {
            "status": "success",
            "cached": True,
            **data
        }

    def get_odds_history(self, sport: Optional[str] = None, game_id: Optional[str] = None) -> Dict:
        """
        Get historical odds movements.

        Args:
            sport: Filter by sport (NBA/NFL)
            game_id: Filter by specific game
        """
        if not self.history_file.exists():
            return {
                "status": "empty",
                "message": "No historical odds data yet",
                "history": []
            }

        with open(self.history_file, 'r') as f:
            history = json.load(f)

        # Filter by sport
        if sport:
            history = [h for h in history if h["sport"] == sport]

        # Filter by game_id
        if game_id:
            filtered_history = []
            for snapshot in history:
                matching_games = [g for g in snapshot["games"] if g["game_id"] == game_id]
                if matching_games:
                    filtered_history.append({
                        "timestamp": snapshot["timestamp"],
                        "sport": snapshot["sport"],
                        "games": matching_games
                    })
            history = filtered_history

        return {
            "status": "success",
            "count": len(history),
            "history": history
        }
