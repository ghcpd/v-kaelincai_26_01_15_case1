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
)

REQUIRED_FIELDS = {
    "useragent": str,
    "percent": (float, int),
    "type": str,
    "system": str,
    "browser": str,
    "version": (float, int),
    "os": str,
}

EXPECTED_TOTAL = 165
EXPECTED_DUPLICATES = 83  # Derived from dataset (165 total, 82 unique)
EXPECTED_BROWSERS = {"chrome", "edge", "firefox", "safari", "DuckDuckGo Mobile"}
EXPECTED_OSES = {"android", "ios", "linux", "macos", "win10"}
EXPECTED_TYPES = {"pc", "mobile", "tablet"}


def run() -> None:
    print_header("Data Integrity Tests")
    passed = 0
    total = 0

    data_path = get_fixed_data_path()
    records = load_jsonl(data_path)
    stats = compute_stats(records)

    # Count check
    total += 1
    ok = stats["total"] == EXPECTED_TOTAL
    print_result(ok, f"Test Item 1: UA count == {EXPECTED_TOTAL} (got {stats['total']})")
    passed += ok

    # Required fields & types
    total += 1
    missing_or_type_errors = []
    for idx, rec in enumerate(records, 1):
        for field, expected_type in REQUIRED_FIELDS.items():
            if field not in rec:
                missing_or_type_errors.append((idx, field, "missing"))
                continue
            val = rec[field]
            if not isinstance(val, expected_type):
                missing_or_type_errors.append((idx, field, f"type {type(val)}"))
    ok = len(missing_or_type_errors) == 0
    print_result(ok, "Test Item 2: Required fields present with correct types")
    if not ok:
        print(f"       Errors (first 5): {missing_or_type_errors[:5]}")
    passed += ok

    # Value domains
    total += 1
    bad_domain = []
    for idx, rec in enumerate(records, 1):
        if rec["browser"] not in EXPECTED_BROWSERS:
            bad_domain.append((idx, "browser", rec["browser"]))
        if rec["os"] not in EXPECTED_OSES:
            bad_domain.append((idx, "os", rec["os"]))
        if rec["type"] not in EXPECTED_TYPES:
            bad_domain.append((idx, "type", rec["type"]))
        if not (0 <= float(rec["percent"]) <= 100):
            bad_domain.append((idx, "percent", rec["percent"]))
    ok = len(bad_domain) == 0
    print_result(ok, "Test Item 3: Fields within expected domains")
    if not ok:
        print(f"       Errors (first 5): {bad_domain[:5]}")
    passed += ok

    # Duplicates (informational but ensure integrity relative to original)
    total += 1
    ok = stats["dups"] == EXPECTED_DUPLICATES
    print_result(ok, f"Test Item 4: Duplicate count matches expected ({EXPECTED_DUPLICATES})")
    if not ok:
        print(f"       Observed duplicates: {stats['dups']}")
    passed += ok

    summarize(total, passed)


def test_data_integrity():
    run()


if __name__ == "__main__":
    run()
