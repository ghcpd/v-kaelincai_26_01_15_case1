__version__ = "1.5.1-fix307"

# Normalize requested browser/attr tokens
REPLACEMENTS = {
    " ": "",
    "_": "",
    "-": "",
    "/": "",
}

SHORTCUTS = {
    "ff": "firefox",
    "fx": "firefox",
    "firefox": "firefox",
    "chrome": "chrome",
    "googlechrome": "chrome",
    "gc": "chrome",
    "edge": "edge",
    "edg": "edge",
    "edgios": "edge",
    "edga": "edge",
    "safari": "safari",
    "duckduckgo": "DuckDuckGo Mobile",
    "duckduckgomobile": "DuckDuckGo Mobile",
    "ddg": "DuckDuckGo Mobile",
    "random": "random",
    # Platforms
    "pc": "pc",
    "mobile": "mobile",
    "tablet": "tablet",
}

# Expand coarse OS tokens into the granular values present in the dataset
OS_REPLACEMENTS = {
    "windows": ["win10"],
    "win": ["win10"],
    "mac": ["macos"],
    "macos": ["macos"],
    "linux": ["linux"],
    "android": ["android"],
    "ios": ["ios"],
}
