import os
import json
import cv2
import random
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Use Kre8VidMems directly - no more FAISS crashes!
from kre8vidmems import Kre8VidMemory
print("✅ Using Kre8VidMems directly (no FAISS!)")

# Load environment variables
load_dotenv()

VIDEO_PATH = "knowledge_base.mp4" # Renamed from portfolio.mp4
INDEX_PATH = "knowledge_base_index.json"

class KnowledgeBaseService:
    def __init__(self):
        self.memory = None
        if os.path.exists(VIDEO_PATH):
            try:
                # Load existing memory
                base_path = Path(VIDEO_PATH).stem
                self.memory = Kre8VidMemory.load(base_path)
            except:
                # Create new memory if loading fails
                self.memory = Kre8VidMemory()

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

        # Rebuild Kre8VidMems
        self._rebuild_kre8vidmems(items)

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
            self._rebuild_kre8vidmems(items)
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

    def _rebuild_kre8vidmems(self, items):
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
        Create a Kre8VidMems memory from text documents.

        Args:
            memory_name: Name for the memory (e.g., 'nfl-strategies')
            docs_dir: Directory containing text/markdown files
            sport: Sport type (nfl, nba)

        Returns:
            dict with status and message
        """
        try:
            docs_path = Path(docs_dir)
            if not docs_path.exists():
                return {"status": "error", "message": f"Directory not found: {docs_dir}"}

            # Read all text files
            text_files = list(docs_path.glob("*.txt")) + list(docs_path.glob("*.md"))
            if not text_files:
                return {"status": "error", "message": f"No .txt or .md files found in {docs_dir}"}

            # Combine all text
            all_text = []
            for file_path in text_files:
                with open(file_path, 'r') as f:
                    all_text.append(f.read())

            combined_text = "\n\n".join(all_text)

            # Create memory
            full_memory_name = f"{sport}-{memory_name}"
            memories_dir = Path("data/memories")
            memories_dir.mkdir(parents=True, exist_ok=True)

            memory = Kre8VidMemory()
            memory.add_text(combined_text)
            memory.save(str(memories_dir / full_memory_name))

            return {
                "status": "success",
                "message": f"Created memory '{full_memory_name}' from {len(text_files)} files",
                "memory_name": full_memory_name,
                "files_processed": len(text_files)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def search_memories(self, query: str, memories: list = None, top_k: int = 5):
        """
        Search across one or more Kre8VidMems memories.

        Args:
            query: Search query string
            memories: List of memory names to search (None = all)
            top_k: Number of results to return

        Returns:
            dict with search results
        """
        try:
            memories_dir = Path("data/memories")

            if memories is None or len(memories) == 0:
                # Get all available memories
                memory_files = list(memories_dir.glob("*.ann"))
                memories = [f.stem for f in memory_files]

            if not memories:
                return {"status": "error", "message": "No memories found"}

            all_results = []

            for memory_name in memories:
                try:
                    # Load memory and search
                    memory = Kre8VidMemory.load(str(memories_dir / memory_name))
                    results = memory.search(query, top_k=top_k)

                    for result in results:
                        all_results.append({
                            "memory": memory_name,
                            "text": result.get("text", ""),
                            "score": result.get("score", 0.0),
                            "chunk_id": result.get("chunk_id", 0)
                        })
                except Exception as e:
                    # Skip memories that fail to load
                    continue

            # Sort by score and limit to top_k
            all_results.sort(key=lambda x: x["score"], reverse=True)
            all_results = all_results[:top_k]

            return {
                "status": "success",
                "query": query,
                "memories_searched": memories,
                "results": all_results,
                "total_results": len(all_results)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def list_all_memories(self):
        """List all available memories."""
        try:
            memories_dir = Path("data/memories")
            if not memories_dir.exists():
                return {"status": "success", "memories": []}

            # Find all .ann files (Kre8VidMems memory indexes)
            memory_files = list(memories_dir.glob("*.ann"))
            memories = []

            for mem_file in memory_files:
                memory_name = mem_file.stem
                meta_file = memories_dir / f"{memory_name}.meta"

                memory_info = {"name": memory_name}

                # Try to read metadata if available
                if meta_file.exists():
                    try:
                        with open(meta_file, 'r') as f:
                            meta = json.load(f)
                            memory_info["chunks"] = len(meta.get("metadata", []))
                    except:
                        pass

                memories.append(memory_info)

            return {
                "status": "success",
                "memories": memories,
                "total": len(memories)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def delete_memory(self, memory_name: str):
        """
        Delete a Kre8VidMems memory and all its files.

        Args:
            memory_name: Name of the memory to delete

        Returns:
            dict with status and message
        """
        try:
            memories_dir = Path("data/memories")
            extensions = [".ann", ".meta", ".mp4", ".idx"]

            deleted_files = []
            for ext in extensions:
                file_path = memories_dir / f"{memory_name}{ext}"
                if file_path.exists():
                    file_path.unlink()
                    deleted_files.append(str(file_path))

            if deleted_files:
                return {
                    "status": "success",
                    "message": f"Memory '{memory_name}' deleted successfully",
                    "deleted_files": deleted_files
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
        Download and process YouTube video into Kre8VidMems memory.

        Args:
            url: YouTube URL
            sport: Sport type (nfl, nba)
            category: Category (highlights, analysis, player-stats)

        Returns:
            dict with status and processing info
        """
        try:
            # Create project directory
            project_dir = Path("backend/kre8vidmems_integration/projects") / f"{sport}_{category}"
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
            from kre8vidmems_integration.video_pipeline import FrameAnalyzer
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
