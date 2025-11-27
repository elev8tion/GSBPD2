#!/usr/bin/env python3
"""
Quick script to trigger NBA data scraping
"""

import sys
sys.path.insert(0, '/Users/kcdacre8tor/GSBPD2/backend')

from services.nba_service import NBADataService

if __name__ == "__main__":
    print("Starting NBA data scraping...")
    service = NBADataService()
    result = service.scrape_all_teams()
    print(f"\nDone! Scraped {result['total']} teams")
    print(f"Data saved to: {service.teams_file}")
