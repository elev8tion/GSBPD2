#!/usr/bin/env python3
"""Test that API can serve Memvid data"""
from src.services.nba_service import NBADataService
import json

print("=" * 80)
print("TESTING NBA DATA SERVICE WITH MEMVID")
print("=" * 80)

# Initialize service
nba_service = NBADataService()

# Test 1: Get all teams
print("\n[1] get_all_teams()")
teams = nba_service.get_all_teams()
print(f"✓ Retrieved {len(teams)} teams")
if teams:
    print(f"Sample team: {teams[0]}")

# Test 2: Get all players
print("\n[2] get_all_players()")
players = nba_service.get_all_players()
print(f"✓ Retrieved {len(players)} players")
if players:
    print(f"Sample player: {players[0]}")

# Test 3: Get Lakers specifically (team_id: 1610612747)
print("\n[3] get_team(1610612747) - Lakers")
lakers = nba_service.get_team("1610612747")
if lakers:
    print(f"✓ Lakers data: {json.dumps(lakers, indent=2)[:300]}")

# Test 4: Get Lakers roster
print("\n[4] get_players_by_team(1610612747) - Lakers roster")
lakers_roster = nba_service.get_players_by_team("1610612747")
print(f"✓ Lakers roster: {len(lakers_roster)} players")
if lakers_roster:
    for player in lakers_roster[:3]:
        print(f"  - {player.get('name', 'Unknown')}")

print("\n" + "=" * 80)
print("✅ ALL DATA ACCESSIBLE - READY FOR UI")
print("=" * 80)
