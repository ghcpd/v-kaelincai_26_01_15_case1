"""Whitespace checks for user agent strings."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests import DATA_FILE, ORIGINAL_DATA_FILE, count_space_issues, load_jsonl


def run() -> bool:
    print("=" * 36)
    print("Test: Trailing/Leading Spaces")
    print("=" * 36)

    fixed_records = load_jsonl(DATA_FILE)
    original_records = load_jsonl(ORIGINAL_DATA_FILE)

    fixed_trailing, fixed_leading, fixed_double = count_space_issues(fixed_records)
    orig_trailing, orig_leading, orig_double = count_space_issues(original_records)

    checks = []
    checks.append(("No trailing spaces remain", fixed_trailing == 0))
    checks.append(("No leading spaces remain", fixed_leading == 0))
    checks.append(("No double spaces inside strings", fixed_double == 0))
    checks.append(("Trailing space count decreased", fixed_trailing < orig_trailing))

    for label, ok in checks:
        status = "[PASS]" if ok else "[FAIL]"
        print(f"{status} {label}")

    print("-" * 36)
    print("Before fix:")
    print(f"  Trailing spaces: {orig_trailing}")
    print(f"  Leading spaces: {orig_leading}")
    print(f"  Double spaces: {orig_double}")

    print("After fix:")
    print(f"  Trailing spaces: {fixed_trailing}")
    print(f"  Leading spaces: {fixed_leading}")
    print(f"  Double spaces: {fixed_double}")

    passed = sum(1 for _, ok in checks if ok)
    total = len(checks)
    pct = passed / total * 100
    print("-" * 36)
    print(f"Total: {passed}/{total} Passed ({pct:.0f}%)")
    return passed == total


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)


def test_pytest_wrapper():
    assert run()
