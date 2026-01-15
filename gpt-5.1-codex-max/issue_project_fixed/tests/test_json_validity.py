"""Ensure the JSONL data file remains valid."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests import DATA_FILE, load_jsonl


def run() -> bool:
    print("=" * 36)
    print("Test: JSON Validity")
    print("=" * 36)

    # Use the shared loader to confirm parseability
    records = load_jsonl(DATA_FILE)

    checks = []
    checks.append(("File exists", Path(DATA_FILE).exists()))
    checks.append(("All lines parse as JSON", bool(records)))
    checks.append(("Every record has useragent field", all("useragent" in r for r in records)))
    checks.append(("UTF-8 encoding preserved", DATA_FILE.read_text(encoding="utf-8")))

    for label, ok in checks:
        status = "[PASS]" if ok else "[FAIL]"
        print(f"{status} {label}")

    # Re-dump a sample to ensure JSON round-trip safety
    sample = records[0] if records else {}
    try:
        json.dumps(sample)
        sample_ok = True
    except TypeError:
        sample_ok = False

    status = "[PASS]" if sample_ok else "[FAIL]"
    print(f"{status} Sample object is JSON-serializable")

    passed = sum(1 for flag in [ok for _, ok in checks] + [sample_ok] if flag)
    total = len(checks) + 1
    pct = passed / total * 100
    print("-" * 36)
    print(f"Total: {passed}/{total} Passed ({pct:.0f}%)")
    return passed == total


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)


def test_pytest_wrapper():
    assert run()
