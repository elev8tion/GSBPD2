"""
NFL Data Downloader Service
Fetches real NFL player data from nflverse
Backend service layer implementation
"""

import pandas as pd
import requests
import sqlite3
import os
from pathlib import Path
from typing import Optional, List


class NFLDataDownloader:
    """Download NFL player stats from nflverse repository"""

    BASE_URL = "https://github.com/nflverse/nflverse-data/releases/download"

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize downloader

        Args:
            data_dir (Path, optional): Directory to save data. Defaults to backend/data
        """
        if data_dir is None:
            # Use backend/data directory
            base_dir = Path(__file__).parent.parent.parent
            self.data_dir = base_dir / 'data'
        else:
            self.data_dir = Path(data_dir)

        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Use backend database paths
        self.db_path = self.data_dir / 'nfl_player_stats.db'
        self.sgp_db_path = self.data_dir / 'nfl_sgp_combos.db'

    def download_weekly_stats(self, years: List[int] = [2023, 2024]) -> pd.DataFrame:
        """
        Download weekly player stats

        Args:
            years (list): List of years to download

        Returns:
            pd.DataFrame: Combined weekly stats
        """
        print(f"📥 Downloading weekly player data for {years}...")
        all_data = []

        for year in years:
            url = f"{self.BASE_URL}/player_stats/player_stats_{year}.parquet"
            print(f"  Fetching {year} data...")

            try:
                # Try parquet first
                response = requests.get(url, timeout=30)
                response.raise_for_status()

                temp_file = f"/tmp/player_stats_{year}.parquet"
                with open(temp_file, 'wb') as f:
                    f.write(response.content)

                df = pd.read_parquet(temp_file)
                all_data.append(df)
                print(f"  ✅ Downloaded {len(df):,} records for {year}")

                os.remove(temp_file)

            except Exception as e:
                print(f"  ⚠️  Parquet failed: {e}")
                print(f"  Trying CSV fallback...")

                # Try CSV fallback
                try:
                    csv_url = f"{self.BASE_URL}/player_stats/player_stats_{year}.csv.gz"
                    df = pd.read_csv(csv_url, compression='gzip')
                    all_data.append(df)
                    print(f"  ✅ Downloaded {len(df):,} records for {year} (CSV)")
                except Exception as e2:
                    print(f"  ❌ CSV fallback also failed: {e2}")

        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            print(f"\n✅ Total records: {len(combined_df):,}")
            return combined_df
        else:
            print("\n❌ No data downloaded!")
            return pd.DataFrame()

    def process_for_training(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process raw data for ML training

        Args:
            df (pd.DataFrame): Raw weekly stats

        Returns:
            pd.DataFrame: Processed data
        """
        print("\n🔧 Processing data for training...")

        # Filter to key positions
        df = df[df['position'].isin(['QB', 'RB', 'WR', 'TE'])].copy()

        # Select relevant columns
        keep_cols = [
            'player_id', 'player_name', 'player_display_name',
            'position', 'recent_team', 'season', 'week', 'season_type',
            'completions', 'attempts', 'passing_yards', 'passing_tds',
            'interceptions', 'carries', 'rushing_yards', 'rushing_tds',
            'targets', 'receptions', 'receiving_yards', 'receiving_tds',
            'fantasy_points', 'fantasy_points_ppr'
        ]

        # Only keep columns that exist
        keep_cols = [col for col in keep_cols if col in df.columns]
        df = df[keep_cols]

        # Fill NaN with 0 for numeric columns
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        df[numeric_cols] = df[numeric_cols].fillna(0)

        # Create combined TD column
        if 'passing_tds' in df.columns and 'rushing_tds' in df.columns and 'receiving_tds' in df.columns:
            df['touchdowns'] = df['passing_tds'] + df['rushing_tds'] + df['receiving_tds']

        print(f"  ✅ Processed {len(df):,} player-games")
        print(f"  Positions: {df['position'].value_counts().to_dict()}")

        return df

    def create_sgp_combinations(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create Same Game Parlay combinations from player data

        Args:
            df (pd.DataFrame): Processed player stats

        Returns:
            pd.DataFrame: SGP combinations
        """
        print("\n🔗 Creating SGP combinations...")

        combinations = []

        # Group by team and week to create same-game combinations
        for (team, week, season), group in df.groupby(['recent_team', 'week', 'season']):

            qbs = group[group['position'] == 'QB']
            rbs = group[group['position'] == 'RB']
            wrs = group[group['position'] == 'WR']
            tes = group[group['position'] == 'TE']

            # QB-WR combinations
            for _, qb in qbs.iterrows():
                for _, wr in wrs.iterrows():
                    combinations.append({
                        'team': team,
                        'week': week,
                        'season': season,
                        'combo_type': 'QB_WR',
                        'player1': qb['player_display_name'],
                        'player1_pos': 'QB',
                        'player1_yards': qb.get('passing_yards', 0),
                        'player2': wr['player_display_name'],
                        'player2_pos': 'WR',
                        'player2_yards': wr.get('receiving_yards', 0)
                    })

            # RB-Team combinations
            for _, rb in rbs.iterrows():
                team_tds = group['touchdowns'].sum() if 'touchdowns' in group.columns else 0
                combinations.append({
                    'team': team,
                    'week': week,
                    'season': season,
                    'combo_type': 'RB_Team_TDs',
                    'player1': rb['player_display_name'],
                    'player1_pos': 'RB',
                    'player1_tds': rb.get('rushing_tds', 0) + rb.get('receiving_tds', 0),
                    'team_total_tds': team_tds
                })

        sgp_df = pd.DataFrame(combinations)
        print(f"  ✅ Created {len(sgp_df):,} SGP combinations")

        return sgp_df

    def save_to_database(self, player_df: pd.DataFrame, sgp_df: Optional[pd.DataFrame] = None):
        """
        Save data to SQLite database

        Args:
            player_df (pd.DataFrame): Player stats
            sgp_df (pd.DataFrame, optional): SGP combinations
        """
        print("\n💾 Saving to database...")

        # Save player stats
        conn = sqlite3.connect(self.db_path)
        player_df.to_sql('NFL_Model_Data', conn, if_exists='replace', index=False)
        conn.close()
        print(f"  ✅ Saved player stats to: {self.db_path}")

        # Save SGP combinations
        if sgp_df is not None and not sgp_df.empty:
            conn = sqlite3.connect(self.sgp_db_path)
            sgp_df.to_sql('NFL_Model_Data', conn, if_exists='replace', index=False)
            conn.close()
            print(f"  ✅ Saved SGP combos to: {self.sgp_db_path}")

    def download_all(self, years: List[int] = [2023, 2024]) -> tuple:
        """
        Complete download pipeline

        Args:
            years (list): Years to download

        Returns:
            tuple: (player_df, sgp_df)
        """
        # Download
        raw_df = self.download_weekly_stats(years)

        if raw_df.empty:
            print("❌ Download failed!")
            return None, None

        # Process
        player_df = self.process_for_training(raw_df)

        # Create combinations
        sgp_df = self.create_sgp_combinations(player_df)

        # Save
        self.save_to_database(player_df, sgp_df)

        print("\n✅ Download complete!")
        return player_df, sgp_df

    def get_player_stats(self, player_name: str, week: Optional[int] = None) -> pd.DataFrame:
        """
        Get stats for a specific player

        Args:
            player_name (str): Player name
            week (int, optional): Filter by week

        Returns:
            pd.DataFrame: Player stats
        """
        if not self.db_path.exists():
            print(f"❌ Database not found: {self.db_path}")
            return pd.DataFrame()

        conn = sqlite3.connect(self.db_path)

        query = "SELECT * FROM NFL_Model_Data WHERE player_display_name LIKE ?"
        params = [f"%{player_name}%"]

        if week is not None:
            query += " AND week = ?"
            params.append(week)

        df = pd.read_sql_query(query, conn, params=params)
        conn.close()

        return df

    def get_team_stats(self, team: str, week: int, season: int = 2024) -> pd.DataFrame:
        """
        Get all player stats for a team in a specific week

        Args:
            team (str): Team abbreviation
            week (int): Week number
            season (int): Season year

        Returns:
            pd.DataFrame: Team player stats
        """
        if not self.db_path.exists():
            print(f"❌ Database not found: {self.db_path}")
            return pd.DataFrame()

        conn = sqlite3.connect(self.db_path)

        query = """
            SELECT * FROM NFL_Model_Data
            WHERE recent_team = ? AND week = ? AND season = ?
        """

        df = pd.read_sql_query(query, conn, params=[team, week, season])
        conn.close()

        return df
