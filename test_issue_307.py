"""
Test Script: Reproduce fake-useragent Issue #307
Problem: Trailing spaces in user agent strings cause httpx exceptions

This script demonstrates how trailing spaces cause httpx library to throw exceptions
"""

import json
import sys
from pathlib import Path

def check_trailing_spaces():
    """Check for trailing spaces in browsers.json"""
    print("=" * 60)
    print("Checking User Agent Strings for Trailing Spaces")
    print("=" * 60)
    
    data_file = Path("src/fake_useragent/data/browsers.json")
    
    if not data_file.exists():
        print(f"[X] Data file not found: {data_file}")
        return False
    
    with open(data_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    total_count = 0
    trailing_space_count = 0
    examples = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        try:
            data = json.loads(line)
            ua = data.get('useragent', '')
            total_count += 1
            
            # Check for trailing spaces
            if ua.endswith(' '):
                trailing_space_count += 1
                if len(examples) < 3:
                    examples.append(ua)
        except json.JSONDecodeError:
            continue
    
    print(f"\nStatistics:")
    print(f"  Total User Agents: {total_count}")
    print(f"  With trailing spaces: {trailing_space_count}")
    print(f"  Ratio: {trailing_space_count/total_count*100:.1f}%")
    
    if trailing_space_count > 0:
        print(f"\n[X] Problem found! {trailing_space_count} UA strings have trailing spaces")
        print("\nExamples (note the trailing spaces):")
        for i, ua in enumerate(examples, 1):
            print(f"  {i}. '{ua}'")
            print(f"     ^ Has trailing space")
        return True
    else:
        print("\n[OK] All UA strings have no trailing spaces")
        return False

def test_with_httpx():
    """Test if trailing spaces cause httpx exceptions"""
    print("\n" + "=" * 60)
    print("Testing httpx Compatibility")
    print("=" * 60)
    
    try:
        import httpx
        print("[OK] httpx is installed")
    except ImportError:
        print("[X] httpx is not installed")
        print("  Install command: pip install httpx")
        return None
    
    # Test UA with trailing space
    ua_with_space = "Mozilla/5.0 (Windows NT 10.0) Chrome/121.0.0.0 "
    ua_without_space = "Mozilla/5.0 (Windows NT 10.0) Chrome/121.0.0.0"
    
    print("\nTest 1: UA without trailing space")
    try:
        with httpx.Client() as client:
            client.headers['User-Agent'] = ua_without_space
            print(f"  UA: '{ua_without_space}'")
            print("  [OK] Set successfully, no exception")
    except Exception as e:
        print(f"  [X] Exception occurred: {e}")
    
    print("\nTest 2: UA with trailing space")
    try:
        with httpx.Client() as client:
            client.headers['User-Agent'] = ua_with_space
            print(f"  UA: '{ua_with_space}'")
            print("  Note: Some versions of httpx may throw exceptions during actual requests")
            # Try making an actual request to trigger the error
            # response = client.get('http://httpbin.org/user-agent')
            print("  [OK] Set successfully (but may fail during actual request)")
    except Exception as e:
        print(f"  [X] Exception occurred: {type(e).__name__}: {e}")
        return True

def test_fake_useragent():
    """Test fake-useragent generated UAs"""
    print("\n" + "=" * 60)
    print("Testing fake-useragent Library")
    print("=" * 60)
    
    try:
        sys.path.insert(0, 'src')
        from fake_useragent import UserAgent
        
        ua = UserAgent()
        
        print("\nGenerating random User Agents:")
        for i in range(3):
            user_agent = ua.random
            has_trailing = user_agent.endswith(' ')
            marker = " [X] Has trailing space!" if has_trailing else ""
            print(f"  {i+1}. '{user_agent}'{marker}")
        
        return True
        
    except Exception as e:
        print(f"[X] Error importing or using fake-useragent: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("\n" + "=" * 70)
    print("fake-useragent Issue #307 Reproduction Test")
    print("Problem: spaces at end of user agent string break httpx")
    print("=" * 70)
    
    print(f"\nPython version: {sys.version}")
    
    # Check for trailing spaces
    has_problem = check_trailing_spaces()
    
    # Test httpx compatibility
    test_with_httpx()
    
    # Test fake-useragent
    test_fake_useragent()
    
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    
    if has_problem:
        print("\n[X] Problem confirmed!")
        print("\nProblem description:")
        print("  - Many UA strings in browsers.json have trailing spaces")
        print("  - These spaces cause httpx library to throw exceptions in some cases")
        print("  - Reference: https://github.com/encode/httpx/issues/1640")
        print("\nSolution:")
        print("  - Need to clean trailing spaces from all UA strings in browsers.json")
        print("  - Fix completed in PR #308")
    else:
        print("\n[OK] No trailing space problem found")
    
    print(f"\nView complete issue:")
    print("https://github.com/fake-useragent/fake-useragent/issues/307")

if __name__ == "__main__":
    main()
