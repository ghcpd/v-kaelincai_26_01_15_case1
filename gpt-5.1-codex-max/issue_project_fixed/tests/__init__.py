"""Shared helpers for the lightweight test suite."""

from pathlib import Path
import json
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "src" / "fake_useragent" / "data" / "browsers.json"


def _locate_original_file() -> Path:
    """Find the source browsers.json shipped with the original project."""
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


ORIGINAL_DATA_FILE = _locate_original_file()


def load_jsonl(path: Path) -> List[dict]:
    """Load a JSONL file into a list of dictionaries."""
    lines = path.read_text(encoding="utf-8").splitlines()
    records = []
    for idx, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:  # pragma: no cover - defensive print path
            raise ValueError(f"Invalid JSON on line {idx}: {exc}") from exc
    return records


def count_space_issues(records: List[dict]) -> Tuple[int, int, int]:
    """Return counts for trailing, leading, and double spaces inside user agents."""
    trailing = 0
    leading = 0
    double = 0
    for record in records:
        ua = record.get("useragent", "")
        if ua.endswith(" "):
            trailing += 1
        if ua.startswith(" "):
            leading += 1
        if "  " in ua:
            double += 1
    return trailing, leading, double


def required_fields_present(record: dict) -> bool:
    """Check that a record has all required fields."""
    required_keys = {"useragent", "browser", "version", "os", "type", "system", "percent"}
    return required_keys.issubset(record.keys())
