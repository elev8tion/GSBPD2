"""Test service layer integration"""

from src.services.nfl_sgp_service import NFLSGPService
from src.services.nfl_data_downloader import NFLDataDownloader
from src.services.nfl_service import NFLDataService

def test_nfl_sgp_service():
    """Test NFL SGP service instantiation and methods"""
    print("\n" + "="*60)
    print("Testing NFL SGP Service")
    print("="*60)

    service = NFLSGPService()

    # Test correlations loading
    correlations = service.get_correlations()
    assert 'QB_WR' in correlations, "QB-WR correlation missing"
    print(f"✓ Correlations loaded: {correlations}")

    # Test model status
    model_status = service.get_model_status()
    print(f"\n✓ Models status:")
    print(f"  - Models dir exists: {model_status['models_dir_exists']}")
    print(f"  - Predictor loaded: {model_status['predictor_loaded']}")
    print(f"  - Correlations loaded: {model_status['correlations_loaded']}")

    # Test database status
    print(f"\n✓ Database status:")
    for db_name, db_info in model_status['databases'].items():
        print(f"  - {db_name}:")
        print(f"    Path: {db_info['path']}")
        print(f"    Exists: {db_info['exists']}")
        if 'record_count' in db_info:
            print(f"    Records: {db_info['record_count']:,}")

    # Test weekly picks generation (if data available)
    try:
        picks = service.generate_weekly_picks(week=12, season=2024)
        print(f"\n✓ Generated {len(picks)} picks for Week 12")
        if picks:
            print(f"  Sample pick: {picks[0]['type']} - {picks[0].get('team', 'N/A')}")
    except Exception as e:
        print(f"\n⚠ Could not generate weekly picks: {e}")

    return True


def test_nfl_data_downloader():
    """Test NFL data downloader service"""
    print("\n" + "="*60)
    print("Testing NFL Data Downloader")
    print("="*60)

    downloader = NFLDataDownloader()

    # Test database paths
    assert downloader.db_path.exists(), "Player stats DB not found"
    print(f"✓ Player stats DB: {downloader.db_path}")

    assert downloader.sgp_db_path.exists(), "SGP combos DB not found"
    print(f"✓ SGP combos DB: {downloader.sgp_db_path}")

    # Test can connect to database
    import sqlite3
    conn = sqlite3.connect(downloader.db_path)
    cursor = conn.cursor()

    # Get table count
    cursor.execute("SELECT COUNT(*) FROM NFL_Model_Data")
    count = cursor.fetchone()[0]
    print(f"\n✓ Player stats database contains {count:,} records")

    # Get sample record
    cursor.execute("SELECT * FROM NFL_Model_Data LIMIT 1")
    sample = cursor.fetchone()
    if sample:
        print(f"✓ Sample record found")

    # Get position distribution
    cursor.execute("""
        SELECT position, COUNT(*) as count
        FROM NFL_Model_Data
        GROUP BY position
        ORDER BY count DESC
    """)
    positions = cursor.fetchall()
    print(f"\n✓ Position distribution:")
    for pos, count in positions[:5]:
        print(f"  - {pos}: {count:,} records")

    conn.close()

    # Test SGP combos database
    conn = sqlite3.connect(downloader.sgp_db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM NFL_Model_Data")
    combo_count = cursor.fetchone()[0]
    print(f"\n✓ SGP combos database contains {combo_count:,} combinations")

    # Get combo types
    cursor.execute("""
        SELECT sgp_type, COUNT(*) as count
        FROM NFL_Model_Data
        GROUP BY sgp_type
    """)
    combo_types = cursor.fetchall()
    print(f"\n✓ Combo type distribution:")
    for combo_type, count in combo_types:
        print(f"  - {combo_type}: {count:,}")

    conn.close()

    return True


def test_nfl_service():
    """Test NFL service integration"""
    print("\n" + "="*60)
    print("Testing NFL Data Service")
    print("="*60)

    service = NFLDataService()

    # Test database paths
    print(f"✓ Player stats DB: {service.player_stats_db}")
    print(f"  Exists: {service.player_stats_db.exists()}")

    print(f"✓ SGP combos DB: {service.sgp_combos_db}")
    print(f"  Exists: {service.sgp_combos_db.exists()}")

    # Test player stats retrieval
    player_stats = service.get_player_stats("Patrick Mahomes", week=1)
    print(f"\n✓ Player stats query returned {len(player_stats)} records")
    if player_stats:
        print(f"  Sample: {player_stats[0].get('player_display_name', 'N/A')} - Week {player_stats[0].get('week', 'N/A')}")

    # Test SGP combinations
    sgp_combos = service.get_sgp_combinations("KC", week=1, season=2024)
    print(f"\n✓ SGP combinations query returned {len(sgp_combos)} records")
    if sgp_combos:
        print(f"  Sample: {sgp_combos[0].get('combo_type', 'N/A')}")

    # Test team weekly stats
    team_stats = service.get_team_weekly_stats("KC", week=1, season=2024)
    print(f"\n✓ Team weekly stats query:")
    if team_stats:
        print(f"  Total passing yards: {team_stats.get('total_passing_yards', 'N/A')}")
        print(f"  Total rushing yards: {team_stats.get('total_rushing_yards', 'N/A')}")
        print(f"  Total TDs: {team_stats.get('total_tds', 'N/A')}")
    else:
        print(f"  No stats found")

    return True


if __name__ == "__main__":
    print("\n" + "="*60)
    print("NFL SERVICES INTEGRATION TEST")
    print("="*60)

    all_passed = True

    try:
        test_nfl_data_downloader()
    except AssertionError as e:
        print(f"\n❌ Data Downloader Test Failed: {e}")
        all_passed = False
    except Exception as e:
        print(f"\n❌ Data Downloader Test Error: {e}")
        all_passed = False

    try:
        test_nfl_service()
    except AssertionError as e:
        print(f"\n❌ NFL Service Test Failed: {e}")
        all_passed = False
    except Exception as e:
        print(f"\n❌ NFL Service Test Error: {e}")
        all_passed = False

    try:
        test_nfl_sgp_service()
    except AssertionError as e:
        print(f"\n❌ SGP Service Test Failed: {e}")
        all_passed = False
    except Exception as e:
        print(f"\n❌ SGP Service Test Error: {e}")
        all_passed = False

    print("\n" + "="*60)
    if all_passed:
        print("✅ ALL SERVICE TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED!")
    print("="*60 + "\n")
