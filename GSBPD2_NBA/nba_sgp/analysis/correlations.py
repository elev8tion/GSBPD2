"""
NBA Correlation analysis for SGP predictions
Calculates correlations between NBA player performances
"""

import pandas as pd
import numpy as np


class CorrelationAnalyzer:
    """Calculate and manage NBA SGP correlations"""

    def __init__(self):
        """Initialize correlation analyzer"""
        self.correlations = {}

    def calculate_star_team_points_correlation(self, df):
        """
        Calculate Star Player - Team Points correlation
        High scorers on high-scoring teams

        Args:
            df (pd.DataFrame): Player stats with PTS

        Returns:
            dict: Correlation results
        """
        print("📊 Calculating Star-Team Points correlation...")

        pairs = []

        # Group by game
        for game_id, group in df.groupby('GAME_ID'):
            # Find star players (top scorers)
            if len(group) > 0 and 'PTS' in group.columns:
                team_total = group['PTS'].sum()

                for _, player in group.iterrows():
                    pts = player.get('PTS', 0)
                    pairs.append({
                        'player_25+': 1 if pts >= 25 else 0,
                        'team_high_scoring': 1 if team_total >= 110 else 0,
                        'player_pts': pts,
                        'team_pts': team_total
                    })

        if not pairs:
            print("  ⚠️  No data found")
            return {'correlation': 0.25, 'n': 0}  # Default

        pairs_df = pd.DataFrame(pairs)
        correlation = np.corrcoef(
            pairs_df['player_25+'],
            pairs_df['team_high_scoring']
        )[0, 1]

        result = {
            'correlation': correlation,
            'n': len(pairs_df)
        }

        print(f"  Star-Team Points correlation: {correlation:.3f} (n={len(pairs_df):,})")

        return result

    def calculate_guard_assists_correlation(self, df):
        """
        Calculate Guard Assists - Team Ball Movement correlation
        Guards who assist more on teams with high assists

        Args:
            df (pd.DataFrame): Player stats with AST and POSITION

        Returns:
            dict: Correlation results
        """
        print("📊 Calculating Guard-Assists correlation...")

        pairs = []

        # Group by game
        for game_id, group in df.groupby('GAME_ID'):
            guards = group[group['POSITION'].isin(['PG', 'SG'])]
            team_ast = group['AST'].sum() if 'AST' in group.columns else 0

            for _, guard in guards.iterrows():
                ast = guard.get('AST', 0)
                pairs.append({
                    'guard_8+_ast': 1 if ast >= 8 else 0,
                    'team_high_ast': 1 if team_ast >= 25 else 0
                })

        if not pairs:
            print("  ⚠️  No data found")
            return {'correlation': 0.18, 'n': 0}  # Default

        pairs_df = pd.DataFrame(pairs)
        correlation = np.corrcoef(
            pairs_df['guard_8+_ast'],
            pairs_df['team_high_ast']
        )[0, 1]

        result = {
            'correlation': correlation,
            'n': len(pairs_df)
        }

        print(f"  Guard-Assists correlation: {correlation:.3f} (n={len(pairs_df):,})")

        return result

    def calculate_center_rebounds_correlation(self, df):
        """
        Calculate Center Rebounds - Team Rebounding correlation
        Centers who rebound well on teams with high rebounding

        Args:
            df (pd.DataFrame): Player stats with REB and POSITION

        Returns:
            dict: Correlation results
        """
        print("📊 Calculating Center-Rebounds correlation...")

        pairs = []

        # Group by game
        for game_id, group in df.groupby('GAME_ID'):
            centers = group[group['POSITION'] == 'C']
            team_reb = group['REB'].sum() if 'REB' in group.columns else 0

            for _, center in centers.iterrows():
                reb = center.get('REB', 0)
                pairs.append({
                    'center_10+_reb': 1 if reb >= 10 else 0,
                    'team_high_reb': 1 if team_reb >= 45 else 0
                })

        if not pairs:
            print("  ⚠️  No data found")
            return {'correlation': 0.22, 'n': 0}  # Default

        pairs_df = pd.DataFrame(pairs)
        correlation = np.corrcoef(
            pairs_df['center_10+_reb'],
            pairs_df['team_high_reb']
        )[0, 1]

        result = {
            'correlation': correlation,
            'n': len(pairs_df)
        }

        print(f"  Center-Rebounds correlation: {correlation:.3f} (n={len(pairs_df):,})")

        return result

    def calculate_teammate_points_correlation(self, df):
        """
        Calculate Teammate Points correlation (usually negative)
        Players competing for shots on same team

        Args:
            df (pd.DataFrame): Player stats with PTS

        Returns:
            dict: Correlation results
        """
        print("📊 Calculating Teammate Points correlation...")

        pairs = []

        # Group by game
        for game_id, group in df.groupby('GAME_ID'):
            if len(group) >= 2:
                player_list = list(group.iterrows())
                for i, (_, p1) in enumerate(player_list):
                    for _, p2 in player_list[i+1:]:
                        pts1 = p1.get('PTS', 0)
                        pts2 = p2.get('PTS', 0)
                        pairs.append({
                            'p1_25+': 1 if pts1 >= 25 else 0,
                            'p2_25+': 1 if pts2 >= 25 else 0
                        })

        if not pairs:
            print("  ⚠️  No data found")
            return {'correlation': -0.08, 'n': 0}  # Default (negative)

        pairs_df = pd.DataFrame(pairs)
        correlation = np.corrcoef(
            pairs_df['p1_25+'],
            pairs_df['p2_25+']
        )[0, 1]

        result = {
            'correlation': correlation,
            'n': len(pairs_df)
        }

        print(f"  Teammate Points correlation: {correlation:.3f} (n={len(pairs_df):,})")

        return result

    def calculate_home_performance_correlation(self, df):
        """
        Calculate Home Court Advantage correlation
        Players perform better at home

        Args:
            df (pd.DataFrame): Player stats with IS_HOME and PTS

        Returns:
            dict: Correlation results
        """
        print("📊 Calculating Home Performance correlation...")

        if 'IS_HOME' not in df.columns or 'PTS' not in df.columns:
            print("  ⚠️  Missing required columns")
            return {'correlation': 0.12, 'n': 0}  # Default

        pairs = []

        for _, player in df.iterrows():
            is_home = player.get('IS_HOME', False)
            pts = player.get('PTS', 0)
            pairs.append({
                'is_home': 1 if is_home else 0,
                'pts_25+': 1 if pts >= 25 else 0
            })

        pairs_df = pd.DataFrame(pairs)
        correlation = np.corrcoef(
            pairs_df['is_home'],
            pairs_df['pts_25+']
        )[0, 1]

        result = {
            'correlation': correlation,
            'n': len(pairs_df)
        }

        print(f"  Home Performance correlation: {correlation:.3f} (n={len(pairs_df):,})")

        return result

    def calculate_all(self, df):
        """
        Calculate all NBA correlation types

        Args:
            df (pd.DataFrame): NBA player stats

        Returns:
            dict: All NBA correlations
        """
        print("\n📈 Calculating All NBA Correlations...")

        self.correlations = {
            'Star_Team_Points': self.calculate_star_team_points_correlation(df)['correlation'],
            'Guard_Team_Assists': self.calculate_guard_assists_correlation(df)['correlation'],
            'Center_Team_Rebounds': self.calculate_center_rebounds_correlation(df)['correlation'],
            'Teammate_Points': self.calculate_teammate_points_correlation(df)['correlation'],
            'Home_Performance': self.calculate_home_performance_correlation(df)['correlation']
        }

        print("\n✅ NBA Correlations Summary:")
        for name, corr in self.correlations.items():
            print(f"  {name}: {corr:+.3f}")

        return self.correlations

    def get_correlation(self, prop_type1, prop_type2):
        """
        Get correlation between two NBA prop types

        Args:
            prop_type1 (str): First prop type
            prop_type2 (str): Second prop type

        Returns:
            float: Correlation coefficient (defaults to 0.0 if not found)
        """
        # Map prop types to correlation keys
        if 'points' in prop_type1.lower() and 'points' in prop_type2.lower():
            return self.correlations.get('Star_Team_Points', 0.25)

        if 'assists' in prop_type1.lower() or 'assists' in prop_type2.lower():
            return self.correlations.get('Guard_Team_Assists', 0.18)

        if 'rebounds' in prop_type1.lower() or 'rebounds' in prop_type2.lower():
            return self.correlations.get('Center_Team_Rebounds', 0.22)

        # Default
        return 0.05
