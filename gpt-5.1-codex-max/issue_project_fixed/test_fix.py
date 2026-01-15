"""Quick verification script for the fixed browsers.json file."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIXED_FILE = ROOT / "src" / "fake_useragent" / "data" / "browsers.json"


def _locate_original_file() -> Path:
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


ORIGINAL_FILE = _locate_original_file()


def load_records(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    records = []
    for idx, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON on line {idx}: {exc}") from exc
    return records


def count_trailing(records):
    return sum(rec.get("useragent", "").endswith(" ") for rec in records)


def main() -> int:
    print("=" * 70)
    print("Quick Verification Report")
    print("=" * 70)

    if not FIXED_FILE.exists():
        print(f"[X] Fixed file not found: {FIXED_FILE}")
        print("  Run python fixed_version.py first.")
        return 1

    original = load_records(ORIGINAL_FILE)
    fixed = load_records(FIXED_FILE)

    orig_trailing = count_trailing(original)
    fixed_trailing = count_trailing(fixed)

    checks = []
    checks.append(("User agent count matches original (165)", len(fixed) == 165))
    checks.append(("Trailing spaces removed", fixed_trailing == 0))
    checks.append(("No data loss", len(fixed) == len(original)))
    checks.append(("Trailing space reduction", fixed_trailing < orig_trailing))

    for label, ok in checks:
        status = "[PASS]" if ok else "[FAIL]"
        print(f"{status} {label}")

    print("\nStatistics:")
    print(f"  Original trailing spaces: {orig_trailing}")
    print(f"  Fixed trailing spaces: {fixed_trailing}")
    print(f"  Total user agents: {len(fixed)}")

    success = all(ok for _, ok in checks)
    print("\nSummary:")
    if success:
        print("[OK] Quick verification passed")
    else:
        print("[X] Verification failed")
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
