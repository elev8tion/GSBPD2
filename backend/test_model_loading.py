#!/usr/bin/env python3
"""Test script to verify all NFL model files load correctly."""

import pickle
from pathlib import Path
import json

def test_models():
    models_dir = Path('/Users/kcdacre8tor/GSBPD2/backend/models/nfl')
    results = []

    # Test all SGP models
    for model_file in sorted(models_dir.glob('sgp_*.pkl')):
        try:
            with open(model_file, 'rb') as f:
                model_data = pickle.load(f)

            result = {
                'file': model_file.name,
                'size_mb': round(model_file.stat().st_size / (1024 * 1024), 2),
                'status': 'OK',
                'keys': list(model_data.keys()),
            }

            if 'feature_cols' in model_data:
                result['num_features'] = len(model_data['feature_cols'])

            if 'results' in model_data:
                best_model = max(model_data['results'], key=lambda k: model_data['results'][k]['auc'])
                result['best_model'] = best_model
                result['accuracy'] = round(model_data['results'][best_model]['accuracy'], 3)
                result['auc'] = round(model_data['results'][best_model]['auc'], 3)
                result['log_loss'] = round(model_data['results'][best_model]['log_loss'], 3)

            results.append(result)
            print(f"✓ {model_file.name}")
            print(f"  Size: {result['size_mb']}MB")
            print(f"  Keys: {result['keys']}")
            if 'num_features' in result:
                print(f"  Features: {result['num_features']}")
            if 'best_model' in result:
                print(f"  Best Model: {result['best_model']}")
                print(f"  Accuracy: {result['accuracy']}")
                print(f"  AUC: {result['auc']}")
            print()

        except Exception as e:
            result = {
                'file': model_file.name,
                'status': 'ERROR',
                'error': str(e)
            }
            results.append(result)
            print(f"✗ {model_file.name}: {e}")
            print()

    # Test correlations file
    corr_file = models_dir / 'correlations_20251128_105035.pkl'
    if corr_file.exists():
        try:
            with open(corr_file, 'rb') as f:
                corr_data = pickle.load(f)

            result = {
                'file': corr_file.name,
                'size_kb': round(corr_file.stat().st_size / 1024, 2),
                'status': 'OK',
                'correlations': corr_data
            }
            results.append(result)

            print(f"✓ {corr_file.name}")
            print(f"  Size: {result['size_kb']}KB")
            print(f"  Correlations: {json.dumps(corr_data, indent=4)}")
            print()

        except Exception as e:
            result = {
                'file': corr_file.name,
                'status': 'ERROR',
                'error': str(e)
            }
            results.append(result)
            print(f"✗ {corr_file.name}: {e}")
            print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    successful = sum(1 for r in results if r['status'] == 'OK')
    print(f"Total files: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(results) - successful}")

    # Save results to JSON
    output_file = models_dir / 'model_test_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {output_file}")

    return results

if __name__ == '__main__':
    results = test_models()
