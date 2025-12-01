# hdpitkinter

> **This package has been renamed to [`tkinter-unblur`](https://pypi.org/project/tkinter-unblur/)**

## Migration

### Step 1: Update your dependencies

```bash
pip uninstall hdpitkinter
pip install tkinter-unblur
```

### Step 2: Update your imports

```python
# Old (deprecated)
from hdpitkinter import HdpiTk

# New (recommended)
from tkinter_unblur import Tk
```

### Step 3: Update your code (minimal changes)

```python
# Old
root = HdpiTk()

# New
root = Tk()
```

That's it! The new `Tk` class is a drop-in replacement for `HdpiTk`.

## Why the rename?

- **Better name**: Follows Python naming conventions (`framework-feature`)
- **Better discoverability**: Matches user search terms ("blurry", "unblur")
- **Active development**: Modern codebase with type hints and comprehensive tests

## Compatibility Timeline

| Period | Status |
|--------|--------|
| Now - Dec 2025 | Full support (this meta-package works) |
| Jan 2026 - Dec 2026 | Security fixes only |
| Jan 2027+ | No longer maintained |

## New Features in tkinter-unblur

The new package includes:

- Type hints for better IDE support
- Comprehensive documentation
- Better error handling
- Modern Python packaging (pyproject.toml)
- CI/CD with automated testing

## Links

- **New package**: [tkinter-unblur on PyPI](https://pypi.org/project/tkinter-unblur/)
- **Repository**: [GitHub](https://github.com/unlibra/tkinter-unblur)
- **Migration guide**: [Full documentation](https://github.com/unlibra/tkinter-unblur#migrating-from-hdpitkinter)
