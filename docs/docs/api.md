---
sidebar_position: 2
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
# Scale font size to maintain physical size across different DPI settings
label = Label(root, text="Hello", font=("Arial", root.scale_value(12)))
```

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

The library defines the following exceptions in `tkinter_unblur.exceptions`:

### `TkinterUnblurError`
Base exception for all errors raised by this library.

### `UnsupportedPlatformError`
Raised when attempting to use Windows-specific features on a non-Windows platform (though the main `Tk` class handles this gracefully by disabling DPI features).

### `DPIDetectionError`
Raised when DPI detection fails on Windows.
