from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests import (
    print_header,
    print_result,
    summarize,
    load_jsonl,
    compute_stats,
    get_fixed_data_path,
    get_original_data_path,
)

EXPECTED_TOTAL = 165
EXPECTED_TRAILING_BEFORE = 93  # from the provided issue stats
EXPECTED_TRAILING_AFTER = 0


def run() -> None:
    print_header("Trailing/Leading Space Tests")
    passed = 0
    total = 0

    fixed_path = get_fixed_data_path()
    orig_path = get_original_data_path()

    before_stats = None
    if orig_path.exists():
        before_records = load_jsonl(orig_path)
        before_stats = compute_stats(before_records)

    after_records = load_jsonl(fixed_path)
    after_stats = compute_stats(after_records)

    # Trailing spaces removed
    total += 1
    ok = after_stats["trailing"] == EXPECTED_TRAILING_AFTER
    print_result(ok, "Test Item 1: No trailing spaces after fix")
    passed += ok

    # Leading spaces none
    total += 1
    ok = after_stats["leading"] == 0
    print_result(ok, "Test Item 2: No leading spaces after fix")
    passed += ok

    # Double spaces in middle (conservative check)
    total += 1
    ok = after_stats["double_space"] == 0
    print_result(ok, "Test Item 3: No double spaces in UA strings")
    passed += ok

    # Count unchanged
    total += 1
    ok = after_stats["total"] == EXPECTED_TOTAL
    print_result(ok, f"Test Item 4: Record count preserved ({EXPECTED_TOTAL})")
    passed += ok

    # Before stats checks (if available)
    if before_stats:
        total += 1
        ok = before_stats["trailing"] == EXPECTED_TRAILING_BEFORE
        print_result(ok, f"Test Item 5: Before-fix trailing spaces == {EXPECTED_TRAILING_BEFORE}")
        passed += ok

    summarize(total, passed)


def test_no_trailing_spaces():
    run()


if __name__ == "__main__":
    run()
