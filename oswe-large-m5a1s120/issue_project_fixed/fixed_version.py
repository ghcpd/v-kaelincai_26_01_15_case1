"""
Automated fix script for fake-useragent Issue #307 (trailing spaces in UA strings)

- Reads the original JSONL file from ../issue_project/src/fake_useragent/data/browsers.json
- Strips trailing spaces from the `useragent` field only
- Writes a fixed JSONL file to ./src/fake_useragent/data/browsers.json
- Reports statistics before/after
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List, Tuple, Dict, Any

ROOT = Path(__file__).resolve().parent


def _candidate_original_paths() -> Iterable[Path]:
    # Typical layout: ../issue_project/fake_useragent/... (sibling to fixed project parent)
    yield ROOT.parent / "issue_project" / "src" / "fake_useragent" / "data" / "browsers.json"
    # Workspace layout: ../../issue_project when fixed project inside oswe-large-*/...
    yield ROOT.parent.parent / "issue_project" / "src" / "fake_useragent" / "data" / "browsers.json"
    # Current working directory relative lookup
    yield Path.cwd() / ".." / "issue_project" / "src" / "fake_useragent" / "data" / "browsers.json"
    # Direct relative path from fixed project (if copied)
    yield ROOT / ".." / "issue_project" / "src" / "fake_useragent" / "data" / "browsers.json"


def find_original_path() -> Path:
    for cand in _candidate_original_paths():
        if cand.exists():
            return cand.resolve()
    raise FileNotFoundError(
        "Original data file not found. Checked: "
        + ", ".join(str(p) for p in _candidate_original_paths())
    )


SRC_ORIGINAL = find_original_path()
SRC_FIXED = ROOT / "src" / "fake_useragent" / "data" / "browsers.json"


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    """Load a JSON Lines file (one JSON object per line)."""
    lines = path.read_text(encoding="utf-8").splitlines()
    data = []
    for idx, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            data.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON at line {idx}: {exc}") from exc
    return data


def save_jsonl(path: Path, records: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for obj in records:
            f.write(json.dumps(obj, ensure_ascii=False))
            f.write("\n")


def fix_useragents(records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
    """Strip trailing spaces from the `useragent` field, return new list and count fixed."""
    fixed_records = []
    fixed_count = 0
    for rec in records:
        rec_copy = dict(rec)
        ua = rec_copy.get("useragent")
        if isinstance(ua, str):
            cleaned = ua.rstrip(" ")
            if cleaned != ua:
                fixed_count += 1
                rec_copy["useragent"] = cleaned
        fixed_records.append(rec_copy)
    return fixed_records, fixed_count


def compute_stats(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    ualist = [r.get("useragent", "") for r in records]
    trailing = sum(1 for ua in ualist if isinstance(ua, str) and ua.endswith(" "))
    leading = sum(1 for ua in ualist if isinstance(ua, str) and ua.startswith(" "))
    double_space = sum(1 for ua in ualist if isinstance(ua, str) and "  " in ua)
    unique = len({ua for ua in ualist if isinstance(ua, str)})
    dups = len(ualist) - unique
    return {
        "total": len(records),
        "trailing": trailing,
        "leading": leading,
        "double_space": double_space,
        "unique": unique,
        "dups": dups,
    }


def format_stats(label: str, stats: Dict[str, Any]) -> str:
    return (
        f"{label}:\n"
        f"  - Total:            {stats['total']}\n"
        f"  - Trailing spaces:  {stats['trailing']}\n"
        f"  - Leading spaces:   {stats['leading']}\n"
        f"  - Double spaces:    {stats['double_space']}\n"
        f"  - Unique UAs:       {stats['unique']}\n"
        f"  - Duplicates:       {stats['dups']}\n"
    )


def main() -> None:
    print("=" * 70)
    print("fake-useragent Issue #307 Fix Script")
    print("=" * 70)

    if not SRC_ORIGINAL.exists():
        raise FileNotFoundError(f"Original data file not found at {SRC_ORIGINAL}")

    # Load original
    original_records = load_jsonl(SRC_ORIGINAL)
    stats_before = compute_stats(original_records)

    # Fix
    fixed_records, fixed_count = fix_useragents(original_records)
    stats_after = compute_stats(fixed_records)

    # Save
    save_jsonl(SRC_FIXED, fixed_records)

    # Report
    print("\nFix Completion Report")
    print("-" * 70)
    print(format_stats("Before", stats_before))
    print(format_stats("After", stats_after))
    ratio = (fixed_count / stats_before["total"] * 100) if stats_before["total"] else 0
    print(f"  - Fixed UA Count:    {fixed_count}")
    print(f"  - Fix Ratio:         {ratio:.1f}%")

    # Simple assertions
    assert stats_after["total"] == 165, "Expected 165 records after fix"
    assert stats_after["trailing"] == 0, "Trailing spaces should be zero after fix"

    print("\n[SUCCESS] Fix completed and validated.")


if __name__ == "__main__":
    main()
