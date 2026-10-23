"""Manual check of when DPI awareness is set, for Windows only.

Prints the DPI awareness of the process and of the Tk windows, plus the
values Tk uses to size text, then opens a window to inspect by eye.

Set display scaling above 100% (for example 150%) and run each mode:

    uv run python tests/manual/check_dpi_awareness.py plain
    uv run python tests/manual/check_dpi_awareness.py oneliner
    uv run python tests/manual/check_dpi_awareness.py unblur

plain     tkinter.Tk() with no DPI awareness (blurry baseline)
oneliner  SetProcessDpiAwareness(1), then tkinter.Tk() (reference order)
unblur    tkinter_unblur.Tk()

The "unblur" output should match the "oneliner" output.
"""

from __future__ import annotations

import argparse
import ctypes
import logging
import sys
import tkinter
from tkinter import font as tkfont

SAMPLE_TEXT = "The quick brown fox 0123456789"

# PROCESS_DPI_AWARENESS / DPI_AWARENESS values
AWARENESS_NAMES = {
    -1: "invalid",
    0: "unaware",
    1: "system aware",
    2: "per-monitor aware",
}


def process_awareness() -> str:
    value = ctypes.c_int(-1)
    ctypes.windll.shcore.GetProcessDpiAwareness(None, ctypes.byref(value))
    return AWARENESS_NAMES.get(value.value, str(value.value))


def window_awareness(hwnd: int) -> str:
    # Requires Windows 10 version 1607 or later
    user32 = ctypes.windll.user32
    user32.GetWindowDpiAwarenessContext.restype = ctypes.c_void_p
    user32.GetWindowDpiAwarenessContext.argtypes = [ctypes.c_void_p]
    user32.GetAwarenessFromDpiAwarenessContext.restype = ctypes.c_int
    user32.GetAwarenessFromDpiAwarenessContext.argtypes = [ctypes.c_void_p]
    context = user32.GetWindowDpiAwarenessContext(hwnd)
    value = user32.GetAwarenessFromDpiAwarenessContext(context)
    return AWARENESS_NAMES.get(value, str(value))


def create_root(mode: str) -> tkinter.Tk:
    if mode == "plain":
        return tkinter.Tk()
    if mode == "oneliner":
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        return tkinter.Tk()
    from tkinter_unblur import Tk

    return Tk()


def main() -> None:
    if sys.platform != "win32":
        sys.exit("This check runs only on Windows.")

    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["plain", "oneliner", "unblur"])
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG, format="%(name)s: %(message)s")

    root = create_root(args.mode)
    root.title(f"DPI check: {args.mode}")
    tkinter.Label(root, text=SAMPLE_TEXT).pack(padx=10, pady=10)
    root.update()

    default_font = tkfont.nametofont("TkDefaultFont")
    results = {
        "mode": args.mode,
        "process awareness": process_awareness(),
        "root window awareness": window_awareness(int(root.wm_frame(), 16)),
        "client window awareness": window_awareness(root.winfo_id()),
        "tk scaling": root.tk.call("tk", "scaling"),
        "pixels per inch (Tk)": root.winfo_fpixels("1i"),
        "TkDefaultFont size": default_font.actual("size"),
        "TkDefaultFont linespace": default_font.metrics("linespace"),
        "sample text width": default_font.measure(SAMPLE_TEXT),
        "window size": f"{root.winfo_width()}x{root.winfo_height()}",
        "dpi_x, dpi_y, dpi_scaling": (
            getattr(root, "dpi_x", "-"),
            getattr(root, "dpi_y", "-"),
            getattr(root, "dpi_scaling", "-"),
        ),
    }
    for key, value in results.items():
        print(f"{key:28} {value}")  # noqa: T201

    root.mainloop()


if __name__ == "__main__":
    main()
