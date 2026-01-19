from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests import (
    print_header,
    print_result,
    summarize,
    get_fixed_data_path,
)

EXPECTED_TOTAL = 165


def run() -> None:
    print_header("JSON Validity Tests")
    passed = 0
    total = 0

    path = get_fixed_data_path()

    # Encoding check
    total += 1
    try:
        raw = path.read_bytes()
        raw.decode("utf-8")
        ok = True
    except Exception as exc:
        ok = False
        print(f"       Decoding error: {exc}")
    print_result(ok, "Test Item 1: File decodes as UTF-8")
    passed += ok

    # JSONL parsing
    total += 1
    parsed = []
    try:
        with path.open(encoding="utf-8") as f:
            for idx, line in enumerate(f, 1):
                line = line.strip("\n")
                if not line.strip():
                    continue
                parsed.append(json.loads(line))
        ok = True
    except Exception as exc:
        ok = False
        print(f"       JSON parse error at line {idx}: {exc}")
    print_result(ok, "Test Item 2: Each line parses as JSON object")
    passed += ok

    # Count check
    total += 1
    ok = len(parsed) == EXPECTED_TOTAL
    print_result(ok, f"Test Item 3: Parsed object count == {EXPECTED_TOTAL} (got {len(parsed)})")
    passed += ok

    # Object type check
    total += 1
    ok = all(isinstance(obj, dict) for obj in parsed)
    print_result(ok, "Test Item 4: All parsed entries are JSON objects")
    passed += ok

    summarize(total, passed)


def test_json_validity():
    run()


if __name__ == "__main__":
    run()
