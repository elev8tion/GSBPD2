"""
Export NFL SGP picks to Kre8VidMems knowledge base
Phase 8: Kre8VidMems Integration
"""

from pathlib import Path
from typing import List, Dict, Optional
import sys

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.nfl_sgp_service import NFLSGPService
from src.services.knowledge_base import KnowledgeBaseService


def format_picks_as_text(picks: List[Dict], week: int, season: int) -> str:
    """Format picks as human-readable text for knowledge base ingestion"""

    text = f"NFL SGP Picks - Week {week}, {season} Season\n"
    text += "=" * 80 + "\n\n"

    if not picks:
        text += "No picks generated for this week.\n"
        return text

    for i, pick in enumerate(picks, 1):
        pick_type = pick.get('type', 'Unknown')
        team = pick.get('team', 'N/A')

        text += f"Pick #{i}: {team} - {pick_type}\n"
        text += f"  Combined Probability: {pick.get('combined_probability', 0):.3%}\n"
        text += f"  Fair Odds: {pick.get('fair_odds', 'N/A')}\n"
        text += f"  Correlation: {pick.get('correlation', 0):.4f}\n"

        # Add type-specific details
        if pick_type == 'QB-WR Stack':
            text += f"  QB: {pick.get('qb', 'N/A')} - {pick.get('qb_prop', 'N/A')}\n"
            text += f"  WR: {pick.get('wr', 'N/A')} - {pick.get('wr_prop', 'N/A')}\n"
        elif pick_type == 'RB-Team TDs':
            text += f"  RB: {pick.get('rb', 'N/A')} - {pick.get('rb_prop', 'N/A')}\n"
            text += f"  Team: {pick.get('team_prop', 'N/A')}\n"

        text += "-" * 80 + "\n"

    return text


def export_weekly_picks_to_memory(week: int, season: int = 2024) -> Dict:
    """
    Export weekly picks to Kre8VidMems memory

    Args:
        week: Week number (1-18)
        season: Season year (default 2024)

    Returns:
        Dict with status and result information
    """

    print(f"\n📊 Exporting NFL SGP Picks to Kre8VidMems")
    print(f"   Week: {week}, Season: {season}")
    print("-" * 80)

    try:
        # Generate picks
        print("🎯 Generating weekly picks...")
        sgp_service = NFLSGPService()
        picks = sgp_service.generate_weekly_picks(week, season)

        if not picks:
            print("⚠️  No picks generated. This may indicate missing data.")
            return {
                "status": "warning",
                "message": "No picks generated",
                "picks_count": 0
            }

        print(f"✅ Generated {len(picks)} picks")

        # Convert to text format
        picks_text = format_picks_as_text(picks, week, season)

        # Save to temp file
        temp_dir = Path('/tmp/sgp_picks')
        temp_dir.mkdir(exist_ok=True)

        temp_file = temp_dir / f'nfl_week_{week}_{season}.txt'
        with open(temp_file, 'w') as f:
            f.write(picks_text)

        print(f"✅ Formatted picks saved to: {temp_file}")

        # Create memory using knowledge base service
        print("📚 Creating Kre8VidMems memory...")
        kb = KnowledgeBaseService()
        result = kb.create_memory_from_text(
            memory_name=f'week-{week}-{season}-sgp-picks',
            docs_dir=str(temp_dir),
            sport='nfl'
        )

        print(f"✅ Memory creation result: {result}")

        return {
            "status": "success",
            "message": f"Successfully exported {len(picks)} picks to Kre8VidMems",
            "memory_name": result.get('memory_name'),
            "picks_count": len(picks),
            "picks": picks
        }

    except Exception as e:
        print(f"❌ Error during export: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "message": str(e)
        }


def search_memory_for_picks(query: str, memory_names: Optional[List[str]] = None, top_k: int = 5) -> Dict:
    """
    Search Kre8VidMems memory for SGP picks

    Args:
        query: Search query (e.g., "QB-WR stack Patrick Mahomes")
        memory_names: List of memory names to search (None = all)
        top_k: Number of results to return

    Returns:
        Dict with search results
    """

    print(f"\n🔍 Searching Kre8VidMems for: '{query}'")
    print("-" * 80)

    try:
        kb = KnowledgeBaseService()

        # List available memories
        print("📋 Available memories:")
        memories_result = kb.list_all_memories()
        if memories_result.get('status') == 'success':
            for mem in memories_result.get('memories', []):
                print(f"   - {mem.get('name')} ({mem.get('chunks', 0)} chunks)")

        # Search
        print(f"\n🔎 Searching {len(memory_names) if memory_names else 'all'} memories...")
        results = kb.search_memories(
            query=query,
            memories=memory_names,
            top_k=top_k
        )

        print(f"\n✅ Search Results:")
        if results.get('status') == 'success':
            for i, result in enumerate(results.get('results', []), 1):
                print(f"\n   Result {i} (Score: {result.get('score', 0):.4f})")
                print(f"   Memory: {result.get('memory')}")
                text_preview = result.get('text', '')[:100]
                print(f"   Content: {text_preview}...")

            print(f"\n   Total Results Found: {results.get('total_results', 0)}")
        else:
            print(f"   Error: {results.get('message')}")

        return results

    except Exception as e:
        print(f"❌ Error during search: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "message": str(e)
        }


def main():
    """Main entry point for the export script"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Export NFL SGP picks to Kre8VidMems knowledge base'
    )
    parser.add_argument('--week', type=int, default=12, help='Week number (1-18)')
    parser.add_argument('--season', type=int, default=2024, help='Season year')
    parser.add_argument('--search', action='store_true', help='Test memory search after export')
    parser.add_argument('--query', type=str, default='QB-WR stack', help='Search query')
    parser.add_argument('--list-memories', action='store_true', help='List all available memories')

    args = parser.parse_args()

    if args.list_memories:
        kb = KnowledgeBaseService()
        result = kb.list_all_memories()
        print("\n📋 Available Kre8VidMems Memories:")
        print("-" * 80)
        if result.get('status') == 'success':
            memories = result.get('memories', [])
            if memories:
                for mem in memories:
                    print(f"  Name: {mem.get('name')}")
                    if 'chunks' in mem:
                        print(f"  Chunks: {mem.get('chunks')}")
                print(f"\n  Total: {result.get('total')} memories")
            else:
                print("  No memories found")
        else:
            print(f"  Error: {result.get('message')}")
        return

    # Export picks
    result = export_weekly_picks_to_memory(args.week, args.season)

    print(f"\n📊 Export Result:")
    print(f"   Status: {result.get('status')}")
    print(f"   Message: {result.get('message')}")
    if 'memory_name' in result:
        print(f"   Memory: {result.get('memory_name')}")
    if 'picks_count' in result:
        print(f"   Picks: {result.get('picks_count')}")

    # Test search if requested
    if args.search and result.get('status') == 'success':
        memory_name = result.get('memory_name')
        search_result = search_memory_for_picks(
            query=args.query,
            memory_names=[memory_name] if memory_name else None
        )


if __name__ == "__main__":
    main()
