from __future__ import annotations

import time
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests import print_header

TEST_MODULES = [
    "tests.test_data_integrity",
    "tests.test_no_trailing_spaces",
    "tests.test_httpx_compatibility",
    "tests.test_json_validity",
]


def main() -> None:
    print_header("All Tests Runner")
    start = time.perf_counter()
    total_modules = len(TEST_MODULES)
    failures = 0

    for mod_name in TEST_MODULES:
        module = __import__(mod_name, fromlist=["run"])
        try:
            module.run()
        except Exception as exc:
            failures += 1
            print(f"[FAIL] {mod_name}: {exc}")

    elapsed = time.perf_counter() - start
    print("=" * 36)
    print(f"Test modules run: {total_modules}, Failures: {failures}")
    print(f"Elapsed time: {elapsed:.2f}s")
    if failures == 0:
        print("[PASS] All test modules passed")
    else:
        print("[FAIL] Some test modules failed")


def test_all_modules():
    main()


if __name__ == "__main__":
    main()
