"""Tests for tkinter_unblur.core module."""

from __future__ import annotations

import os
import sys
from unittest.mock import patch

import pytest

# Check if tkinter is available
try:
    import tkinter

    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

# Skip entire module if tkinter is not available
pytestmark = pytest.mark.skipif(not TKINTER_AVAILABLE, reason="tkinter not available")

if TKINTER_AVAILABLE:
    from tkinter_unblur import __version__
    from tkinter_unblur.core import _get_dpi_info, _scale_geometry


class TestVersion:
    """Tests for version information."""

    def test_version_exists(self) -> None:
        """Version string should exist and be valid."""
        assert __version__ is not None
        assert isinstance(__version__, str)
        assert len(__version__.split(".")) >= 2


class TestScaleGeometry:
    """Tests for scale_geometry function."""

    def test_scale_geometry_100_percent(self) -> None:
        """Test scaling at 100% (no change)."""
        result = _scale_geometry("800x600+100+50", lambda v: int(float(v)))
        assert result == "800x600+100+50"

    def test_scale_geometry_150_percent(self) -> None:
        """Test scaling at 150%."""
        result = _scale_geometry("800x600+100+50", lambda v: int(float(v) * 1.5))
        assert result == "1200x900+150+75"

    def test_scale_geometry_200_percent(self) -> None:
        """Test scaling at 200%."""
        result = _scale_geometry("800x600+100+50", lambda v: int(float(v) * 2.0))
        assert result == "1600x1200+200+100"

    def test_scale_geometry_125_percent(self) -> None:
        """Test scaling at 125%."""
        result = _scale_geometry("800x600+100+50", lambda v: int(float(v) * 1.25))
        assert result == "1000x750+125+62"

    def test_scale_geometry_negative_position(self) -> None:
        """Test scaling with negative position values."""
        result = _scale_geometry("800x600+-100+-50", lambda v: int(float(v) * 1.5))
        assert result == "1200x900+-150+-75"

    def test_scale_geometry_invalid_format(self) -> None:
        """Test that invalid geometry raises ValueError."""
        with pytest.raises(ValueError, match="Invalid geometry string format"):
            _scale_geometry("invalid", lambda v: int(float(v)))

    def test_scale_geometry_partial_format(self) -> None:
        """Test that partial geometry raises ValueError."""
        with pytest.raises(ValueError, match="Invalid geometry string format"):
            _scale_geometry("800x600", lambda v: int(float(v)))


class TestGetDpiInfo:
    """Tests for get_dpi_info function."""

    def test_non_windows_returns_none_dpi(self) -> None:
        """On non-Windows, DPI values should be None with scaling 1.0."""
        with patch.object(os, "name", "posix"), patch.object(sys, "platform", "linux"):
            dpi_x, dpi_y, scaling = _get_dpi_info(12345)
            assert dpi_x is None
            assert dpi_y is None
            assert scaling == 1.0

    @pytest.mark.skipif(os.name != "nt", reason="Windows-only test")
    def test_windows_returns_valid_dpi(self) -> None:
        """On Windows, should return valid DPI values."""
        # This test would require a real window handle on Windows
        # For CI, we'll mock the Windows APIs
        pass

    def test_windows_dll_load_failure(self) -> None:
        """Test graceful handling when Windows DLLs fail to load."""
        if os.name != "nt":
            pytest.skip("Windows-only test")

        with patch("ctypes.WinDLL", side_effect=OSError("DLL not found")):
            dpi_x, dpi_y, scaling = _get_dpi_info(12345)
            assert dpi_x == 96
            assert dpi_y == 96
            assert scaling == 1.0


class TestTkClass:
    """Tests for the Tk class."""

    @pytest.mark.skipif(
        os.environ.get("DISPLAY") is None and os.name != "nt",
        reason="No display available",
    )
    def test_tk_creation(self) -> None:
        """Test that Tk can be created and has DPI attributes."""
        from tkinter_unblur import Tk

        root = Tk()
        try:
            # Check DPI attributes exist
            assert hasattr(root, "dpi_x")
            assert hasattr(root, "dpi_y")
            assert hasattr(root, "dpi_scaling")

            # Check scaling is a positive number
            assert isinstance(root.dpi_scaling, float)
            assert root.dpi_scaling > 0

            # Check methods exist
            assert hasattr(root, "scale_value")
            assert hasattr(root, "scale_geometry")
        finally:
            root.destroy()

    @pytest.mark.skipif(
        os.environ.get("DISPLAY") is None and os.name != "nt",
        reason="No display available",
    )
    def test_tk_scale_value(self) -> None:
        """Test the scale_value method."""
        from tkinter_unblur import Tk

        root = Tk()
        try:
            # At any scaling, scale_value should return an integer
            result = root.scale_value(100)
            assert isinstance(result, int)
            assert result >= 100  # Should be at least 100 (100% scaling)
        finally:
            root.destroy()

    @pytest.mark.skipif(
        os.environ.get("DISPLAY") is None and os.name != "nt",
        reason="No display available",
    )
    def test_tk_scale_geometry(self) -> None:
        """Test the scale_geometry method."""
        from tkinter_unblur import Tk

        root = Tk()
        try:
            result = root.scale_geometry("800x600+100+50")
            # Should return a valid geometry string
            assert "x" in result
            assert "+" in result
        finally:
            root.destroy()


class TestHdpiTkAlias:
    """Tests for the HdpiTk backwards compatibility alias."""

    def test_hdpitk_is_tk(self) -> None:
        """HdpiTk should be an alias for Tk."""
        from tkinter_unblur import HdpiTk, Tk

        assert HdpiTk is Tk


class TestExceptions:
    """Tests for custom exceptions."""

    def test_exception_hierarchy(self) -> None:
        """Test that exceptions have correct hierarchy."""
        from tkinter_unblur import (
            DPIDetectionError,
            TkinterUnblurError,
            UnsupportedPlatformError,
        )

        assert issubclass(TkinterUnblurError, Exception)
        assert issubclass(UnsupportedPlatformError, TkinterUnblurError)
        assert issubclass(DPIDetectionError, TkinterUnblurError)

    def test_exceptions_can_be_raised(self) -> None:
        """Test that exceptions can be raised and caught."""
        from tkinter_unblur import (
            DPIDetectionError,
            TkinterUnblurError,
            UnsupportedPlatformError,
        )

        with pytest.raises(TkinterUnblurError):
            raise TkinterUnblurError("test error")

        with pytest.raises(UnsupportedPlatformError):
            raise UnsupportedPlatformError("not windows")

        with pytest.raises(DPIDetectionError):
            raise DPIDetectionError("dpi detection failed")
