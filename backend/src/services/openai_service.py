"""
OpenAI GPT-4o-mini service for betting insights and odds analysis.
Uses GPT-4o-mini for cost-effective, fast analysis of DraftKings odds data.
"""
import os
import json
from typing import Dict, List, Optional
from pathlib import Path
from openai import OpenAI


class OpenAIInsightsService:
    """Service for generating betting insights using OpenAI GPT-4o-mini."""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"

        # Reference to odds data
        base_dir = Path(__file__).parent.parent.parent
        self.odds_dir = base_dir / "odds_data"

    def analyze_game_odds(self, game_data: Dict) -> Dict:
        """
        Analyze a single game's odds and provide betting insights.

        Args:
            game_data: Game odds data from DraftKings

        Returns:
            Dict with analysis and insights
        """
        prompt = self._build_game_analysis_prompt(game_data)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert sports betting analyst. Analyze odds data and provide clear, concise insights about value, line movements, and betting opportunities. Focus on data-driven analysis only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )

            analysis = response.choices[0].message.content

            return {
                "game_id": game_data.get("id"),
                "sport": game_data.get("sport_key"),
                "matchup": f"{game_data.get('home_team')} vs {game_data.get('away_team')}",
                "analysis": analysis,
                "model_used": self.model,
                "tokens_used": {
                    "prompt": response.usage.prompt_tokens,
                    "completion": response.usage.completion_tokens,
                    "total": response.usage.total_tokens
                }
            }

        except Exception as e:
            return {
                "error": f"Failed to analyze game: {str(e)}",
                "game_id": game_data.get("id")
            }

    def analyze_multiple_games(self, sport: str = "nba") -> Dict:
        """
        Analyze all games for a sport and find best betting opportunities.

        Args:
            sport: "nba" or "nfl"

        Returns:
            Dict with overall analysis and top opportunities
        """
        # Load cached odds data
        cache_file = self.odds_dir / f"{sport}_draftkings_odds.json"

        if not cache_file.exists():
            return {"error": f"No cached {sport.upper()} odds data found. Please refresh odds first."}

        with open(cache_file, 'r') as f:
            data = json.load(f)
            games = data.get("games", [])

        if not games:
            return {"error": f"No games found in {sport.upper()} odds cache"}

        prompt = self._build_multi_game_analysis_prompt(games, sport)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert sports betting analyst. Analyze multiple games and identify the top 3-5 betting opportunities based on odds value, line analysis, and market inefficiencies. Be specific and data-driven."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )

            analysis = response.choices[0].message.content

            return {
                "sport": sport.upper(),
                "games_analyzed": len(games),
                "analysis": analysis,
                "model_used": self.model,
                "tokens_used": {
                    "prompt": response.usage.prompt_tokens,
                    "completion": response.usage.completion_tokens,
                    "total": response.usage.total_tokens
                }
            }

        except Exception as e:
            return {"error": f"Failed to analyze games: {str(e)}"}

    def compare_odds_movement(self, sport: str, game_id: str) -> Dict:
        """
        Analyze historical odds movement for a specific game.

        Args:
            sport: "nba" or "nfl"
            game_id: Game ID to analyze

        Returns:
            Dict with movement analysis
        """
        history_file = self.odds_dir / "odds_history.json"

        if not history_file.exists():
            return {"error": "No historical odds data found"}

        with open(history_file, 'r') as f:
            history = json.load(f)

        # Filter history for this sport and game
        sport_history = history.get(sport.lower(), [])
        game_snapshots = []

        for snapshot in sport_history:
            for game in snapshot.get("games", []):
                if game.get("id") == game_id:
                    game_snapshots.append({
                        "timestamp": snapshot.get("timestamp"),
                        "game": game
                    })

        if not game_snapshots:
            return {"error": f"No historical data found for game {game_id}"}

        prompt = self._build_movement_analysis_prompt(game_snapshots)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at analyzing betting line movements. Identify significant shifts in odds, explain what they might indicate (sharp money, public betting, injury news), and suggest if there's value in the current lines."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=600
            )

            analysis = response.choices[0].message.content

            return {
                "game_id": game_id,
                "sport": sport.upper(),
                "snapshots_analyzed": len(game_snapshots),
                "analysis": analysis,
                "model_used": self.model,
                "tokens_used": {
                    "prompt": response.usage.prompt_tokens,
                    "completion": response.usage.completion_tokens,
                    "total": response.usage.total_tokens
                }
            }

        except Exception as e:
            return {"error": f"Failed to analyze movement: {str(e)}"}

    def _build_game_analysis_prompt(self, game: Dict) -> str:
        """Build prompt for single game analysis."""
        home = game.get("home_team")
        away = game.get("away_team")
        commence = game.get("commence_time")

        moneyline = game.get("moneyline", {})
        spreads = game.get("spreads", {})
        totals = game.get("totals", {})

        prompt = f"""Analyze this {game.get('sport_key', 'game').upper()} matchup:

**{away} @ {home}**
Game Time: {commence}

**DraftKings Odds:**

Moneyline:
- {home}: {moneyline.get('home_price', 'N/A')}
- {away}: {moneyline.get('away_price', 'N/A')}

Spread:
- {home} {spreads.get('home_point', 'N/A')} at {spreads.get('home_price', 'N/A')}
- {away} {spreads.get('away_point', 'N/A')} at {spreads.get('away_price', 'N/A')}

Total: {totals.get('point', 'N/A')}
- Over: {totals.get('over_price', 'N/A')}
- Under: {totals.get('under_price', 'N/A')}

Provide:
1. Overall value assessment
2. Any notable odds patterns
3. Best betting angle (if any)
4. Key factors to watch

Keep it concise (3-4 sentences max)."""

        return prompt

    def _build_multi_game_analysis_prompt(self, games: List[Dict], sport: str) -> str:
        """Build prompt for analyzing multiple games."""
        games_summary = []

        for game in games[:15]:  # Limit to 15 games to stay within token limits
            home = game.get("home_team")
            away = game.get("away_team")
            ml = game.get("moneyline", {})
            spreads = game.get("spreads", {})
            totals = game.get("totals", {})

            summary = f"""
{away} @ {home}
- ML: {away} {ml.get('away_price')} | {home} {ml.get('home_price')}
- Spread: {away} {spreads.get('away_point')} ({spreads.get('away_price')}) | {home} {spreads.get('home_point')} ({spreads.get('home_price')})
- Total: {totals.get('point')} | O: {totals.get('over_price')} | U: {totals.get('under_price')}
"""
            games_summary.append(summary.strip())

        prompt = f"""Analyze these {sport.upper()} games from DraftKings and identify the TOP 3-5 betting opportunities:

{chr(10).join(games_summary)}

Provide:
1. Top 3-5 best betting opportunities with specific picks
2. Reasoning for each (value, line analysis, etc.)
3. Any notable market trends across games
4. Risk level for each opportunity (Low/Medium/High)

Format as a numbered list with clear, actionable recommendations."""

        return prompt

    def _build_movement_analysis_prompt(self, snapshots: List[Dict]) -> str:
        """Build prompt for odds movement analysis."""
        if not snapshots:
            return "No data available"

        latest = snapshots[-1]["game"]
        home = latest.get("home_team")
        away = latest.get("away_team")

        movement_data = []

        for snap in snapshots:
            timestamp = snap["timestamp"]
            game = snap["game"]
            ml = game.get("moneyline", {})
            spreads = game.get("spreads", {})
            totals = game.get("totals", {})

            movement_data.append(f"""
{timestamp}:
- ML: {away} {ml.get('away_price')} | {home} {ml.get('home_price')}
- Spread: {spreads.get('home_point')} | Total: {totals.get('point')}
""")

        prompt = f"""Analyze the odds movement for this game:

**{away} @ {home}**

Historical Odds Movement:
{chr(10).join(movement_data)}

Provide:
1. Significant line movements (moneyline, spread, total)
2. What the movement might indicate (sharp action, public betting, news)
3. Current value assessment based on movement
4. Recommended betting timing (now vs wait)

Be specific about which direction lines moved and why it matters."""

        return prompt
