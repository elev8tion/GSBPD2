#!/usr/bin/env python3
"""
Test Memvid Database Contents
Verify what data is stored in both NBA memories
"""
from memvid import MemvidRetriever
from pathlib import Path

def test_nba_players():
    print("=" * 80)
    print("NBA PLAYERS MEMORY TEST")
    print("=" * 80)

    players_video = Path("memories/nba-players/nba-players.mp4")
    players_index = Path("memories/nba-players/nba-players_index.json")

    retriever = MemvidRetriever(str(players_video), str(players_index))

    # Test 1: Lakers roster
    print("\n[1] Query: 'Lakers roster with LeBron James'")
    results = retriever.search('Lakers roster with LeBron James', top_k=2)
    for i, text in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(text[:400] + "..." if len(text) > 400 else text)

    # Test 2: All teams check
    print("\n" + "=" * 80)
    print("[2] Query: 'All NBA teams rosters'")
    results = retriever.search('All NBA teams rosters', top_k=3)
    for i, text in enumerate(results, 1):
        print(f"\nResult {i} preview:")
        lines = text.split('\n')[:5]  # First 5 lines
        print('\n'.join(lines))

def test_nba_games():
    print("\n" + "=" * 80)
    print("NBA GAMES MEMORY TEST")
    print("=" * 80)

    games_video = Path("memories/nba-games/nba-games.mp4")
    games_index = Path("memories/nba-games/nba-games_index.json")

    retriever = MemvidRetriever(str(games_video), str(games_index))

    # Test 1: Lakers stats
    print("\n[1] Query: 'Lakers team record and statistics'")
    results = retriever.search('Lakers team record and statistics', top_k=2)
    for i, text in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(text[:300] + "..." if len(text) > 300 else text)

    # Test 2: Standings table
    print("\n" + "=" * 80)
    print("[2] Query: 'NBA standings Eastern Conference'")
    results = retriever.search('NBA standings Eastern Conference', top_k=2)
    for i, text in enumerate(results, 1):
        print(f"\nResult {i} preview:")
        lines = text.split('\n')[:10]  # First 10 lines
        print('\n'.join(lines))

if __name__ == "__main__":
    try:
        test_nba_players()
        test_nba_games()
        print("\n" + "=" * 80)
        print("✅ All Memvid tests completed successfully")
        print("=" * 80)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
