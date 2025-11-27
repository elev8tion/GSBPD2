#!/usr/bin/env python3
"""Test NBA endpoints directly with FastAPI TestClient"""
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

print("=" * 80)
print("TESTING NBA ENDPOINTS")
print("=" * 80)

# Test 1: Health check
print("\n[1] GET /health")
response = client.get("/health")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 2: Get all teams
print("\n[2] GET /nba/teams")
try:
    response = client.get("/nba/teams", timeout=30)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total teams: {data.get('total', 0)}")
    if data.get('teams'):
        print(f"First team: {data['teams'][0]['name']}")
        print(f"Sample: {json.dumps(data['teams'][0], indent=2)[:300]}")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Get all players
print("\n[3] GET /nba/players")
try:
    response = client.get("/nba/players", timeout=30)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total players: {data.get('total', 0)}")
    if data.get('players'):
        print(f"First player: {data['players'][0]['name']}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 80)
print("✅ ENDPOINT TESTING COMPLETE")
print("=" * 80)
