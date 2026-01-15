"""
Test package initialization for issue_project_fixed tests.

This module provides common utilities for testing the fixed fake-useragent data.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional


def get_project_root() -> Path:
    """Get the root directory of the fixed project."""
    return Path(__file__).parent.parent


def get_data_file_path() -> Path:
    """Get the path to browsers.json data file."""
    return get_project_root() / "src" / "fake_useragent" / "data" / "browsers.json"


def load_browsers_data() -> List[Dict]:
    """
    Load all browser data from browsers.json.
    
    Returns:
        List of dictionaries containing browser data
    """
    data = []
    data_path = get_data_file_path()
    
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    
    with open(data_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line:
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON on line {line_num}: {e}")
    
    return data


def get_all_useragents() -> List[str]:
    """
    Get all User Agent strings from browsers.json.
    
    Returns:
        List of User Agent strings
    """
    data = load_browsers_data()
    return [item.get('useragent', '') for item in data]


def format_test_result(test_name: str, passed: bool, details: Optional[str] = None) -> str:
    """
    Format a test result for display.
    
    Args:
        test_name: Name of the test
        passed: Whether the test passed
        details: Optional details about the result
    
    Returns:
        Formatted result string
    """
    status = "[PASS]" if passed else "[FAIL]"
    result = f"{status} {test_name}"
    if details:
        result += f": {details}"
    return result


class SimpleTestRunner:
    """Simple test runner for collecting and running tests (not a pytest class)."""
    
    def __init__(self, test_name: str):
        self.test_name = test_name
        self.results = []
        self.passed = 0
        self.failed = 0
    
    def add_result(self, test_item: str, passed: bool, details: str = None):
        """Add a test result."""
        self.results.append({
            'test': test_item,
            'passed': passed,
            'details': details
        })
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def print_header(self):
        """Print the test header."""
        print("=" * 60)
        print(f"Test: {self.test_name}")
        print("=" * 60)
    
    def print_results(self):
        """Print all test results."""
        for result in self.results:
            status = "[PASS]" if result['passed'] else "[FAIL]"
            line = f"{status} {result['test']}"
            if result['details']:
                line += f": {result['details']}"
            print(line)
    
    def print_summary(self):
        """Print the test summary."""
        total = self.passed + self.failed
        print("-" * 60)
        print(f"Total: {self.passed}/{total} Passed ({self.passed/total*100:.0f}%)")
    
    def run_report(self):
        """Print full test report."""
        self.print_header()
        self.print_results()
        self.print_summary()
        return self.failed == 0
