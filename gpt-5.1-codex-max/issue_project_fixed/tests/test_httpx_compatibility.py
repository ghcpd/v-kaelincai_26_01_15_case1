"""Validate that each user agent is accepted as an HTTP header value."""

from __future__ import annotations

from pathlib import Path
from typing import Callable
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests import DATA_FILE, load_jsonl

try:  # pragma: no cover - environment dependent
    import httpx

    HTTPX_AVAILABLE = True
except ImportError:  # pragma: no cover - environment dependent
    httpx = None
    HTTPX_AVAILABLE = False


def _fallback_validator(ua: str) -> None:
    """Minimal header check mirroring httpx constraints."""
    if ua.startswith(" ") or ua.endswith(" "):
        raise ValueError("Header value has surrounding spaces")
    for ch in ua:
        if ord(ch) < 32 or ord(ch) == 127:
            raise ValueError("Control character in header")


def _httpx_validator(ua: str) -> None:
    with httpx.Client() as client:  # type: ignore[arg-type]
        client.headers["User-Agent"] = ua


def run() -> bool:
    print("=" * 36)
    print("Test: httpx Compatibility")
    print("=" * 36)

    records = load_jsonl(DATA_FILE)
    validator: Callable[[str], None] = _httpx_validator if HTTPX_AVAILABLE else _fallback_validator

    errors = []
    for record in records:
        ua = record.get("useragent", "")
        try:
            validator(ua)
        except Exception as exc:  # pragma: no cover - defensive
            errors.append((ua, exc))

    if HTTPX_AVAILABLE:
        print("[INFO] httpx available: real header validation used")
    else:
        print("[INFO] httpx not installed: using lightweight header validator")

    if not errors:
        print("[PASS] All user agents accepted")
    else:
        print(f"[FAIL] {len(errors)} user agents were rejected")
        for ua, exc in errors[:3]:
            print(f"  Example failure: {exc} for '{ua[:80]}'")

    total = len(records)
    passed = total - len(errors)
    pct = (passed / total * 100) if total else 0
    print("-" * 36)
    print(f"Total: {passed}/{total} Accepted ({pct:.0f}%)")
    return not errors


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)


def test_pytest_wrapper():
    assert run()
