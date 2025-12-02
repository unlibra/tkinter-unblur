"""tkinter-unblur: Fix blurry Tkinter on Windows high-DPI displays.

This package provides a drop-in replacement for tkinter.Tk that automatically
applies DPI awareness on Windows 10/11, fixing the common "blurry text" problem.

Basic Usage:
    >>> from tkinter_unblur import Tk
    >>> root = Tk()
    >>> root.mainloop()

That's it! Your Tkinter application will now render crisply on high-DPI displays.

For advanced usage, you can access the DPI information:
    >>> root = Tk()
    >>> print(f"DPI: {root.dpi_x}x{root.dpi_y}")
    >>> print(f"Scaling: {root.dpi_scaling:.0%}")

Or scale values manually:
    >>> scaled_width = root.scale_value(800)  # Returns 1200 at 150% scaling
"""

from __future__ import annotations

from tkinter_unblur.core import HdpiTk, Tk
from tkinter_unblur.exceptions import (
    DPIDetectionError,
    TkinterUnblurError,
    UnsupportedPlatformError,
)

__version__ = "1.0.0"
__all__ = [
    "DPIDetectionError",
    "HdpiTk",
    "Tk",
    "TkinterUnblurError",
    "UnsupportedPlatformError",
    "__version__",
]
