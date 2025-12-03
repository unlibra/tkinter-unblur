"""Demo application for tkinter-unblur.

Run with: python -m tkinter_unblur
"""

from __future__ import annotations

import tkinter as tk

from tkinter_unblur import Tk, __version__


def main() -> None:
    """Run the demo application."""
    root = Tk()
    root.title(f"tkinter-unblur v{__version__} Demo")
    root.geometry("400x300")

    # Main frame
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)

    # Title
    title = tk.Label(
        frame,
        text="tkinter-unblur",
        font=("Segoe UI", 24, "bold"),
    )
    title.pack(pady=(0, 10))

    # Subtitle
    subtitle = tk.Label(
        frame,
        text="Fix blurry Tkinter on Windows high-DPI displays",
        font=("Segoe UI", 10),
        fg="gray",
    )
    subtitle.pack(pady=(0, 20))

    # DPI info
    dpi_text = f"DPI: {root.dpi_x} x {root.dpi_y}"
    scaling_text = f"Scaling: {root.dpi_scaling:.0%}"

    info_frame = tk.Frame(frame)
    info_frame.pack(pady=10)

    tk.Label(
        info_frame,
        text=dpi_text,
        font=("Consolas", 12),
    ).pack()

    tk.Label(
        info_frame,
        text=scaling_text,
        font=("Consolas", 12),
    ).pack()

    # Status
    if root.dpi_scaling > 1.0:
        status = "DPI awareness is active"
        status_color = "green"
    else:
        status = "No scaling detected (100%)"
        status_color = "gray"

    tk.Label(
        frame,
        text=status,
        font=("Segoe UI", 10),
        fg=status_color,
    ).pack(pady=20)

    # Close button
    tk.Button(
        frame,
        text="Close",
        command=root.destroy,
        width=10,
    ).pack()

    root.mainloop()


if __name__ == "__main__":
    main()
