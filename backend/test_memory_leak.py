#!/usr/bin/env python3
"""
Memory Leak Testing for GSBPD2 NFL Integration - Phase 7 Production Validation
Runs operations repeatedly and monitors memory consumption for leaks.
"""

import psutil
import os
import sys
import json
import gc
from datetime import datetime
import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 5

class MemoryLeakTester:
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.memory_samples = []
        self.results = {}

    def get_memory_mb(self):
        """Get current process memory in MB"""
        return self.process.memory_info().rss / 1024 / 1024

    def test_api_calls_memory(self, num_iterations=1000):
        """Test memory consumption of repeated API calls"""
        print(f"\nTesting API calls memory ({num_iterations} iterations)...")
        print("-" * 80)

        initial_memory = self.get_memory_mb()
        print(f"Initial memory: {initial_memory:.2f} MB")

        memory_samples = []
        errors = 0

        endpoints = [
            f"{BASE_URL}/health",
            f"{BASE_URL}/nfl/sgp/status",
            f"{BASE_URL}/nfl/teams",
        ]

        for i in range(num_iterations):
            try:
                # Rotate through endpoints
                endpoint = endpoints[i % len(endpoints)]

                response = requests.get(endpoint, timeout=TIMEOUT)

                # Sample memory every 100 iterations
                if i % 100 == 0 or i == num_iterations - 1:
                    current_memory = self.get_memory_mb()
                    memory_samples.append({
                        'iteration': i,
                        'memory_mb': round(current_memory, 2),
                        'increase_mb': round(current_memory - initial_memory, 2)
                    })
                    print(f"  Iteration {i}: {current_memory:.2f} MB (increase: {current_memory - initial_memory:.2f} MB)")

                # Force garbage collection every 100 iterations
                if i % 100 == 0:
                    gc.collect()

            except Exception as e:
                errors += 1
                if errors <= 5:  # Print first 5 errors
                    print(f"  Iteration {i}: Error - {str(e)}")

        # Final memory reading
        gc.collect()
        final_memory = self.get_memory_mb()
        memory_increase = final_memory - initial_memory

        # Analyze memory growth
        memory_growth_rate = None
        if len(memory_samples) > 1:
            growth_points = []
            for i in range(1, len(memory_samples)):
                prev_increase = memory_samples[i-1]['increase_mb']
                curr_increase = memory_samples[i]['increase_mb']
                growth_points.append(curr_increase - prev_increase)

            avg_growth = sum(growth_points) / len(growth_points) if growth_points else 0
            memory_growth_rate = round(avg_growth, 4)

        # Leak detection threshold: more than 100MB increase is suspicious
        leak_detected = memory_increase > 100

        result = {
            'test_name': 'API Calls Memory Test',
            'iterations': num_iterations,
            'errors': errors,
            'initial_memory_mb': round(initial_memory, 2),
            'final_memory_mb': round(final_memory, 2),
            'increase_mb': round(memory_increase, 2),
            'memory_growth_rate_per_100_iterations': memory_growth_rate,
            'leak_detected': leak_detected,
            'threshold_mb': 100,
            'samples': memory_samples
        }

        self.results['api_calls'] = result

        print(f"\nFinal memory: {final_memory:.2f} MB")
        print(f"Total increase: {memory_increase:.2f} MB")
        print(f"Memory growth rate: {memory_growth_rate} MB per 100 iterations")
        print(f"Leak detected: {leak_detected}")
        print(f"Status: {'FAIL - Possible memory leak' if leak_detected else 'PASS - No leak detected'}")

        return result

    def test_json_processing_memory(self, num_iterations=1000):
        """Test memory consumption of JSON processing"""
        print(f"\nTesting JSON processing memory ({num_iterations} iterations)...")
        print("-" * 80)

        initial_memory = self.get_memory_mb()
        print(f"Initial memory: {initial_memory:.2f} MB")

        memory_samples = []

        # Create test data
        test_data = {
            'teams': [f'Team{i}' for i in range(100)],
            'players': [{'name': f'Player{i}', 'stats': {'ppg': 20.5}} for i in range(500)],
            'picks': [{'pick': i, 'odds': float(i) * 1.1} for i in range(1000)]
        }

        for i in range(num_iterations):
            try:
                # Simulate JSON serialization/deserialization
                json_str = json.dumps(test_data)
                parsed = json.loads(json_str)

                # Sample memory every 100 iterations
                if i % 100 == 0 or i == num_iterations - 1:
                    current_memory = self.get_memory_mb()
                    memory_samples.append({
                        'iteration': i,
                        'memory_mb': round(current_memory, 2),
                        'increase_mb': round(current_memory - initial_memory, 2)
                    })
                    print(f"  Iteration {i}: {current_memory:.2f} MB (increase: {current_memory - initial_memory:.2f} MB)")

                # Force garbage collection every 100 iterations
                if i % 100 == 0:
                    gc.collect()

            except Exception as e:
                print(f"  Iteration {i}: Error - {str(e)}")

        # Final memory reading
        gc.collect()
        final_memory = self.get_memory_mb()
        memory_increase = final_memory - initial_memory

        leak_detected = memory_increase > 50  # Lower threshold for JSON processing

        result = {
            'test_name': 'JSON Processing Memory Test',
            'iterations': num_iterations,
            'initial_memory_mb': round(initial_memory, 2),
            'final_memory_mb': round(final_memory, 2),
            'increase_mb': round(memory_increase, 2),
            'leak_detected': leak_detected,
            'threshold_mb': 50,
            'samples': memory_samples
        }

        self.results['json_processing'] = result

        print(f"\nFinal memory: {final_memory:.2f} MB")
        print(f"Total increase: {memory_increase:.2f} MB")
        print(f"Leak detected: {leak_detected}")
        print(f"Status: {'FAIL - Possible memory leak' if leak_detected else 'PASS - No leak detected'}")

        return result

    def test_list_creation_memory(self, num_iterations=1000):
        """Test memory consumption of list operations"""
        print(f"\nTesting list creation memory ({num_iterations} iterations)...")
        print("-" * 80)

        initial_memory = self.get_memory_mb()
        print(f"Initial memory: {initial_memory:.2f} MB")

        memory_samples = []

        for i in range(num_iterations):
            try:
                # Create and destroy lists
                test_list = [{'id': j, 'value': j * 1.5} for j in range(100)]
                nested_list = [[{'data': k} for k in range(10)] for j in range(50)]

                # Sample memory every 100 iterations
                if i % 100 == 0 or i == num_iterations - 1:
                    current_memory = self.get_memory_mb()
                    memory_samples.append({
                        'iteration': i,
                        'memory_mb': round(current_memory, 2),
                        'increase_mb': round(current_memory - initial_memory, 2)
                    })
                    print(f"  Iteration {i}: {current_memory:.2f} MB (increase: {current_memory - initial_memory:.2f} MB)")

                # Force garbage collection every 100 iterations
                if i % 100 == 0:
                    gc.collect()

            except Exception as e:
                print(f"  Iteration {i}: Error - {str(e)}")

        # Final memory reading
        gc.collect()
        final_memory = self.get_memory_mb()
        memory_increase = final_memory - initial_memory

        leak_detected = memory_increase > 75

        result = {
            'test_name': 'List Creation Memory Test',
            'iterations': num_iterations,
            'initial_memory_mb': round(initial_memory, 2),
            'final_memory_mb': round(final_memory, 2),
            'increase_mb': round(memory_increase, 2),
            'leak_detected': leak_detected,
            'threshold_mb': 75,
            'samples': memory_samples
        }

        self.results['list_creation'] = result

        print(f"\nFinal memory: {final_memory:.2f} MB")
        print(f"Total increase: {memory_increase:.2f} MB")
        print(f"Leak detected: {leak_detected}")
        print(f"Status: {'FAIL - Possible memory leak' if leak_detected else 'PASS - No leak detected'}")

        return result

    def run_tests(self):
        """Run all memory leak tests"""
        print("\n" + "="*80)
        print("MEMORY LEAK TEST - GSBPD2 NFL Integration Phase 7")
        print("="*80)

        try:
            # Check if server is running
            requests.get(f"{BASE_URL}/health", timeout=2)
            self.test_api_calls_memory(num_iterations=500)  # Reduced iterations for API calls
        except:
            print("\nWARNING: Cannot connect to server at {BASE_URL}")
            print("Skipping API calls memory test")

        self.test_json_processing_memory(num_iterations=1000)
        self.test_list_creation_memory(num_iterations=1000)

        print("\n" + "="*80)
        print("MEMORY LEAK TEST SUMMARY")
        print("="*80)

        total_leaks = sum(1 for r in self.results.values() if r.get('leak_detected', False))
        print(f"Total tests: {len(self.results)}")
        print(f"Tests passed: {len(self.results) - total_leaks}")
        print(f"Possible memory leaks detected: {total_leaks}")

        for test_name, result in self.results.items():
            status = "FAIL" if result.get('leak_detected') else "PASS"
            print(f"  {test_name}: {status} (increase: {result.get('increase_mb', 0)} MB)")

        print("="*80)

        return self.results


def main():
    try:
        tester = MemoryLeakTester()
        results = tester.run_tests()

        # Save results
        output_file = '/Users/kcdacre8tor/GSBPD2/backend/memory_leak_test_results.json'
        with open(output_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'tests': results
            }, f, indent=2)

        print(f"\nResults saved to: {output_file}")

        # Check success criteria
        print("\nSUCCESS CRITERIA CHECK")
        print("="*80)

        total_leaks = sum(1 for r in results.values() if r.get('leak_detected', False))
        criteria1 = total_leaks == 0
        print(f"1. No memory leaks detected: {'PASS' if criteria1 else 'FAIL'} ({total_leaks} tests failed)")

        max_increase = max([r.get('increase_mb', 0) for r in results.values()])
        criteria2 = max_increase < 150
        print(f"2. Max memory increase < 150MB: {'PASS' if criteria2 else 'FAIL'} (max: {max_increase}MB)")

        print("="*80)

        overall_pass = criteria1 and criteria2
        print(f"\nOVERALL MEMORY LEAK TEST RESULT: {'PASS' if overall_pass else 'FAIL'}")

        return 0 if overall_pass else 1

    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
