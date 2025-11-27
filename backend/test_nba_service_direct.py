#!/usr/bin/env python3
"""Direct test of NBA service to isolate the hang"""
import sys
from services.nba_service import NBADataService

print("Initializing NBA service...")
try:
    service = NBADataService()
    print("✓ Service initialized")

    print("\nCalling get_upcoming_games()...")
    games = service.get_upcoming_games()
    print(f"✓ Got {len(games)} games")

    if games:
        print(f"\nFirst game:")
        print(f"  {games[0]['away_team']} @ {games[0]['home_team']}")
        print(f"  Spread: {games[0].get('spread')}")
        print(f"  Total: {games[0].get('total')}")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
