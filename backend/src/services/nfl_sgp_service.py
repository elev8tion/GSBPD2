"""
NFL Same Game Parlay (SGP) Service
Integrates core modules for SGP prediction and analysis
"""

from pathlib import Path
from typing import List, Dict, Optional
import sqlite3
import pandas as pd
import json

from src.core.odds_calculator import calculate_ev, calculate_parlay_odds, compare_odds
from src.core.correlations import CorrelationAnalyzer
from src.core.feature_engineering import FeatureEngineer
from src.core.model_trainer import ModelTrainer
from src.core.model_predictor import Predictor
from src.core.parlay_builder import ParlayBuilder
from src.core.ev_calculator import EVCalculator


class NFLSGPService:
    """NFL SGP prediction and analysis service"""

    def __init__(self, base_dir: Optional[Path] = None):
        if base_dir is None:
            base_dir = Path(__file__).parent.parent.parent

        self.base_dir = Path(base_dir)
        self.data_dir = self.base_dir / 'data'
        self.models_dir = self.base_dir / 'models' / 'nfl'

        # Database paths
        self.player_stats_db = self.data_dir / 'nfl_player_stats.db'
        self.sgp_combos_db = self.data_dir / 'nfl_sgp_combos.db'

        # Initialize core components
        self.correlation_analyzer = CorrelationAnalyzer()
        self.feature_engineer = FeatureEngineer()
        self.parlay_builder = ParlayBuilder()
        self.ev_calculator = EVCalculator()

        # Predictor will be initialized when models are available
        self.predictor = None
        if self.models_dir.exists():
            try:
                self.predictor = Predictor(models_dir=str(self.models_dir))
            except Exception as e:
                print(f"⚠️ Could not initialize predictor: {e}")

        # Load correlations if available
        self.loaded_correlations = {}
        self._load_correlations()

    def _load_correlations(self):
        """Load pre-calculated correlations from models directory"""
        correlations_file = self.models_dir / 'correlations.json'

        if correlations_file.exists():
            try:
                with open(correlations_file, 'r') as f:
                    self.loaded_correlations = json.load(f)
                print(f"✅ Loaded correlations: {self.loaded_correlations}")
            except Exception as e:
                print(f"⚠️ Could not load correlations: {e}")
                self._set_default_correlations()
        else:
            self._set_default_correlations()

    def _set_default_correlations(self):
        """Set default correlation values from research"""
        self.loaded_correlations = {
            'QB_WR': 0.12,
            'QB_TE': 0.092,
            'RB_Team_TDs': 0.13,
            'WR_WR': -0.016
        }
        print(f"✅ Using default correlations: {self.loaded_correlations}")

    def generate_weekly_picks(self, week: int, season: int = 2024) -> List[Dict]:
        """
        Generate SGP picks for a specific week

        Args:
            week (int): Week number
            season (int): Season year

        Returns:
            List[Dict]: List of SGP picks with probabilities and odds
        """
        print(f"\n🎯 Generating SGP picks for Week {week}, {season}")

        picks = []

        if not self.player_stats_db.exists():
            print(f"❌ Player stats database not found: {self.player_stats_db}")
            return picks

        try:
            # Load player data for the week
            conn = sqlite3.connect(self.player_stats_db)
            query = """
                SELECT * FROM NFL_Model_Data
                WHERE week = ? AND season = ?
                AND position IN ('QB', 'RB', 'WR', 'TE')
            """
            df = pd.read_sql_query(query, conn, params=[week, season])
            conn.close()

            if df.empty:
                print(f"⚠️ No data found for Week {week}, {season}")
                return picks

            print(f"  ✅ Loaded {len(df)} player records")

            # Generate QB-WR stacks
            qb_wr_picks = self._generate_qb_wr_stacks(df)
            picks.extend(qb_wr_picks)

            # Generate RB-Team TD combos
            rb_team_picks = self._generate_rb_team_combos(df)
            picks.extend(rb_team_picks)

            print(f"  ✅ Generated {len(picks)} total picks")

            return picks

        except Exception as e:
            print(f"❌ Error generating picks: {e}")
            return picks

    def _generate_qb_wr_stacks(self, df: pd.DataFrame) -> List[Dict]:
        """Generate QB-WR stack picks"""
        picks = []

        # Group by team to find same-game stacks
        for team, group in df.groupby('recent_team'):
            qbs = group[group['position'] == 'QB']
            wrs = group[group['position'] == 'WR']

            if len(qbs) == 0 or len(wrs) == 0:
                continue

            # Get primary QB
            qb = qbs.iloc[0]

            # Top 2 WRs by receiving yards (historical average)
            top_wrs = wrs.nlargest(2, 'receiving_yards')

            for _, wr in top_wrs.iterrows():
                # Estimate probabilities (simplified - would use ML models in production)
                qb_prob = 0.60  # 60% chance QB hits 250+ yards
                wr_prob = 0.55  # 55% chance WR hits 75+ yards

                # Build parlay with correlation
                parlay = self.parlay_builder.build_qb_wr_stack(
                    qb_prob,
                    wr_prob,
                    correlation=self.loaded_correlations.get('QB_WR', 0.12)
                )

                pick = {
                    'type': 'QB-WR Stack',
                    'team': team,
                    'qb': qb['player_display_name'],
                    'qb_prop': 'Pass Yards 250+',
                    'wr': wr['player_display_name'],
                    'wr_prop': 'Rec Yards 75+',
                    'combined_probability': parlay['combined_probability'],
                    'fair_odds': parlay['fair_odds'],
                    'correlation': parlay['correlation']
                }
                picks.append(pick)

        return picks

    def _generate_rb_team_combos(self, df: pd.DataFrame) -> List[Dict]:
        """Generate RB-Team TD combination picks"""
        picks = []

        for team, group in df.groupby('recent_team'):
            rbs = group[group['position'] == 'RB']

            if len(rbs) == 0:
                continue

            # Get primary RB
            rb = rbs.iloc[0]

            # Estimate probabilities
            rb_prob = 0.50  # 50% chance RB scores TD
            team_prob = 0.65  # 65% chance team scores 2+ TDs

            # Build parlay
            combined_prob, american_odds = calculate_parlay_odds(
                [rb_prob, team_prob],
                correlation=self.loaded_correlations.get('RB_Team_TDs', 0.13)
            )

            pick = {
                'type': 'RB-Team TDs',
                'team': team,
                'rb': rb['player_display_name'],
                'rb_prop': 'Anytime TD',
                'team_prop': 'Team 2+ TDs',
                'combined_probability': combined_prob,
                'fair_odds': f"+{american_odds}" if american_odds > 0 else str(american_odds),
                'correlation': self.loaded_correlations.get('RB_Team_TDs', 0.13)
            }
            picks.append(pick)

        return picks

    def calculate_ev_vs_draftkings(self, our_picks: List[Dict], dk_odds: Dict) -> List[Dict]:
        """
        Compare our fair value picks vs DraftKings odds

        Args:
            our_picks (List[Dict]): Our generated picks with probabilities
            dk_odds (Dict): DraftKings odds by pick identifier

        Returns:
            List[Dict]: Picks with EV calculations, filtered to +EV only
        """
        ev_picks = []

        for pick in our_picks:
            # Create identifier for matching with DK odds
            identifier = f"{pick['team']}_{pick['type']}"

            if identifier not in dk_odds:
                continue

            dk_american = dk_odds[identifier]

            # Calculate EV
            ev_result = calculate_ev(
                our_probability=pick['combined_probability'],
                sportsbook_odds=dk_american
            )

            # Only include +EV picks
            if ev_result['ev_percentage'] > 0:
                pick_with_ev = pick.copy()
                pick_with_ev.update({
                    'dk_odds': dk_american,
                    'fair_odds': pick['fair_odds'],
                    'ev_percentage': ev_result['ev_percentage'],
                    'expected_value': ev_result['expected_value']
                })
                ev_picks.append(pick_with_ev)

        # Sort by EV percentage descending
        ev_picks.sort(key=lambda x: x['ev_percentage'], reverse=True)

        print(f"✅ Found {len(ev_picks)} +EV picks")

        return ev_picks

    def get_correlations(self) -> Dict:
        """Get current correlation coefficients"""
        return self.loaded_correlations.copy()

    def predict_player_props(self, player_name: str, week: int) -> Dict:
        """
        Predict all props for a specific player

        Args:
            player_name (str): Player name
            week (int): Week number

        Returns:
            Dict: Predictions for various prop bets
        """
        if not self.player_stats_db.exists():
            return {'error': 'Player stats database not found'}

        try:
            conn = sqlite3.connect(self.player_stats_db)
            query = """
                SELECT * FROM NFL_Model_Data
                WHERE player_display_name LIKE ? AND week <= ?
                ORDER BY week DESC
                LIMIT 5
            """
            df = pd.read_sql_query(query, conn, params=[f"%{player_name}%", week])
            conn.close()

            if df.empty:
                return {'error': f'No data found for {player_name}'}

            # Get recent stats
            position = df.iloc[0]['position']
            recent_avg = df[['passing_yards', 'rushing_yards', 'receiving_yards']].mean()

            predictions = {
                'player': player_name,
                'position': position,
                'week': week,
                'predictions': {}
            }

            # Position-specific predictions
            if position == 'QB':
                predictions['predictions']['pass_yards_250+'] = {
                    'probability': 0.60,
                    'recent_avg': recent_avg['passing_yards']
                }
            elif position == 'RB':
                predictions['predictions']['rush_yards_75+'] = {
                    'probability': 0.55,
                    'recent_avg': recent_avg['rushing_yards']
                }
            elif position in ['WR', 'TE']:
                predictions['predictions']['rec_yards_75+'] = {
                    'probability': 0.50,
                    'recent_avg': recent_avg['receiving_yards']
                }

            return predictions

        except Exception as e:
            return {'error': str(e)}

    def get_model_status(self) -> Dict:
        """Get status of loaded models"""
        status = {
            'models_dir': str(self.models_dir),
            'models_dir_exists': self.models_dir.exists(),
            'predictor_loaded': self.predictor is not None,
            'correlations_loaded': len(self.loaded_correlations) > 0,
            'correlations': self.loaded_correlations,
            'databases': {
                'player_stats': {
                    'path': str(self.player_stats_db),
                    'exists': self.player_stats_db.exists()
                },
                'sgp_combos': {
                    'path': str(self.sgp_combos_db),
                    'exists': self.sgp_combos_db.exists()
                }
            }
        }

        # Get database record counts
        if self.player_stats_db.exists():
            try:
                conn = sqlite3.connect(self.player_stats_db)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM NFL_Model_Data")
                count = cursor.fetchone()[0]
                status['databases']['player_stats']['record_count'] = count
                conn.close()
            except Exception as e:
                status['databases']['player_stats']['error'] = str(e)

        if self.sgp_combos_db.exists():
            try:
                conn = sqlite3.connect(self.sgp_combos_db)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM SGP_Combinations")
                count = cursor.fetchone()[0]
                status['databases']['sgp_combos']['record_count'] = count
                conn.close()
            except Exception as e:
                status['databases']['sgp_combos']['error'] = str(e)

        return status

    def get_sgp_combinations(self, team: str, week: int, season: int = 2024) -> List[Dict]:
        """
        Get pre-calculated SGP combinations for a team

        Args:
            team (str): Team abbreviation
            week (int): Week number
            season (int): Season year

        Returns:
            List[Dict]: SGP combinations from database
        """
        if not self.sgp_combos_db.exists():
            print(f"❌ SGP combos database not found: {self.sgp_combos_db}")
            return []

        try:
            conn = sqlite3.connect(self.sgp_combos_db)
            query = """
                SELECT * FROM NFL_Model_Data
                WHERE team = ? AND week = ? AND season = ?
            """
            df = pd.read_sql_query(query, conn, params=[team, week, season])
            conn.close()

            return df.to_dict('records')

        except Exception as e:
            print(f"❌ Error fetching SGP combinations: {e}")
            return []
