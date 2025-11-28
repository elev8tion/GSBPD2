#!/usr/bin/env python3
"""
Error Handling Test for GSBPD2 NFL Integration - Phase 7 Production Validation
Tests API error responses with invalid inputs and boundary conditions.
"""

import requests
import json
from datetime import datetime
import sys

BASE_URL = "http://localhost:8000"
TIMEOUT = 5

class ErrorHandlingTester:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.results = []
        self.passed = 0
        self.failed = 0

    def test_case(self, url, expected_status, description, method="GET", data=None):
        """Test a single error case"""
        try:
            if method == "GET":
                response = requests.get(url, timeout=TIMEOUT)
            elif method == "POST":
                response = requests.post(url, json=data, timeout=TIMEOUT)
            elif method == "DELETE":
                response = requests.delete(url, timeout=TIMEOUT)
            else:
                response = requests.get(url, timeout=TIMEOUT)

            passed = response.status_code == expected_status
            error_message = None
            if not passed:
                try:
                    error_message = response.json().get('detail', response.text)
                except:
                    error_message = response.text[:100]

            result = {
                'description': description,
                'url': url,
                'method': method,
                'expected_status': expected_status,
                'actual_status': response.status_code,
                'passed': passed,
                'error_message': error_message,
                'response_time_ms': round(response.elapsed.total_seconds() * 1000, 2)
            }

            self.results.append(result)
            if passed:
                self.passed += 1
            else:
                self.failed += 1

            return result

        except requests.exceptions.Timeout:
            result = {
                'description': description,
                'url': url,
                'passed': False,
                'error_message': 'Request timeout',
                'actual_status': None
            }
            self.results.append(result)
            self.failed += 1
            return result
        except Exception as e:
            result = {
                'description': description,
                'url': url,
                'passed': False,
                'error_message': str(e),
                'actual_status': None
            }
            self.results.append(result)
            self.failed += 1
            return result

    def run_tests(self):
        """Run all error handling tests"""
        print("\n" + "="*80)
        print("ERROR HANDLING TEST - GSBPD2 NFL Integration Phase 7")
        print("="*80)
        print(f"Base URL: {self.base_url}")
        print("="*80 + "\n")

        # Test 1: Invalid player name (should be 404)
        self.test_case(
            f"{self.base_url}/nfl/player-stats/InvalidPlayer?week=1",
            404,
            "Invalid player name should return 404"
        )

        # Test 2: Invalid week number (should be 400 or 404)
        self.test_case(
            f"{self.base_url}/nfl/sgp/weekly/999?season=2024",
            400,
            "Invalid week number should return 400"
        )

        # Test 3: Missing required parameter (should be 422)
        self.test_case(
            f"{self.base_url}/nfl/sgp/weekly/12",
            422,
            "Missing season parameter should return 422"
        )

        # Test 4: Invalid team name (should be 404)
        self.test_case(
            f"{self.base_url}/nfl/sgp/INVALID/12?season=2024",
            404,
            "Invalid team name should return 404"
        )

        # Test 5: Invalid top_k parameter (should be 400)
        self.test_case(
            f"{self.base_url}/memories/search?query=test&top_k=100",
            400,
            "top_k > 20 should return 400",
            method="POST",
            data={"query": "test", "top_k": 100}
        )

        # Test 6: Empty search query (should be 400)
        self.test_case(
            f"{self.base_url}/memories/search",
            400,
            "Empty search query should return 400",
            method="POST",
            data={"query": "", "top_k": 5}
        )

        # Test 7: Invalid bet type (should be 400)
        self.test_case(
            f"{self.base_url}/portfolio/bet",
            400,
            "Invalid bet type should return 400",
            method="POST",
            data={
                "bet_type": "invalid_type",
                "wager_amount": 100,
                "odds": -110
            }
        )

        # Test 8: Zero wager amount (should be 400)
        self.test_case(
            f"{self.base_url}/portfolio/bet",
            400,
            "Zero wager amount should return 400",
            method="POST",
            data={
                "bet_type": "spread",
                "wager_amount": 0,
                "odds": -110
            }
        )

        # Test 9: Wager exceeds limit (should be 400)
        self.test_case(
            f"{self.base_url}/portfolio/bet",
            400,
            "Wager > $10000 should return 400",
            method="POST",
            data={
                "bet_type": "spread",
                "wager_amount": 15000,
                "odds": -110
            }
        )

        # Test 10: Invalid outcome (should be 400)
        self.test_case(
            f"{self.base_url}/portfolio/resolve",
            400,
            "Invalid outcome should return 400",
            method="POST",
            data={
                "bet_id": "test123",
                "outcome": "invalid"
            }
        )

        # Test 11: Nonexistent memory (should be 404)
        self.test_case(
            f"{self.base_url}/memories/nonexistent_memory_12345",
            404,
            "Nonexistent memory should return 404",
            method="DELETE"
        )

        # Test 12: Invalid memory name (should be 400)
        self.test_case(
            f"{self.base_url}/memories/create",
            400,
            "Memory with special chars should return 400",
            method="POST",
            data={
                "memory_name": "invalid@#$%",
                "docs_dir": "/some/path"
            }
        )

        # Test 13: Nonexistent directory (should be 404)
        self.test_case(
            f"{self.base_url}/memories/create",
            404,
            "Nonexistent docs_dir should return 404",
            method="POST",
            data={
                "memory_name": "test_memory",
                "docs_dir": "/nonexistent/path/12345"
            }
        )

        # Test 14: Invalid sport parameter (should be 400)
        self.test_case(
            f"{self.base_url}/ai/insights/baseball",
            400,
            "Invalid sport should return 400"
        )

        # Test 15: Invalid EV calculation (should be 500 or 400)
        self.test_case(
            f"{self.base_url}/nfl/sgp/calculate-ev",
            400,
            "Invalid EV request should return error",
            method="POST",
            data={
                "our_picks": [],
                "dk_odds": None
            }
        )

        print("\nTest Results:")
        print("-" * 80)

        for i, result in enumerate(self.results, 1):
            status = "PASS" if result['passed'] else "FAIL"
            print(f"\n{i}. [{status}] {result['description']}")
            print(f"   Expected: {result.get('expected_status', 'N/A')} | Actual: {result.get('actual_status', 'ERROR')}")
            if result.get('error_message'):
                print(f"   Error: {result['error_message']}")

        print("\n" + "="*80)
        print("ERROR HANDLING TEST SUMMARY")
        print("="*80)
        print(f"Total tests: {len(self.results)}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Pass rate: {round((self.passed / len(self.results)) * 100, 1)}%")
        print("="*80 + "\n")

        return self.results


def main():
    try:
        # Check if server is running
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
        except:
            print(f"ERROR: Cannot connect to server at {BASE_URL}")
            print("Please start the FastAPI server with: python main.py")
            sys.exit(1)

        # Run error handling tests
        tester = ErrorHandlingTester()
        results = tester.run_tests()

        # Save results
        output_file = '/Users/kcdacre8tor/GSBPD2/backend/error_handling_test_results.json'
        with open(output_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total_tests': len(results),
                'passed': sum(1 for r in results if r['passed']),
                'failed': sum(1 for r in results if not r['passed']),
                'results': results
            }, f, indent=2)

        print(f"Results saved to: {output_file}")

        # Check success criteria
        print("SUCCESS CRITERIA CHECK")
        print("="*80)
        pass_rate = sum(1 for r in results if r['passed']) / len(results)
        criteria1 = pass_rate >= 0.90  # 90% pass rate
        print(f"1. Error handling test pass rate >= 90%: {'PASS' if criteria1 else 'FAIL'} ({round(pass_rate * 100, 1)}%)")

        no_timeouts = all(r.get('actual_status') is not None or r['passed'] for r in results)
        criteria2 = no_timeouts
        print(f"2. No request timeouts: {'PASS' if criteria2 else 'FAIL'}")

        print("="*80)

        overall_pass = criteria1 and criteria2
        print(f"\nOVERALL ERROR HANDLING TEST RESULT: {'PASS' if overall_pass else 'FAIL'}")

        return 0 if overall_pass else 1

    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
