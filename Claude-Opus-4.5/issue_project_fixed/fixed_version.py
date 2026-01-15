#!/usr/bin/env python
"""
Fixed Version Script: Demonstrates how to fix User Agent trailing spaces
This script reads the original browsers.json and creates a fixed version.

Usage:
    python fixed_version.py

Author: Issue #307 Fix
Reference: https://github.com/fake-useragent/fake-useragent/issues/307
"""

import json
import os
from pathlib import Path


def fix_browsers_json(original_path: str, fixed_path: str) -> dict:
    """
    Fix trailing spaces in User Agent strings.
    
    Args:
        original_path: Path to original browsers.json file
        fixed_path: Path to output fixed browsers.json file
    
    Returns:
        Dictionary with fix statistics
    """
    stats = {
        'total_uas': 0,
        'fixed_uas': 0,
        'unchanged_uas': 0,
        'errors': 0
    }
    
    fixed_lines = []
    
    with open(original_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        
        try:
            data = json.loads(line)
            stats['total_uas'] += 1
            
            # Get the useragent string
            ua = data.get('useragent', '')
            
            # Check for trailing spaces
            if ua.endswith(' '):
                # Fix by removing trailing whitespace
                data['useragent'] = ua.rstrip()
                stats['fixed_uas'] += 1
            else:
                stats['unchanged_uas'] += 1
            
            # Add to fixed lines
            fixed_lines.append(json.dumps(data, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            print(f"[ERROR] Line {line_num}: JSON parse error - {e}")
            stats['errors'] += 1
            continue
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(fixed_path), exist_ok=True)
    
    # Write the fixed file
    with open(fixed_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(fixed_lines))
    
    return stats


def verify_fix(fixed_path: str) -> dict:
    """
    Verify that the fixed file has no trailing spaces.
    
    Args:
        fixed_path: Path to the fixed browsers.json file
    
    Returns:
        Dictionary with verification results
    """
    results = {
        'total_uas': 0,
        'with_trailing_spaces': 0,
        'without_trailing_spaces': 0,
        'valid_json': True
    }
    
    with open(fixed_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        try:
            data = json.loads(line)
            results['total_uas'] += 1
            
            ua = data.get('useragent', '')
            if ua.endswith(' '):
                results['with_trailing_spaces'] += 1
            else:
                results['without_trailing_spaces'] += 1
                
        except json.JSONDecodeError:
            results['valid_json'] = False
    
    return results


def main():
    """Main function to run the fix process."""
    print("=" * 70)
    print("Issue #307 Fix Script: Remove Trailing Spaces from User Agents")
    print("=" * 70)
    
    # Paths
    script_dir = Path(__file__).parent
    
    # For demonstration - use original project path
    original_path = script_dir.parent / "issue_project" / "src" / "fake_useragent" / "data" / "browsers.json"
    
    # If original doesn't exist, use a relative reference
    if not original_path.exists():
        original_path = Path("../issue_project/src/fake_useragent/data/browsers.json")
    
    fixed_path = script_dir / "src" / "fake_useragent" / "data" / "browsers.json"
    
    print(f"\nOriginal file: {original_path}")
    print(f"Fixed file: {fixed_path}")
    
    if not original_path.exists():
        print(f"\n[WARNING] Original file not found at {original_path}")
        print("The fixed file already exists in this project.")
        print("This script demonstrates the fix methodology.\n")
        
        # Just verify existing fixed file
        if fixed_path.exists():
            print("Verifying existing fixed file...")
            verify_results = verify_fix(str(fixed_path))
            print_verification_report(verify_results)
        return
    
    # Apply the fix
    print("\n" + "-" * 70)
    print("Applying Fix...")
    print("-" * 70)
    
    stats = fix_browsers_json(str(original_path), str(fixed_path))
    
    # Print fix report
    print_fix_report(stats)
    
    # Verify the fix
    print("\n" + "-" * 70)
    print("Verifying Fix...")
    print("-" * 70)
    
    verify_results = verify_fix(str(fixed_path))
    print_verification_report(verify_results)
    
    # Final status
    print("\n" + "=" * 70)
    print("Fix Completion Report")
    print("=" * 70)
    
    if verify_results['with_trailing_spaces'] == 0 and verify_results['valid_json']:
        print("\n[SUCCESS] Fix Completed Successfully!")
        print(f"  - Original UA Count: {stats['total_uas']}")
        print(f"  - Fixed UA Count: {stats['fixed_uas']}")
        print(f"  - Fix Ratio: {stats['fixed_uas']/stats['total_uas']*100:.1f}%")
        print(f"  - Output File: {fixed_path}")
    else:
        print("\n[FAILED] Fix incomplete or errors detected")
        if verify_results['with_trailing_spaces'] > 0:
            print(f"  - Still has {verify_results['with_trailing_spaces']} UAs with trailing spaces")
        if not verify_results['valid_json']:
            print("  - JSON validation failed")


def print_fix_report(stats: dict):
    """Print the fix statistics report."""
    print(f"\n[STATS] Fix Statistics:")
    print(f"  - Total User Agents: {stats['total_uas']}")
    print(f"  - Fixed (had trailing spaces): {stats['fixed_uas']}")
    print(f"  - Unchanged (no trailing spaces): {stats['unchanged_uas']}")
    print(f"  - Parse Errors: {stats['errors']}")
    
    if stats['total_uas'] > 0:
        fix_ratio = stats['fixed_uas'] / stats['total_uas'] * 100
        print(f"  - Fix Ratio: {fix_ratio:.1f}%")


def print_verification_report(results: dict):
    """Print the verification results report."""
    print(f"\n[VERIFY] Verification Results:")
    print(f"  - Total User Agents: {results['total_uas']}")
    print(f"  - With Trailing Spaces: {results['with_trailing_spaces']}")
    print(f"  - Without Trailing Spaces: {results['without_trailing_spaces']}")
    print(f"  - Valid JSON: {'Yes' if results['valid_json'] else 'No'}")
    
    if results['with_trailing_spaces'] == 0:
        print("\n  [OK] All User Agents have no trailing spaces!")
    else:
        print(f"\n  [X] Found {results['with_trailing_spaces']} UAs with trailing spaces")


if __name__ == "__main__":
    main()
