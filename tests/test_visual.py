"""Visual test script to verify DPI awareness works correctly.

Run this on a Windows machine with high-DPI display to verify text is sharp.
"""

import tkinter
from tkinter import ttk

from tkinter_unblur import Tk


def main() -> None:
    """Create test windows to compare standard Tk vs DPI-aware Tk."""

    # Standard tkinter.Tk (will be blurry on high-DPI)
    standard_root = tkinter.Tk()
    standard_root.title("Standard Tk (Blurry)")
    standard_root.geometry("400x300+100+100")

    frame1 = ttk.Frame(standard_root, padding=20)
    frame1.pack(fill="both", expand=True)

    ttk.Label(
        frame1,
        text="Standard tkinter.Tk",
        font=("Segoe UI", 16, "bold"),
    ).pack(pady=10)

    ttk.Label(
        frame1,
        text="This window uses standard Tk.\nText should appear BLURRY on high-DPI displays.",
        font=("Segoe UI", 10),
        justify="center",
    ).pack(pady=10)

    ttk.Button(frame1, text="Test Button").pack(pady=5)

    # DPI-aware Tk (should be sharp)
    dpi_root = Tk()
    dpi_root.title("tkinter-unblur Tk (Sharp)")
    dpi_root.geometry("400x300+550+100")

    frame2 = ttk.Frame(dpi_root, padding=20)
    frame2.pack(fill="both", expand=True)

    ttk.Label(
        frame2,
        text="tkinter-unblur Tk",
        font=("Segoe UI", 16, "bold"),
    ).pack(pady=10)

    ttk.Label(
        frame2,
        text="This window uses DPI-aware Tk.\nText should appear SHARP and CLEAR.",
        font=("Segoe UI", 10),
        justify="center",
    ).pack(pady=10)

    # Display DPI info
    info_text = (
        f"DPI: {dpi_root.dpi_x} x {dpi_root.dpi_y}\n"
        f"Scaling: {dpi_root.dpi_scaling:.0%}"
    )
    ttk.Label(
        frame2,
        text=info_text,
        font=("Consolas", 9),
        justify="center",
    ).pack(pady=10)

    ttk.Button(frame2, text="Test Button").pack(pady=5)

    # Instructions
    instructions = """
VISUAL TEST INSTRUCTIONS:

1. Compare the text sharpness between the two windows
2. On high-DPI displays (125%, 150%, 200% scaling):
   - LEFT window (Standard Tk): Text should appear BLURRY
   - RIGHT window (tkinter-unblur): Text should be SHARP and CLEAR

3. On 100% scaling displays:
   - Both windows should look identical (sharp)

Press Ctrl+C in terminal or close windows to exit.
"""
    print(instructions)

    standard_root.mainloop()


if __name__ == "__main__":
    main()
