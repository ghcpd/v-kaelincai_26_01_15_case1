#!/usr/bin/env python
"""
Test JSON Validity
Verifies that browsers.json is valid JSON and properly formatted.

Test Coverage:
- Correct JSONL format (one JSON object per line)
- Each line is valid JSON
- No parse exceptions
- Correct UTF-8 encoding
"""

import json
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from __init__ import get_data_file_path, SimpleTestRunner


def test_json_validity():
    """Run all JSON validity tests."""
    runner = SimpleTestRunner("JSON Validity Tests")
    
    data_path = get_data_file_path()
    
    # Test 1: File exists
    runner.add_result(
        "Data File Exists",
        data_path.exists(),
        str(data_path) if data_path.exists() else "File not found"
    )
    
    if not data_path.exists():
        runner.run_report()
        return False
    
    # Test 2: UTF-8 encoding
    encoding_valid = True
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError as e:
        encoding_valid = False
        content = None
    
    runner.add_result(
        "UTF-8 Encoding",
        encoding_valid,
        "Valid UTF-8" if encoding_valid else "Encoding error"
    )
    
    if not encoding_valid:
        runner.run_report()
        return False
    
    # Test 3: Valid JSONL format (each line is valid JSON)
    lines = content.strip().split('\n')
    parse_errors = []
    parsed_objects = []
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            parsed_objects.append(obj)
        except json.JSONDecodeError as e:
            parse_errors.append({
                'line': line_num,
                'error': str(e),
                'content': line[:50] + '...' if len(line) > 50 else line
            })
    
    runner.add_result(
        "Valid JSONL Format",
        len(parse_errors) == 0,
        f"All {len(parsed_objects)} lines valid" if not parse_errors
        else f"{len(parse_errors)} parse errors"
    )
    
    # Test 4: Each object has expected structure
    structure_errors = []
    for i, obj in enumerate(parsed_objects):
        if not isinstance(obj, dict):
            structure_errors.append(f"Line {i+1}: Not a JSON object")
    
    runner.add_result(
        "Correct Object Structure",
        len(structure_errors) == 0,
        "All objects are dictionaries" if not structure_errors
        else f"{len(structure_errors)} structure errors"
    )
    
    # Print report
    success = runner.run_report()
    
    # Show parse error details if any
    if parse_errors:
        print("\n" + "=" * 60)
        print("Parse Error Details")
        print("=" * 60)
        for error in parse_errors[:5]:
            print(f"  Line {error['line']}: {error['error']}")
            print(f"    Content: {error['content']}")
    
    # Additional stats
    print("\n" + "=" * 60)
    print("JSON Statistics")
    print("=" * 60)
    print(f"Total lines: {len(lines)}")
    print(f"Valid JSON objects: {len(parsed_objects)}")
    print(f"Parse errors: {len(parse_errors)}")
    print(f"File size: {len(content)} bytes")
    
    # For pytest compatibility - assert instead of return
    assert success, "JSON validity tests failed"


if __name__ == "__main__":
    test_json_validity()
    sys.exit(0)
