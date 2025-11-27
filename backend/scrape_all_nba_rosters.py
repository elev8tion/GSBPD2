#!/usr/bin/env python3
"""
Scrape ALL 30 NBA team rosters using Firecrawl MCP
This script will be used with Firecrawl batch scraping to get real data
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, '/Users/kcdacre8tor/GSBPD2/backend')
from services.nba_service import NBA_TEAMS

# Generate all roster URLs for 30 NBA teams
def generate_roster_urls():
    """Generate roster URLs for all 30 NBA teams"""
    urls = []
    for team in NBA_TEAMS:
        url = f"https://www.nba.com/{team['slug']}/roster"
        urls.append({
            'team_id': team['id'],
            'team_name': team['name'],
            'team_slug': team['slug'],
            'url': url
        })
    return urls

if __name__ == "__main__":
    urls = generate_roster_urls()

    print("=" * 70)
    print("NBA ROSTER URLs - ALL 30 TEAMS")
    print("=" * 70)
    print()

    for item in urls:
        print(f"✓ {item['team_name']:<25} → {item['url']}")

    print()
    print(f"Total teams: {len(urls)}")
    print()

    # Save URLs to file for reference
    base_dir = Path(__file__).parent
    urls_file = base_dir / "nba_data" / "roster_urls.json"

    with open(urls_file, 'w') as f:
        json.dump(urls, f, indent=2)

    print(f"✓ URLs saved to: {urls_file}")
    print()
    print("=" * 70)
    print("NEXT: Use these URLs with Firecrawl batch_scrape")
    print("=" * 70)
