"""Windows-specific DPI detection functionality.

This module should only be imported on Windows platforms.
"""

from __future__ import annotations

import logging
from ctypes import POINTER, WinDLL, byref, c_uint
from ctypes.wintypes import DWORD, HMONITOR, HWND

__all__ = ["get_dpi_info_windows"]

logger = logging.getLogger(__name__)

# DPI constants
DPI_100_PERCENT = 96
DPI_TYPE_EFFECTIVE = 0  # MDT_EFFECTIVE_DPI
MONITOR_DEFAULTTONEAREST = 2


def get_dpi_info_windows(window_handle: int) -> tuple[int, int, float]:
    """Get DPI information on Windows platform.

    Args:
        window_handle: The native window handle (HWND).

    Returns:
        A tuple of (dpi_x, dpi_y, scaling_factor).
    """
    try:
        shcore = WinDLL("shcore")
        user32 = WinDLL("user32")
    except OSError:
        logger.warning("Failed to load Windows DLLs for DPI detection")
        return 96, 96, 1.0

    # Set process DPI awareness
    try:
        shcore.SetProcessDpiAwareness(1)
        logger.debug("SetProcessDpiAwareness(1) succeeded")
    except OSError:
        # This can fail on Windows Server or older Windows versions
        logger.debug(
            "SetProcessDpiAwareness failed (may be already set or unsupported)"
        )

    # Get monitor handle for the window
    user32.MonitorFromWindow.restype = HMONITOR
    user32.MonitorFromWindow.argtypes = [HWND, DWORD]
    monitor_handle = user32.MonitorFromWindow(
        HWND(window_handle), DWORD(MONITOR_DEFAULTTONEAREST)
    )

    if not monitor_handle:
        logger.warning("Failed to get monitor handle for window")
        return 96, 96, 1.0

    # Query DPI for the monitor
    shcore.GetDpiForMonitor.restype = c_uint
    shcore.GetDpiForMonitor.argtypes = [
        HMONITOR,
        c_uint,
        POINTER(c_uint),
        POINTER(c_uint),
    ]

    dpi_x = c_uint()
    dpi_y = c_uint()

    try:
        result = shcore.GetDpiForMonitor(
            monitor_handle,
            c_uint(DPI_TYPE_EFFECTIVE),
            byref(dpi_x),
            byref(dpi_y),
        )
        if result != 0:
            logger.warning(f"GetDpiForMonitor returned error code: {result}")
            return 96, 96, 1.0
    except OSError as e:
        logger.warning(f"GetDpiForMonitor failed: {e}")
        return 96, 96, 1.0

    x_val = dpi_x.value
    y_val = dpi_y.value
    scaling = (x_val + y_val) / (2 * DPI_100_PERCENT)

    logger.debug(f"DPI detected: x={x_val}, y={y_val}, scaling={scaling:.2f}")

    return x_val, y_val, scaling
