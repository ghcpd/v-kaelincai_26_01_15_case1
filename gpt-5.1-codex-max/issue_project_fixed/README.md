# issue_project_fixed

A cleaned copy of the fake-useragent sample project. The original `issue_project` bundled user agent strings with trailing spaces, which breaks strict HTTP header validation in libraries like httpx. This fixed version trims whitespace and includes a small regression test suite to keep the data healthy.

## What changed
- Removed trailing whitespace from every `useragent` entry in `src/fake_useragent/data/browsers.json` (165 rows preserved)
- Added a repeatable fix script (`fixed_version.py`) so the cleanup can be regenerated from the original file
- Added quick verification (`test_fix.py`) and a focused test suite under `tests/`
- Documented the issue, approach, and verification steps in `SOLUTION.md`

## Quick start
```bash
cd issue_project_fixed
python fixed_version.py      # rebuild cleaned data
python test_fix.py           # quick verification
python tests/test_all.py     # full suite (or run individual test_*.py files)
```
If pytest is installed, you can also run `pytest tests/`.

## Verifying the fix
The key checks are:
- 165 user agents remain after cleanup
- No `useragent` string starts or ends with whitespace
- httpx accepts every string as a header value
- JSON lines remain valid UTF-8 JSON objects

## Differences from the original
- Data is whitespace-normalized only; no fields were altered or removed
- Added lightweight `settings.py` and `log.py` so `fake_useragent` imports cleanly
- Added documentation and tests to make the fix reproducible

## Project layout
```
issue_project_fixed/
├── fixed_version.py
├── test_fix.py
├── README.md
├── SOLUTION.md
├── src/fake_useragent/
│   ├── __init__.py
│   ├── errors.py
│   ├── fake.py
│   ├── log.py
│   ├── settings.py
│   ├── utils.py
│   └── data/browsers.json
└── tests/
    ├── __init__.py
    ├── test_all.py
    ├── test_data_integrity.py
    ├── test_httpx_compatibility.py
    ├── test_json_validity.py
    └── test_no_trailing_spaces.py
```
