"""Windows-specific DPI detection functionality.

This module should only be imported on Windows platforms.
"""

from __future__ import annotations

import logging
from ctypes import POINTER, WinDLL, byref, c_int, c_long, c_uint
from ctypes.wintypes import DWORD, HMONITOR, HWND

__all__ = ["get_dpi_info_windows", "set_process_dpi_awareness"]

logger = logging.getLogger(__name__)

# DPI constants
DPI_100_PERCENT = 96
DPI_TYPE_EFFECTIVE = 0  # MDT_EFFECTIVE_DPI
MONITOR_DEFAULTTONEAREST = 2
PROCESS_SYSTEM_DPI_AWARE = 1

# HRESULT values (signed 32-bit)
S_OK = 0
E_ACCESSDENIED = -2147024891  # 0x80070005


def set_process_dpi_awareness() -> None:
    """Make the process system DPI aware.

    Microsoft requires SetProcessDpiAwareness to be called before any API
    that depends on DPI awareness, so call this before creating a Tk window.
    """
    try:
        shcore = WinDLL("shcore")
    except OSError:
        logger.warning("Failed to load shcore.dll for DPI awareness")
        return

    # Return the HRESULT as a signed value instead of an int of unknown sign
    shcore.SetProcessDpiAwareness.restype = c_long
    shcore.SetProcessDpiAwareness.argtypes = [c_int]

    try:
        result = shcore.SetProcessDpiAwareness(PROCESS_SYSTEM_DPI_AWARE)
    except OSError as e:
        logger.warning(f"SetProcessDpiAwareness failed: {e}")
        return

    if result == S_OK:
        logger.debug("SetProcessDpiAwareness(1) succeeded")
    elif result == E_ACCESSDENIED:
        # Set earlier by another call or by the application manifest
        logger.debug("SetProcessDpiAwareness(1) skipped: awareness already set")
    else:
        logger.warning(
            f"SetProcessDpiAwareness returned error code: {result & 0xFFFFFFFF:#010x}"
        )


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
