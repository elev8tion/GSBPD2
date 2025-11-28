#!/usr/bin/env python3
"""
Performance Benchmarking for GSBPD2 NFL Integration - Phase 7 Production Validation
Measures response times and throughput for key operations.
"""

import time
import json
from datetime import datetime
import requests
import sys

BASE_URL = "http://localhost:8000"
TIMEOUT = 5

class PerformanceBenchmark:
    def __init__(self):
        self.benchmarks = {}

    def benchmark_endpoint(self, endpoint_url, name, iterations=5):
        """Benchmark an endpoint with multiple iterations"""
        times = []
        errors = 0

        print(f"Benchmarking: {name}")
        print(f"  URL: {endpoint_url}")
        print(f"  Iterations: {iterations}")

        for i in range(iterations):
            try:
                start = time.time()
                response = requests.get(endpoint_url, timeout=TIMEOUT)
                elapsed = (time.time() - start) * 1000  # ms

                if response.status_code == 200:
                    times.append(elapsed)
                else:
                    errors += 1
                    print(f"  Iteration {i+1}: Status {response.status_code}")

            except Exception as e:
                errors += 1
                print(f"  Iteration {i+1}: Error - {str(e)}")

        if times:
            benchmark_result = {
                'name': name,
                'url': endpoint_url,
                'iterations': iterations,
                'successful': len(times),
                'errors': errors,
                'avg_ms': round(sum(times) / len(times), 2),
                'min_ms': round(min(times), 2),
                'max_ms': round(max(times), 2),
                'total_time_ms': round(sum(times), 2)
            }
        else:
            benchmark_result = {
                'name': name,
                'url': endpoint_url,
                'iterations': iterations,
                'successful': 0,
                'errors': errors,
                'avg_ms': 0,
                'min_ms': 0,
                'max_ms': 0,
                'total_time_ms': 0
            }

        self.benchmarks[name] = benchmark_result

        print(f"  Average time: {benchmark_result['avg_ms']}ms")
        print(f"  Min time: {benchmark_result['min_ms']}ms")
        print(f"  Max time: {benchmark_result['max_ms']}ms")
        print(f"  Success rate: {round((benchmark_result['successful'] / iterations) * 100, 1)}%")
        print()

        return benchmark_result

    def run_benchmarks(self):
        """Run all performance benchmarks"""
        print("\n" + "="*80)
        print("PERFORMANCE BENCHMARK - GSBPD2 NFL Integration Phase 7")
        print("="*80)
        print(f"Base URL: {BASE_URL}")
        print("="*80 + "\n")

        # Benchmark endpoints
        endpoints = [
            (f"{BASE_URL}/health", "Health Check", 10),
            (f"{BASE_URL}/nfl/sgp/weekly/12?season=2024", "NFL SGP Weekly Picks", 5),
            (f"{BASE_URL}/nfl/sgp/correlations", "SGP Correlations", 5),
            (f"{BASE_URL}/nfl/sgp/status", "SGP Service Status", 5),
            (f"{BASE_URL}/nfl/teams", "Get NFL Teams", 5),
            (f"{BASE_URL}/nfl/players", "Get NFL Players", 3),
            (f"{BASE_URL}/portfolio", "Get Portfolio", 5),
            (f"{BASE_URL}/memories/list", "List Memories", 5),
            (f"{BASE_URL}/nba/teams", "Get NBA Teams", 3),
            (f"{BASE_URL}/nba/games", "Get NBA Games", 3),
        ]

        for endpoint_url, name, iterations in endpoints:
            self.benchmark_endpoint(endpoint_url, name, iterations)

        # Calculate summary statistics
        print("\n" + "="*80)
        print("PERFORMANCE BENCHMARK SUMMARY")
        print("="*80)

        total_endpoints = len(self.benchmarks)
        avg_times = [b['avg_ms'] for b in self.benchmarks.values()]
        max_times = [b['max_ms'] for b in self.benchmarks.values()]

        print(f"Total endpoints benchmarked: {total_endpoints}")
        print(f"Overall average response time: {round(sum(avg_times) / len(avg_times), 2)}ms")
        print(f"Overall max response time: {round(max(max_times), 2)}ms")
        print(f"Overall min response time: {round(min([b['min_ms'] for b in self.benchmarks.values()]), 2)}ms")

        # Categorize performance
        print("\nPerformance Categories:")
        fast = [b for b in self.benchmarks.values() if b['avg_ms'] < 100]
        normal = [b for b in self.benchmarks.values() if 100 <= b['avg_ms'] < 500]
        slow = [b for b in self.benchmarks.values() if 500 <= b['avg_ms'] < 2000]
        very_slow = [b for b in self.benchmarks.values() if b['avg_ms'] >= 2000]

        print(f"  Fast (< 100ms): {len(fast)} endpoints")
        print(f"  Normal (100-500ms): {len(normal)} endpoints")
        print(f"  Slow (500-2000ms): {len(slow)} endpoints")
        print(f"  Very Slow (>= 2000ms): {len(very_slow)} endpoints")

        print("\n" + "="*80)

        return self.benchmarks

    def get_summary(self):
        """Get summary statistics"""
        if not self.benchmarks:
            return None

        successful_benchmarks = [b for b in self.benchmarks.values() if b['successful'] > 0]
        failed_benchmarks = [b for b in self.benchmarks.values() if b['successful'] == 0]

        avg_times = [b['avg_ms'] for b in successful_benchmarks]

        summary = {
            'total_endpoints': len(self.benchmarks),
            'successful_endpoints': len(successful_benchmarks),
            'failed_endpoints': len(failed_benchmarks),
            'avg_response_time_ms': round(sum(avg_times) / len(avg_times), 2) if avg_times else 0,
            'max_response_time_ms': round(max([b['max_ms'] for b in successful_benchmarks], default=0), 2),
            'min_response_time_ms': round(min([b['min_ms'] for b in successful_benchmarks], default=0), 2),
            'p95_response_time_ms': round(sorted(avg_times)[int(len(avg_times) * 0.95)] if avg_times else 0, 2),
            'endpoints_under_2sec': len([b for b in successful_benchmarks if b['avg_ms'] < 2000]),
            'endpoints_under_500ms': len([b for b in successful_benchmarks if b['avg_ms'] < 500])
        }

        return summary


def main():
    try:
        # Check if server is running
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
        except:
            print(f"ERROR: Cannot connect to server at {BASE_URL}")
            print("Please start the FastAPI server with: python main.py")
            sys.exit(1)

        # Run benchmarks
        benchmark = PerformanceBenchmark()
        results = benchmark.run_benchmarks()
        summary = benchmark.get_summary()

        # Save results
        output_file = '/Users/kcdacre8tor/GSBPD2/backend/performance_benchmark_results.json'
        with open(output_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'summary': summary,
                'benchmarks': results
            }, f, indent=2)

        print(f"\nResults saved to: {output_file}")

        # Check success criteria
        print("\nSUCCESS CRITERIA CHECK")
        print("="*80)

        # Criteria 1: Average response time < 2000ms
        criteria1 = summary['avg_response_time_ms'] < 2000
        print(f"1. Average response time < 2000ms: {'PASS' if criteria1 else 'FAIL'} ({summary['avg_response_time_ms']}ms)")

        # Criteria 2: All endpoints respond
        criteria2 = summary['failed_endpoints'] == 0
        print(f"2. All endpoints responding: {'PASS' if criteria2 else 'FAIL'} ({summary['failed_endpoints']} failed)")

        # Criteria 3: 95% of endpoints under 2000ms
        criteria3 = summary['endpoints_under_2sec'] >= (summary['total_endpoints'] * 0.95)
        print(f"3. 95%+ endpoints under 2000ms: {'PASS' if criteria3 else 'FAIL'} ({summary['endpoints_under_2sec']}/{summary['total_endpoints']})")

        # Criteria 4: Key endpoints under 500ms
        criteria4 = summary['endpoints_under_500ms'] >= 5
        print(f"4. At least 5 endpoints under 500ms: {'PASS' if criteria4 else 'FAIL'} ({summary['endpoints_under_500ms']} endpoints)")

        print("="*80)

        overall_pass = criteria1 and criteria2 and criteria3 and criteria4
        print(f"\nOVERALL PERFORMANCE BENCHMARK RESULT: {'PASS' if overall_pass else 'FAIL'}")

        return 0 if overall_pass else 1

    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
