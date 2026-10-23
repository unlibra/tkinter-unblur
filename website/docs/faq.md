---
description: "Answers to common tkinter-unblur questions: smaller windows after the fix, checking that it works, multiple monitors, Toplevel windows, Linux and macOS."
---

# FAQ

## How do I check that it works?

Run the built-in demo:

```bash
python -m tkinter_unblur
```

It opens a window that shows the detected DPI and scaling factor. On a display scaled above 100%, it reports "DPI awareness is active".

You can also print the values from your own app:

```python
from tkinter_unblur import Tk

root = Tk()
print(root.dpi_x, root.dpi_y, f"{root.dpi_scaling:.0%}")
```

## My window got smaller. Is that a bug?

No. Without tkinter-unblur, Windows stretches the whole window to the expected size, which is why it looked blurry. With it, Windows stops stretching, so pixel sizes are real screen pixels and the window looks smaller at scaling above 100%.

Use `scale_geometry()` to keep the original size:

```python
root.geometry(root.scale_geometry("800x600"))
```

For other pixel values, such as padding or a canvas size, use `scale_value()`. See [Why Tkinter Looks Blurry on Windows](./why-blurry#why-the-window-can-look-smaller).

## The window is sharp on one monitor and blurry on another

This is a limitation of the DPI awareness mode that tkinter-unblur uses. Windows renders the app at one DPI for the whole session and stretches it on monitors with a different scaling. See [Limitation: monitors with different scaling](./why-blurry#limitation-monitors-with-different-scaling).

## `dpi_scaling` is 1.0 on my high-DPI display

Turn on debug logging to see what happened during detection:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from tkinter_unblur import Tk
root = Tk()
```

If a Windows call fails, tkinter-unblur logs a warning, such as "Failed to load Windows DLLs for DPI detection", and falls back to 96 DPI and a scaling of 1.0.

## Do I need to change `Toplevel` windows or dialogs?

No. DPI awareness is a setting of the whole process, and `SetProcessDpiAwareness` sets the process default. Windows created after the root window, such as `Toplevel` windows and dialogs, use it too. Create the root window with `tkinter_unblur.Tk` before them.

## What happens on Linux and macOS?

Nothing changes. `Tk` behaves exactly like `tkinter.Tk`, `dpi_x` and `dpi_y` are `None`, and `dpi_scaling` is `1.0`. You can keep the same import on every platform.

## Something else already set DPI awareness

DPI awareness can be set only once per process, for example by an application manifest or an earlier `SetProcessDpiAwareness` call. In that case Windows keeps the existing setting, and the call from tkinter-unblur has no effect. tkinter-unblur still creates the window and asks Windows for the DPI as usual.

## Which Windows and Python versions are supported?

Windows 10 and 11, and Python 3.9 to 3.14. The Windows API it uses, `SetProcessDpiAwareness`, needs Windows 8.1 or later.

## I used `hdpitkinter`

`hdpitkinter` was renamed to `tkinter-unblur`. See [Migrating from hdpitkinter](./#migrating-from-hdpitkinter).
