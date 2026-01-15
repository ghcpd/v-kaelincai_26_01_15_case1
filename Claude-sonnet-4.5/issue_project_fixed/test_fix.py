#!/usr/bin/env python3
"""
Quick Fix Verification Script

This script provides a quick way to verify that the fix has been applied correctly.
It checks for trailing spaces and provides statistics.
"""

import json
import sys
from pathlib import Path


def verify_fix():
    """Verify the fix has been applied correctly"""
    print("=" * 70)
    print("Quick Fix Verification")
    print("=" * 70)
    print()
    
    # Get file paths
    base_dir = Path(__file__).parent
    fixed_file = base_dir / 'src' / 'fake_useragent' / 'data' / 'browsers.json'
    original_file = base_dir.parent.parent / 'issue_project' / 'src' / 'fake_useragent' / 'data' / 'browsers.json'
    
    # Load fixed data
    print(f"Loading fixed file: {fixed_file}")
    fixed_uas = []
    with open(fixed_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                data = json.loads(line)
                fixed_uas.append(data.get('useragent', ''))
    
    # Check for trailing spaces in fixed file
    fixed_with_trailing = sum(1 for ua in fixed_uas if ua != ua.rstrip())
    
    print()
    print("-" * 70)
    print("Fixed File Analysis:")
    print("-" * 70)
    print(f"Total User Agents:       {len(fixed_uas)}")
    print(f"With Trailing Spaces:    {fixed_with_trailing}")
    print(f"Clean User Agents:       {len(fixed_uas) - fixed_with_trailing}")
    
    # Load original data if available
    if original_file.exists():
        print()
        print(f"Loading original file: {original_file}")
        original_uas = []
        with open(original_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    data = json.loads(line)
                    original_uas.append(data.get('useragent', ''))
        
        original_with_trailing = sum(1 for ua in original_uas if ua != ua.rstrip())
        
        print()
        print("-" * 70)
        print("Original File Analysis:")
        print("-" * 70)
        print(f"Total User Agents:       {len(original_uas)}")
        print(f"With Trailing Spaces:    {original_with_trailing}")
        print(f"Clean User Agents:       {len(original_uas) - original_with_trailing}")
        
        print()
        print("-" * 70)
        print("Comparison:")
        print("-" * 70)
        fixed_count = original_with_trailing - fixed_with_trailing
        fix_percentage = (fixed_count / original_with_trailing * 100) if original_with_trailing > 0 else 0
        print(f"User Agents Fixed:       {fixed_count}")
        print(f"Fix Success Rate:        {fix_percentage:.1f}%")
    
    # Verification result
    print()
    print("=" * 70)
    if fixed_with_trailing == 0:
        print("✓ VERIFICATION PASSED!")
        print()
        print("All User Agent strings have been successfully cleaned.")
        print("No trailing spaces found in the fixed file.")
        result = 0
    else:
        print("✗ VERIFICATION FAILED!")
        print()
        print(f"Found {fixed_with_trailing} User Agent(s) with trailing spaces.")
        print("Please review the fix process.")
        result = 1
    
    print("=" * 70)
    
    return result


def main():
    """Main function"""
    return verify_fix()


if __name__ == '__main__':
    sys.exit(main())
