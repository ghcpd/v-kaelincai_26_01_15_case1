#!/usr/bin/env python
"""
Test All - Integration Test Runner
Runs all test modules and generates a comprehensive report.

Usage:
    python test_all.py

This script:
- Runs all individual test modules
- Generates comprehensive test report
- Provides statistics on test pass rate
- Shows detailed error information (if any)
- Outputs performance metrics
"""

import sys
import time
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))


def run_test_module(module_name: str, test_func: callable) -> dict:
    """
    Run a test module and capture results.
    
    Args:
        module_name: Name of the test module
        test_func: Test function to run
    
    Returns:
        Dictionary with test results
    """
    result = {
        'name': module_name,
        'passed': False,
        'duration': 0,
        'error': None
    }
    
    start_time = time.time()
    
    try:
        test_func()
        # If no exception, test passed (functions now use assert)
        result['passed'] = True
    except AssertionError as e:
        result['passed'] = False
        result['error'] = str(e)
    except Exception as e:
        result['passed'] = False
        result['error'] = str(e)
    
    result['duration'] = time.time() - start_time
    
    return result


def main():
    """Run all tests and generate comprehensive report."""
    print("=" * 70)
    print("Issue #307 Fix - Comprehensive Test Suite")
    print("=" * 70)
    print(f"Python Version: {sys.version}")
    print(f"Test Directory: {Path(__file__).parent}")
    print()
    
    total_start = time.time()
    
    # Import test modules
    print("Loading test modules...")
    try:
        from test_data_integrity import test_data_integrity
        from test_no_trailing_spaces import test_no_trailing_spaces
        from test_httpx_compatibility import test_httpx_compatibility
        from test_json_validity import test_json_validity
        print("[OK] All test modules loaded\n")
    except ImportError as e:
        print(f"[ERROR] Failed to import test modules: {e}")
        return 1
    
    # Define test suite
    tests = [
        ("Data Integrity Tests", test_data_integrity),
        ("Trailing Space Tests", test_no_trailing_spaces),
        ("httpx Compatibility Tests", test_httpx_compatibility),
        ("JSON Validity Tests", test_json_validity),
    ]
    
    # Run all tests
    results = []
    
    for test_name, test_func in tests:
        print("\n" + "=" * 70)
        print(f"Running: {test_name}")
        print("=" * 70 + "\n")
        
        result = run_test_module(test_name, test_func)
        results.append(result)
        
        if result['error']:
            print(f"\n[ERROR] {result['error']}")
    
    total_duration = time.time() - total_start
    
    # Generate summary report
    print("\n" + "=" * 70)
    print("=" * 70)
    print("COMPREHENSIVE TEST RESULTS SUMMARY")
    print("=" * 70)
    print("=" * 70)
    
    passed_count = sum(1 for r in results if r['passed'])
    failed_count = len(results) - passed_count
    
    # Individual test results
    print("\nIndividual Test Results:")
    print("-" * 70)
    
    for result in results:
        status = "[PASS]" if result['passed'] else "[FAIL]"
        duration = f"({result['duration']:.2f}s)"
        print(f"  {status} {result['name']}: {'Passed' if result['passed'] else 'Failed'} {duration}")
        if result['error']:
            print(f"         Error: {result['error']}")
    
    # Summary statistics
    print("\n" + "-" * 70)
    print("Summary Statistics:")
    print("-" * 70)
    print(f"  Total Tests: {len(results)}")
    print(f"  Passed: {passed_count}")
    print(f"  Failed: {failed_count}")
    print(f"  Pass Rate: {passed_count/len(results)*100:.0f}%")
    print(f"  Total Duration: {total_duration:.2f}s")
    
    # Final verdict
    print("\n" + "=" * 70)
    
    if failed_count == 0:
        print("[SUCCESS] All tests passed!")
        print("=" * 70)
        print("\nThe fix has been verified successfully:")
        print("  ✓ Data integrity maintained (165 User Agents)")
        print("  ✓ No trailing spaces in any UA string")
        print("  ✓ httpx compatibility confirmed")
        print("  ✓ JSON format is valid")
    else:
        print(f"[WARNING] {failed_count} test(s) failed!")
        print("=" * 70)
        print("\nFailed tests:")
        for result in results:
            if not result['passed']:
                print(f"  ✗ {result['name']}")
    
    print("\n" + "=" * 70)
    print(f"Test execution completed in {total_duration:.2f} seconds")
    print("=" * 70)
    
    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
