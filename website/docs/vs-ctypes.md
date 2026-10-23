---
description: "tkinter-unblur compared with the common ctypes fix for blurry Tkinter, SetProcessDpiAwareness(1): what each does, and when the one-liner is enough."
---

# Compared to the ctypes One-Liner

The usual answer to "Tkinter is blurry on Windows" is a single `ctypes` call before creating the window:

```python
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

import tkinter as tk
root = tk.Tk()
```

tkinter-unblur makes the same Windows API call, with the same value. This page shows what else it adds, so you can decide whether you need it.

## What is the same

Both declare the process as **system DPI aware** through [`SetProcessDpiAwareness`](https://learn.microsoft.com/en-us/windows/win32/api/shellscalingapi/nf-shellscalingapi-setprocessdpiawareness) with the value `1` (`PROCESS_SYSTEM_DPI_AWARE`). Windows stops stretching the window in both cases, and both share the [multi-monitor limitation](./why-blurry#limitation-monitors-with-different-scaling) of that mode.

An older variant, `ctypes.windll.user32.SetProcessDPIAware()`, also makes the process system DPI aware.

## What tkinter-unblur adds

| | ctypes one-liner | tkinter-unblur |
|---|---|---|
| Change in your code | Two lines before `Tk()` | One import |
| Linux and macOS | `ctypes.windll` does not exist there, so the call raises `AttributeError` unless you guard it | Skips the Windows calls and behaves like `tkinter.Tk` |
| `shcore.dll` fails to load | Raises `OSError` | Logs a warning and continues |
| Detected DPI | Not available; query it yourself | `dpi_x`, `dpi_y`, `dpi_scaling` |
| Keeping the old window size | Multiply every pixel value yourself | `scale_geometry()`, `scale_value()` |

A portable version of the one-liner needs a platform check and error handling:

```python
import sys

if sys.platform == "win32":
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except OSError:
        pass
```

With tkinter-unblur that becomes:

```python
from tkinter_unblur import Tk

root = Tk()
```

## When the one-liner is enough

The one-liner is a fine choice when all of these are true:

- Your app runs only on Windows.
- You do not need the detected DPI or scaling factor.
- You do not want an extra dependency.

tkinter-unblur is for when you want the fix to stay out of the way on every platform, or when you want to scale your layout with the detected factor.

## A third option: the application manifest

Microsoft [recommends](https://learn.microsoft.com/en-us/windows/win32/hidpi/setting-the-default-dpi-awareness-for-a-process) declaring DPI awareness in the application manifest of an `.exe` rather than with an API call. This applies when you ship your app as an executable and control its manifest. If a manifest already declares DPI awareness, Windows keeps that setting, and later `SetProcessDpiAwareness` calls, from either approach, have no effect.
