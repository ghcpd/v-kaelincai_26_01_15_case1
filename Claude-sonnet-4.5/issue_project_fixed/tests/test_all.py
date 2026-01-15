#!/usr/bin/env python3
"""
Run All Tests

This script runs all test suites and provides a comprehensive test report.
"""

import sys
import time
from pathlib import Path

# Add test directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import all test modules
import test_data_integrity
import test_no_trailing_spaces
import test_httpx_compatibility
import test_json_validity


def run_test_suite(name, test_module):
    """Run a test suite and return results"""
    print()
    print("*" * 70)
    print(f"Running: {name}")
    print("*" * 70)
    
    start_time = time.time()
    result = test_module.main()
    elapsed_time = time.time() - start_time
    
    return result, elapsed_time


def main():
    """Run all test suites"""
    print("=" * 70)
    print("COMPREHENSIVE TEST SUITE")
    print("Issue #307 Fix Verification")
    print("=" * 70)
    
    test_suites = [
        ("Data Integrity Tests", test_data_integrity),
        ("Trailing Space Tests", test_no_trailing_spaces),
        ("httpx Compatibility Tests", test_httpx_compatibility),
        ("JSON Validity Tests", test_json_validity)
    ]
    
    results = []
    total_time = 0
    
    for name, module in test_suites:
        result, elapsed = run_test_suite(name, module)
        results.append((name, result, elapsed))
        total_time += elapsed
    
    # Print summary
    print()
    print("=" * 70)
    print("TEST RESULTS SUMMARY")
    print("=" * 70)
    
    passed_suites = 0
    failed_suites = 0
    
    for name, result, elapsed in results:
        status = "[PASS]" if result == 0 else "[FAIL]"
        print(f"{status} {name}: {elapsed:.2f}s")
        if result == 0:
            passed_suites += 1
        else:
            failed_suites += 1
    
    print("-" * 70)
    total_suites = len(results)
    percentage = (passed_suites / total_suites * 100) if total_suites > 0 else 0
    print(f"Total: {passed_suites}/{total_suites} Test Suites Passed ({percentage:.1f}%)")
    print(f"Total Time: {total_time:.2f}s")
    
    if failed_suites == 0:
        print()
        print("✓ ALL TESTS PASSED!")
        print()
        print("The fix for Issue #307 has been successfully verified:")
        print("  - All 165 User Agents processed correctly")
        print("  - No trailing spaces found")
        print("  - httpx compatibility confirmed")
        print("  - JSON format valid")
        print()
    else:
        print()
        print("✗ SOME TESTS FAILED")
        print(f"  {failed_suites} test suite(s) need attention")
        print()
    
    print("=" * 70)
    
    return 0 if failed_suites == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
