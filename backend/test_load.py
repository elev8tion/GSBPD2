#!/usr/bin/env python3
"""
Load Testing for GSBPD2 NFL Integration - Phase 7 Production Validation
Tests concurrent requests to key endpoints and measures performance metrics.
"""

import concurrent.futures
import requests
import time
from statistics import mean, median, stdev
import json
from datetime import datetime
import sys

# Configuration
BASE_URL = "http://localhost:8000"
NUM_REQUESTS = 100
MAX_WORKERS = 10
TIMEOUT = 5

class LoadTester:
    def __init__(self, base_url=BASE_URL, timeout=TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
        self.results = {}

    def load_test_endpoint(self, endpoint_url, num_requests=NUM_REQUESTS, name=""):
        """Send num_requests to endpoint and measure performance"""
        response_times = []
        errors = 0
        error_details = []
        status_codes = {}

        def make_request():
            start = time.time()
            try:
                response = requests.get(endpoint_url, timeout=self.timeout)
                elapsed = (time.time() - start) * 1000  # ms

                # Track status codes
                status_code = response.status_code
                if status_code not in status_codes:
                    status_codes[status_code] = 0
                status_codes[status_code] += 1

                if status_code == 200:
                    return elapsed, None
                else:
                    return None, f"Status {status_code}"
            except requests.exceptions.Timeout:
                error_details.append("Timeout")
                return None, "Timeout"
            except requests.exceptions.ConnectionError:
                error_details.append("Connection Error")
                return None, "Connection Error"
            except Exception as e:
                error_details.append(str(e))
                return None, str(e)

        # Run concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(make_request) for _ in range(num_requests)]
            for future in concurrent.futures.as_completed(futures):
                result, error = future.result()
                if result is not None:
                    response_times.append(result)
                else:
                    errors += 1

        # Calculate statistics
        stats = {
            'endpoint_name': name,
            'url': endpoint_url,
            'total_requests': num_requests,
            'successful': len(response_times),
            'errors': errors,
            'error_rate': round((errors / num_requests) * 100, 2),
            'status_codes': status_codes,
            'avg_time_ms': round(mean(response_times), 2) if response_times else 0,
            'median_time_ms': round(median(response_times), 2) if response_times else 0,
            'max_time_ms': round(max(response_times), 2) if response_times else 0,
            'min_time_ms': round(min(response_times), 2) if response_times else 0,
            'stdev_ms': round(stdev(response_times), 2) if len(response_times) > 1 else 0,
            'requests_per_sec': round(num_requests / (max(response_times) / 1000 if response_times else 1), 2)
        }

        return stats

    def run_load_tests(self):
        """Run load tests on key endpoints"""

        endpoints = [
            (f"{self.base_url}/health", "Health Check"),
            (f"{self.base_url}/nfl/sgp/weekly/12?season=2024", "NFL SGP Weekly Picks"),
            (f"{self.base_url}/nfl/sgp/correlations", "SGP Correlations"),
            (f"{self.base_url}/nfl/sgp/status", "SGP Service Status"),
            (f"{self.base_url}/nfl/teams", "Get NFL Teams"),
            (f"{self.base_url}/nfl/players", "Get NFL Players"),
            (f"{self.base_url}/portfolio", "Get Portfolio"),
            (f"{self.base_url}/memories/list", "List Memories"),
        ]

        print("\n" + "="*80)
        print("LOAD TEST - GSBPD2 NFL Integration Phase 7")
        print("="*80)
        print(f"Base URL: {self.base_url}")
        print(f"Requests per endpoint: {NUM_REQUESTS}")
        print(f"Concurrent workers: {MAX_WORKERS}")
        print(f"Timeout: {TIMEOUT}s")
        print("="*80 + "\n")

        for endpoint_url, endpoint_name in endpoints:
            print(f"Testing: {endpoint_name}")
            print(f"  URL: {endpoint_url}")
            print(f"  Sending {NUM_REQUESTS} concurrent requests...")

            try:
                result = self.load_test_endpoint(endpoint_url, num_requests=NUM_REQUESTS, name=endpoint_name)
                self.results[endpoint_name] = result

                # Print results
                print(f"  Results:")
                print(f"    Successful: {result['successful']}/{result['total_requests']}")
                print(f"    Error Rate: {result['error_rate']}%")
                print(f"    Avg Response Time: {result['avg_time_ms']}ms")
                print(f"    Median Response Time: {result['median_time_ms']}ms")
                print(f"    Min/Max Response Time: {result['min_time_ms']}/{result['max_time_ms']}ms")
                print(f"    Std Dev: {result['stdev_ms']}ms")
                print(f"    Status Codes: {result['status_codes']}")
                print()
            except Exception as e:
                print(f"  ERROR: {str(e)}")
                self.results[endpoint_name] = {
                    'endpoint_name': endpoint_name,
                    'url': endpoint_url,
                    'error': str(e),
                    'total_requests': NUM_REQUESTS,
                    'successful': 0,
                    'errors': NUM_REQUESTS,
                    'error_rate': 100.0
                }
                print()

        return self.results

    def get_summary(self):
        """Get summary statistics"""
        if not self.results:
            return None

        successful_endpoints = [r for r in self.results.values() if r.get('successful', 0) > 0]
        failed_endpoints = [r for r in self.results.values() if r.get('successful', 0) == 0]

        avg_response_times = [r['avg_time_ms'] for r in successful_endpoints if 'avg_time_ms' in r]

        summary = {
            'total_endpoints_tested': len(self.results),
            'successful_endpoints': len(successful_endpoints),
            'failed_endpoints': len(failed_endpoints),
            'avg_response_time_across_all': round(mean(avg_response_times), 2) if avg_response_times else 0,
            'max_response_time': round(max([r['max_time_ms'] for r in successful_endpoints if 'max_time_ms' in r], default=0), 2),
            'min_response_time': round(min([r['min_time_ms'] for r in successful_endpoints if 'min_time_ms' in r], default=0), 2),
            'total_requests': NUM_REQUESTS * len(self.results),
            'total_successful': sum([r['successful'] for r in self.results.values()]),
            'total_errors': sum([r['errors'] for r in self.results.values()]),
            'overall_error_rate': round((sum([r['errors'] for r in self.results.values()]) / (NUM_REQUESTS * len(self.results))) * 100, 2)
        }

        return summary


def main():
    try:
        # Check if server is running
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
            print(f"Server status: {response.status_code}")
        except:
            print("ERROR: Cannot connect to server at {BASE_URL}")
            print("Please start the FastAPI server with: python main.py")
            sys.exit(1)

        # Run load tests
        tester = LoadTester()
        results = tester.run_load_tests()

        # Print summary
        summary = tester.get_summary()
        print("\n" + "="*80)
        print("LOAD TEST SUMMARY")
        print("="*80)
        print(f"Total endpoints tested: {summary['total_endpoints_tested']}")
        print(f"Successful endpoints: {summary['successful_endpoints']}")
        print(f"Failed endpoints: {summary['failed_endpoints']}")
        print(f"Total requests sent: {summary['total_requests']}")
        print(f"Total successful responses: {summary['total_successful']}")
        print(f"Total errors: {summary['total_errors']}")
        print(f"Overall error rate: {summary['overall_error_rate']}%")
        print(f"Average response time across all endpoints: {summary['avg_response_time_across_all']}ms")
        print(f"Max response time: {summary['max_response_time']}ms")
        print(f"Min response time: {summary['min_response_time']}ms")
        print("="*80 + "\n")

        # Save results to JSON
        output_file = '/Users/kcdacre8tor/GSBPD2/backend/load_test_results.json'
        with open(output_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'summary': summary,
                'endpoint_results': results
            }, f, indent=2)

        print(f"Results saved to: {output_file}")

        # Check success criteria
        print("\n" + "="*80)
        print("SUCCESS CRITERIA CHECK")
        print("="*80)

        # Criteria 1: Overall error rate < 1%
        criteria1 = summary['overall_error_rate'] < 1.0
        print(f"1. Overall error rate < 1%: {'PASS' if criteria1 else 'FAIL'} ({summary['overall_error_rate']}%)")

        # Criteria 2: Average response time < 2000ms
        criteria2 = summary['avg_response_time_across_all'] < 2000
        print(f"2. Average response time < 2000ms: {'PASS' if criteria2 else 'FAIL'} ({summary['avg_response_time_across_all']}ms)")

        # Criteria 3: No endpoint has > 5% error rate
        high_error_endpoints = [r for r in results.values() if r.get('error_rate', 0) > 5]
        criteria3 = len(high_error_endpoints) == 0
        print(f"3. No endpoint > 5% error rate: {'PASS' if criteria3 else 'FAIL'} ({len(high_error_endpoints)} endpoints failed)")

        # Criteria 4: All endpoints responding
        criteria4 = summary['failed_endpoints'] == 0
        print(f"4. All endpoints responding: {'PASS' if criteria4 else 'FAIL'} ({summary['failed_endpoints']} endpoints down)")

        print("="*80)

        overall_pass = criteria1 and criteria2 and criteria3 and criteria4
        print(f"\nOVERALL LOAD TEST RESULT: {'PASS' if overall_pass else 'FAIL'}")

        return 0 if overall_pass else 1

    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
