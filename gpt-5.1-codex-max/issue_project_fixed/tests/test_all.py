"""Run the full test suite in sequence."""

from __future__ import annotations

import importlib
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

TEST_MODULES = [
    "tests.test_data_integrity",
    "tests.test_no_trailing_spaces",
    "tests.test_httpx_compatibility",
    "tests.test_json_validity",
]


def run() -> bool:
    print("=" * 36)
    print("Test: Full Suite")
    print("=" * 36)

    start = time.time()
    results = []
    for module_name in TEST_MODULES:
        module = importlib.import_module(module_name)
        outcome = bool(module.run())
        results.append((module_name, outcome))

    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    pct = passed / total * 100 if total else 0

    for module_name, ok in results:
        status = "[PASS]" if ok else "[FAIL]"
        print(f"{status} {module_name}")

    duration = time.time() - start
    print("-" * 36)
    print(f"Total: {passed}/{total} Passed ({pct:.0f}%)")
    print(f"Elapsed: {duration:.2f}s")
    return passed == total


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)


def test_pytest_wrapper():
    assert run()
