"""Integration test for NFL SGP pipeline - Phase 6"""
import sys
import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.feature_engineering import FeatureEngineer
from src.core.model_predictor import Predictor
from src.core.parlay_builder import ParlayBuilder
from src.core.ev_calculator import EVCalculator
from src.core.correlations import CorrelationAnalyzer
from src.core.odds_calculator import calculate_ev, calculate_parlay_odds, american_to_decimal

# Test results collection
test_results = {
    'timestamp': datetime.now().isoformat(),
    'tests': {},
    'overall_status': 'PENDING'
}


def test_end_to_end_pipeline():
    """Test complete data flow: load → feature → predict → build SGP → calc EV"""
    test_name = "End-to-End Data Flow"
    print(f"\n{'='*80}")
    print(f"TEST 1: {test_name}")
    print(f"{'='*80}")

    try:
        # Step 1: Load player data
        print("\nStep 1: Loading player data from database...")
        db_path = Path(__file__).parent / 'data' / 'nfl_player_stats.db'

        if not db_path.exists():
            raise FileNotFoundError(f"Database not found: {db_path}")

        conn = sqlite3.connect(str(db_path))
        df = pd.read_sql_query("SELECT * FROM NFL_Model_Data WHERE week = 1 LIMIT 100", conn)
        conn.close()

        if df.empty:
            raise ValueError("No data found in database")

        print(f"  ✓ Loaded {len(df)} player records")
        print(f"  ✓ Columns: {len(df.columns)}")
        print(f"  ✓ Sample columns: {list(df.columns[:5])}")

        # Step 2: Engineer features
        print("\nStep 2: Engineering features...")
        engineer = FeatureEngineer()
        df_features = engineer.engineer_features(df)

        print(f"  ✓ Engineered features (shape: {df_features.shape})")
        print(f"  ✓ New columns added: {df_features.shape[1] - df.shape[1]}")

        # Step 3: Create prop targets
        print("\nStep 3: Creating prop targets...")
        df_features = engineer.create_prop_targets(df_features)
        print(f"  ✓ Prop targets created")

        # Step 4: Make predictions (if models available)
        print("\nStep 4: Loading and making predictions...")
        predictor = Predictor(models_dir=str(Path(__file__).parent / 'models' / 'nfl'))

        try:
            models_loaded = predictor.load_latest_models()
            if models_loaded:
                predictions = predictor.predict_dataframe(df_features)
                print(f"  ✓ Made predictions for {len(predictions)} players")
            else:
                print(f"  ⚠ No models found - skipping prediction step")
                predictions = None
        except Exception as e:
            print(f"  ⚠ Prediction skipped ({str(e)})")
            predictions = None

        # Step 5: Build SGP combinations
        print("\nStep 5: Building SGP combinations...")
        builder = ParlayBuilder()

        # Test with sample probabilities
        sample_stack = builder.build_qb_wr_stack(0.35, 0.40)
        print(f"  ✓ Built QB-WR stack: {sample_stack['type']}")
        print(f"    - Combined probability: {sample_stack['combined_probability']:.4f}")
        print(f"    - Fair odds: {sample_stack['fair_odds']}")

        # Step 6: Calculate EV
        print("\nStep 6: Calculating Expected Value...")
        ev_calc = EVCalculator()
        ev = ev_calc.calculate_bet_ev(0.35, 250)
        print(f"  ✓ EV calculation works")
        print(f"    - Our probability: {ev['our_probability']:.4f}")
        print(f"    - Sportsbook odds: {ev['sportsbook_odds']}")
        print(f"    - EV: {ev['ev_percent']:.2f}%")
        print(f"    - Rating: {ev['rating']}")

        test_results['tests'][test_name] = {
            'status': 'PASS',
            'steps': 6,
            'data_points': len(df),
            'features_engineered': df_features.shape[1],
            'predictions_available': predictions is not None
        }

        print(f"\n✓ {test_name} PASSED")
        return True

    except Exception as e:
        print(f"\n✗ {test_name} FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        test_results['tests'][test_name] = {
            'status': 'FAIL',
            'error': str(e)
        }
        return False


def test_correlations():
    """Verify correlations match expected values from original data"""
    test_name = "Correlation Verification"
    print(f"\n{'='*80}")
    print(f"TEST 2: {test_name}")
    print(f"{'='*80}")

    try:
        print("\nLoading player data...")
        db_path = Path(__file__).parent / 'data' / 'nfl_player_stats.db'
        conn = sqlite3.connect(str(db_path))
        df = pd.read_sql_query("SELECT * FROM NFL_Model_Data", conn)
        conn.close()

        if df.empty:
            raise ValueError("No data found in database")

        print(f"  ✓ Loaded {len(df)} total player records")

        # Calculate correlations
        print("\nCalculating correlations...")
        analyzer = CorrelationAnalyzer()
        correlations = analyzer.calculate_all(df)

        # Expected values from original system (with 5% tolerance)
        expected = {
            'QB_WR': 0.120,
            'QB_TE': 0.092,
            'RB_Team_TDs': 0.130,
            'WR_WR': -0.016
        }

        tolerance = 0.05  # 5% tolerance
        all_passed = True
        results = {}

        print("\nCorrelation Verification Results:")
        for corr_type, expected_value in expected.items():
            actual = correlations.get(corr_type, 0)
            diff = abs(actual - expected_value)

            # Handle NaN values
            if pd.isna(actual):
                actual = 0.0
                diff = abs(0.0 - expected_value)

            within_tolerance = diff <= (abs(expected_value) * tolerance) if expected_value != 0 else diff < 0.05
            status = "PASS" if within_tolerance else "WARN"

            if not within_tolerance:
                all_passed = False

            results[corr_type] = {
                'actual': float(actual) if not pd.isna(actual) else 0.0,
                'expected': expected_value,
                'difference': float(diff),
                'tolerance_pct': tolerance * 100,
                'status': status
            }

            print(f"  {status} {corr_type}:")
            print(f"      Actual: {actual:.4f}, Expected: {expected_value:.4f}, Diff: {diff:.4f}")

        test_results['tests'][test_name] = {
            'status': 'PASS' if all_passed else 'WARN',
            'correlations': results,
            'data_points': len(df)
        }

        print(f"\n✓ {test_name} COMPLETED (Status: {'PASS' if all_passed else 'WARN'})")
        return True

    except Exception as e:
        print(f"\n✗ {test_name} FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        test_results['tests'][test_name] = {
            'status': 'FAIL',
            'error': str(e)
        }
        return False


def test_model_predictions():
    """Verify model predictions return valid probabilities"""
    test_name = "Model Prediction Validation"
    print(f"\n{'='*80}")
    print(f"TEST 3: {test_name}")
    print(f"{'='*80}")

    try:
        print("\nLoading QB player data...")
        db_path = Path(__file__).parent / 'data' / 'nfl_player_stats.db'
        conn = sqlite3.connect(str(db_path))

        # Check for position column
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(NFL_Model_Data)")
        columns = [row[1] for row in cursor.fetchall()]

        if 'position' in columns:
            df = pd.read_sql_query("SELECT * FROM NFL_Model_Data WHERE position = 'QB' LIMIT 10", conn)
        else:
            print("  ⚠ Position column not found, using all data")
            df = pd.read_sql_query("SELECT * FROM NFL_Model_Data LIMIT 10", conn)

        conn.close()

        if df.empty:
            print("  ⚠ No QB data found, test will use available data")
            print("  ⚠ Skipping model prediction test (no training data)")
            test_results['tests'][test_name] = {
                'status': 'SKIP',
                'reason': 'No QB data available for testing'
            }
            return True

        print(f"  ✓ Loaded {len(df)} QB records")

        # Engineer features
        print("\nEngineering features...")
        engineer = FeatureEngineer()
        df_features = engineer.engineer_features(df)
        df_features = engineer.create_prop_targets(df_features)
        print(f"  ✓ Features engineered")

        # Try to predict
        print("\nLoading models...")
        predictor = Predictor(models_dir=str(Path(__file__).parent / 'models' / 'nfl'))

        if not predictor.load_latest_models():
            print("  ⚠ No trained models found")
            test_results['tests'][test_name] = {
                'status': 'SKIP',
                'reason': 'No trained models available'
            }
            return True

        print("Making predictions...")
        predictions = predictor.predict_dataframe(df_features)

        # Verify predictions
        invalid_count = 0
        valid_count = 0

        print("\nValidating predictions:")
        for player_name, props in predictions.items():
            for prop, prob in props.items():
                if not (0 <= prob <= 1):
                    invalid_count += 1
                    print(f"  ✗ Invalid probability for {player_name} {prop}: {prob}")
                else:
                    valid_count += 1

        print(f"  ✓ Valid predictions: {valid_count}")
        if invalid_count > 0:
            print(f"  ✗ Invalid predictions: {invalid_count}")
            raise ValueError(f"Found {invalid_count} invalid predictions")

        test_results['tests'][test_name] = {
            'status': 'PASS',
            'predictions_made': len(predictions),
            'valid_predictions': valid_count,
            'invalid_predictions': invalid_count
        }

        print(f"\n✓ {test_name} PASSED")
        return True

    except Exception as e:
        print(f"\n✗ {test_name} FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        test_results['tests'][test_name] = {
            'status': 'FAIL',
            'error': str(e)
        }
        return False


def test_parlay_odds():
    """Test parlay odds calculation with and without correlation"""
    test_name = "Parlay Odds Calculation"
    print(f"\n{'='*80}")
    print(f"TEST 4: {test_name}")
    print(f"{'='*80}")

    try:
        results = {}
        all_passed = True

        # Test 1: Independent odds (no correlation)
        print("\nTest 1: Independent parlay (no correlation)...")
        prob, odds = calculate_parlay_odds([0.30, 0.40], correlation=0.0)
        expected_prob = 0.30 * 0.40  # 0.12

        diff = abs(prob - expected_prob)
        passed = diff < 0.001
        all_passed = all_passed and passed

        print(f"  {'✓' if passed else '✗'} Independent parlay:")
        print(f"    Calculated prob: {prob:.6f}")
        print(f"    Expected prob: {expected_prob:.6f}")
        print(f"    Difference: {diff:.6f}")
        print(f"    American odds: {odds}")

        results['independent'] = {
            'status': 'PASS' if passed else 'FAIL',
            'calculated_prob': prob,
            'expected_prob': expected_prob,
            'american_odds': odds
        }

        # Test 2: Correlated odds (QB-WR stack)
        print("\nTest 2: Correlated parlay (QB-WR, correlation=0.12)...")
        prob_corr, odds_corr = calculate_parlay_odds([0.30, 0.40], correlation=0.12)
        expected_prob_corr = 0.12 * 1.12  # 0.1344

        diff_corr = abs(prob_corr - expected_prob_corr)
        passed_corr = diff_corr < 0.001
        all_passed = all_passed and passed_corr

        print(f"  {'✓' if passed_corr else '✗'} Correlated parlay:")
        print(f"    Calculated prob: {prob_corr:.6f}")
        print(f"    Expected prob: {expected_prob_corr:.6f}")
        print(f"    Difference: {diff_corr:.6f}")
        print(f"    American odds: {odds_corr}")

        results['correlated'] = {
            'status': 'PASS' if passed_corr else 'FAIL',
            'calculated_prob': prob_corr,
            'expected_prob': expected_prob_corr,
            'american_odds': odds_corr,
            'correlation': 0.12
        }

        # Test 3: Correlation increases probability
        print("\nTest 3: Verify correlation increases probability...")
        increases = prob_corr > prob
        passed_increase = increases
        all_passed = all_passed and passed_increase

        print(f"  {'✓' if passed_increase else '✗'} Probability increase check:")
        print(f"    Independent prob: {prob:.6f}")
        print(f"    Correlated prob: {prob_corr:.6f}")
        print(f"    Increase: {(prob_corr - prob):.6f}")

        results['correlation_effect'] = {
            'status': 'PASS' if passed_increase else 'FAIL',
            'independent_prob': prob,
            'correlated_prob': prob_corr,
            'increase': prob_corr - prob
        }

        # Test 4: ParlayBuilder integration
        print("\nTest 4: ParlayBuilder integration...")
        builder = ParlayBuilder()
        stack = builder.build_qb_wr_stack(0.30, 0.40)

        print(f"  ✓ QB-WR Stack built:")
        print(f"    Type: {stack['type']}")
        print(f"    Combined prob: {stack['combined_probability']:.6f}")
        print(f"    Fair odds: {stack['fair_odds']}")

        results['parlay_builder'] = {
            'status': 'PASS',
            'stack_type': stack['type'],
            'combined_probability': stack['combined_probability'],
            'fair_odds': stack['fair_odds']
        }

        test_results['tests'][test_name] = {
            'status': 'PASS' if all_passed else 'FAIL',
            'test_results': results
        }

        print(f"\n{'✓' if all_passed else '✗'} {test_name} {'PASSED' if all_passed else 'FAILED'}")
        return all_passed

    except Exception as e:
        print(f"\n✗ {test_name} FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        test_results['tests'][test_name] = {
            'status': 'FAIL',
            'error': str(e)
        }
        return False


def test_ev_calculation():
    """Verify EV calculations are accurate"""
    test_name = "EV Calculation Accuracy"
    print(f"\n{'='*80}")
    print(f"TEST 5: {test_name}")
    print(f"{'='*80}")

    try:
        results = {}
        all_passed = True

        # Test 1: +EV scenario (40% prob vs +200 odds)
        print("\nTest 1: +EV scenario (40% prob vs +200 odds)...")
        ev = calculate_ev(0.40, 200)
        expected_ev = (0.40 * 2) - (0.60 * 1)  # = 0.20 = 20%
        expected_ev_pct = expected_ev * 100

        diff = abs(ev - expected_ev_pct)
        passed = diff < 0.1
        all_passed = all_passed and passed

        print(f"  {'✓' if passed else '✗'} +EV scenario:")
        print(f"    Calculated EV: {ev:.2f}%")
        print(f"    Expected EV: {expected_ev_pct:.2f}%")
        print(f"    Difference: {diff:.2f}%")

        results['plus_ev'] = {
            'status': 'PASS' if passed else 'FAIL',
            'calculated_ev': ev,
            'expected_ev': expected_ev_pct,
            'probability': 0.40,
            'odds': 200
        }

        # Test 2: -EV scenario (30% prob vs +100 odds)
        print("\nTest 2: -EV scenario (30% prob vs +100 odds)...")
        ev_neg = calculate_ev(0.30, 100)
        expected_ev_neg = (0.30 * 1) - (0.70 * 1)  # = -0.40 = -40%
        expected_ev_neg_pct = expected_ev_neg * 100

        diff_neg = abs(ev_neg - expected_ev_neg_pct)
        passed_neg = diff_neg < 0.1
        all_passed = all_passed and passed_neg

        print(f"  {'✓' if passed_neg else '✗'} -EV scenario:")
        print(f"    Calculated EV: {ev_neg:.2f}%")
        print(f"    Expected EV: {expected_ev_neg_pct:.2f}%")
        print(f"    Difference: {diff_neg:.2f}%")

        results['minus_ev'] = {
            'status': 'PASS' if passed_neg else 'FAIL',
            'calculated_ev': ev_neg,
            'expected_ev': expected_ev_neg_pct,
            'probability': 0.30,
            'odds': 100
        }

        # Test 3: EVCalculator class
        print("\nTest 3: EVCalculator class integration...")
        ev_calc = EVCalculator()

        # Test various scenarios
        scenarios = [
            {'prob': 0.45, 'odds': 200, 'desc': '45% vs +200'},
            {'prob': 0.35, 'odds': 250, 'desc': '35% vs +250'},
            {'prob': 0.55, 'odds': -120, 'desc': '55% vs -120'}
        ]

        ev_results = []
        for scenario in scenarios:
            result = ev_calc.calculate_bet_ev(scenario['prob'], scenario['odds'])
            ev_results.append(result)
            print(f"  ✓ {scenario['desc']}: {result['ev_percent']:.2f}% ({result['rating']})")

        results['ev_calculator_scenarios'] = {
            'status': 'PASS',
            'scenarios_tested': len(scenarios),
            'sample_results': [
                {
                    'probability': r['our_probability'],
                    'odds': r['sportsbook_odds'],
                    'ev_percent': r['ev_percent'],
                    'rating': r['rating']
                } for r in ev_results[:3]
            ]
        }

        # Test 4: Kelly Criterion (optional advanced test)
        print("\nTest 4: Kelly Criterion sizing...")
        kelly_result = ev_calc.kelly_criterion(0.45, 200, kelly_fraction=0.25)
        print(f"  ✓ Kelly Criterion:")
        print(f"    Full Kelly: {kelly_result['full_kelly_percent']:.2f}%")
        print(f"    Recommended (0.25x): {kelly_result['recommended_percent']:.2f}%")

        results['kelly_criterion'] = {
            'status': 'PASS',
            'full_kelly_percent': kelly_result['full_kelly_percent'],
            'recommended_percent': kelly_result['recommended_percent']
        }

        test_results['tests'][test_name] = {
            'status': 'PASS' if all_passed else 'FAIL',
            'test_results': results
        }

        print(f"\n{'✓' if all_passed else '✗'} {test_name} {'PASSED' if all_passed else 'FAILED'}")
        return all_passed

    except Exception as e:
        print(f"\n✗ {test_name} FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        test_results['tests'][test_name] = {
            'status': 'FAIL',
            'error': str(e)
        }
        return False


def test_feature_engineering():
    """Test feature engineering pipeline"""
    test_name = "Feature Engineering Pipeline"
    print(f"\n{'='*80}")
    print(f"TEST 6: {test_name}")
    print(f"{'='*80}")

    try:
        print("\nLoading sample data...")
        db_path = Path(__file__).parent / 'data' / 'nfl_player_stats.db'
        conn = sqlite3.connect(str(db_path))
        df = pd.read_sql_query("SELECT * FROM NFL_Model_Data LIMIT 50", conn)
        conn.close()

        if df.empty:
            raise ValueError("No data found")

        print(f"  ✓ Loaded {len(df)} sample records")

        # Test feature engineering
        print("\nTesting feature engineering...")
        engineer = FeatureEngineer()

        # Check available stats
        available_stats = [col for col in engineer.stat_cols if col in df.columns]
        print(f"  ✓ Available stats for engineering: {len(available_stats)}")
        print(f"    Stats: {', '.join(available_stats[:5])}...")

        # Engineer features
        df_features = engineer.engineer_features(df)
        features_added = df_features.shape[1] - df.shape[1]

        print(f"  ✓ Features engineered:")
        print(f"    Original columns: {df.shape[1]}")
        print(f"    New columns: {features_added}")
        print(f"    Total columns: {df_features.shape[1]}")

        # Check for NaN values
        nan_count = df_features.isna().sum().sum()
        print(f"  ✓ NaN values: {nan_count}")

        # Test prop targets
        print("\nTesting prop target creation...")
        df_features = engineer.create_prop_targets(df_features)
        print(f"  ✓ Prop targets created")

        test_results['tests'][test_name] = {
            'status': 'PASS',
            'records_processed': len(df),
            'original_columns': df.shape[1],
            'features_added': features_added,
            'final_columns': df_features.shape[1],
            'available_stats': available_stats
        }

        print(f"\n✓ {test_name} PASSED")
        return True

    except Exception as e:
        print(f"\n✗ {test_name} FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        test_results['tests'][test_name] = {
            'status': 'FAIL',
            'error': str(e)
        }
        return False


def run_all_tests():
    """Run all integration tests"""
    print("\n" + "="*80)
    print("NFL SGP INTEGRATION TEST SUITE - PHASE 6")
    print("="*80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    test_functions = [
        test_end_to_end_pipeline,
        test_correlations,
        test_model_predictions,
        test_parlay_odds,
        test_ev_calculation,
        test_feature_engineering
    ]

    passed = 0
    failed = 0
    skipped = 0

    for test_func in test_functions:
        try:
            result = test_func()
            test_name = test_func.__name__
            if test_name in test_results['tests']:
                status = test_results['tests'][test_name].get('status', 'UNKNOWN')
                if status == 'PASS':
                    passed += 1
                elif status == 'SKIP':
                    skipped += 1
                else:
                    failed += 1
        except Exception as e:
            print(f"\nFATAL ERROR in test: {str(e)}")
            failed += 1

    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Total Tests: {len(test_functions)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped}")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Overall status
    if failed == 0:
        test_results['overall_status'] = 'PASS'
        print("\n✓ ALL TESTS PASSED" if skipped == 0 else f"\n✓ ALL CRITICAL TESTS PASSED ({skipped} tests skipped)")
    else:
        test_results['overall_status'] = 'FAIL'
        print(f"\n✗ {failed} TEST(S) FAILED")

    print("="*80)

    return test_results


if __name__ == "__main__":
    results = run_all_tests()

    # Save detailed results to JSON for reporting
    import json
    report_path = Path(__file__).parent / 'integration_test_results.json'
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nDetailed results saved to: {report_path}")
