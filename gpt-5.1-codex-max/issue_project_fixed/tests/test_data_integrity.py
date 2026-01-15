"""Data integrity checks for the fixed dataset."""

from __future__ import annotations

from pathlib import Path
from statistics import mean
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests import DATA_FILE, load_jsonl, required_fields_present


def run() -> bool:
    print("=" * 36)
    print("Test: Data Integrity")
    print("=" * 36)

    records = load_jsonl(DATA_FILE)

    checks = []
    checks.append(("Row count is 165", len(records) == 165))
    checks.append(("All records have required fields", all(required_fields_present(r) for r in records)))
    checks.append(("User agents are non-empty strings", all(isinstance(r.get("useragent", ""), str) and r.get("useragent", "") for r in records)))
    checks.append(("Numeric fields are numbers", all(isinstance(r.get("percent"), (int, float)) and isinstance(r.get("version"), (int, float)) for r in records)))
    checks.append(("Categorical fields are strings", all(isinstance(r.get(key, ""), str) for r in records for key in ("browser", "os", "system", "type"))))

    for label, ok in checks:
        status = "[PASS]" if ok else "[FAIL]"
        print(f"{status} {label}")

    # Informational stats
    versions = [r.get("version", 0) for r in records if isinstance(r.get("version"), (int, float))]
    percents = [r.get("percent", 0.0) for r in records if isinstance(r.get("percent"), (int, float))]
    unique_uas = len({r.get("useragent", "") for r in records})

    print("-" * 36)
    print("Stats:")
    print(f"  Unique user agents: {unique_uas} of {len(records)}")
    print(f"  Avg version: {mean(versions):.2f}")
    print(f"  Avg percent: {mean(percents):.2f}")

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
