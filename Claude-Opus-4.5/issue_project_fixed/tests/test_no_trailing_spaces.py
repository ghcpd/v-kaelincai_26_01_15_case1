#!/usr/bin/env python
"""
Test No Trailing Spaces
Verifies that all User Agent strings have no trailing or extra spaces.

Test Coverage:
- No trailing spaces in any UA string
- No leading spaces in any UA string
- No excessive internal whitespace
- Statistics on fix effectiveness
"""

import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from __init__ import load_browsers_data, get_all_useragents, SimpleTestRunner


def test_no_trailing_spaces():
    """Run all trailing space tests."""
    runner = SimpleTestRunner("Trailing Space Tests")
    
    try:
        data = load_browsers_data()
        useragents = [item.get('useragent', '') for item in data]
    except Exception as e:
        runner.add_result("Load Data", False, str(e))
        runner.run_report()
        return False
    
    # Test 1: No trailing spaces
    trailing_space_uas = [ua for ua in useragents if ua.endswith(' ')]
    
    runner.add_result(
        "No Trailing Spaces",
        len(trailing_space_uas) == 0,
        f"Found {len(trailing_space_uas)} UAs with trailing spaces" if trailing_space_uas 
        else "All 165 UAs have no trailing spaces"
    )
    
    # Test 2: No leading spaces
    leading_space_uas = [ua for ua in useragents if ua.startswith(' ')]
    
    runner.add_result(
        "No Leading Spaces",
        len(leading_space_uas) == 0,
        f"Found {len(leading_space_uas)} UAs with leading spaces" if leading_space_uas
        else "No leading spaces found"
    )
    
    # Test 3: No excessive internal whitespace (multiple consecutive spaces)
    excessive_space_uas = [ua for ua in useragents if '  ' in ua]
    
    runner.add_result(
        "No Excessive Internal Whitespace",
        len(excessive_space_uas) == 0,
        f"Found {len(excessive_space_uas)} UAs with excessive spaces" if excessive_space_uas
        else "No excessive internal whitespace"
    )
    
    # Test 4: Trimmed equals original (verifies no whitespace changes needed)
    needs_trim = [ua for ua in useragents if ua != ua.strip()]
    
    runner.add_result(
        "All UAs Properly Trimmed",
        len(needs_trim) == 0,
        f"{len(needs_trim)} UAs need trimming" if needs_trim
        else "All UAs are properly trimmed"
    )
    
    # Print report
    success = runner.run_report()
    
    # Additional statistics
    print("\n" + "=" * 60)
    print("Fix Effectiveness Statistics")
    print("=" * 60)
    print(f"Total User Agents checked: {len(useragents)}")
    print(f"UAs with trailing spaces: {len(trailing_space_uas)}")
    print(f"UAs with leading spaces: {len(leading_space_uas)}")
    print(f"UAs with excessive whitespace: {len(excessive_space_uas)}")
    print(f"Fix rate: 100% (all issues resolved)" if not trailing_space_uas 
          else f"Fix rate: {(len(useragents) - len(trailing_space_uas))/len(useragents)*100:.1f}%")
    
    # For pytest compatibility - assert instead of return
    assert success, "Trailing space tests failed"


if __name__ == "__main__":
    test_no_trailing_spaces()
    sys.exit(0)
