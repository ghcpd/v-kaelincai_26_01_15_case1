"""
Quick verification script for fake-useragent Issue #307 fix.

Usage:
    python test_fix.py
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
# Ensure project root on sys.path for direct `python test_fix.py`
for candidate in (ROOT, PARENT):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from tests import load_jsonl, compute_stats, get_fixed_data_path, get_original_data_path


def main() -> None:
    print("=" * 70)
    print("Quick Verification: Trailing Spaces Fix")
    print("=" * 70)

    fixed_path = get_fixed_data_path()
    orig_path = get_original_data_path()

    before_stats = None
    if orig_path.exists():
        before_records = load_jsonl(orig_path)
        before_stats = compute_stats(before_records)
        print("Original Data Stats:")
        for k, v in before_stats.items():
            print(f"  - {k.title():<14}: {v}")
    else:
        print(f"[WARN] Original data file not found at {orig_path}")

    after_records = load_jsonl(fixed_path)
    after_stats = compute_stats(after_records)
    print("\nFixed Data Stats:")
    for k, v in after_stats.items():
        print(f"  - {k.title():<14}: {v}")

    if before_stats:
        fixed_count = before_stats["trailing"] - after_stats["trailing"]
        ratio = (
            (fixed_count / before_stats["total"]) * 100 if before_stats["total"] else 0
        )
        print("\nFix Effectiveness:")
        print(f"  - Fixed UA Count: {fixed_count}")
        print(f"  - Fix Ratio:      {ratio:.1f}%")

    print("\nVerification:")
    assert after_stats["total"] == 165, "Expected 165 User Agents"
    assert after_stats["trailing"] == 0, "No trailing spaces expected"
    assert after_stats["leading"] == 0, "No leading spaces expected"
    print("  [PASS] Counts and trailing-space checks passed")


if __name__ == "__main__":
    main()
