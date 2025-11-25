#!/usr/bin/env python3
"""
Parse scraped NBA standings data and populate teams.json
Using data from Firecrawl scrape of https://www.nba.com/standings
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, '/Users/kcdacre8tor/GSBPD2/backend')
from services.nba_service import NBADataService, NBA_TEAMS

# Real standings data from NBA.com (scraped via Firecrawl)
STANDINGS = {
    # Eastern Conference
    "1610612765": {"wins": 15, "losses": 2, "win_pct": 0.882},  # Detroit Pistons
    "1610612761": {"wins": 13, "losses": 5, "win_pct": 0.722},  # Toronto Raptors
    "1610612748": {"wins": 12, "losses": 6, "win_pct": 0.667},  # Miami Heat
    "1610612739": {"wins": 12, "losses": 7, "win_pct": 0.632},  # Cleveland Cavaliers
    "1610612752": {"wins": 10, "losses": 6, "win_pct": 0.625},  # New York Knicks
    "1610612737": {"wins": 11, "losses": 7, "win_pct": 0.611},  # Atlanta Hawks
    "1610612755": {"wins": 9, "losses": 7, "win_pct": 0.563},   # Philadelphia 76ers
    "1610612753": {"wins": 10, "losses": 8, "win_pct": 0.556},  # Orlando Magic
    "1610612741": {"wins": 9, "losses": 8, "win_pct": 0.529},   # Chicago Bulls
    "1610612738": {"wins": 9, "losses": 8, "win_pct": 0.529},   # Boston Celtics
    "1610612749": {"wins": 8, "losses": 10, "win_pct": 0.444},  # Milwaukee Bucks
    "1610612766": {"wins": 4, "losses": 13, "win_pct": 0.235},  # Charlotte Hornets
    "1610612751": {"wins": 3, "losses": 14, "win_pct": 0.176},  # Brooklyn Nets
    "1610612754": {"wins": 2, "losses": 15, "win_pct": 0.118},  # Indiana Pacers
    "1610612764": {"wins": 1, "losses": 15, "win_pct": 0.063},  # Washington Wizards

    # Western Conference
    "1610612760": {"wins": 17, "losses": 1, "win_pct": 0.944},  # Oklahoma City Thunder
    "1610612743": {"wins": 13, "losses": 4, "win_pct": 0.765},  # Denver Nuggets
    "1610612747": {"wins": 12, "losses": 4, "win_pct": 0.750},  # Los Angeles Lakers
    "1610612745": {"wins": 10, "losses": 4, "win_pct": 0.714},  # Houston Rockets
    "1610612759": {"wins": 11, "losses": 5, "win_pct": 0.688},  # San Antonio Spurs
    "1610612756": {"wins": 11, "losses": 6, "win_pct": 0.647},  # Phoenix Suns
    "1610612750": {"wins": 10, "losses": 6, "win_pct": 0.625},  # Minnesota Timberwolves
    "1610612744": {"wins": 9, "losses": 9, "win_pct": 0.500},   # Golden State Warriors
    "1610612757": {"wins": 8, "losses": 10, "win_pct": 0.444},  # Portland Trail Blazers
    "1610612763": {"wins": 6, "losses": 12, "win_pct": 0.333},  # Memphis Grizzlies
    "1610612762": {"wins": 5, "losses": 11, "win_pct": 0.313},  # Utah Jazz
    "1610612746": {"wins": 5, "losses": 12, "win_pct": 0.294},  # LA Clippers
    "1610612742": {"wins": 5, "losses": 14, "win_pct": 0.263},  # Dallas Mavericks
    "1610612758": {"wins": 4, "losses": 13, "win_pct": 0.235},  # Sacramento Kings
    "1610612740": {"wins": 3, "losses": 15, "win_pct": 0.167},  # New Orleans Pelicans
}

# Stats leaders from https://www.nba.com/stats/teams
TEAM_STATS = {
    "1610612748": {"ppg": 123.9, "rpg": 46.4, "apg": 30.2, "oppg": 113.2},  # Miami Heat
    "1610612743": {"ppg": 123.8, "rpg": 46.1, "apg": 29.2, "oppg": 114.1},  # Denver Nuggets
    "1610612760": {"ppg": 122.6, "rpg": 44.8, "apg": 28.9, "oppg": 105.7},  # Oklahoma City Thunder
    "1610612745": {"ppg": 122.3, "rpg": 49.1, "apg": 28.4, "oppg": 111.9},  # Houston Rockets
    "1610612741": {"ppg": 121.3, "rpg": 46.4, "apg": 29.6, "oppg": 118.1},  # Chicago Bulls
    "1610612761": {"ppg": 121.0, "rpg": 45.2, "apg": 30.3, "oppg": 114.4},  # Toronto Raptors
    "1610612747": {"ppg": 119.4, "rpg": 43.7, "apg": 27.5, "oppg": 113.8},  # Los Angeles Lakers
    "1610612756": {"ppg": 118.7, "rpg": 43.2, "apg": 28.6, "oppg": 112.5},  # Phoenix Suns
    "1610612753": {"ppg": 118.3, "rpg": 45.8, "apg": 26.5, "oppg": 112.7},  # Orlando Magic
    "1610612737": {"ppg": 117.3, "rpg": 44.0, "apg": 30.4, "oppg": 114.2},  # Atlanta Hawks
    "1610612765": {"ppg": 117.1, "rpg": 43.5, "apg": 26.8, "oppg": 110.0},  # Detroit Pistons
    "1610612749": {"ppg": 117.6, "rpg": 44.2, "apg": 28.1, "oppg": 114.9},  # Milwaukee Bucks
    "1610612752": {"ppg": 116.7, "rpg": 44.1, "apg": 28.4, "oppg": 112.1},  # New York Knicks
    "1610612744": {"ppg": 116.2, "rpg": 42.5, "apg": 27.4, "oppg": 113.8},  # Golden State Warriors
    "1610612759": {"ppg": 115.8, "rpg": 44.6, "apg": 27.3, "oppg": 111.8},  # San Antonio Spurs
    "1610612750": {"ppg": 114.9, "rpg": 43.8, "apg": 26.7, "oppg": 109.3},  # Minnesota Timberwolves
    "1610612738": {"ppg": 114.2, "rpg": 44.5, "apg": 26.3, "oppg": 110.8},  # Boston Celtics
    "1610612757": {"ppg": 113.7, "rpg": 44.9, "apg": 26.1, "oppg": 115.3},  # Portland Trail Blazers
    "1610612762": {"ppg": 113.6, "rpg": 46.6, "apg": 29.6, "oppg": 119.2},  # Utah Jazz
    "1610612739": {"ppg": 113.5, "rpg": 42.8, "apg": 27.1, "oppg": 107.8},  # Cleveland Cavaliers
    "1610612763": {"ppg": 112.4, "rpg": 43.1, "apg": 26.8, "oppg": 116.7},  # Memphis Grizzlies
    "1610612742": {"ppg": 111.8, "rpg": 42.9, "apg": 26.3, "oppg": 117.2},  # Dallas Mavericks
    "1610612754": {"ppg": 111.2, "rpg": 43.9, "apg": 27.5, "oppg": 120.8},  # Indiana Pacers
    "1610612758": {"ppg": 110.7, "rpg": 41.3, "apg": 25.9, "oppg": 116.4},  # Sacramento Kings
    "1610612755": {"ppg": 109.8, "rpg": 43.7, "apg": 25.9, "oppg": 107.6},  # Philadelphia 76ers
    "1610612746": {"ppg": 109.3, "rpg": 41.7, "apg": 24.8, "oppg": 114.9},  # LA Clippers
    "1610612764": {"ppg": 108.9, "rpg": 41.7, "apg": 25.7, "oppg": 119.3},  # Washington Wizards
    "1610612766": {"ppg": 108.5, "rpg": 42.1, "apg": 25.3, "oppg": 115.2},  # Charlotte Hornets
    "1610612740": {"ppg": 107.2, "rpg": 42.6, "apg": 25.1, "oppg": 118.8},  # New Orleans Pelicans
    "1610612751": {"ppg": 104.7, "rpg": 40.8, "apg": 24.1, "oppg": 112.5},  # Brooklyn Nets
}

if __name__ == "__main__":
    print("Parsing NBA standings data from Firecrawl scrape...")

    service = NBADataService()
    teams = []

    for team_info in NBA_TEAMS:
        team_id = team_info["id"]
        standings = STANDINGS.get(team_id, {"wins": 0, "losses": 0, "win_pct": 0.0})
        stats = TEAM_STATS.get(team_id, {"ppg": 0.0, "rpg": 0.0, "apg": 0.0, "oppg": 0.0})

        team_data = {
            "team_id": team_id,
            "name": team_info["name"],
            "slug": team_info["slug"],
            "division": team_info["division"],
            "conference": team_info["conference"],
            "logo_url": None,
            "wins": standings["wins"],
            "losses": standings["losses"],
            "win_percentage": standings["win_pct"],
            "ppg": stats["ppg"],
            "rpg": stats["rpg"],
            "apg": stats["apg"],
            "oppg": stats["oppg"],
            "last_updated": "2025-11-25T00:00:00"
        }

        teams.append(team_data)
        print(f"✓ {team_info['name']}: {standings['wins']}-{standings['losses']} | PPG: {stats['ppg']}")

    # Save to file
    with open(service.teams_file, 'w') as f:
        json.dump(teams, f, indent=2)

    print(f"\n✓ Populated {len(teams)} NBA teams with real data from NBA.com")
    print(f"Data saved to: {service.teams_file}")
