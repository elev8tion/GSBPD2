#!/usr/bin/env python3
"""
Test NFL integration with Kre8VidMems
Tests the NFL service and API endpoints
"""

import requests
import json
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from services.nfl_service import NFLDataService

def test_direct_service():
    """Test the NFL service directly."""
    print("=" * 60)
    print("Testing NFL Service Directly")
    print("=" * 60)

    # Initialize service
    nfl_service = NFLDataService()

    # Test team search
    print("\n📍 Testing team search...")
    teams = nfl_service.search_teams("Buffalo Bills", top_k=3)
    print(f"✓ Found {len(teams)} teams matching 'Buffalo Bills'")
    if teams:
        print(f"  Sample team: {teams[0].get('team', 'N/A')}")

    # Test player search
    print("\n📍 Testing player search...")
    players = nfl_service.search_players("Josh Allen quarterback", top_k=5)
    print(f"✓ Found {len(players)} players matching 'Josh Allen quarterback'")
    if players:
        player = players[0]
        print(f"  Sample player: {player.get('name', 'N/A')}, {player.get('position', 'N/A')} for {player.get('team', 'N/A')}")

    # Test team roster
    print("\n📍 Testing team roster retrieval...")
    roster = nfl_service.get_team_roster("Kansas City Chiefs")
    print(f"✓ Found {len(roster)} players for Kansas City Chiefs")
    if roster:
        print(f"  Sample: {roster[0].get('name', 'N/A')} - {roster[0].get('position', 'N/A')}")

    return True

def test_api_endpoints():
    """Test the NFL API endpoints."""
    print("\n" + "=" * 60)
    print("Testing NFL API Endpoints")
    print("=" * 60)

    base_url = "http://localhost:8000"

    # Test teams endpoint
    print("\n📍 Testing GET /nfl/teams...")
    try:
        response = requests.get(f"{base_url}/nfl/teams")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Retrieved {data['total']} teams")
        else:
            print(f"✗ Failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test team search
    print("\n📍 Testing GET /nfl/search/teams...")
    try:
        response = requests.get(f"{base_url}/nfl/search/teams?query=Dallas Cowboys&limit=3")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Found {data['count']} teams for 'Dallas Cowboys'")
            if data['results']:
                print(f"  Top result: {data['results'][0].get('team', 'N/A')}")
        else:
            print(f"✗ Failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test player search
    print("\n📍 Testing GET /nfl/search/players...")
    try:
        response = requests.get(f"{base_url}/nfl/search/players?query=Patrick Mahomes&limit=5")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Found {data['count']} players for 'Patrick Mahomes'")
            if data['results']:
                player = data['results'][0]
                print(f"  Top result: {player.get('name', 'N/A')}, {player.get('position', 'N/A')}")
        else:
            print(f"✗ Failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test roster by team name
    print("\n📍 Testing GET /nfl/roster/{team_name}...")
    try:
        response = requests.get(f"{base_url}/nfl/roster/Green Bay Packers")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Retrieved {data['total']} players for Green Bay Packers")
            if data['players']:
                print(f"  Sample player: {data['players'][0].get('name', 'N/A')}")
        else:
            print(f"✗ Failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")

    return True

def main():
    """Main test function."""
    print("🏈 NFL Integration Test Suite")
    print("=" * 60)

    # Test direct service
    try:
        test_direct_service()
        print("\n✅ Direct service tests passed!")
    except Exception as e:
        print(f"\n❌ Direct service tests failed: {e}")
        return 1

    # Test API endpoints
    print("\n⚠️  Note: API tests require the backend server to be running")
    print("   Run 'python main.py' in another terminal if not already running")

    try:
        input("\nPress Enter to test API endpoints...")
        test_api_endpoints()
        print("\n✅ API tests completed!")
    except KeyboardInterrupt:
        print("\n⚠️  API tests skipped")
    except Exception as e:
        print(f"\n❌ API tests failed: {e}")
        return 1

    print("\n" + "=" * 60)
    print("🎉 All NFL integration tests completed successfully!")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    exit(main())