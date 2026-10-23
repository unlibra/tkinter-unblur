---
description: "API reference for tkinter-unblur: the Tk class, a drop-in replacement for tkinter.Tk with DPI awareness, plus its attributes, scaling methods and exceptions."
---

# API Reference

## `Tk` Class

The `Tk` class is a drop-in replacement for `tkinter.Tk` with DPI awareness capabilities.

```python
from tkinter_unblur import Tk
```

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `dpi_x` | `int` \| `None` | Horizontal DPI (96 = 100% scaling). `None` on non-Windows platforms. |
| `dpi_y` | `int` \| `None` | Vertical DPI (96 = 100% scaling). `None` on non-Windows platforms. |
| `dpi_scaling` | `float` | Scaling factor (1.0 = 100%, 1.5 = 150%, etc.). |

**Example:**

```python
root = Tk()
print(f"DPI: {root.dpi_x}x{root.dpi_y}")
print(f"Scaling: {root.dpi_scaling:.0%}")
# Output: Scaling: 150%
```

### Methods

#### `scale_value`

Scale a numeric value according to the current DPI scaling factor.

```python
def scale_value(self, value: float | str) -> int
```

**Arguments:**
- `value`: The value to scale (can be int, float, or numeric string).

**Returns:**
- The scaled value as an integer.

**Example:**

```python
from tkinter import Label

root = Tk()
# Tk does not scale pixel values, such as padding, so scale them yourself
label = Label(root, text="Hello", font=("Arial", 12))
label.pack(padx=root.scale_value(10), pady=root.scale_value(10))
```

Font sizes in points, such as `("Arial", 12)`, need no scaling: Tk already sizes them for the display's DPI. Scaling them again with `scale_value()` makes the text too large.

#### `scale_geometry`

Scale a geometry string according to the current DPI scaling factor.

```python
def scale_geometry(self, geometry: str) -> str
```

**Arguments:**
- `geometry`: A Tkinter geometry string in format `"WxH+X+Y"`.

**Returns:**
- The scaled geometry string.

**Example:**

```python
root = Tk()
# Scale window geometry (width x height + x + y)
root.geometry(root.scale_geometry("800x600+100+50"))
```

## Exceptions

The library defines the following exceptions in `tkinter_unblur.exceptions`.

`UnsupportedPlatformError` and `DPIDetectionError` are reserved for future use. The library does not currently raise them; it falls back to default values instead (see below).

### `TkinterUnblurError`
Base exception for this library's custom exceptions.

### `UnsupportedPlatformError`
Reserved. Not currently raised.

On non-Windows platforms, `Tk` skips DPI detection and sets `dpi_x = None`, `dpi_y = None` and `dpi_scaling = 1.0`.

### `DPIDetectionError`
Reserved. Not currently raised.

On Windows, if DPI detection fails, the library logs a warning through the `logging` module (logger `tkinter_unblur._windows`) and sets `dpi_x = 96`, `dpi_y = 96` and `dpi_scaling = 1.0` (100% scaling). This happens when:

- `shcore.dll` or `user32.dll` cannot be loaded
- The monitor for the window cannot be determined
- `GetDpiForMonitor` returns an error code or fails
