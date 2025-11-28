"""
Feature engineering for NFL player data
Standalone module - only depends on pandas/numpy
"""

import pandas as pd
import numpy as np


class FeatureEngineer:
    """Engineer advanced features for ML training"""

    def __init__(self):
        """Initialize feature engineer"""
        self.stat_cols = [
            'passing_yards', 'passing_tds', 'completions', 'attempts',
            'rushing_yards', 'rushing_tds', 'carries',
            'receiving_yards', 'receiving_tds', 'receptions', 'targets',
            'fantasy_points_ppr'
        ]

    def engineer_features(self, df):
        """
        Create advanced features from raw player stats

        Args:
            df (pd.DataFrame): Raw player stats with columns:
                - player_display_name
                - season
                - week
                - stat columns (passing_yards, etc.)

        Returns:
            pd.DataFrame: DataFrame with engineered features added
        """
        print("🔧 Engineering advanced features...")

        # Sort by player and time
        df = df.sort_values(['player_display_name', 'season', 'week']).reset_index(drop=True)

        # Get available stats
        available_stats = [col for col in self.stat_cols if col in df.columns]
        print(f"  Creating features for {len(available_stats)} stats...")

        # 1. ROLLING AVERAGES (multiple windows)
        for window in [3, 5, 10]:
            for stat in available_stats:
                # Mean
                df[f'{stat}_roll{window}_mean'] = df.groupby('player_display_name')[stat].transform(
                    lambda x: x.rolling(window, min_periods=1).mean().shift(1)
                )
                # Max (peak performance)
                df[f'{stat}_roll{window}_max'] = df.groupby('player_display_name')[stat].transform(
                    lambda x: x.rolling(window, min_periods=1).max().shift(1)
                )
                # Std (consistency)
                df[f'{stat}_roll{window}_std'] = df.groupby('player_display_name')[stat].transform(
                    lambda x: x.rolling(window, min_periods=1).std().shift(1)
                )

        # 2. EXPANDING AVERAGES (season-long)
        for stat in available_stats:
            df[f'{stat}_season_mean'] = df.groupby(['player_display_name', 'season'])[stat].transform(
                lambda x: x.expanding().mean().shift(1)
            )

        # 3. TREND INDICATORS (is player improving or declining?)
        for stat in available_stats:
            # Recent vs season average
            if f'{stat}_roll3_mean' in df.columns and f'{stat}_season_mean' in df.columns:
                df[f'{stat}_trend'] = df[f'{stat}_roll3_mean'] - df[f'{stat}_season_mean']
                df[f'{stat}_trend_pct'] = df[f'{stat}_trend'] / (df[f'{stat}_season_mean'] + 1)

        # 4. CONSISTENCY SCORE (lower variance = more consistent)
        for stat in available_stats:
            if f'{stat}_roll10_std' in df.columns and f'{stat}_roll10_mean' in df.columns:
                df[f'{stat}_consistency'] = 1 / (1 + df[f'{stat}_roll10_std'] / (df[f'{stat}_roll10_mean'] + 1))

        # 5. GAMES PLAYED (experience factor)
        df['games_played'] = df.groupby('player_display_name').cumcount()
        df['games_this_season'] = df.groupby(['player_display_name', 'season']).cumcount()

        # 6. REST INDICATOR
        df['rest_indicator'] = (df['week'] - df.groupby('player_display_name')['week'].shift(1)).fillna(1)

        # Clean up
        df = self._clean_features(df)

        feature_count = len([col for col in df.columns if any(x in col for x in ['roll', 'trend', 'consistency', 'season_mean'])])
        print(f"  ✅ Created {feature_count} advanced features")

        return df

    def _clean_features(self, df):
        """Clean NaN and infinity values"""
        # Fill NaN with 0
        df = df.fillna(0)

        # Replace infinity values with large finite numbers
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.fillna(0)

        # Clip extreme values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col not in ['week', 'season', 'games_played', 'games_this_season']:
                df[col] = df[col].clip(-1e10, 1e10)

        return df

    def create_prop_targets(self, df):
        """
        Create binary target variables for prop bets

        Args:
            df (pd.DataFrame): DataFrame with player stats

        Returns:
            pd.DataFrame: DataFrame with prop targets added
        """
        print("🎯 Creating prop bet targets...")

        targets_created = []

        # Passing props
        if 'passing_yards' in df.columns:
            df['passing_250+'] = (df['passing_yards'] >= 250).astype(int)
            df['passing_300+'] = (df['passing_yards'] >= 300).astype(int)
            targets_created.extend(['passing_250+', 'passing_300+'])

        # Rushing props
        if 'rushing_yards' in df.columns:
            df['rushing_80+'] = (df['rushing_yards'] >= 80).astype(int)
            df['rushing_100+'] = (df['rushing_yards'] >= 100).astype(int)
            targets_created.extend(['rushing_80+', 'rushing_100+'])

        # Receiving props
        if 'receiving_yards' in df.columns:
            df['receiving_75+'] = (df['receiving_yards'] >= 75).astype(int)
            df['receiving_100+'] = (df['receiving_yards'] >= 100).astype(int)
            targets_created.extend(['receiving_75+', 'receiving_100+'])

        # Receptions
        if 'receptions' in df.columns:
            df['receptions_5+'] = (df['receptions'] >= 5).astype(int)
            targets_created.append('receptions_5+')

        # Touchdowns
        if 'touchdowns' in df.columns or ('passing_tds' in df.columns and 'rushing_tds' in df.columns and 'receiving_tds' in df.columns):
            if 'touchdowns' not in df.columns:
                df['touchdowns'] = df['passing_tds'] + df['rushing_tds'] + df['receiving_tds']
            df['anytime_td'] = (df['touchdowns'] >= 1).astype(int)
            targets_created.append('anytime_td')

        print(f"  ✅ Created {len(targets_created)} prop targets: {targets_created}")

        return df

    def get_feature_columns(self, df, exclude_targets=True):
        """
        Get list of engineered feature columns

        Args:
            df (pd.DataFrame): DataFrame with features
            exclude_targets (bool): Exclude target columns

        Returns:
            list: List of feature column names
        """
        # Engineered feature patterns
        feature_patterns = ['roll', 'trend', 'consistency', 'season_mean', 'games_played', 'rest_indicator']

        feature_cols = [col for col in df.columns if any(pattern in col for pattern in feature_patterns)]

        # Also include base stats
        base_stats = [col for col in self.stat_cols if col in df.columns]
        feature_cols.extend(base_stats)

        # Exclude targets if requested
        if exclude_targets:
            target_patterns = ['passing_', 'rushing_', 'receiving_', 'receptions_', 'anytime_td']
            feature_cols = [col for col in feature_cols if not any(col.startswith(pattern) and '+' in col for pattern in target_patterns)]

        return feature_cols
