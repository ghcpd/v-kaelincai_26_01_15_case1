#!/usr/bin/env python
"""
Quick Fix Verification Script
Verifies that the browsers.json fix was applied correctly.

Usage:
    python test_fix.py

This script provides a quick summary of:
- Before vs After comparison
- Trailing space detection
- Basic httpx compatibility check
"""

import json
import sys
from pathlib import Path


def get_script_dir():
    """Get the directory where this script is located."""
    return Path(__file__).parent


def load_browsers_json(path: Path) -> list:
    """Load and parse browsers.json file."""
    if not path.exists():
        return []
    
    data = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return data


def check_trailing_spaces(data: list) -> dict:
    """Check for trailing spaces in User Agent strings."""
    stats = {
        'total': len(data),
        'with_trailing': 0,
        'without_trailing': 0,
        'examples_with_trailing': []
    }
    
    for item in data:
        ua = item.get('useragent', '')
        if ua.endswith(' '):
            stats['with_trailing'] += 1
            if len(stats['examples_with_trailing']) < 3:
                stats['examples_with_trailing'].append(ua[:60] + '...')
        else:
            stats['without_trailing'] += 1
    
    return stats


def _check_httpx_compatibility(data: list, sample_size: int = 10) -> dict:
    """Check if UAs are compatible with httpx (internal helper, not a pytest test)."""
    results = {
        'httpx_available': False,
        'tested': 0,
        'passed': 0,
        'failed': 0,
        'errors': []
    }
    
    try:
        import httpx
        results['httpx_available'] = True
    except ImportError:
        return results
    
    import random
    samples = random.sample(data, min(sample_size, len(data)))
    
    for item in samples:
        ua = item.get('useragent', '')
        results['tested'] += 1
        
        try:
            # Try setting the header - this validates the UA string
            client = httpx.Client()
            client.headers['User-Agent'] = ua
            client.close()
            results['passed'] += 1
        except Exception as e:
            results['failed'] += 1
            results['errors'].append(f"{ua[:40]}... -> {str(e)[:50]}")
    
    return results


def main():
    """Main verification function."""
    print("=" * 70)
    print("Quick Fix Verification Report")
    print("=" * 70)
    
    script_dir = get_script_dir()
    
    # Paths
    fixed_path = script_dir / "src" / "fake_useragent" / "data" / "browsers.json"
    original_path = script_dir.parent / "issue_project" / "src" / "fake_useragent" / "data" / "browsers.json"
    
    print(f"\nFixed file: {fixed_path}")
    print(f"Original file: {original_path}")
    
    # Load fixed data
    fixed_data = load_browsers_json(fixed_path)
    
    if not fixed_data:
        print("\n[ERROR] Could not load fixed browsers.json!")
        return 1
    
    print(f"\n{'-' * 70}")
    print("1. Fixed File Analysis")
    print(f"{'-' * 70}")
    
    fixed_stats = check_trailing_spaces(fixed_data)
    print(f"\n  Total User Agents: {fixed_stats['total']}")
    print(f"  With Trailing Spaces: {fixed_stats['with_trailing']}")
    print(f"  Without Trailing Spaces: {fixed_stats['without_trailing']}")
    
    if fixed_stats['with_trailing'] == 0:
        print("\n  [PASS] No trailing spaces found in fixed file!")
    else:
        print(f"\n  [FAIL] Found {fixed_stats['with_trailing']} UAs with trailing spaces")
        for ex in fixed_stats['examples_with_trailing']:
            print(f"    - {ex}")
    
    # Compare with original if available
    original_data = load_browsers_json(original_path)
    
    if original_data:
        print(f"\n{'-' * 70}")
        print("2. Before/After Comparison")
        print(f"{'-' * 70}")
        
        original_stats = check_trailing_spaces(original_data)
        
        print(f"\n  Original file:")
        print(f"    - Total: {original_stats['total']}")
        print(f"    - With trailing spaces: {original_stats['with_trailing']}")
        print(f"    - Ratio: {original_stats['with_trailing']/original_stats['total']*100:.1f}%")
        
        print(f"\n  Fixed file:")
        print(f"    - Total: {fixed_stats['total']}")
        print(f"    - With trailing spaces: {fixed_stats['with_trailing']}")
        print(f"    - Ratio: {fixed_stats['with_trailing']/fixed_stats['total']*100:.1f}% (should be 0%)")
        
        if original_stats['total'] == fixed_stats['total']:
            print(f"\n  [PASS] Data integrity preserved: {fixed_stats['total']} UAs")
        else:
            print(f"\n  [WARN] UA count mismatch: {original_stats['total']} -> {fixed_stats['total']}")
    
    # Test httpx compatibility
    print(f"\n{'-' * 70}")
    print("3. httpx Compatibility Test")
    print(f"{'-' * 70}")
    
    httpx_results = _check_httpx_compatibility(fixed_data)
    
    if not httpx_results['httpx_available']:
        print("\n  [SKIP] httpx not installed")
        print("  Install with: pip install httpx")
    else:
        print(f"\n  Tested: {httpx_results['tested']} random User Agents")
        print(f"  Passed: {httpx_results['passed']}")
        print(f"  Failed: {httpx_results['failed']}")
        
        if httpx_results['failed'] == 0:
            print("\n  [PASS] All tested UAs are httpx compatible!")
        else:
            print(f"\n  [FAIL] {httpx_results['failed']} UAs failed httpx test")
            for err in httpx_results['errors'][:3]:
                print(f"    - {err}")
    
    # Summary
    print(f"\n{'=' * 70}")
    print("Summary")
    print(f"{'=' * 70}")
    
    all_pass = True
    
    # Check 1: No trailing spaces
    if fixed_stats['with_trailing'] == 0:
        print("\n[PASS] Trailing Space Check: No trailing spaces")
    else:
        print(f"\n[FAIL] Trailing Space Check: {fixed_stats['with_trailing']} issues")
        all_pass = False
    
    # Check 2: Data count
    if fixed_stats['total'] == 165:
        print("[PASS] Data Integrity: 165 User Agents present")
    else:
        print(f"[WARN] Data Integrity: Expected 165, found {fixed_stats['total']}")
    
    # Check 3: httpx
    if httpx_results['httpx_available']:
        if httpx_results['failed'] == 0:
            print("[PASS] httpx Compatibility: All tests passed")
        else:
            print(f"[FAIL] httpx Compatibility: {httpx_results['failed']} failures")
            all_pass = False
    else:
        print("[SKIP] httpx Compatibility: httpx not installed")
    
    print(f"\n{'=' * 70}")
    if all_pass:
        print("[SUCCESS] All checks passed! Fix verified successfully.")
    else:
        print("[WARNING] Some checks failed. Please review.")
    print(f"{'=' * 70}")
    
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
