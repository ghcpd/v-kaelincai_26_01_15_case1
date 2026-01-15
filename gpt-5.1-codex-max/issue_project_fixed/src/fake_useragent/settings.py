"""Lightweight settings used by the bundled fake_useragent clone."""

__version__ = "1.0.0-fixed"

# Replacements used to normalize browser keys
REPLACEMENTS = {
    " ": "",
    "-": "",
    "_": "",
}

# Friendly shortcuts that map to canonical browser keys
SHORTCUTS = {
    "google": "chrome",
    "googlechrome": "chrome",
    "chrome": "chrome",
    "edge": "edge",
    "edg": "edge",
    "firefox": "firefox",
    "ff": "firefox",
    "safari": "safari",
    "random": "random",
}

# Map coarse OS names to the values present in the dataset
OS_REPLACEMENTS = {
    "windows": ["win10"],
    "win": ["win10"],
    "mac": ["macos"],
    "macos": ["macos"],
    "linux": ["linux"],
    "android": ["android"],
    "ios": ["ios"],
}
