#!/usr/bin/env python
"""
Test Data Integrity
Verifies that all data fields exist and are valid in browsers.json.

Test Coverage:
- Correct User Agent count (165)
- Required fields present in each UA object
- Correct data types for each field
- No duplicate or missing data
"""

import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from __init__ import load_browsers_data, SimpleTestRunner


def test_data_integrity():
    """Run all data integrity tests."""
    runner = SimpleTestRunner("Data Integrity Tests")
    
    try:
        data = load_browsers_data()
    except Exception as e:
        runner.add_result("Load Data File", False, str(e))
        runner.run_report()
        return False
    
    # Test 1: Correct UA count
    expected_count = 165
    actual_count = len(data)
    runner.add_result(
        "User Agent Count",
        actual_count == expected_count,
        f"Expected {expected_count}, got {actual_count}"
    )
    
    # Test 2: Required fields present
    required_fields = ['useragent', 'browser', 'version', 'os', 'type', 'percent', 'system']
    missing_fields_count = 0
    
    for i, item in enumerate(data):
        for field in required_fields:
            if field not in item:
                missing_fields_count += 1
    
    runner.add_result(
        "Required Fields Present",
        missing_fields_count == 0,
        f"{missing_fields_count} missing fields" if missing_fields_count > 0 else "All fields present"
    )
    
    # Test 3: Correct data types
    type_errors = []
    
    for i, item in enumerate(data):
        ua = item.get('useragent')
        if not isinstance(ua, str):
            type_errors.append(f"Item {i}: useragent not string")
        
        browser = item.get('browser')
        if not isinstance(browser, str):
            type_errors.append(f"Item {i}: browser not string")
        
        version = item.get('version')
        if not isinstance(version, (int, float)):
            type_errors.append(f"Item {i}: version not number")
        
        os_name = item.get('os')
        if not isinstance(os_name, str):
            type_errors.append(f"Item {i}: os not string")
        
        ua_type = item.get('type')
        if not isinstance(ua_type, str):
            type_errors.append(f"Item {i}: type not string")
        
        percent = item.get('percent')
        if not isinstance(percent, (int, float)):
            type_errors.append(f"Item {i}: percent not number")
    
    runner.add_result(
        "Correct Data Types",
        len(type_errors) == 0,
        f"{len(type_errors)} type errors" if type_errors else "All types correct"
    )
    
    # Test 4: Non-empty User Agents
    empty_uas = [i for i, item in enumerate(data) if not item.get('useragent', '').strip()]
    
    runner.add_result(
        "Non-Empty User Agents",
        len(empty_uas) == 0,
        f"{len(empty_uas)} empty UAs" if empty_uas else "All UAs have content"
    )
    
    # Test 5: Valid browser types
    valid_types = {'pc', 'mobile', 'tablet'}
    invalid_types = [item.get('type') for item in data if item.get('type') not in valid_types]
    
    runner.add_result(
        "Valid Browser Types",
        len(invalid_types) == 0,
        f"{len(invalid_types)} invalid types" if invalid_types else "All types valid"
    )
    
    # Print report
    success = runner.run_report()
    
    # For pytest compatibility - assert instead of return
    assert success, "Data integrity tests failed"


if __name__ == "__main__":
    test_data_integrity()
    sys.exit(0)
