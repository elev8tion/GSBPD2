# Memvid Integration for GSBPD2

## Overview

GSBPD2 now includes a complete memvid-powered knowledge base system for sports betting intelligence. This allows you to:

- **Process YouTube videos** (game highlights, analysis, player stats)
- **Scrape and index text** (stats websites, betting strategies, news)
- **Search your knowledge base** semantically across all sports data
- **Support multiple sports** (NFL and NBA)

## Architecture

```
GSBPD2/
├── backend/
│   ├── memvid_integration/          # Copied pipelines
│   │   ├── video_pipeline/          # YouTube processing
│   │   ├── text_pipeline/           # Text scraping
│   │   └── helpers/                 # Memvid utilities
│   ├── memories/                    # Memory storage
│   │   ├── nfl-games/
│   │   ├── nba-games/
│   │   ├── betting-strategies/
│   │   └── player-stats/
│   └── services/
│       └── knowledge_base.py        # Extended with pipelines
├── frontend/
│   └── src/components/
│       ├── MemorySearch.jsx         # Search UI
│       └── Pipeline.jsx             # YouTube + file ingest
└── scripts/
    └── create_memory.sh             # Helper script
```

## Setup

### 1. Install Dependencies

```bash
source venv/bin/activate
pip install -r backend/requirements.txt
```

### 2. Install External Tools

```bash
# Required for YouTube pipeline
brew install yt-dlp ffmpeg

# Optional: Tesseract for OCR
brew install tesseract
```

### 3. Configure Environment

Edit `.env` and set:
```bash
MEMVID_BASE_PATH=/Users/kcdacre8tor/GSBPD2/backend/memories
SPORTS=nfl,nba
OCR_ENGINE=easyocr
```

## Usage

### YouTube Video Processing

1. Open the **Pipeline** tab in the frontend
2. Select sport (NFL/NBA) and category (highlights/analysis/player-stats)
3. Paste a YouTube URL (e.g., `https://youtube.com/watch?v=...`)
4. Click **Process Video**

The system will:
- Download the video using yt-dlp
- Extract frames at 1 fps
- Analyze frames intelligently (skip redundant frames)
- Create a queryable memory

### Text Document Ingestion

**Via Script:**
```bash
./scripts/create_memory.sh nfl-strategies /path/to/docs/
```

**Via API:**
```bash
curl -X POST http://localhost:8000/memories/create \
  -H "Content-Type: application/json" \
  -d '{
    "memory_name": "nfl-strategies",
    "docs_dir": "/path/to/docs/",
    "sport": "nfl"
  }'
```

### Searching Memories

**Via Frontend:**
1. Go to **Knowledge Base** tab
2. Select sport filter (All/NFL/NBA)
3. Enter your query (e.g., "red zone touchdowns", "Mahomes passing stats")
4. Click **Search**

**Via API:**
```bash
curl -X POST http://localhost:8000/memories/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "red zone touchdowns",
    "memories": ["nfl-games"],
    "top_k": 5
  }'
```

### Listing Memories

```bash
curl http://localhost:8000/memories/list
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/memories/search` | POST | Search across memories |
| `/memories/list` | GET | List all available memories |
| `/memories/create` | POST | Create memory from text |
| `/pipeline/youtube` | POST | Process YouTube video |
| `/pipeline/ingest` | POST | Ingest local video file |

## Example Workflows

### 1. Analyze Game Highlights

```bash
# Process NFL game highlight video
POST /pipeline/youtube
{
  "url": "https://youtube.com/watch?v=XYZ",
  "sport": "nfl",
  "category": "highlights"
}

# Query the memory
POST /memories/search
{
  "query": "third down conversions",
  "memories": ["nfl-highlights"],
  "top_k": 5
}
```

### 2. Build Betting Strategy Knowledge Base

```bash
# Create memory from strategy documents
./scripts/create_memory.sh betting-strategies ~/betting-docs/

# Search for strategy patterns
POST /memories/search
{
  "query": "Same Game Parlay correlation patterns",
  "memories": ["betting-strategies"],
  "top_k": 3
}
```

### 3. Multi-Sport Analysis

```bash
# Search across both NFL and NBA
POST /memories/search
{
  "query": "home team advantage in playoffs",
  "memories": [],  # Empty = search all
  "top_k": 10
}
```

## Memory Categories

- **nfl-games** / **nba-games**: Game data, scores, outcomes
- **betting-strategies**: Strategy guides, patterns, SGP correlations
- **player-stats**: Player performance data, injury reports
- **nfl-highlights** / **nba-highlights**: Processed video memories

## Technical Details

### Frame Analysis

The video pipeline uses intelligent frame selection:
- **First pass**: Sample every 30th frame
- **Detect change regions**: Identify scene changes
- **Second pass**: Dense sampling (every 10th frame) in high-change areas
- **Result**: 70-90% frame reduction → massive token cost savings

### Memory Format

Memories are stored as:
```
backend/memories/<sport>-<category>/
├── <name>.mp4              # Video encoding
├── <name>_index.json       # Vector index
└── metadata.json           # Creation info
```

### Search Performance

- Semantic similarity search using sentence transformers
- Average query time: <100ms
- Supports fuzzy matching and natural language queries

## Troubleshooting

**Import errors:**
```bash
# Ensure venv is activated
source venv/bin/activate
pip install -r backend/requirements.txt
```

**YouTube download fails:**
```bash
# Update yt-dlp
brew upgrade yt-dlp
```

**Memory not found:**
```bash
# Check MEMVID_BASE_PATH in .env
# Verify memory exists
ls backend/memories/
```

## Next Steps

1. **Populate knowledge base** with game data, strategies
2. **Integrate with predictions** - use memory search to enhance XGBoost features
3. **Add real-time ingestion** - automatically process new game videos
4. **Expand to more sports** - add MLB, NHL, etc.

## Credits

Based on the memvid video memory system. Adapted from ~/memvid-projects.
