#!/usr/bin/env python3
"""
Complete NBA roster scraper for all 30 teams
This script coordinates Firecrawl scraping and parsing to build players.json
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, '/Users/kcdacre8tor/GSBPD2/backend')
from src.services.nba_service import NBA_TEAMS
from parse_roster_v2 import parse_roster_markdown_v2

def main():
    """
    Main orchestration function
    Note: Actual Firecrawl scraping should be done via MCP tool in Claude Code
    This script provides the structure for processing scraped data
    """

    print("=" * 80)
    print("NBA COMPLETE ROSTER SCRAPER - ALL 30 TEAMS")
    print("=" * 80)
    print()
    print(f"Total teams to process: {len(NBA_TEAMS)}")
    print()

    # Example: Show what needs to be scraped
    print("Teams and their roster URLs:")
    print("-" * 80)
    for i, team in enumerate(NBA_TEAMS, 1):
        url = f"https://www.nba.com/{team['slug']}/roster"
        print(f"{i:2d}. {team['name']:<30} {url}")

    print()
    print("=" * 80)
    print("SCRAPING INSTRUCTIONS:")
    print("=" * 80)
    print()
    print("For each team URL above, use Firecrawl MCP tool:")
    print("  mcp__firecrawl-mcp__firecrawl_scrape(")
    print("    url='https://www.nba.com/{team_slug}/roster',")
    print("    formats=['markdown']")
    print("  )")
    print()
    print("Then parse the markdown using parse_roster_markdown_v2()")
    print("and aggregate all players into players.json")
    print()
    print("=" * 80)

    # Load existing players (Lakers that we already have)
    base_dir = Path(__file__).parent
    players_file = base_dir / "nba_data" / "players.json"

    try:
        with open(players_file, 'r') as f:
            existing_players = json.load(f)
        print(f"✓ Found {len(existing_players)} existing players in players.json")
        print(f"  (from {len(set(p['team_id'] for p in existing_players))} teams)")
    except:
        print("✗ No existing players.json found")
        existing_players = []

    print()
    print("=" * 80)
    print("Ready to scrape remaining teams via Firecrawl MCP")
    print("=" * 80)

if __name__ == "__main__":
    main()
