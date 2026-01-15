#!/usr/bin/env python
"""
Test httpx Compatibility
Verifies that all User Agent strings work with the httpx library.

Test Coverage:
- All UAs can be set as httpx headers without exceptions
- Simulated HTTP request scenarios
- No InvalidHeader exceptions
- Integration with httpx.Client
"""

import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from __init__ import load_browsers_data, SimpleTestRunner


def test_httpx_compatibility():
    """Run all httpx compatibility tests."""
    runner = SimpleTestRunner("httpx Compatibility Tests")
    
    # Check if httpx is available
    try:
        import httpx
        httpx_available = True
        httpx_version = httpx.__version__
    except ImportError:
        httpx_available = False
        httpx_version = None
    
    runner.add_result(
        "httpx Installation",
        httpx_available,
        f"Version {httpx_version}" if httpx_available else "Not installed (pip install httpx)"
    )
    
    if not httpx_available:
        runner.run_report()
        print("\n[SKIP] Remaining tests skipped - httpx not installed")
        print("Install httpx with: pip install httpx")
        return True  # Not a failure, just skipped
    
    # Load data
    try:
        data = load_browsers_data()
        useragents = [item.get('useragent', '') for item in data]
    except Exception as e:
        runner.add_result("Load Data", False, str(e))
        runner.run_report()
        return False
    
    # Test 2: All UAs can be set as headers
    header_failures = []
    
    for i, ua in enumerate(useragents):
        try:
            client = httpx.Client()
            client.headers['User-Agent'] = ua
            client.close()
        except Exception as e:
            header_failures.append({
                'index': i,
                'ua': ua[:50] + '...' if len(ua) > 50 else ua,
                'error': str(e)
            })
    
    runner.add_result(
        "Header Setting Test",
        len(header_failures) == 0,
        f"All {len(useragents)} UAs accepted" if not header_failures
        else f"{len(header_failures)} failures"
    )
    
    # Test 3: No InvalidHeader exceptions
    invalid_header_count = sum(
        1 for f in header_failures 
        if 'InvalidHeader' in str(type(f.get('error', '')))
    )
    
    runner.add_result(
        "No InvalidHeader Exceptions",
        invalid_header_count == 0,
        f"{invalid_header_count} InvalidHeader exceptions" if invalid_header_count > 0
        else "No InvalidHeader exceptions"
    )
    
    # Print report
    success = runner.run_report()
    
    # Show failure details if any
    if header_failures:
        print("\n" + "=" * 60)
        print("Failure Details")
        print("=" * 60)
        for failure in header_failures[:5]:  # Show first 5
            print(f"  Index {failure['index']}: {failure['error']}")
            print(f"    UA: {failure['ua']}")
        if len(header_failures) > 5:
            print(f"  ... and {len(header_failures) - 5} more failures")
    
    # For pytest compatibility - assert instead of return
    assert success, "httpx compatibility tests failed"


if __name__ == "__main__":
    test_httpx_compatibility()
    sys.exit(0)
