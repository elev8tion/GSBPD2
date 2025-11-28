"""
Correlation analysis for SGP predictions
Calculates correlations between player performances
"""

import pandas as pd
import numpy as np


class CorrelationAnalyzer:
    """Calculate and manage SGP correlations"""

    def __init__(self):
        """Initialize correlation analyzer"""
        self.correlations = {}

    def calculate_qb_wr_correlation(self, df):
        """
        Calculate QB-WR same-team correlation

        Args:
            df (pd.DataFrame): Player stats with columns:
                - player_display_name
                - position
                - recent_team
                - week
                - season
                - passing_yards
                - receiving_yards

        Returns:
            dict: Correlation results with coefficient and sample size
        """
        print("📊 Calculating QB-WR correlation...")

        qb_wr_pairs = []

        # Group by team, week, season
        for (team, week, season), group in df.groupby(['recent_team', 'week', 'season']):
            qbs = group[group['position'] == 'QB']
            wrs = group[group['position'] == 'WR']

            if len(qbs) > 0 and len(wrs) > 0:
                for _, qb in qbs.iterrows():
                    for _, wr in wrs.iterrows():
                        qb_wr_pairs.append({
                            'qb_passing_yards': qb.get('passing_yards', 0),
                            'wr_receiving_yards': wr.get('receiving_yards', 0),
                            'qb_passing_250+': 1 if qb.get('passing_yards', 0) >= 250 else 0,
                            'wr_receiving_75+': 1 if wr.get('receiving_yards', 0) >= 75 else 0
                        })

        if not qb_wr_pairs:
            print("  ⚠️  No QB-WR pairs found")
            return {'correlation': 0.0, 'n': 0}

        pairs_df = pd.DataFrame(qb_wr_pairs)

        # Calculate correlation on binary outcomes
        correlation = np.corrcoef(
            pairs_df['qb_passing_250+'],
            pairs_df['wr_receiving_75+']
        )[0, 1]

        result = {
            'correlation': correlation,
            'n': len(pairs_df)
        }

        print(f"  QB-WR correlation: {correlation:.3f} (n={len(pairs_df):,})")

        return result

    def calculate_qb_te_correlation(self, df):
        """Calculate QB-TE same-team correlation"""
        print("📊 Calculating QB-TE correlation...")

        qb_te_pairs = []

        for (team, week, season), group in df.groupby(['recent_team', 'week', 'season']):
            qbs = group[group['position'] == 'QB']
            tes = group[group['position'] == 'TE']

            if len(qbs) > 0 and len(tes) > 0:
                for _, qb in qbs.iterrows():
                    for _, te in tes.iterrows():
                        qb_te_pairs.append({
                            'qb_passing_250+': 1 if qb.get('passing_yards', 0) >= 250 else 0,
                            'te_receiving_75+': 1 if te.get('receiving_yards', 0) >= 75 else 0
                        })

        if not qb_te_pairs:
            return {'correlation': 0.0, 'n': 0}

        pairs_df = pd.DataFrame(qb_te_pairs)
        correlation = np.corrcoef(
            pairs_df['qb_passing_250+'],
            pairs_df['te_receiving_75+']
        )[0, 1]

        result = {
            'correlation': correlation,
            'n': len(pairs_df)
        }

        print(f"  QB-TE correlation: {correlation:.3f} (n={len(pairs_df):,})")

        return result

    def calculate_rb_team_tds_correlation(self, df):
        """Calculate RB touchdown correlation with team total TDs"""
        print("📊 Calculating RB-Team TDs correlation...")

        rb_team_pairs = []

        for (team, week, season), group in df.groupby(['recent_team', 'week', 'season']):
            rbs = group[group['position'] == 'RB']

            if 'touchdowns' in group.columns:
                team_tds = group['touchdowns'].sum()

                for _, rb in rbs.iterrows():
                    rb_td = rb.get('rushing_tds', 0) + rb.get('receiving_tds', 0)
                    rb_team_pairs.append({
                        'rb_has_td': 1 if rb_td >= 1 else 0,
                        'team_3+_tds': 1 if team_tds >= 3 else 0
                    })

        if not rb_team_pairs:
            return {'correlation': 0.0, 'n': 0}

        pairs_df = pd.DataFrame(rb_team_pairs)
        correlation = np.corrcoef(
            pairs_df['rb_has_td'],
            pairs_df['team_3+_tds']
        )[0, 1]

        result = {
            'correlation': correlation,
            'n': len(pairs_df)
        }

        print(f"  RB-Team TDs correlation: {correlation:.3f} (n={len(pairs_df):,})")

        return result

    def calculate_wr_wr_correlation(self, df):
        """Calculate WR-WR same-team correlation (usually negative - competing for targets)"""
        print("📊 Calculating WR-WR correlation...")

        wr_wr_pairs = []

        for (team, week, season), group in df.groupby(['recent_team', 'week', 'season']):
            wrs = group[group['position'] == 'WR']

            if len(wrs) >= 2:
                wr_list = list(wrs.iterrows())
                for i, (_, wr1) in enumerate(wr_list):
                    for _, wr2 in wr_list[i+1:]:
                        wr_wr_pairs.append({
                            'wr1_receiving_75+': 1 if wr1.get('receiving_yards', 0) >= 75 else 0,
                            'wr2_receiving_75+': 1 if wr2.get('receiving_yards', 0) >= 75 else 0
                        })

        if not wr_wr_pairs:
            return {'correlation': 0.0, 'n': 0}

        pairs_df = pd.DataFrame(wr_wr_pairs)
        correlation = np.corrcoef(
            pairs_df['wr1_receiving_75+'],
            pairs_df['wr2_receiving_75+']
        )[0, 1]

        result = {
            'correlation': correlation,
            'n': len(pairs_df)
        }

        print(f"  WR-WR correlation: {correlation:.3f} (n={len(pairs_df):,})")

        return result

    def calculate_all(self, df):
        """
        Calculate all correlation types

        Args:
            df (pd.DataFrame): Player stats

        Returns:
            dict: All correlations
        """
        print("\n📈 Calculating All Correlations...")

        self.correlations = {
            'QB_WR': self.calculate_qb_wr_correlation(df)['correlation'],
            'QB_TE': self.calculate_qb_te_correlation(df)['correlation'],
            'RB_Team_TDs': self.calculate_rb_team_tds_correlation(df)['correlation'],
            'WR_WR': self.calculate_wr_wr_correlation(df)['correlation']
        }

        print("\n✅ Correlations calculated:")
        for corr_type, value in self.correlations.items():
            print(f"  {corr_type}: {value:.3f}")

        return self.correlations

    def get_correlation(self, corr_type):
        """
        Get a specific correlation value

        Args:
            corr_type (str): Type of correlation (e.g., 'QB_WR')

        Returns:
            float: Correlation value
        """
        return self.correlations.get(corr_type, 0.0)
