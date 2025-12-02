# hdpitkinter

⚠️ **This package has been renamed to [`tkinter-unblur`](https://pypi.org/project/tkinter-unblur/)**

## Quick Migration

```bash
pip uninstall hdpitkinter
pip install tkinter-unblur
```

**Update imports:**

```python
# Old
from hdpitkinter import HdpiTk

# New (recommended)
from tkinter_unblur import Tk
```

**Note:** The `hdpitkinter` package remains available as a compatibility wrapper. Both `Tk` and `HdpiTk` can be imported from `hdpitkinter`:

```python
from hdpitkinter import Tk      # Works (new class)
from hdpitkinter import HdpiTk  # Works (backwards compatible)
```

However, migrating to `tkinter-unblur` is strongly recommended.

## Why Migrate?

This project was unmaintained from 2020-2025. The new version includes:

- **Python 3.9-3.13 support** (modern Python versions)
- **Modern packaging** (pyproject.toml, PEP 621)
- **Type hints** for better IDE support
- **Comprehensive tests** and CI/CD
- **Simplified API** (drop-in replacement for `tkinter.Tk`)
- **Better documentation** and examples

The `hdpitkinter` package remains available as a compatibility wrapper.

## More Info

- Repository: <https://github.com/unlibra/tkinter-unblur>
- PyPI: <https://pypi.org/project/tkinter-unblur>
