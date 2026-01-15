"""
Test package initialization file.

This module provides shared utilities for all test modules.
"""

import json
from pathlib import Path


def load_browsers_json(file_path=None):
    """
    Load and parse browsers.json file.
    
    Args:
        file_path (str, optional): Path to browsers.json file.
                                  If None, uses default location.
    
    Returns:
        list: List of user agent dictionaries
    """
    if file_path is None:
        # Default to the fixed browsers.json in this project
        base_dir = Path(__file__).parent.parent
        file_path = base_dir / 'src' / 'fake_useragent' / 'data' / 'browsers.json'
    
    user_agents = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                user_agents.append(json.loads(line))
    
    return user_agents


def get_all_useragents(file_path=None):
    """
    Get all user agent strings from browsers.json.
    
    Args:
        file_path (str, optional): Path to browsers.json file
    
    Returns:
        list: List of user agent strings
    """
    data = load_browsers_json(file_path)
    return [item.get('useragent', '') for item in data]


def print_test_header(test_name):
    """Print a formatted test header."""
    print()
    print("=" * 70)
    print(f"Test: {test_name}")
    print("=" * 70)


def print_test_result(passed, failed, total):
    """Print formatted test results."""
    print("-" * 70)
    percentage = (passed / total * 100) if total > 0 else 0
    print(f"Total: {passed}/{total} Passed ({percentage:.1f}%)")
    if failed > 0:
        print(f"Failed: {failed}")
    print()
