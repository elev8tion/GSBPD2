import os
import json
import cv2
import random
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Migration: Use adapter instead of direct memvid import
# This provides backward compatibility while using Kre8VidMems underneath
try:
    # Try the migration adapter first (Kre8VidMems backend)
    from services.memvid_adapter import MemvidEncoder, MemvidRetriever
    print("✅ Using Kre8VidMems adapter (no FAISS!)")
except ImportError:
    # Fallback to original memvid if adapter not available
    try:
        from memvid import MemvidEncoder, MemvidRetriever
        print("⚠️ Using original Memvid (FAISS issues may occur)")
    except ImportError:
        print("❌ Neither Kre8VidMems adapter nor Memvid available")
        raise

# Load environment variables
load_dotenv()

VIDEO_PATH = "knowledge_base.mp4" # Renamed from portfolio.mp4
INDEX_PATH = "knowledge_base_index.json"

class KnowledgeBaseService:
    def __init__(self):
        self.encoder = MemvidEncoder()
        if not os.path.exists(VIDEO_PATH):
            pass

    def ingest_video(self, file_path: str):
        """
        Ingests a video file, scans for betting data, and stores it in the Knowledge Base.
        """
        if not os.path.exists(file_path):
            return {"status": "error", "message": "File not found"}

        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            return {"status": "error", "message": "Could not open video file"}

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps
        
        # Simulate "Scanning" the video
        # In a real implementation, we would run OCR on frames here.
        # For this demo, we will generate "Detected" events based on the video duration.
        
        detected_items = []
        
        # Mocking detection of a game result from the screen recording
        # We'll assume the video contains a scroll of recent scores
        mock_detections = [
            {"home_team": "Ravens", "away_team": "Bengals", "home_score": 34, "away_score": 20, "timestamp": 5.0},
            {"home_team": "Eagles", "away_team": "Cowboys", "home_score": 28, "away_score": 23, "timestamp": 12.5},
            {"home_team": "49ers", "away_team": "Seahawks", "home_score": 21, "away_score": 17, "timestamp": 20.0}
        ]
        
        for detection in mock_detections:
            if detection['timestamp'] <= duration:
                # Create an observation record
                observation = {
                    "type": "OBSERVATION",
                    "source": "VIDEO_INGEST",
                    "source_file": os.path.basename(file_path),
                    "timestamp": datetime.now().isoformat(),
                    "game_id": f"vid_{int(detection['timestamp'])}",
                    "home_team": detection['home_team'],
                    "away_team": detection['away_team'],
                    "status": "FINAL",
                    "home_score": detection['home_score'],
                    "away_score": detection['away_score'],
                    "home_covered": (detection['home_score'] - detection['away_score']) > 3.5, # Mock spread logic
                    "team_strength": random.uniform(80, 95), # Inferred stats
                    "opponent_strength": random.uniform(75, 90)
                }
                self.record_item(observation, "OBSERVATION")
                detected_items.append(observation)

        cap.release()
        
        return {
            "status": "success", 
            "message": f"Processed {duration:.1f}s video. Extracted {len(detected_items)} data points.",
            "data": detected_items
        }

    def record_item(self, item_data: dict, item_type: str = "BET"):
        """
        Generic method to record any item (BET, RESULT, OBSERVATION) to Memvid.
        """
        import uuid

        # Generate unique ID if not present
        if 'id' not in item_data:
            item_data['id'] = str(uuid.uuid4())

        item_data['timestamp'] = datetime.now().isoformat()
        item_data['type'] = item_type # 'BET', 'OBSERVATION'

        if 'status' not in item_data:
            item_data['status'] = 'PENDING' if item_type == 'BET' else 'FINAL'

        # Load existing
        items = self._load_local_items()
        items.append(item_data)
        self._save_local_items(items)

        # Rebuild Memvid
        self._rebuild_memvid(items)

        return {"status": "success", "message": f"{item_type} recorded in Knowledge Base", "id": item_data['id']}

    def place_bet(self, bet_data: dict):
        """Wrapper for backward compatibility"""
        return self.record_item(bet_data, "BET")

    def record_observation(self, game_data: dict):
        """
        Records a game result that we didn't necessarily bet on.
        """
        return self.record_item(game_data, "OBSERVATION")

    def resolve_bet(self, bet_id: str, outcome: str):
        """
        Resolve a bet by its unique ID.

        Args:
            bet_id: Unique bet identifier
            outcome: Bet outcome ('win', 'loss', 'push')

        Returns:
            dict with status and message
        """
        items = self._load_local_items()
        updated = False

        for item in items:
            # Try both 'id' (new) and 'game_id' (legacy) for backward compatibility
            if (item.get('id') == bet_id or item.get('game_id') == bet_id) and item.get('type') == 'BET':
                item['status'] = outcome.upper()  # Ensure uppercase for consistency
                item['resolved_at'] = datetime.now().isoformat()
                updated = True
                break

        if updated:
            self._save_local_items(items)
            self._rebuild_memvid(items)
            return {"status": "success", "message": f"Bet {bet_id} resolved as {outcome.upper()}"}

        return {"status": "error", "message": "Bet not found"}

    def get_all_items(self):
        return self._load_local_items()

    def get_training_data(self):
        """
        Reconstructs training data from BOTH resolved bets and observations.
        """
        items = self._load_local_items()
        training_data = []
        for item in items:
            # Include Resolved Bets AND Observations (which are always final)
            if item.get('status') in ['WIN', 'LOSS'] or item.get('type') == 'OBSERVATION':
                
                # Extract features
                features = {
                    "team_strength": item.get('team_strength', 0),
                    "opponent_strength": item.get('opponent_strength', 0),
                    "home_advantage": item.get('home_advantage', 0)
                }
                
                # Determine Label
                # For Bets: WIN=1, LOSS=0
                # For Observations: We need to derive it from the score (e.g., did Home cover?)
                # For simplicity in this mock, we'll assume observations have a 'covered' field
                label = 0
                if item.get('status') == 'WIN':
                    label = 1
                elif item.get('type') == 'OBSERVATION' and item.get('home_covered'):
                    label = 1
                    
                training_data.append((features, label))
        return training_data

    def _rebuild_memvid(self, items):
        chunks = [json.dumps(i) for i in items]
        self.encoder = MemvidEncoder()
        self.encoder.add_chunks(chunks)
        self.encoder.build_video(VIDEO_PATH, INDEX_PATH)

    def _load_local_items(self):
        if os.path.exists("kb_backup.json"):
            with open("kb_backup.json", "r") as f:
                return json.load(f)
        # Fallback to old portfolio backup if exists to migrate data
        if os.path.exists("bets_backup.json"):
            with open("bets_backup.json", "r") as f:
                return json.load(f)
        return []

    def _save_local_items(self, items):
        with open("kb_backup.json", "w") as f:
            json.dump(items, f)

    # ==================== NEW PIPELINE METHODS ====================

    def create_memory_from_text(self, memory_name: str, docs_dir: str, sport: str = "nfl"):
        """
        Create a memvid memory from text documents.

        Args:
            memory_name: Name for the memory (e.g., 'nfl-strategies')
            docs_dir: Directory containing text/markdown files
            sport: Sport type (nfl, nba)

        Returns:
            dict with status and message
        """
        try:
            from memvid_integration.helpers import create_memory

            # Create memory with categorization
            result = create_memory(
                project_name=f"{sport}-{memory_name}",
                directory=docs_dir,
                chunk_size=512
            )

            return {
                "status": "success" if result else "error",
                "message": f"Created memory '{sport}-{memory_name}' from {docs_dir}",
                "memory_name": f"{sport}-{memory_name}"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def search_memories(self, query: str, memories: list = None, top_k: int = 5):
        """
        Search across one or more memories.

        Args:
            query: Search query string
            memories: List of memory names to search (None = all)
            top_k: Number of results to return

        Returns:
            dict with search results
        """
        try:
            from memvid_integration.helpers import query_memory, query_multiple, list_memories

            if memories is None or len(memories) == 0:
                # Search all memories
                all_mems = list_memories(output_json=False)
                memories = [m['project_name'] for m in all_mems]

            if len(memories) == 1:
                result = query_memory(memories[0], query, top_k)
                return {
                    "status": "success",
                    "query": query,
                    "memory": memories[0],
                    "results": result
                }
            else:
                result = query_multiple(memories, query, top_k)
                return {
                    "status": "success",
                    "query": query,
                    "memories": memories,
                    "results": result
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def list_all_memories(self):
        """List all available memories."""
        try:
            from memvid_integration.helpers import list_memories
            memories = list_memories(output_json=False)
            return {
                "status": "success",
                "memories": memories
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def delete_memory(self, memory_name: str):
        """
        Delete a memvid memory and all its files.

        Args:
            memory_name: Name of the memory to delete

        Returns:
            dict with status and message
        """
        try:
            from memvid_integration.helpers import delete_memory

            result = delete_memory(memory_name)

            if result:
                return {
                    "status": "success",
                    "message": f"Memory '{memory_name}' deleted successfully"
                }
            else:
                return {
                    "status": "error",
                    "message": f"Memory '{memory_name}' not found"
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def ingest_youtube_video(self, url: str, sport: str = "nfl", category: str = "highlights"):
        """
        Download and process YouTube video into memvid memory.

        Args:
            url: YouTube URL
            sport: Sport type (nfl, nba)
            category: Category (highlights, analysis, player-stats)

        Returns:
            dict with status and processing info
        """
        try:
            # Create project directory
            project_dir = Path("backend/memvid_integration/projects") / f"{sport}_{category}"
            project_dir.mkdir(parents=True, exist_ok=True)

            # Download video using yt-dlp
            video_path = project_dir / "video.mp4"
            subprocess.run([
                "yt-dlp",
                "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "--merge-output-format", "mp4",
                "-o", str(video_path),
                url
            ], check=True)

            # Extract frames
            frames_dir = project_dir / "frames"
            frames_dir.mkdir(exist_ok=True)
            subprocess.run([
                "ffmpeg",
                "-i", str(video_path),
                "-vf", "fps=1",
                "-q:v", "2",
                str(frames_dir / "frame_%04d.png"),
                "-hide_banner",
                "-loglevel", "error"
            ], check=True)

            # Analyze frames (using the frame analyzer)
            from memvid_integration.video_pipeline import FrameAnalyzer
            analyzer = FrameAnalyzer(base_dir=str(frames_dir.parent))
            plan = analyzer.generate_analysis_plan()

            return {
                "status": "success",
                "message": f"YouTube video processed successfully",
                "video_path": str(video_path),
                "frames": plan['total_frames_selected'],
                "sport": sport,
                "category": category
            }
        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": f"Pipeline error: {str(e)}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
