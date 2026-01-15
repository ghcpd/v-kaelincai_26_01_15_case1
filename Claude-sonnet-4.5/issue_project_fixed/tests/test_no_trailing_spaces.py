#!/usr/bin/env python3
"""
Test No Trailing Spaces

This test verifies that all User Agent strings have been properly cleaned:
- No trailing spaces at the end of UA strings
- No leading spaces at the beginning
- Statistics on fix effectiveness
"""

import sys
from pathlib import Path

# Add parent directory to path to import test utilities
sys.path.insert(0, str(Path(__file__).parent))

from __init__ import get_all_useragents, load_browsers_json, print_test_header, print_test_result


def test_no_trailing_spaces():
    """Test that no User Agent has trailing spaces"""
    useragents = get_all_useragents()
    
    passed = 0
    failed = 0
    
    for i, ua in enumerate(useragents, 1):
        if ua.endswith(' '):
            failed += 1
            print(f"[FAIL] UA #{i} has trailing space(s): '{ua[-20:]}'")
        else:
            passed += 1
    
    total = len(useragents)
    status = "[PASS]" if failed == 0 else "[FAIL]"
    print(f"{status} No Trailing Spaces: {passed}/{total} UAs are clean")
    
    return failed == 0


def test_no_leading_spaces():
    """Test that no User Agent has leading spaces"""
    useragents = get_all_useragents()
    
    passed = 0
    failed = 0
    
    for i, ua in enumerate(useragents, 1):
        if ua.startswith(' '):
            failed += 1
            print(f"[FAIL] UA #{i} has leading space(s): '{ua[:20]}'")
        else:
            passed += 1
    
    total = len(useragents)
    status = "[PASS]" if failed == 0 else "[FAIL]"
    print(f"{status} No Leading Spaces: {passed}/{total} UAs are clean")
    
    return failed == 0


def test_trimmed_strings():
    """Test that all User Agents are properly trimmed"""
    useragents = get_all_useragents()
    
    passed = 0
    failed = 0
    
    for i, ua in enumerate(useragents, 1):
        if ua != ua.strip():
            failed += 1
            print(f"[FAIL] UA #{i} is not trimmed properly")
        else:
            passed += 1
    
    total = len(useragents)
    status = "[PASS]" if failed == 0 else "[FAIL]"
    print(f"{status} Trimmed Strings: {passed}/{total} UAs are properly trimmed")
    
    return failed == 0


def test_fix_effectiveness():
    """Compare with original file to show fix effectiveness"""
    # Get the fixed UAs
    base_dir = Path(__file__).parent.parent
    fixed_file = base_dir / 'src' / 'fake_useragent' / 'data' / 'browsers.json'
    fixed_uas = get_all_useragents(str(fixed_file))
    
    # Try to get original UAs
    original_file = base_dir.parent.parent / 'issue_project' / 'src' / 'fake_useragent' / 'data' / 'browsers.json'
    
    if original_file.exists():
        original_uas = get_all_useragents(str(original_file))
        
        original_with_spaces = sum(1 for ua in original_uas if ua != ua.rstrip())
        fixed_with_spaces = sum(1 for ua in fixed_uas if ua != ua.rstrip())
        
        print(f"[INFO] Original file: {original_with_spaces}/{len(original_uas)} UAs had trailing spaces")
        print(f"[INFO] Fixed file: {fixed_with_spaces}/{len(fixed_uas)} UAs have trailing spaces")
        print(f"[INFO] Improvement: {original_with_spaces - fixed_with_spaces} UAs fixed")
        
        passed = fixed_with_spaces == 0
    else:
        print("[INFO] Original file not found, skipping comparison")
        passed = True
    
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} Fix Effectiveness: All trailing spaces removed")
    
    return passed


def main():
    """Run all trailing space tests"""
    print_test_header("Trailing Space Tests")
    
    tests = [
        test_no_trailing_spaces,
        test_no_leading_spaces,
        test_trimmed_strings,
        test_fix_effectiveness
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
