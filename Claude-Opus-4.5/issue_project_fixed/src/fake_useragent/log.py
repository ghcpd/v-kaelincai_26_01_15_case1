"""
Logging configuration for fake-useragent
"""

import logging

logger = logging.getLogger("fake_useragent")
logger.setLevel(logging.WARNING)

# Add a handler if none exists
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
