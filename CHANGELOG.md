# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - Unreleased

### Changed

- **Breaking:** `Tk` now sets DPI awareness before the Tk window is created, as
  Microsoft requires. Tk now reads the display's real DPI, so text and widgets
  sized by text render larger on scaled displays (1.25x at 125% scaling). They
  now match the Windows display setting. The API is unchanged, but layouts that
  were tuned to the old, smaller text may need adjusting.

### Fixed

- A failed `SetProcessDpiAwareness` call was logged as a success.

## [2.0.1] - 2025-12-15

### Added

- Support for Python 3.14.

### Fixed

- `__version__` reported `1.0.0` instead of the package version.

## [2.0.0] - 2025-12-03

### Changed

- **Breaking:** Renamed the package from `hdpitkinter` to `tkinter-unblur`.
  Import from `tkinter_unblur`.
- **Breaking:** The `HdpiTk()` function is replaced by the `Tk` class, a
  subclass of `tkinter.Tk`. `HdpiTk` remains as an alias of `Tk`.
- **Breaking:** Renamed attributes and methods: `DPI_X` to `dpi_x`, `DPI_Y` to
  `dpi_y`, `DPI_scaling` to `dpi_scaling`, `TkScale` to `scale_value` and
  `TkGeometryScale` to `scale_geometry`.
- Requires Python 3.9 or later.
- The `hdpitkinter` package is now a compatibility package that installs
  `tkinter-unblur` and warns that the package was renamed.

### Added

- Exception classes in `tkinter_unblur.exceptions`.
- Type hints (`py.typed`).

## 1.x and earlier

Published as `hdpitkinter`. No changelog was kept for these versions.

[3.0.0]: https://github.com/unlibra/tkinter-unblur/compare/v2.0.1...v3.0.0
[2.0.1]: https://github.com/unlibra/tkinter-unblur/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/unlibra/tkinter-unblur/compare/v1.0.3...v2.0.0
