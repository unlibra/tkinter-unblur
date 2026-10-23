# tkinter-unblur

[![PyPI version](https://img.shields.io/pypi/v/tkinter-unblur)](https://pypi.org/project/tkinter-unblur/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/tkinter-unblur)](https://pepy.tech/project/tkinter-unblur)
[![Python versions](https://img.shields.io/pypi/pyversions/tkinter-unblur.svg)](https://pypi.org/project/tkinter-unblur/)
[![Type checked](https://img.shields.io/badge/type%20checked-mypy-blue)](https://mypy-lang.org/)
[![CI](https://github.com/unlibra/tkinter-unblur/actions/workflows/ci.yml/badge.svg)](https://github.com/unlibra/tkinter-unblur/actions)
[![License](https://img.shields.io/github/license/unlibra/tkinter-unblur.svg)](https://github.com/unlibra/tkinter-unblur/blob/main/LICENSE)
[![Docs](https://img.shields.io/badge/docs-online-blue)](https://docs.unlibra.com/tkinter-unblur/)

> **Note:** `hdpitkinter` has been reborn as `tkinter-unblur` with modern features. See [migration guide](#migrating-from-hdpitkinter).

**Fix blurry Tkinter applications on Windows 10/11 high-DPI displays.**

**[Documentation](https://docs.unlibra.com/tkinter-unblur/)** · **[PyPI](https://pypi.org/project/tkinter-unblur/)**

## The Problem

Tkinter applications look blurry and pixelated on modern high-resolution displays with scaling enabled (125%, 150%, 200%, etc.). This is because Tkinter is not DPI-aware by default on Windows.

## The Solution

```python
# Before (blurry)
from tkinter import Tk

# After (crystal clear)
from tkinter_unblur import Tk
```

That's it. One import change, and your Tkinter app renders sharply.

### Visual Comparison

![Blurry vs Sharp Comparison](images/comparison.png)

**Left:** Standard Tkinter (blurry) | **Right:** tkinter-unblur (sharp)

## Installation

```bash
pip install tkinter-unblur
```

## Usage

```python
from tkinter_unblur import Tk

root = Tk()
root.title("My App")
root.geometry("800x600")
root.mainloop()
```

That's all you need! For advanced usage, see [API Reference](#api-reference).

## API Reference

### `Tk` Class

A drop-in replacement for `tkinter.Tk` with DPI awareness.

#### Attributes

- `dpi_x: int | None` - Horizontal DPI (96 = 100% scaling)
- `dpi_y: int | None` - Vertical DPI (96 = 100% scaling)
- `dpi_scaling: float` - Scaling factor (1.0 = 100%, 1.5 = 150%)

**Example:**

```python
root = Tk()
print(f"DPI: {root.dpi_x}x{root.dpi_y}")
print(f"Scaling: {root.dpi_scaling:.0%}")  # e.g., "Scaling: 150%"
```

#### Methods

##### `scale_value(value: float | str) -> int`

Scale a numeric value by the DPI factor.

**Example:**

```python
from tkinter import Label

root = Tk()
# Tk does not scale pixel values, such as padding, so scale them yourself
label = Label(root, text="Hello", font=("Arial", 12))
label.pack(padx=root.scale_value(10), pady=root.scale_value(10))
```

Font sizes in points, such as `("Arial", 12)`, need no scaling: Tk already sizes them for the display's DPI. Scaling them again with `scale_value()` makes the text too large.

##### `scale_geometry(geometry: str) -> str`

Scale a geometry string by the DPI factor. It accepts every form `root.geometry()` accepts:

- `"WxH"`, such as `"800x600"`
- `"WxH+X+Y"`, such as `"800x600+100+50"`. Each sign can be `+` or `-`, as in `"800x600-100-50"`.
- `"+X+Y"`, a position only. Each sign can be `+` or `-` here too.
- Any of these with a leading `"="`

The result has the same form as the input, with the signs kept. Any other string raises `ValueError`.

**Example:**

```python
root = Tk()
root.geometry(root.scale_geometry("800x600"))          # "1200x900" at 150%
root.geometry(root.scale_geometry("800x600+100+50"))   # "1200x900+150+75" at 150%
```

### Exceptions

- `TkinterUnblurError` - Base exception
- `UnsupportedPlatformError` - Reserved, not currently raised (non-Windows: `dpi_scaling` is `1.0`)
- `DPIDetectionError` - Reserved, not currently raised (on failure: warning logged, `dpi_scaling` is `1.0`)

## How It Works

On Windows, this library:

1. Calls `SetProcessDpiAwareness(1)` to enable system DPI awareness, before the Tk window is created
2. Queries the monitor's DPI using `GetDpiForMonitor`
3. Provides scaling utilities for your application

On non-Windows platforms, the library is a simple passthrough to `tkinter.Tk`.

The implementation is based on [this Stack Overflow answer](https://stackoverflow.com/questions/41315873/attempting-to-resolve-blurred-tkinter-text-scaling-on-windows-10-high-dpi-disp).

## Compatibility

| Platform | Status |
|----------|--------|
| Windows 10/11 | System DPI awareness (one DPI for all monitors, see [limitation](https://docs.unlibra.com/tkinter-unblur/why-blurry#limitation-monitors-with-different-scaling)) |
| Linux | Passthrough (OS handles DPI) |
| macOS | Passthrough (OS handles DPI) |

| Python Version | Status |
|----------------|--------|
| 3.10 - 3.15 | Supported |
| 3.9 and earlier | Not supported |

## Migrating from hdpitkinter

This package was formerly known as `hdpitkinter`. To migrate:

```bash
pip uninstall hdpitkinter
pip install tkinter-unblur
```

```python
# Old
from hdpitkinter import HdpiTk
root = HdpiTk()

# New
from tkinter_unblur import Tk
root = Tk()
```

The `HdpiTk` name is still available as an alias for backwards compatibility:

```python
from tkinter_unblur import HdpiTk  # Works, but Tk is preferred
```

## License

MIT License - see [LICENSE](LICENSE) for details.
