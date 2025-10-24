"""
Custom logger configuration using `loguru` for enhanced terminal output.

This logger:
- Uses stream output with color formatting.
- Supports all standard logging levels.
- Displays function names, file names, and line numbers.
- Can be reused as `logger` across the application for consistent logging.
"""

from loguru import logger as loguru_logger
import sys

# Remove default handlers (to avoid duplicate logs)
loguru_logger.remove()

# Add custom handler with color formatting
loguru_logger.add(
    sys.stdout,
    format="<green>[{time:YYYY-MM-DD HH:mm:ss}]</green> - "
    "<cyan>[{level}]</cyan> - "
    "def <yellow>{function}</yellow> - "
    "<white>{message}</white> - "
    "({name}:{line})",
    level="DEBUG",  # Capture all logs from DEBUG and above
    colorize=True,
    backtrace=False,  # Optional: set to True if you want deep tracebacks
    diagnose=False,  # Optional: extra debug info for exceptions
)

# Expose the configured logger as `logger` for reuse
logger = loguru_logger
