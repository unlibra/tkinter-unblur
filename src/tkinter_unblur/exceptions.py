"""Custom exceptions for tkinter-unblur."""

from __future__ import annotations


class TkinterUnblurError(Exception):
    """Base exception for tkinter-unblur."""

    pass


class UnsupportedPlatformError(TkinterUnblurError):
    """Reserved for platforms that do not support DPI awareness features.

    This exception is not currently raised. On non-Windows platforms,
    DPI detection is skipped and Tk sets dpi_x and dpi_y to None and
    dpi_scaling to 1.0.
    """

    pass


class DPIDetectionError(TkinterUnblurError):
    """Reserved for DPI detection failures on Windows.

    This exception is not currently raised. When DPI detection fails,
    a warning is logged and Tk falls back to dpi_x = 96, dpi_y = 96 and
    dpi_scaling = 1.0 (100% scaling). This happens when:
    - The Windows DLLs (shcore, user32) cannot be loaded
    - The monitor for the window cannot be determined
    - The DPI query (GetDpiForMonitor) fails
    """

    pass
