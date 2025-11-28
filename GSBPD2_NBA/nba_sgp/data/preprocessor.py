"""
Feature engineering for NBA player data
Standalone module - only depends on pandas/numpy
"""

import pandas as pd
import numpy as np


class FeatureEngineer:
    """Engineer advanced features for NBA ML training"""

    def __init__(self):
        """Initialize feature engineer"""
        self.stat_cols = [
            'PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV',
            'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA',
            'MIN', 'PLUS_MINUS', 'PRA'
        ]

    def engineer_features(self, df):
        """
        Create advanced features from raw NBA player stats

        Args:
            df (pd.DataFrame): Raw player stats with columns:
                - PLAYER_NAME
                - GAME_DATE or GAME_NUM
                - stat columns (PTS, REB, AST, etc.)

        Returns:
            pd.DataFrame: DataFrame with engineered features added
        """
        print("🔧 Engineering NBA advanced features...")

        # Sort by player and time
        df = df.sort_values(['PLAYER_NAME', 'GAME_NUM']).reset_index(drop=True)

        # Get available stats
        available_stats = [col for col in self.stat_cols if col in df.columns]
        print(f"  Creating features for {len(available_stats)} stats...")

        # 1. ROLLING AVERAGES (3, 5, 10 game windows)
        for window in [3, 5, 10]:
            for stat in available_stats:
                df[f'{stat}_roll{window}_mean'] = df.groupby('PLAYER_NAME')[stat].transform(
                    lambda x: x.rolling(window, min_periods=1).mean().shift(1)
                )
                df[f'{stat}_roll{window}_max'] = df.groupby('PLAYER_NAME')[stat].transform(
                    lambda x: x.rolling(window, min_periods=1).max().shift(1)
                )
                df[f'{stat}_roll{window}_std'] = df.groupby('PLAYER_NAME')[stat].transform(
                    lambda x: x.rolling(window, min_periods=1).std().shift(1)
                )

        # 2. SEASON AVERAGES (expanding)
        for stat in available_stats:
            df[f'{stat}_season_mean'] = df.groupby('PLAYER_NAME')[stat].transform(
                lambda x: x.expanding().mean().shift(1)
            )

        # 3. TREND INDICATORS
        for stat in available_stats:
            if f'{stat}_roll3_mean' in df.columns and f'{stat}_season_mean' in df.columns:
                df[f'{stat}_trend'] = df[f'{stat}_roll3_mean'] - df[f'{stat}_season_mean']
                df[f'{stat}_trend_pct'] = df[f'{stat}_trend'] / (df[f'{stat}_season_mean'] + 1)

        # 4. CONSISTENCY SCORE
        for stat in available_stats:
            if f'{stat}_roll10_std' in df.columns and f'{stat}_roll10_mean' in df.columns:
                df[f'{stat}_consistency'] = 1 / (1 + df[f'{stat}_roll10_std'] / (df[f'{stat}_roll10_mean'] + 1))

        # 5. GAMES PLAYED
        df['games_played'] = df.groupby('PLAYER_NAME').cumcount()

        # 6. REST INDICATOR (days between games)
        if 'GAME_DATE' in df.columns:
            df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
            df['days_rest'] = df.groupby('PLAYER_NAME')['GAME_DATE'].diff().dt.days.fillna(2)
        else:
            df['days_rest'] = 0

        # Clean up
        df = self._clean_features(df)

        feature_count = len([col for col in df.columns if any(x in col for x in ['roll', 'trend', 'consistency', 'season_mean'])])
        print(f"  ✅ Created {feature_count} advanced features")

        return df

    def _clean_features(self, df):
        """Clean NaN and infinity values"""
        df = df.fillna(0)
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.fillna(0)

        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col not in ['GAME_NUM', 'games_played', 'days_rest']:
                df[col] = df[col].clip(-1e10, 1e10)

        return df

    def create_prop_targets(self, df):
        """
        Create binary target variables for NBA prop bets

        Args:
            df (pd.DataFrame): DataFrame with player stats

        Returns:
            pd.DataFrame: DataFrame with prop targets added
        """
        print("🎯 Creating NBA prop bet targets...")

        targets_created = []

        # Points props
        if 'PTS' in df.columns:
            df['points_25+'] = (df['PTS'] >= 25).astype(int)
            df['points_30+'] = (df['PTS'] >= 30).astype(int)
            targets_created.extend(['points_25+', 'points_30+'])

        # Rebounds props
        if 'REB' in df.columns:
            df['rebounds_10+'] = (df['REB'] >= 10).astype(int)
            df['rebounds_12+'] = (df['REB'] >= 12).astype(int)
            targets_created.extend(['rebounds_10+', 'rebounds_12+'])

        # Assists props
        if 'AST' in df.columns:
            df['assists_8+'] = (df['AST'] >= 8).astype(int)
            df['assists_10+'] = (df['AST'] >= 10).astype(int)
            targets_created.extend(['assists_8+', 'assists_10+'])

        # Three-pointers props
        if 'FG3M' in df.columns:
            df['threes_3+'] = (df['FG3M'] >= 3).astype(int)
            df['threes_4+'] = (df['FG3M'] >= 4).astype(int)
            targets_created.extend(['threes_3+', 'threes_4+'])

        # PRA (Points + Rebounds + Assists) props
        if 'PRA' in df.columns:
            df['pra_35+'] = (df['PRA'] >= 35).astype(int)
            df['pra_40+'] = (df['PRA'] >= 40).astype(int)
            targets_created.extend(['pra_35+', 'pra_40+'])

        # Double-Double (10+ in any 2 categories)
        if all(col in df.columns for col in ['PTS', 'REB', 'AST']):
            double_double = (
                ((df['PTS'] >= 10) & (df['REB'] >= 10)) |
                ((df['PTS'] >= 10) & (df['AST'] >= 10)) |
                ((df['REB'] >= 10) & (df['AST'] >= 10))
            )
            df['double_double'] = double_double.astype(int)
            targets_created.append('double_double')

        # Triple-Double (10+ in 3 categories)
        if all(col in df.columns for col in ['PTS', 'REB', 'AST']):
            triple_double = (df['PTS'] >= 10) & (df['REB'] >= 10) & (df['AST'] >= 10)
            df['triple_double'] = triple_double.astype(int)
            targets_created.append('triple_double')

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
        feature_patterns = ['roll', 'trend', 'consistency', 'season_mean', 'games_played', 'days_rest']
        feature_cols = [col for col in df.columns if any(pattern in col for pattern in feature_patterns)]

        # Add base stats
        base_stats = [col for col in self.stat_cols if col in df.columns]
        feature_cols.extend(base_stats)

        # Add home/away if exists
        if 'IS_HOME' in df.columns:
            feature_cols.append('IS_HOME')

        # Exclude targets if requested
        if exclude_targets:
            target_patterns = ['points_', 'rebounds_', 'assists_', 'threes_', 'pra_', 'double_double', 'triple_double']
            feature_cols = [col for col in feature_cols if not any(col.startswith(pattern) and '+' in col for pattern in target_patterns)]
            feature_cols = [col for col in feature_cols if col not in ['double_double', 'triple_double']]

        return feature_cols
