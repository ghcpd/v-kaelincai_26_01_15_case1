"""
Settings and constants for fake-useragent
"""

__version__ = "1.5.0"

# OS name replacements
OS_REPLACEMENTS = {
    "windows": ["win10", "win7"],
    "mac": ["macos"],
    "linux": ["linux"],
}

# Browser name replacements
REPLACEMENTS = {
    " ": "",
    "_": "",
}

# Browser shortcuts
SHORTCUTS = {
    "googlechrome": "chrome",
    "google": "chrome",
    "gc": "chrome",
    "ff": "firefox",
    "ie": "edge",
    "internetexplorer": "edge",
    "msedge": "edge",
    "microsoftedge": "edge",
}
