"""Custom exceptions for tkinter-unblur."""

from __future__ import annotations


class TkinterUnblurError(Exception):
    """Base exception for tkinter-unblur."""

    pass


class UnsupportedPlatformError(TkinterUnblurError):
    """Raised when the platform does not support DPI awareness features.

    This typically occurs on non-Windows platforms where the DPI awareness
    APIs are not available. The library will still work, but DPI scaling
    will not be applied.
    """

    pass


class DPIDetectionError(TkinterUnblurError):
    """Raised when DPI detection fails.

    This can occur when:
    - The window handle is invalid
    - The monitor cannot be determined
    - The DPI query fails for any reason
    """

    pass
