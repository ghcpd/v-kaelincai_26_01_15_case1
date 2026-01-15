"""Clean trailing whitespace from browsers.json user agent strings.

Run this script from the project root to regenerate the fixed data file.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple

ROOT = Path(__file__).resolve().parent


def _locate_source_file() -> Path:
    """Find the original browsers.json shipped with issue_project."""
    candidates = [
        ROOT.parent / "issue_project" / "src" / "fake_useragent" / "data" / "browsers.json",
        ROOT.parent.parent
        / "issue_project"
        / "src"
        / "fake_useragent"
        / "data"
        / "browsers.json",
    ]
    for path in candidates:
        if path.exists():
            return path
    return candidates[0]


SOURCE = _locate_source_file()
TARGET = ROOT / "src" / "fake_useragent" / "data" / "browsers.json"


def _clean_record(record: dict) -> Tuple[dict, bool]:
    """Strip whitespace from the useragent field, leaving other fields intact."""
    ua = record.get("useragent", "")
    cleaned = ua.strip()
    updated = dict(record)
    updated["useragent"] = cleaned
    return updated, cleaned != ua


def fix_file(source: Path = SOURCE, target: Path = TARGET) -> Tuple[int, int, int]:
    """Clean the source JSONL file and write the fixed copy.

    Returns a tuple of (total, fixed_count, unchanged_count).
    """
    if not source.exists():
        raise FileNotFoundError(f"Missing source data file: {source}")

    lines = source.read_text(encoding="utf-8").splitlines()
    records = []
    fixed_count = 0

    for idx, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON on line {idx}: {exc}") from exc
        cleaned, changed = _clean_record(payload)
        if changed:
            fixed_count += 1
        records.append(cleaned)

    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as outfile:
        for record in records:
            outfile.write(json.dumps(record, ensure_ascii=False))
            outfile.write("\n")

    total = len(records)
    unchanged = total - fixed_count
    return total, fixed_count, unchanged


def main() -> None:
    print("=" * 70)
    print("Fix Completion Report")
    print("=" * 70)

    try:
        total, fixed, unchanged = fix_file()
    except Exception as exc:  # pragma: no cover - fatal path
        print(f"[X] Fix failed: {exc}")
        return

    ratio = (fixed / total * 100) if total else 0

    print(f"[SUCCESS] Fix completed!")
    print(f"  - Source file: {SOURCE}")
    print(f"  - Target file: {TARGET}")
    print(f"  - Original UA Count: {total}")
    print(f"  - Fixed UA Count: {fixed}")
    print(f"  - Unchanged UA Count: {unchanged}")
    print(f"  - Fix Ratio: {ratio:.1f}%")

    print("\nNext steps:")
    print("  - Run python test_fix.py for a quick verification")
    print("  - Run python tests/test_all.py for full coverage")


if __name__ == "__main__":
    main()
