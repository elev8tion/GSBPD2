#!/usr/bin/env python3
"""Quick test of the betting insights endpoint"""
import requests
import json

try:
    print("Testing /nba/betting-insights endpoint...")
    response = requests.get("http://localhost:8000/nba/betting-insights", timeout=5)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"\nTotal insights: {data.get('total', 0)}")
        print(f"Disclaimer: {data.get('disclaimer', 'N/A')}")
        if data.get('insights'):
            print(f"\nFirst insight:")
            print(json.dumps(data['insights'][0], indent=2))
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")
