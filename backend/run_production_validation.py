#!/usr/bin/env python3
"""
Production Validation Test Runner for GSBPD2 NFL Integration - Phase 7
Runs all validation tests and generates comprehensive report.
"""

import subprocess
import sys
import json
import time
from datetime import datetime
from pathlib import Path

class ProductionValidationRunner:
    def __init__(self):
        self.results = {}
        self.backend_path = Path("/Users/kcdacre8tor/GSBPD2/backend")

    def run_test(self, test_name, test_script):
        """Run a single test script and collect results"""
        print(f"\n{'='*80}")
        print(f"Running: {test_name}")
        print(f"{'='*80}")

        try:
            result = subprocess.run(
                [sys.executable, str(self.backend_path / test_script)],
                cwd=str(self.backend_path),
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            # Check for result files
            result_file = None
            if "load" in test_script:
                result_file = "load_test_results.json"
            elif "error" in test_script:
                result_file = "error_handling_test_results.json"
            elif "edge" in test_script:
                result_file = "edge_case_test_results.json"
            elif "performance" in test_script:
                result_file = "performance_benchmark_results.json"
            elif "memory" in test_script:
                result_file = "memory_leak_test_results.json"

            result_data = None
            if result_file:
                result_path = self.backend_path / result_file
                if result_path.exists():
                    with open(result_path) as f:
                        result_data = json.load(f)

            test_result = {
                'test_name': test_name,
                'script': test_script,
                'return_code': result.returncode,
                'passed': result.returncode == 0,
                'stdout': result.stdout[-1000:] if result.stdout else "",  # Last 1000 chars
                'stderr': result.stderr[-1000:] if result.stderr else "",  # Last 1000 chars
                'result_file': result_file,
                'result_data': result_data
            }

            self.results[test_name] = test_result
            return test_result

        except subprocess.TimeoutExpired:
            print(f"ERROR: {test_name} timed out (> 5 minutes)")
            return {
                'test_name': test_name,
                'script': test_script,
                'passed': False,
                'error': 'Test timed out'
            }
        except Exception as e:
            print(f"ERROR: {test_name} failed - {str(e)}")
            return {
                'test_name': test_name,
                'script': test_script,
                'passed': False,
                'error': str(e)
            }

    def run_all_tests(self):
        """Run all production validation tests"""
        print("\n" + "="*80)
        print("GSBPD2 NFL INTEGRATION - PHASE 7 PRODUCTION VALIDATION")
        print("="*80)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)

        tests = [
            ("Load Test", "test_load.py"),
            ("Error Handling Test", "test_error_handling.py"),
            ("Edge Case Test", "test_edge_cases.py"),
            ("Performance Benchmark", "test_performance.py"),
            ("Memory Leak Test", "test_memory_leak.py"),
        ]

        for test_name, test_script in tests:
            self.run_test(test_name, test_script)
            time.sleep(1)  # Small delay between tests

        print("\n" + "="*80)
        print("ALL TESTS COMPLETED")
        print("="*80)

        return self.results

    def generate_report(self):
        """Generate comprehensive validation report"""
        report_lines = []

        report_lines.append("# PRODUCTION VALIDATION REPORT")
        report_lines.append(f"## GSBPD2 NFL Integration - Phase 7")
        report_lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Executive Summary
        report_lines.append("## Executive Summary\n")

        passed_tests = sum(1 for r in self.results.values() if r.get('passed', False))
        total_tests = len(self.results)
        pass_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0

        report_lines.append(f"**Overall Status:** {'PASS' if passed_tests == total_tests else 'FAIL'}\n")
        report_lines.append(f"- Total Tests: {total_tests}")
        report_lines.append(f"- Passed: {passed_tests}")
        report_lines.append(f"- Failed: {total_tests - passed_tests}")
        report_lines.append(f"- Pass Rate: {pass_rate:.1f}%\n")

        # Detailed Results for Each Test
        report_lines.append("## Detailed Test Results\n")

        # 1. Load Test
        if "Load Test" in self.results:
            report_lines.append("### 1. Load Test Results\n")
            load_result = self.results["Load Test"]
            if load_result.get('result_data'):
                data = load_result['result_data']
                summary = data.get('summary', {})
                report_lines.append(f"**Status:** {'PASS' if load_result['passed'] else 'FAIL'}\n")
                report_lines.append(f"- Total Endpoints Tested: {summary.get('total_endpoints_tested', 'N/A')}")
                report_lines.append(f"- Total Requests Sent: {summary.get('total_requests', 'N/A')}")
                report_lines.append(f"- Successful Responses: {summary.get('total_successful', 'N/A')}")
                report_lines.append(f"- Total Errors: {summary.get('total_errors', 'N/A')}")
                report_lines.append(f"- Overall Error Rate: {summary.get('overall_error_rate', 'N/A')}%")
                report_lines.append(f"- Average Response Time: {summary.get('avg_response_time_across_all', 'N/A')}ms")
                report_lines.append(f"- Max Response Time: {summary.get('max_response_time', 'N/A')}ms")
                report_lines.append(f"- Min Response Time: {summary.get('min_response_time', 'N/A')}ms\n")
            else:
                report_lines.append(f"**Error:** {load_result.get('error', 'Unknown error')}\n")

        # 2. Error Handling Test
        if "Error Handling Test" in self.results:
            report_lines.append("### 2. Error Handling Test Results\n")
            error_result = self.results["Error Handling Test"]
            if error_result.get('result_data'):
                data = error_result['result_data']
                report_lines.append(f"**Status:** {'PASS' if error_result['passed'] else 'FAIL'}\n")
                report_lines.append(f"- Total Tests: {data.get('total_tests', 'N/A')}")
                report_lines.append(f"- Passed: {data.get('passed', 'N/A')}")
                report_lines.append(f"- Failed: {data.get('failed', 'N/A')}\n")
            else:
                report_lines.append(f"**Error:** {error_result.get('error', 'Unknown error')}\n")

        # 3. Edge Case Test
        if "Edge Case Test" in self.results:
            report_lines.append("### 3. Edge Case Test Results\n")
            edge_result = self.results["Edge Case Test"]
            if edge_result.get('result_data'):
                data = edge_result['result_data']
                report_lines.append(f"**Status:** {'PASS' if edge_result['passed'] else 'FAIL'}\n")
                report_lines.append(f"- Total Tests: {data.get('total_tests', 'N/A')}")
                report_lines.append(f"- Passed: {data.get('passed', 'N/A')}")
                report_lines.append(f"- Failed: {data.get('failed', 'N/A')}\n")
            else:
                report_lines.append(f"**Error:** {edge_result.get('error', 'Unknown error')}\n")

        # 4. Performance Benchmark
        if "Performance Benchmark" in self.results:
            report_lines.append("### 4. Performance Benchmark Results\n")
            perf_result = self.results["Performance Benchmark"]
            if perf_result.get('result_data'):
                data = perf_result['result_data']
                summary = data.get('summary', {})
                report_lines.append(f"**Status:** {'PASS' if perf_result['passed'] else 'FAIL'}\n")
                report_lines.append(f"- Total Endpoints Benchmarked: {summary.get('total_endpoints', 'N/A')}")
                report_lines.append(f"- Average Response Time: {summary.get('avg_response_time_ms', 'N/A')}ms")
                report_lines.append(f"- Max Response Time: {summary.get('max_response_time_ms', 'N/A')}ms")
                report_lines.append(f"- Min Response Time: {summary.get('min_response_time_ms', 'N/A')}ms")
                report_lines.append(f"- P95 Response Time: {summary.get('p95_response_time_ms', 'N/A')}ms")
                report_lines.append(f"- Endpoints Under 500ms: {summary.get('endpoints_under_500ms', 'N/A')}")
                report_lines.append(f"- Endpoints Under 2000ms: {summary.get('endpoints_under_2sec', 'N/A')}\n")
            else:
                report_lines.append(f"**Error:** {perf_result.get('error', 'Unknown error')}\n")

        # 5. Memory Leak Test
        if "Memory Leak Test" in self.results:
            report_lines.append("### 5. Memory Leak Test Results\n")
            memory_result = self.results["Memory Leak Test"]
            if memory_result.get('result_data'):
                data = memory_result['result_data']
                report_lines.append(f"**Status:** {'PASS' if memory_result['passed'] else 'FAIL'}\n")
                report_lines.append(f"- Tests Run: {len(data.get('tests', {}))}")

                for test_name, test_data in data.get('tests', {}).items():
                    leak_status = "FAIL" if test_data.get('leak_detected') else "PASS"
                    report_lines.append(f"  - {test_name}: {leak_status}")
                    report_lines.append(f"    - Memory Increase: {test_data.get('increase_mb', 'N/A')}MB")
                    report_lines.append(f"    - Threshold: {test_data.get('threshold_mb', 'N/A')}MB")

                report_lines.append()
            else:
                report_lines.append(f"**Error:** {memory_result.get('error', 'Unknown error')}\n")

        # Production Readiness Assessment
        report_lines.append("\n## Production Readiness Assessment\n")

        all_passed = all(r.get('passed', False) for r in self.results.values())

        if all_passed:
            report_lines.append("**VERDICT: PRODUCTION READY**\n")
            report_lines.append("All validation tests have passed. The system is ready for production deployment.\n")
        else:
            report_lines.append("**VERDICT: NOT PRODUCTION READY**\n")
            report_lines.append("One or more tests have failed. Please address issues before deployment.\n")
            report_lines.append("Failed Tests:")
            for test_name, result in self.results.items():
                if not result.get('passed', False):
                    report_lines.append(f"- {test_name}")
            report_lines.append()

        # Success Criteria
        report_lines.append("## Success Criteria\n")

        # Criteria 1: Load Test
        load_passed = self.results.get("Load Test", {}).get('passed', False)
        report_lines.append(f"1. Load Test: {'PASS' if load_passed else 'FAIL'}")
        report_lines.append("   - Requirement: 100+ requests/sec with < 1% error rate")
        report_lines.append()

        # Criteria 2: Error Handling
        error_passed = self.results.get("Error Handling Test", {}).get('passed', False)
        report_lines.append(f"2. Error Handling: {'PASS' if error_passed else 'FAIL'}")
        report_lines.append("   - Requirement: Invalid inputs return proper error codes (400/404/422)")
        report_lines.append()

        # Criteria 3: Edge Cases
        edge_passed = self.results.get("Edge Case Test", {}).get('passed', False)
        report_lines.append(f"3. Edge Cases: {'PASS' if edge_passed else 'FAIL'}")
        report_lines.append("   - Requirement: All boundary conditions handled gracefully")
        report_lines.append()

        # Criteria 4: Performance
        perf_passed = self.results.get("Performance Benchmark", {}).get('passed', False)
        report_lines.append(f"4. Performance: {'PASS' if perf_passed else 'FAIL'}")
        report_lines.append("   - Requirement: Key operations complete in < 2 seconds")
        report_lines.append()

        # Criteria 5: Memory
        memory_passed = self.results.get("Memory Leak Test", {}).get('passed', False)
        report_lines.append(f"5. Memory Leak Detection: {'PASS' if memory_passed else 'FAIL'}")
        report_lines.append("   - Requirement: No leaks detected (< 100MB increase after iterations)")
        report_lines.append()

        # Recommendations
        report_lines.append("\n## Recommendations\n")

        if all_passed:
            report_lines.append("- System is ready for production deployment")
            report_lines.append("- Continue monitoring performance metrics in production")
            report_lines.append("- Set up alerting for error rates and response times")
            report_lines.append("- Schedule regular performance audits\n")
        else:
            report_lines.append("- Fix all failing tests before production deployment")
            report_lines.append("- Review error handling and edge cases")
            report_lines.append("- Optimize endpoints exceeding performance thresholds")
            report_lines.append("- Investigate and fix any memory leaks")
            report_lines.append("- Re-run validation after fixes\n")

        return "\n".join(report_lines)

    def save_report(self, report_content):
        """Save report to file"""
        report_path = self.backend_path / "PRODUCTION_VALIDATION_REPORT.md"
        with open(report_path, 'w') as f:
            f.write(report_content)
        print(f"\nReport saved to: {report_path}")
        return str(report_path)


def main():
    try:
        runner = ProductionValidationRunner()

        print("\n" + "="*80)
        print("PRODUCTION VALIDATION TEST RUNNER")
        print("="*80)

        # Run all tests
        runner.run_all_tests()

        # Generate report
        report = runner.generate_report()
        report_path = runner.save_report(report)

        # Print report to console
        print("\n" + "="*80)
        print(report)
        print("="*80)

        # Save raw results
        results_file = runner.backend_path / "validation_results.json"
        with open(results_file, 'w') as f:
            # Clean up results for JSON serialization
            clean_results = {}
            for test_name, result in runner.results.items():
                clean_results[test_name] = {
                    'passed': result.get('passed', False),
                    'return_code': result.get('return_code'),
                    'error': result.get('error'),
                    'result_file': result.get('result_file')
                }
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'summary': {
                    'total_tests': len(runner.results),
                    'passed_tests': sum(1 for r in runner.results.values() if r.get('passed', False)),
                    'failed_tests': sum(1 for r in runner.results.values() if not r.get('passed', False))
                },
                'results': clean_results
            }, f, indent=2)

        print(f"Raw results saved to: {results_file}")

        # Overall success
        all_passed = all(r.get('passed', False) for r in runner.results.values())
        return 0 if all_passed else 1

    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
