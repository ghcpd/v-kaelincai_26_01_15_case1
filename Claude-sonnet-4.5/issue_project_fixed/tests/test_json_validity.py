#!/usr/bin/env python3
"""
Test JSON Validity

This test verifies that the browsers.json file is properly formatted:
- Valid JSON format (JSONL - one JSON object per line)
- Each line parses correctly
- Correct encoding (UTF-8)
- No JSON parsing errors
"""

import json
import sys
from pathlib import Path

# Add parent directory to path to import test utilities
sys.path.insert(0, str(Path(__file__).parent))

from __init__ import print_test_header, print_test_result


def get_browsers_file_path():
    """Get path to browsers.json file"""
    base_dir = Path(__file__).parent.parent
    return base_dir / 'src' / 'fake_useragent' / 'data' / 'browsers.json'


def test_file_exists():
    """Test that browsers.json file exists"""
    file_path = get_browsers_file_path()
    passed = file_path.exists()
    
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} File Exists: {file_path}")
    
    return passed


def test_utf8_encoding():
    """Test that file is UTF-8 encoded"""
    file_path = get_browsers_file_path()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read()
        passed = True
        status = "[PASS]"
        print(f"{status} UTF-8 Encoding: File is properly encoded")
    except UnicodeDecodeError as e:
        passed = False
        status = "[FAIL]"
        print(f"{status} UTF-8 Encoding: {e}")
    
    return passed


def test_jsonl_format():
    """Test that each line is valid JSON"""
    file_path = get_browsers_file_path()
    
    passed = 0
    failed = 0
    total_lines = 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            total_lines += 1
            try:
                json.loads(line)
                passed += 1
            except json.JSONDecodeError as e:
                failed += 1
                print(f"[FAIL] Line {i} is not valid JSON: {e}")
    
    status = "[PASS]" if failed == 0 else "[FAIL]"
    print(f"{status} JSONL Format: {passed}/{total_lines} lines are valid JSON")
    
    return failed == 0


def test_json_objects():
    """Test that each line contains a JSON object (not array or primitive)"""
    file_path = get_browsers_file_path()
    
    passed = 0
    failed = 0
    total_lines = 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            total_lines += 1
            try:
                data = json.loads(line)
                if isinstance(data, dict):
                    passed += 1
                else:
                    failed += 1
                    print(f"[FAIL] Line {i} is not a JSON object: {type(data)}")
            except json.JSONDecodeError:
                failed += 1
                print(f"[FAIL] Line {i} failed to parse")
    
    status = "[PASS]" if failed == 0 else "[FAIL]"
    print(f"{status} JSON Objects: {passed}/{total_lines} lines contain objects")
    
    return failed == 0


def test_no_trailing_commas():
    """Test that there are no trailing commas (which would break JSONL format)"""
    file_path = get_browsers_file_path()
    
    passed = 0
    failed = 0
    total_lines = 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            total_lines += 1
            if line.endswith(','):
                failed += 1
                print(f"[FAIL] Line {i} has trailing comma")
            else:
                passed += 1
    
    status = "[PASS]" if failed == 0 else "[FAIL]"
    print(f"{status} No Trailing Commas: {passed}/{total_lines} lines are clean")
    
    return failed == 0


def main():
    """Run all JSON validity tests"""
    print_test_header("JSON Validity Tests")
    
    tests = [
        test_file_exists,
        test_utf8_encoding,
        test_jsonl_format,
        test_json_objects,
        test_no_trailing_commas
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
