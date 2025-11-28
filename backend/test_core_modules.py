"""
Test script for core module migration
Tests imports and basic functionality of all 7 migrated modules
"""

import sys
from pathlib import Path

# Add backend to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def test_odds_calculator():
    """Test odds_calculator module"""
    print("\n" + "="*80)
    print("TEST 1: odds_calculator")
    print("="*80)

    try:
        from src.core.odds_calculator import calculate_ev
        result = calculate_ev(0.40, 200)
        assert result > 0, "EV calculation failed"
        print(f"✅ calculate_ev(0.40, 200) = {result:.2f}%")
        print("✅ odds_calculator module imported successfully")
        return True
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_correlations():
    """Test correlations module"""
    print("\n" + "="*80)
    print("TEST 2: correlations")
    print("="*80)

    try:
        from src.core.correlations import CorrelationAnalyzer
        analyzer = CorrelationAnalyzer()
        assert hasattr(analyzer, 'calculate_qb_wr_correlation'), "CorrelationAnalyzer missing method"
        print("✅ CorrelationAnalyzer instantiated successfully")
        print(f"✅ Has methods: {[m for m in dir(analyzer) if not m.startswith('_')]}")
        return True
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_feature_engineering():
    """Test feature_engineering module"""
    print("\n" + "="*80)
    print("TEST 3: feature_engineering")
    print("="*80)

    try:
        from src.core.feature_engineering import FeatureEngineer
        engineer = FeatureEngineer()
        assert hasattr(engineer, 'engineer_features'), "FeatureEngineer missing method"
        print("✅ FeatureEngineer instantiated successfully")
        print(f"✅ Stat columns configured: {len(engineer.stat_cols)}")
        return True
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_model_trainer():
    """Test model_trainer module"""
    print("\n" + "="*80)
    print("TEST 4: model_trainer")
    print("="*80)

    try:
        from src.core.model_trainer import ModelTrainer
        trainer = ModelTrainer()
        assert hasattr(trainer, 'train_prop_model'), "ModelTrainer missing method"
        print("✅ ModelTrainer instantiated successfully")
        print(f"✅ Prop types configured: {len(trainer.prop_types)}")
        print(f"✅ Models dir: {trainer.models_dir}")
        return True
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_model_predictor():
    """Test model_predictor module"""
    print("\n" + "="*80)
    print("TEST 5: model_predictor")
    print("="*80)

    try:
        from src.core.model_predictor import Predictor
        predictor = Predictor()
        assert hasattr(predictor, 'predict_dataframe'), "Predictor missing method"
        print("✅ Predictor instantiated successfully")
        print(f"✅ Models loaded: {len(predictor.models)}")
        return True
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_parlay_builder():
    """Test parlay_builder module"""
    print("\n" + "="*80)
    print("TEST 6: parlay_builder")
    print("="*80)

    try:
        from src.core.parlay_builder import ParlayBuilder
        builder = ParlayBuilder()
        assert hasattr(builder, 'build_from_predictions'), "ParlayBuilder missing method"

        # Test QB-WR stack
        parlay = builder.build_qb_wr_stack(0.40, 0.30)
        print(f"✅ ParlayBuilder instantiated successfully")
        print(f"✅ Test parlay: {parlay['combined_probability']:.3f} probability, {parlay['fair_odds']}")
        return True
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ev_calculator():
    """Test ev_calculator module"""
    print("\n" + "="*80)
    print("TEST 7: ev_calculator")
    print("="*80)

    try:
        from src.core.ev_calculator import EVCalculator
        ev_calc = EVCalculator()
        assert hasattr(ev_calc, 'calculate_bet_ev'), "EVCalculator missing method"

        # Test EV calculation
        result = ev_calc.calculate_bet_ev(0.40, 200)
        print(f"✅ EVCalculator instantiated successfully")
        print(f"✅ Test EV: {result['ev_percent']:.2f}% ({result['rating']})")
        return True
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_all_imports():
    """Test importing all modules from __init__"""
    print("\n" + "="*80)
    print("TEST 8: __init__.py imports")
    print("="*80)

    try:
        from src.core import (
            american_to_decimal,
            decimal_to_american,
            calculate_ev,
            calculate_parlay_odds,
            compare_odds,
            CorrelationAnalyzer,
            FeatureEngineer,
            ModelTrainer,
            Predictor,
            ParlayBuilder,
            EVCalculator
        )

        print("✅ All modules imported from src.core successfully")
        print(f"✅ Functions: american_to_decimal, decimal_to_american, calculate_ev, calculate_parlay_odds, compare_odds")
        print(f"✅ Classes: CorrelationAnalyzer, FeatureEngineer, ModelTrainer, Predictor, ParlayBuilder, EVCalculator")
        return True
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("CORE MODULE MIGRATION TEST SUITE")
    print("="*80)

    tests = [
        test_odds_calculator,
        test_correlations,
        test_feature_engineering,
        test_model_trainer,
        test_model_predictor,
        test_parlay_builder,
        test_ev_calculator,
        test_all_imports
    ]

    results = []
    for test in tests:
        results.append(test())

    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)

    passed = sum(results)
    total = len(results)

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Core module migration successful!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
