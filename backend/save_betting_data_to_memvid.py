#!/usr/bin/env python3
"""
Save historical betting data to Memvid for AI analysis and predictions.
Creates markdown files from odds API data that can be encoded into Memvid memory.
"""
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Directories
SCRAPED_DIR = Path(__file__).parent / "memvid_integration" / "scraped" / "betting-history"
SCRAPED_DIR.mkdir(parents=True, exist_ok=True)

def format_odds_american(decimal_odds: float) -> str:
    """Convert decimal odds to American format for readability"""
    if decimal_odds >= 2.0:
        return f"+{int((decimal_odds - 1) * 100)}"
    else:
        return f"-{int(100 / (decimal_odds - 1))}"

def create_game_betting_markdown(game: Dict) -> str:
    """Create markdown content for a game's betting data"""

    # Parse game time
    game_time = datetime.fromisoformat(game['commence_time'].replace('Z', '+00:00'))
    formatted_time = game_time.strftime("%B %d, %Y at %I:%M %p %Z")

    # Build markdown
    md = f"""# {game['away_team']} @ {game['home_team']}
**Game Time:** {formatted_time}
**Bookmaker:** {game['bookmaker']}

## Betting Lines

### Moneyline
- **{game['home_team']}:** {game.get('home_odds', 'N/A')} ({format_odds_american(game['home_odds']) if game.get('home_odds') else 'N/A'})
- **{game['away_team']}:** {game.get('away_odds', 'N/A')} ({format_odds_american(game['away_odds']) if game.get('away_odds') else 'N/A'})

### Point Spread
- **Line:** {game.get('spread', 'N/A')}
- **{game['home_team']} {game.get('spread', '')}**

### Total (Over/Under)
- **Line:** {game.get('total', 'N/A')} points
- **Over:** {game.get('over_odds', 'N/A')} ({format_odds_american(game['over_odds']) if game.get('over_odds') else 'N/A'})
- **Under:** {game.get('under_odds', 'N/A')} ({format_odds_american(game['under_odds']) if game.get('under_odds') else 'N/A'})

## Analysis Context
This game is scheduled for {formatted_time}. The betting lines suggest:
- **Favorite:** {game['home_team'] if game.get('spread', 0) < 0 else game['away_team']}
- **Expected Total Score:** {game.get('total', 'Unknown')} points
- **Spread:** {abs(game.get('spread', 0))} points

Historical performance and current team form should be considered when analyzing these lines.
"""

    return md

def save_game_to_memvid(game: Dict) -> Path:
    """Save a single game's betting data to Memvid scraped directory"""

    # Create filename from teams and date
    game_date = datetime.fromisoformat(game['commence_time'].replace('Z', '+00:00'))
    date_str = game_date.strftime("%Y%m%d")

    away_slug = game['away_team'].lower().replace(' ', '_')
    home_slug = game['home_team'].lower().replace(' ', '_')

    filename = f"{date_str}_{away_slug}_at_{home_slug}.md"
    filepath = SCRAPED_DIR / filename

    # Create frontmatter
    frontmatter = f"""---
source: DraftKings via The Odds API
scraped_at: {datetime.now().isoformat()}
category: betting-history
sport: NBA
game_id: {game['id']}
home_team: {game['home_team']}
away_team: {game['away_team']}
commence_time: {game['commence_time']}
bookmaker: {game['bookmaker']}
---

"""

    # Generate content
    content = create_game_betting_markdown(game)

    # Save file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)

    print(f"✓ Saved: {filename}")
    return filepath

def save_all_games_to_memvid(games: List[Dict]) -> int:
    """Save all games to Memvid format"""
    print("=" * 80)
    print("SAVING BETTING DATA TO MEMVID")
    print("=" * 80)
    print(f"\nTarget directory: {SCRAPED_DIR}")
    print(f"Total games: {len(games)}\n")

    saved_count = 0
    for game in games:
        try:
            save_game_to_memvid(game)
            saved_count += 1
        except Exception as e:
            print(f"✗ Error saving {game.get('home_team', 'Unknown')}: {e}")

    print(f"\n{'=' * 80}")
    print(f"✓ Saved {saved_count}/{len(games)} games to Memvid format")
    print(f"{'=' * 80}")
    print("\nNext steps:")
    print("1. Run: python memvid_integration/text_pipeline/encode_to_memvid.py --name betting-history")
    print("2. This will create a Memvid memory for AI-powered betting analysis")

    return saved_count

def load_games_from_cache() -> List[Dict]:
    """Load games from the cache file"""
    cache_file = Path(__file__).parent / "nba_data" / "games_cache.json"

    if not cache_file.exists():
        print("⚠ No games cache found. Run the server first to fetch games.")
        return []

    with open(cache_file, 'r') as f:
        data = json.load(f)
        return data.get('games', [])

def main():
    """Main execution"""
    # Load current games from cache
    games = load_games_from_cache()

    if not games:
        print("No games to save. Exiting.")
        return

    # Save to Memvid format
    save_all_games_to_memvid(games)

if __name__ == "__main__":
    main()
