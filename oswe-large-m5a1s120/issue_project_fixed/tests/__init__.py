"""Test helpers for the fixed fake-useragent project."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, Any, Iterable, List

ROOT = Path(__file__).resolve().parents[1]
# Ensure project root is on sys.path for `python tests/xyz.py`
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def get_fixed_data_path() -> Path:
    return ROOT / "src" / "fake_useragent" / "data" / "browsers.json"


def get_original_data_path() -> Path:
    # Candidates relative to fixed project
    candidates = [
        ROOT.parent / "issue_project" / "src" / "fake_useragent" / "data" / "browsers.json",
        ROOT.parent.parent / "issue_project" / "src" / "fake_useragent" / "data" / "browsers.json",
    ]
    for cand in candidates:
        if cand.exists():
            return cand.resolve()
    # Fallback: return expected sibling path even if missing
    return candidates[0]


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    data: List[Dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            line = line.strip("\n")
            if not line.strip():
                continue
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise AssertionError(f"Invalid JSON at line {idx}: {exc}") from exc
    return data


def compute_stats(records: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    records = list(records)
    uas = [r.get("useragent", "") for r in records]
    trailing = sum(1 for ua in uas if isinstance(ua, str) and ua.endswith(" "))
    leading = sum(1 for ua in uas if isinstance(ua, str) and ua.startswith(" "))
    double_space = sum(1 for ua in uas if isinstance(ua, str) and "  " in ua)
    unique = len({ua for ua in uas if isinstance(ua, str)})
    dups = len(uas) - unique
    return {
        "total": len(records),
        "trailing": trailing,
        "leading": leading,
        "double_space": double_space,
        "unique": unique,
        "dups": dups,
    }


def print_header(title: str) -> None:
    bar = "=" * 36
    print(f"{bar}\nTest: {title}\n{bar}")


def print_result(ok: bool, message: str) -> None:
    status = "[PASS]" if ok else "[FAIL]"
    print(f"{status} {message}")


def summarize(total: int, passed: int) -> None:
    print("-" * 36)
    pct = (passed / total * 100) if total else 0
    print(f"Total: {passed}/{total} Passed ({pct:.0f}%)")


def try_import_httpx():
    try:
        import httpx  # type: ignore

        return httpx
    except ImportError:
        return None
