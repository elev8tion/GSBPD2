import os
import json
from datetime import datetime
from memvid import MemvidEncoder, MemvidRetriever

VIDEO_PATH = "portfolio.mp4"
INDEX_PATH = "portfolio_index.json"

class PortfolioService:
    def __init__(self):
        self.encoder = MemvidEncoder()
        # Ensure files exist or handle initialization
        if not os.path.exists(VIDEO_PATH):
            # Initialize empty video if possible, or just wait for first add
            pass

    def place_bet(self, bet_data: dict):
        """
        Saves a bet as a text chunk in the Memvid video.
        Includes SHAP values for future analysis.
        """
        # Add timestamp and initial status
        bet_data['timestamp'] = datetime.now().isoformat()
        bet_data['status'] = 'PENDING' # PENDING, WIN, LOSS
        
        # Load existing bets
        bets = self._load_local_bets()
        bets.append(bet_data)
        self._save_local_bets(bets)
        
        # Rebuild Memvid video
        self._rebuild_memvid(bets)
        
        return {"status": "success", "message": "Bet recorded in Memvid with Analysis Data"}

    def resolve_bet(self, game_id: str, outcome: str):
        """
        Updates the outcome of a bet (WIN/LOSS).
        """
        bets = self._load_local_bets()
        updated = False
        for bet in bets:
            if bet.get('game_id') == game_id:
                bet['status'] = outcome
                updated = True
        
        if updated:
            self._save_local_bets(bets)
            self._rebuild_memvid(bets)
            return {"status": "success", "message": f"Bet {game_id} resolved as {outcome}"}
        return {"status": "error", "message": "Bet not found"}

    def get_bets(self):
        """
        Retrieves all bets. 
        """
        return self._load_local_bets()

    def get_training_data(self):
        """
        Reconstructs a training dataset from resolved bets.
        Returns a list of (features, label) tuples.
        """
        bets = self._load_local_bets()
        training_data = []
        for bet in bets:
            if bet.get('status') in ['WIN', 'LOSS']:
                # Reconstruct features (this assumes we stored them or can derive them)
                # For now, we'll use the 'prediction_used' as a proxy feature, 
                # but ideally we should store the full feature vector in place_bet
                features = {
                    "team_strength": bet.get('team_strength', 0), # Placeholder if not stored
                    "opponent_strength": bet.get('opponent_strength', 0),
                    "home_advantage": bet.get('home_advantage', 0)
                }
                label = 1 if bet['status'] == 'WIN' else 0
                training_data.append((features, label))
        return training_data

    def _rebuild_memvid(self, bets):
        chunks = [json.dumps(b) for b in bets]
        self.encoder = MemvidEncoder() # Reset
        self.encoder.add_chunks(chunks)
        self.encoder.build_video(VIDEO_PATH, INDEX_PATH)

    def _load_local_bets(self):
        if os.path.exists("bets_backup.json"):
            with open("bets_backup.json", "r") as f:
                return json.load(f)
        return []

    def _save_local_bets(self, bets):
        with open("bets_backup.json", "w") as f:
            json.dump(bets, f)
