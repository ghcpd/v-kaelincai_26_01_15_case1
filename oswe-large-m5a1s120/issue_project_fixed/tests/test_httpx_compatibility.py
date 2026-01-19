from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests import (
    print_header,
    print_result,
    summarize,
    load_jsonl,
    get_fixed_data_path,
    try_import_httpx,
)


def simple_header_validator(ua: str) -> bool:
    """Mimic httpx header validation constraints relevant to trailing spaces.

    httpx disallows header values with trailing/leading whitespace or control chars
    (see encode/httpx#1640). This function returns True if the value is acceptable.
    """
    if not isinstance(ua, str):
        return False
    if ua.endswith(" ") or ua.startswith(" "):
        return False
    # Disallow control characters \r, \n, \0 per RFC 7230
    if any(ch in ua for ch in ("\r", "\n", "\0")):
        return False
    return True


def validate_with_httpx(httpx_mod, ua: str) -> bool:
    try:
        # Construct headers object directly to trigger validation
        httpx_mod.Headers({"User-Agent": ua})
        return True
    except Exception:
        return False


def run() -> None:
    print_header("httpx Compatibility Tests")
    passed = 0
    total = 0

    data_path = get_fixed_data_path()
    records = load_jsonl(data_path)
    uas = [r.get("useragent", "") for r in records]

    httpx_mod = try_import_httpx()
    use_httpx = httpx_mod is not None
    if use_httpx:
        print("[INFO] httpx detected; running strict header validation")
    else:
        print("[WARN] httpx not installed; using fallback validator (no network)")

    # Validate all UAs
    total += 1
    all_ok = True
    for ua in uas:
        ok = (
            validate_with_httpx(httpx_mod, ua) if use_httpx else simple_header_validator(ua)
        )
        if not ok:
            all_ok = False
            break
    print_result(all_ok, "Test Item 1: All User-Agent values accepted")
    passed += all_ok

    # Spot-check a couple of UAs to ensure they are strings and non-empty
    total += 1
    sample_ok = all(isinstance(u, str) and len(u) > 0 for u in uas[:5])
    print_result(sample_ok, "Test Item 2: Sample UAs are valid strings")
    passed += sample_ok

    summarize(total, passed)


def test_httpx_compatibility():
    run()


if __name__ == "__main__":
    run()
