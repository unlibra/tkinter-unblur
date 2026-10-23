---
description: "Why Tkinter apps look blurry on Windows at 125%, 150% or 200% display scaling: DPI awareness, bitmap stretching, and what tkinter-unblur changes."
---

# Why Tkinter Looks Blurry on Windows

On a Windows laptop or monitor with display scaling set above 100%, a plain Tkinter window often looks soft: text has fuzzy edges and lines look smeared. This page explains where that comes from and what tkinter-unblur does about it.

## Display scaling and DPI

Windows describes display scaling as DPI (dots per inch). 100% scaling is 96 DPI, and the other settings are multiples of it:

| Scaling | DPI |
|---------|-----|
| 100% | 96 |
| 125% | 120 |
| 150% | 144 |
| 200% | 192 |

High-resolution laptop screens usually ship with 125% to 200% scaling, so that text stays readable.

## DPI-unaware apps are stretched

Windows has to know whether an app can draw itself at these higher DPIs. An app says so by declaring a *DPI awareness* mode. An app that declares nothing is treated as **DPI unaware**.

Windows draws a DPI-unaware app as if the screen were 96 DPI, then stretches that image up to the expected physical size. [Microsoft's documentation](https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows#dpi-unaware) describes the result: "This results in the application appearing blurry."

Tkinter does not declare DPI awareness by default, so a Tkinter window is stretched like this. The window has the right size, but every pixel of it is enlarged, which is the blur you see.

## What tkinter-unblur changes

When you create a window with `tkinter_unblur.Tk`, it does two things on Windows:

1. **Declares the process as system DPI aware.** It calls the Windows API [`SetProcessDpiAwareness`](https://learn.microsoft.com/en-us/windows/win32/api/shellscalingapi/nf-shellscalingapi-setprocessdpiawareness) with `PROCESS_SYSTEM_DPI_AWARE`. Windows then stops stretching the window, and Tkinter draws text and widgets at the screen's real resolution.
2. **Reads the DPI of the window's monitor.** It calls [`GetDpiForMonitor`](https://learn.microsoft.com/en-us/windows/win32/api/shellscalingapi/nf-shellscalingapi-getdpiformonitor) and stores the result as `dpi_x`, `dpi_y` and `dpi_scaling` (1.0 = 100%, 1.5 = 150%). If the query fails, it falls back to 96 DPI and a scaling of 1.0.

On Linux and macOS it does neither, and `Tk` behaves exactly like `tkinter.Tk`.

## Why the window can look smaller

Once Windows stops stretching the window, sizes given in pixels are real screen pixels. At 150% scaling, `root.geometry("800x600")` now covers fewer physical inches than before, so the window looks smaller, but sharp.

To keep the size the window had before, scale pixel values with the detected factor:

```python
from tkinter_unblur import Tk

root = Tk()
root.geometry(root.scale_geometry("800x600"))  # 1200x900 at 150%
```

See [`scale_geometry` and `scale_value`](./api#methods) in the API reference.

## Limitation: monitors with different scaling

System DPI awareness has one DPI for the whole session. Microsoft's documentation explains that such an app uses the DPI of the primary display at the time the user signed in. [When the app is moved to a display with a different scale factor](https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows#system-dpi-awareness), "Windows will bitmap scale the application's windows, making them appear blurry."

So with two monitors at different scaling, for example a 150% laptop and a 100% external monitor, a tkinter-unblur window is sharp on one of them and stretched on the other.

`dpi_x`, `dpi_y` and `dpi_scaling` are read once, when the window is created. They are not updated when the window moves to another monitor.
