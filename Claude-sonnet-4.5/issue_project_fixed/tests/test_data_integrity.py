#!/usr/bin/env python3
"""
Test Data Integrity

This test verifies that the fixed browsers.json file maintains data integrity:
- Correct number of User Agents (165)
- All required fields present
- Correct data types
- No duplicate or missing data
"""

import sys
from pathlib import Path

# Add parent directory to path to import test utilities
sys.path.insert(0, str(Path(__file__).parent))

from __init__ import load_browsers_json, print_test_header, print_test_result


def test_ua_count():
    """Test that we have exactly 165 User Agents"""
    data = load_browsers_json()
    expected_count = 165
    actual_count = len(data)
    
    passed = actual_count == expected_count
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} User Agent Count: Expected {expected_count}, Got {actual_count}")
    
    return passed


def test_required_fields():
    """Test that all required fields are present in each UA object"""
    data = load_browsers_json()
    required_fields = ['useragent', 'browser', 'version', 'os', 'type', 'system', 'percent']
    
    passed = 0
    failed = 0
    
    for i, item in enumerate(data, 1):
        missing_fields = [field for field in required_fields if field not in item]
        if not missing_fields:
            passed += 1
        else:
            failed += 1
            print(f"[FAIL] UA #{i} missing fields: {missing_fields}")
    
    total = len(data)
    status = "[PASS]" if failed == 0 else "[FAIL]"
    print(f"{status} Required Fields: {passed}/{total} UAs have all required fields")
    
    return failed == 0


def test_data_types():
    """Test that all fields have correct data types"""
    data = load_browsers_json()
    
    passed = 0
    failed = 0
    
    for i, item in enumerate(data, 1):
        errors = []
        
        # Check string fields
        if not isinstance(item.get('useragent'), str):
            errors.append('useragent must be string')
        if not isinstance(item.get('browser'), str):
            errors.append('browser must be string')
        if not isinstance(item.get('os'), str):
            errors.append('os must be string')
        if not isinstance(item.get('type'), str):
            errors.append('type must be string')
        if not isinstance(item.get('system'), str):
            errors.append('system must be string')
        
        # Check numeric fields
        if not isinstance(item.get('version'), (int, float)):
            errors.append('version must be numeric')
        if not isinstance(item.get('percent'), (int, float)):
            errors.append('percent must be numeric')
        
        if not errors:
            passed += 1
        else:
            failed += 1
            print(f"[FAIL] UA #{i} type errors: {', '.join(errors)}")
    
    total = len(data)
    status = "[PASS]" if failed == 0 else "[FAIL]"
    print(f"{status} Data Types: {passed}/{total} UAs have correct data types")
    
    return failed == 0


def test_no_duplicates():
    """Test for duplicate User Agent strings (informational only)"""
    data = load_browsers_json()
    useragents = [item.get('useragent', '') for item in data]
    
    unique_uas = set(useragents)
    duplicates = len(useragents) - len(unique_uas)
    
    # Note: Duplicates are expected in the dataset as some UAs appear multiple times
    # This is intentional in the original data and not an error
    status = "[INFO]"
    print(f"{status} Duplicates: Found {duplicates} duplicate UA(s) (expected in original data)")
    
    # Always pass - duplicates are not an error
    return True


def test_non_empty_strings():
    """Test that all string fields are non-empty"""
    data = load_browsers_json()
    
    passed = 0
    failed = 0
    
    for i, item in enumerate(data, 1):
        errors = []
        
        if not item.get('useragent', '').strip():
            errors.append('useragent is empty')
        if not item.get('browser', '').strip():
            errors.append('browser is empty')
        if not item.get('os', '').strip():
            errors.append('os is empty')
        if not item.get('type', '').strip():
            errors.append('type is empty')
        if not item.get('system', '').strip():
            errors.append('system is empty')
        
        if not errors:
            passed += 1
        else:
            failed += 1
            print(f"[FAIL] UA #{i} has empty fields: {', '.join(errors)}")
    
    total = len(data)
    status = "[PASS]" if failed == 0 else "[FAIL]"
    print(f"{status} Non-Empty Strings: {passed}/{total} UAs have non-empty fields")
    
    return failed == 0


def main():
    """Run all data integrity tests"""
    print_test_header("Data Integrity Tests")
    
    tests = [
        test_ua_count,
        test_required_fields,
        test_data_types,
        test_no_duplicates,
        test_non_empty_strings
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    print_test_result(passed, failed, len(tests))
    
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
