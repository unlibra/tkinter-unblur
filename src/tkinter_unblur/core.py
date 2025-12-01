"""Core functionality for tkinter-unblur.

This module provides DPI awareness functionality for Tkinter applications
on Windows 10/11 high-DPI displays.
"""

from __future__ import annotations

import logging
import re
import sys
from tkinter import Tk as _TkBase
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from re import Match

__all__ = ["Tk", "get_dpi_info", "scale_geometry"]

logger = logging.getLogger(__name__)


def get_dpi_info(window_handle: int) -> tuple[int | None, int | None, float]:
    """Get DPI information for a window.

    Detects the DPI settings for the monitor containing the specified window
    and calculates the scaling factor.

    Args:
        window_handle: The native window handle (HWND on Windows).

    Returns:
        A tuple of (dpi_x, dpi_y, scaling_factor):
        - dpi_x: Horizontal DPI (96 = 100% scaling), or None on non-Windows
        - dpi_y: Vertical DPI (96 = 100% scaling), or None on non-Windows
        - scaling_factor: The scaling multiplier (1.0 = 100%, 1.5 = 150%, etc.)

    Note:
        On non-Windows platforms, returns (None, None, 1.0) as DPI awareness
        is typically handled by the OS.
    """
    if sys.platform != "win32":
        logger.debug("Non-Windows platform detected, skipping DPI detection")
        return None, None, 1.0

    # Import Windows-specific module only on Windows
    from tkinter_unblur._windows import get_dpi_info_windows

    x, y, scaling = get_dpi_info_windows(window_handle)
    return x, y, scaling


def scale_geometry(geometry: str, scale_func: Callable[[str], int]) -> str:
    """Scale a Tkinter geometry string.

    Converts a geometry string like "800x600+100+50" by applying the
    scale function to each numeric component.

    Args:
        geometry: A Tkinter geometry string in format "WxH+X+Y".
        scale_func: A function that takes a string number and returns
            the scaled integer value.

    Returns:
        The scaled geometry string.

    Raises:
        ValueError: If the geometry string format is invalid.

    Example:
        >>> scale_geometry("800x600+100+50", lambda v: int(float(v) * 1.5))
        "1200x900+150+75"
    """
    pattern = r"(?P<W>\d+)x(?P<H>\d+)\+(?P<X>-?\d+)\+(?P<Y>-?\d+)"
    match: Match[str] | None = re.search(pattern, geometry)

    if match is None:
        raise ValueError(f"Invalid geometry string format: {geometry!r}")

    width = scale_func(match.group("W"))
    height = scale_func(match.group("H"))
    x = scale_func(match.group("X"))
    y = scale_func(match.group("Y"))

    return f"{width}x{height}+{x}+{y}"


class Tk(_TkBase):
    """A DPI-aware Tk root window.

    This class extends tkinter.Tk to automatically apply DPI awareness
    on Windows 10/11 high-DPI displays, fixing the common "blurry text"
    problem.

    On non-Windows platforms, this class behaves identically to tkinter.Tk.

    Attributes:
        dpi_x: Horizontal DPI value (96 = 100% scaling), or None on non-Windows.
        dpi_y: Vertical DPI value (96 = 100% scaling), or None on non-Windows.
        dpi_scaling: The scaling factor (1.0 = 100%, 1.5 = 150%, etc.).

    Example:
        >>> from tkinter_unblur import Tk
        >>> root = Tk()
        >>> print(f"Scaling: {root.dpi_scaling:.0%}")
        Scaling: 150%
        >>> root.mainloop()
    """

    dpi_x: int | None
    dpi_y: int | None
    dpi_scaling: float

    def __init__(
        self,
        screenName: str | None = None,
        baseName: str | None = None,
        className: str = "Tk",
        useTk: bool = True,
        sync: bool = False,
        use: str | None = None,
    ) -> None:
        """Initialize a DPI-aware Tk window.

        All arguments are passed directly to tkinter.Tk.__init__.
        """
        super().__init__(
            screenName=screenName,
            baseName=baseName,
            className=className,
            useTk=useTk,
            sync=sync,
            use=use,
        )
        self._apply_dpi_awareness()

    def _apply_dpi_awareness(self) -> None:
        """Apply DPI awareness settings to this window."""
        self.dpi_x, self.dpi_y, self.dpi_scaling = get_dpi_info(self.winfo_id())

    def scale_value(self, value: float | str) -> int:
        """Scale a value according to the current DPI scaling factor.

        Args:
            value: The value to scale (can be int, float, or numeric string).

        Returns:
            The scaled value as an integer.

        Example:
            >>> root = Tk()  # On a 150% scaled display
            >>> root.scale_value(100)
            150
        """
        return int(float(value) * self.dpi_scaling)

    def scale_geometry(self, geometry: str) -> str:
        """Scale a geometry string according to the current DPI scaling factor.

        Args:
            geometry: A Tkinter geometry string in format "WxH+X+Y".

        Returns:
            The scaled geometry string.

        Example:
            >>> root = Tk()  # On a 150% scaled display
            >>> root.scale_geometry("800x600+100+50")
            "1200x900+150+75"
        """
        return scale_geometry(geometry, self.scale_value)


# Backwards compatibility alias
HdpiTk = Tk
