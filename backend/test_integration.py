#!/usr/bin/env python3
"""
Integration test for NBA player data fix
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_players_endpoint():
    """Test /nba/players endpoint"""
    print("\n" + "="*60)
    print("Testing /nba/players endpoint")
    print("="*60)

    start = time.time()
    response = requests.get(f"{BASE_URL}/nba/players")
    elapsed = (time.time() - start) * 1000

    print(f"Status Code: {response.status_code}")
    print(f"Response Time: {elapsed:.2f}ms")

    if response.status_code == 200:
        data = response.json()
        total = data.get('total', 0)
        players = data.get('players', [])

        print(f"Total Players: {total}")
        print(f"Players Returned: {len(players)}")

        if players:
            print(f"\nFirst 3 players:")
            for i, player in enumerate(players[:3], 1):
                print(f"  {i}. {player.get('name')} - {player.get('position')} - {player.get('team_name')}")

            # Check for specific players
            lebron = next((p for p in players if 'LeBron' in p.get('name', '')), None)
            curry = next((p for p in players if 'Stephen Curry' in p.get('name', '')), None)

            print(f"\nKnown Players Found:")
            print(f"  LeBron James: {'✓' if lebron else '✗'}")
            print(f"  Stephen Curry: {'✓' if curry else '✗'}")

            if lebron:
                print(f"\nLeBron James Details:")
                print(f"  Team: {lebron.get('team_name')}")
                print(f"  Position: {lebron.get('position')}")
                print(f"  Jersey: #{lebron.get('jersey_number')}")

        if total >= 500 and elapsed < 100:
            print(f"\n✅ PASS: Endpoint working correctly!")
            return True
        elif total < 500:
            print(f"\n⚠️  WARNING: Expected 500+ players, got {total}")
            return False
        else:
            print(f"\n⚠️  WARNING: Response time {elapsed:.2f}ms exceeds 100ms target")
            return False
    else:
        print(f"\n❌ FAIL: Endpoint returned error {response.status_code}")
        print(f"Error: {response.text}")
        return False

def test_dependent_endpoints():
    """Test endpoints that depend on player data"""
    print("\n" + "="*60)
    print("Testing Dependent Endpoints")
    print("="*60)

    endpoints = [
        "/nba/teams/1610612747/roster",  # Lakers roster
        "/nba/betting-insights",
    ]

    results = {}
    for endpoint in endpoints:
        try:
            start = time.time()
            response = requests.get(f"{BASE_URL}{endpoint}")
            elapsed = (time.time() - start) * 1000

            success = response.status_code == 200
            results[endpoint] = success

            status = "✓" if success else "✗"
            print(f"{status} {endpoint} - {elapsed:.2f}ms")

        except Exception as e:
            results[endpoint] = False
            print(f"✗ {endpoint} - Error: {e}")

    all_passed = all(results.values())
    print(f"\nOverall: {'✅ PASS' if all_passed else '❌ FAIL'}")
    return all_passed

def main():
    print("\n🔍 NBA Players Integration Test")
    print("="*60)

    print("\nWaiting for server to be ready...")
    time.sleep(2)

    # Run tests
    test1 = test_players_endpoint()
    test2 = test_dependent_endpoints()

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Players Endpoint: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"Dependent Endpoints: {'✅ PASS' if test2 else '❌ FAIL'}")

    if test1 and test2:
        print(f"\n🎉 All tests passed! The FAISS/Kre8VidMems fix is working!")
        print(f"\nWhat was fixed:")
        print(f"  - Missing .idx symlinks created for NBA memories")
        print(f"  - Updated memory paths in nba_service.py")
        print(f"  - Re-enabled Kre8VidMems player retrieval")
        print(f"  - No FAISS hang - uses Annoy directly")
        return 0
    else:
        print(f"\n❌ Some tests failed")
        return 1

if __name__ == "__main__":
    exit(main())
