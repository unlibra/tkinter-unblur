"""hdpitkinter - Compatibility meta-package for tkinter-unblur.

NOTICE: This package has been renamed to 'tkinter-unblur'.

Please update your dependencies:
    pip install tkinter-unblur

And update your imports:
    # Old
    from hdpitkinter import HdpiTk

    # New (recommended)
    from tkinter_unblur import Tk

This compatibility package will be maintained until January 2027.
For more information, see: https://github.com/unlibra/tkinter-unblur
"""

from __future__ import annotations

import warnings as _warnings

_warnings.warn(
    "hdpitkinter has been renamed to 'tkinter-unblur'.\n\n"
    "Please update your code:\n"
    "  pip uninstall hdpitkinter\n"
    "  pip install tkinter-unblur\n\n"
    "  # Old import\n"
    "  from hdpitkinter import HdpiTk\n\n"
    "  # New import (recommended)\n"
    "  from tkinter_unblur import Tk\n\n"
    "This compatibility package will be removed in January 2027.\n"
    "See: https://github.com/unlibra/tkinter-unblur#migrating-from-hdpitkinter",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export everything from the new package for backwards compatibility
from tkinter_unblur import (
    DPIDetectionError,
    HdpiTk,
    Tk,
    TkinterUnblurError,
    UnsupportedPlatformError,
    __version__,
    get_dpi_info,
    scale_geometry,
)

# Legacy version tracking
VERSION = __version__

__all__ = [
    "HdpiTk",
    "Tk",
    "get_dpi_info",
    "scale_geometry",
    "TkinterUnblurError",
    "UnsupportedPlatformError",
    "DPIDetectionError",
    "__version__",
    "VERSION",
]
