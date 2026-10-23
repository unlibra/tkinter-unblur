"""Check the installed tkinter-unblur wheel as users receive it.

Run with the interpreter of a fresh virtual environment that has only the
built wheel installed, from the repository root:

    python scripts/check_wheel.py

It does not import tkinter, so it runs without Tk.
"""

from __future__ import annotations

import ast
import sys
from importlib import metadata, util
from pathlib import Path

import tomllib

EXPECTED_FILES = [
    "__init__.py",
    "__main__.py",
    "_windows.py",
    "core.py",
    "exceptions.py",
    "py.typed",
]


def main() -> int:
    errors = []

    project_version = tomllib.loads(Path("pyproject.toml").read_text())["project"][
        "version"
    ]
    installed_version = metadata.version("tkinter-unblur")
    if installed_version != project_version:
        errors.append(
            f"installed version {installed_version} != pyproject {project_version}"
        )

    spec = util.find_spec("tkinter_unblur")
    if spec is None or spec.origin is None:
        errors.append("tkinter_unblur is not installed")
    else:
        package_dir = Path(spec.origin).parent
        if "site-packages" not in package_dir.parts:
            errors.append(f"tkinter_unblur comes from {package_dir}, not the wheel")
        missing = [f for f in EXPECTED_FILES if not (package_dir / f).exists()]
        if missing:
            errors.append(f"missing from the wheel: {', '.join(missing)}")

        tree = ast.parse((package_dir / "__init__.py").read_text())
        versions = [
            node.value.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Assign)
            and any(getattr(t, "id", None) == "__version__" for t in node.targets)
            and isinstance(node.value, ast.Constant)
        ]
        if versions != [project_version]:
            errors.append(f"__version__ is {versions}, expected {project_version}")

    for error in errors:
        print(f"FAIL {error}")
    if not errors:
        print(f"ok   tkinter-unblur {installed_version} wheel")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
