"""
NBA data downloader - fetches real data from NBA stats API
Uses nba_api library for official NBA statistics
"""

import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime

try:
    from nba_api.stats.endpoints import playergamelog, leaguegamefinder
    from nba_api.stats.static import players, teams
    HAS_NBA_API = True
except ImportError:
    HAS_NBA_API = False
    print("⚠️  nba_api not installed. Install with: pip install nba_api")


class DataDownloader:
    """Download NBA player stats from official NBA API"""

    def __init__(self, data_dir=None):
        """
        Initialize downloader

        Args:
            data_dir (str, optional): Directory to save data. Defaults to './data'
        """
        if data_dir is None:
            self.data_dir = Path.cwd() / 'data'
        else:
            self.data_dir = Path(data_dir)

        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.db_path = self.data_dir / 'NBA_Player_Stats_2024.db'
        self.sgp_db_path = self.data_dir / 'NBA_SGP_Combos_2024.db'

    def download_player_gamelogs(self, season='2023-24'):
        """
        Download player game logs for a season

        Args:
            season (str): NBA season (e.g., '2023-24')

        Returns:
            pd.DataFrame: Player game logs
        """
        if not HAS_NBA_API:
            print("❌ nba_api not installed!")
            print("   Install with: pip install nba_api")
            return pd.DataFrame()

        print(f"📥 Downloading NBA player gamelogs for {season}...")

        all_players = players.get_active_players()
        all_gamelogs = []

        print(f"  Found {len(all_players)} active players")
        print("  Downloading gamelogs (this may take a few minutes)...")

        for i, player in enumerate(all_players[:50]):  # Limit to 50 players for demo
            try:
                player_id = player['id']
                player_name = player['full_name']

                # Get game logs
                gamelog = playergamelog.PlayerGameLog(
                    player_id=player_id,
                    season=season
                )

                df = gamelog.get_data_frames()[0]

                if not df.empty:
                    df['PLAYER_NAME'] = player_name
                    df['PLAYER_ID'] = player_id
                    all_gamelogs.append(df)

                if (i + 1) % 10 == 0:
                    print(f"  Progress: {i+1}/{len(all_players[:50])} players")

            except Exception as e:
                print(f"  ⚠️  Error downloading {player_name}: {e}")
                continue

        if all_gamelogs:
            combined_df = pd.concat(all_gamelogs, ignore_index=True)
            print(f"\n✅ Downloaded {len(combined_df):,} player-games")
            return combined_df
        else:
            print("\n❌ No data downloaded!")
            return pd.DataFrame()

    def process_for_training(self, df):
        """
        Process raw NBA data for ML training

        Args:
            df (pd.DataFrame): Raw game logs

        Returns:
            pd.DataFrame: Processed data
        """
        print("\n🔧 Processing data for training...")

        # Select relevant columns
        keep_cols = [
            'PLAYER_ID', 'PLAYER_NAME', 'GAME_DATE', 'MATCHUP',
            'PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'FGM', 'FGA',
            'FG3M', 'FG3A', 'FTM', 'FTA', 'MIN', 'PLUS_MINUS'
        ]

        # Only keep columns that exist
        keep_cols = [col for col in keep_cols if col in df.columns]
        df = df[keep_cols].copy()

        # Fill NaN with 0 for numeric columns
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        df[numeric_cols] = df[numeric_cols].fillna(0)

        # Create combined stats
        df['PRA'] = df['PTS'] + df['REB'] + df['AST']  # Points + Rebounds + Assists

        # Create game number
        df = df.sort_values(['PLAYER_NAME', 'GAME_DATE'])
        df['GAME_NUM'] = df.groupby('PLAYER_NAME').cumcount() + 1

        # Extract home/away
        if 'MATCHUP' in df.columns:
            df['IS_HOME'] = df['MATCHUP'].str.contains('vs.').astype(int)

        print(f"  ✅ Processed {len(df):,} player-games")

        return df

    def create_sgp_combinations(self, df):
        """
        Create Same Game Parlay combinations from player data

        Args:
            df (pd.DataFrame): Processed player stats

        Returns:
            pd.DataFrame: SGP combinations
        """
        print("\n🔗 Creating NBA SGP combinations...")

        combinations = []

        # Extract team from matchup
        if 'MATCHUP' in df.columns:
            df['TEAM'] = df['MATCHUP'].str.extract(r'([A-Z]{3})')[0]
            df['OPP_TEAM'] = df['MATCHUP'].str.extract(r'vs\. ([A-Z]{3})|@ ([A-Z]{3})')[0].fillna(
                df['MATCHUP'].str.extract(r'vs\. ([A-Z]{3})|@ ([A-Z]{3})')[1]
            )

        # Group by game (same matchup, same date)
        for (matchup, game_date), group in df.groupby(['MATCHUP', 'GAME_DATE']):

            # Star Player - Teammate combinations (same team)
            if len(group) >= 2:
                # Sort by points to find star player
                sorted_players = group.sort_values('PTS', ascending=False)

                if len(sorted_players) >= 2:
                    star = sorted_players.iloc[0]
                    teammate = sorted_players.iloc[1]

                    combinations.append({
                        'game_date': game_date,
                        'matchup': matchup,
                        'combo_type': 'Star_Teammate_Points',
                        'player1': star['PLAYER_NAME'],
                        'player1_pts': star['PTS'],
                        'player2': teammate['PLAYER_NAME'],
                        'player2_pts': teammate['PTS'],
                        'team_total_pts': group['PTS'].sum()
                    })

            # Guard-Team Assists correlation
            guards = group[group['AST'] > 5]  # Likely guards
            if len(guards) > 0:
                for _, guard in guards.iterrows():
                    combinations.append({
                        'game_date': game_date,
                        'matchup': matchup,
                        'combo_type': 'Guard_Team_Assists',
                        'player': guard['PLAYER_NAME'],
                        'player_ast': guard['AST'],
                        'team_total_ast': group['AST'].sum()
                    })

        sgp_df = pd.DataFrame(combinations)
        print(f"  ✅ Created {len(sgp_df):,} SGP combinations")

        return sgp_df

    def save_to_database(self, player_df, sgp_df=None):
        """
        Save data to SQLite database

        Args:
            player_df (pd.DataFrame): Player stats
            sgp_df (pd.DataFrame, optional): SGP combinations
        """
        print("\n💾 Saving to database...")

        # Save player stats
        conn = sqlite3.connect(self.db_path)
        player_df.to_sql('NBA_Player_Data', conn, if_exists='replace', index=False)
        conn.close()
        print(f"  ✅ Saved player stats to: {self.db_path}")

        # Save SGP combinations
        if sgp_df is not None and not sgp_df.empty:
            conn = sqlite3.connect(self.sgp_db_path)
            sgp_df.to_sql('SGP_Combinations', conn, if_exists='replace', index=False)
            conn.close()
            print(f"  ✅ Saved SGP combos to: {self.sgp_db_path}")

    def download_all(self, season='2023-24'):
        """
        Complete download pipeline

        Args:
            season (str): NBA season to download

        Returns:
            tuple: (player_df, sgp_df)
        """
        # Download
        raw_df = self.download_player_gamelogs(season)

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
