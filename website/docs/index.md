---
sidebar_position: 1
---

# Introduction

**Fix blurry Tkinter applications on Windows 10/11 high-DPI displays.**

tkinter-unblur provides a drop-in replacement for `tkinter.Tk` that automatically applies DPI awareness on Windows 10/11, fixing the common "blurry text" problem.

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

That's all you need! For advanced usage, see the [API Reference](./api).

## Compatibility

| Platform | Status |
|----------|--------|
| Windows 10/11 | Full DPI awareness support |
| Linux | Passthrough (OS handles DPI) |
| macOS | Passthrough (OS handles DPI) |

| Python Version | Status |
|----------------|--------|
| 3.9 - 3.14 | Supported |
| 3.8 | Not supported (EOL) |

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