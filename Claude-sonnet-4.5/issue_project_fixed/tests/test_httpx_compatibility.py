#!/usr/bin/env python3
"""
Test httpx Compatibility

This test verifies that all User Agent strings are compatible with the httpx library:
- All UAs can be set as headers in httpx
- No InvalidHeader exceptions are thrown
- Simulates actual HTTP request scenarios
"""

import sys
from pathlib import Path

# Add parent directory to path to import test utilities
sys.path.insert(0, str(Path(__file__).parent))

from __init__ import get_all_useragents, print_test_header, print_test_result


def test_httpx_header_validation():
    """Test that all User Agents pass httpx header validation"""
    try:
        import httpx
    except ImportError:
        print("[SKIP] httpx not installed. Install with: pip install httpx")
        return True
    
    useragents = get_all_useragents()
    
    passed = 0
    failed = 0
    
    for i, ua in enumerate(useragents, 1):
        try:
            # Try to create a client with this User-Agent
            client = httpx.Client()
            client.headers['User-Agent'] = ua
            client.close()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"[FAIL] UA #{i} failed httpx validation: {type(e).__name__}: {e}")
    
    total = len(useragents)
    status = "[PASS]" if failed == 0 else "[FAIL]"
    print(f"{status} httpx Header Validation: {passed}/{total} UAs passed")
    
    return failed == 0


def test_httpx_request_simulation():
    """Test that User Agents work in simulated HTTP requests"""
    try:
        import httpx
    except ImportError:
        print("[SKIP] httpx not installed. Install with: pip install httpx")
        return True
    
    useragents = get_all_useragents()
    
    # Test a sample of UAs (first 10)
    sample_size = min(10, len(useragents))
    sample_uas = useragents[:sample_size]
    
    passed = 0
    failed = 0
    
    for i, ua in enumerate(sample_uas, 1):
        try:
            # Create request with this User-Agent
            headers = {'User-Agent': ua}
            # Just create the headers, don't actually send request
            client = httpx.Client(headers=headers)
            
            # Verify the header was set correctly
            if client.headers.get('User-Agent') == ua:
                passed += 1
            else:
                failed += 1
                print(f"[FAIL] UA #{i} was modified during setting")
            
            client.close()
        except Exception as e:
            failed += 1
            print(f"[FAIL] UA #{i} failed in request simulation: {type(e).__name__}: {e}")
    
    total = len(sample_uas)
    status = "[PASS]" if failed == 0 else "[FAIL]"
    print(f"{status} Request Simulation: {passed}/{total} UAs work correctly (sample)")
    
    return failed == 0


def test_no_invalid_header_exception():
    """Test that no InvalidHeader exception is raised"""
    try:
        import httpx
        from httpx import InvalidHeader
    except ImportError:
        print("[SKIP] httpx not installed. Install with: pip install httpx")
        return True
    
    useragents = get_all_useragents()
    
    passed = 0
    failed = 0
    
    for i, ua in enumerate(useragents, 1):
        try:
            client = httpx.Client()
            client.headers['User-Agent'] = ua
            client.close()
            passed += 1
        except InvalidHeader as e:
            failed += 1
            print(f"[FAIL] UA #{i} raised InvalidHeader: {e}")
        except Exception:
            # Other exceptions are not InvalidHeader, so they pass this specific test
            passed += 1
    
    total = len(useragents)
    status = "[PASS]" if failed == 0 else "[FAIL]"
    print(f"{status} No InvalidHeader: {passed}/{total} UAs don't raise InvalidHeader")
    
    return failed == 0


def main():
    """Run all httpx compatibility tests"""
    print_test_header("httpx Compatibility Tests")
    
    tests = [
        test_httpx_header_validation,
        test_httpx_request_simulation,
        test_no_invalid_header_exception
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
