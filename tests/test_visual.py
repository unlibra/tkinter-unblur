"""Visual test script to verify DPI awareness works correctly.

Run this on a Windows machine with high-DPI display to verify text is sharp.

This test shows THREE windows:
1. Standard tkinter.Tk (DPI-unaware) - LARGE and BLURRY
2. tkinter-unblur with scaling - LARGE and SHARP (recommended approach)
3. tkinter-unblur without scaling - SMALL and SHARP (shows what happens without scale_geometry)
"""

import subprocess
import sys
from pathlib import Path


def main() -> None:
    """Create three test windows in separate processes."""
    print("=" * 70)
    print("TKINTER DPI AWARENESS VISUAL TEST")
    print("=" * 70)
    print()
    print("Launching THREE windows for comparison:")
    print("1. LEFT:   Standard Tk (DPI-unaware) - Large but blurry")
    print("2. MIDDLE: Unblur Tk with scaling - Large and sharp ✓")
    print("3. RIGHT:  Unblur Tk no scaling - Small but sharp")
    print()

    test_dir = Path(__file__).parent

    # Temporary script files
    standard_script = test_dir / "_temp_standard.py"
    scaled_script = test_dir / "_temp_scaled.py"
    unscaled_script = test_dir / "_temp_unscaled.py"

    # Window 1: Standard Tk (DPI-unaware)
    standard_code = """
import tkinter
from tkinter import ttk

root = tkinter.Tk()
root.title("1. Standard Tk (Blurry)")
root.geometry("450x400+50+100")

frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Standard tkinter.Tk", font=("Segoe UI", 28, "bold")).pack(pady=8)
ttk.Label(frame, text="BLURRY", font=("Segoe UI", 16), foreground="red").pack(pady=8)
ttk.Label(frame, text="Windows scaled this window", font=("Segoe UI", 12)).pack(pady=5)
ttk.Label(frame, text="abcdefghijklmnopqrstuvwxyz\\nABCDEFGHIJKLMNOPQRSTUVWXYZ\\n0123456789",
          font=("Segoe UI", 14), justify="center").pack(pady=8)
ttk.Button(frame, text="Test Button", width=18).pack(pady=5)

root.mainloop()
"""

    # Window 2: DPI-aware Tk WITH scaling (recommended)
    scaled_code = """
from tkinter import ttk
from tkinter_unblur import Tk

root = Tk()
root.title("2. Unblur Tk + Scaling (Sharp) ✓")
root.geometry(root.scale_geometry("450x400+550+100"))

frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

# Scale font sizes to match physical size of standard Tk
ttk.Label(frame, text="tkinter-unblur Tk", font=("Segoe UI", root.scale_value(28), "bold")).pack(pady=8)
ttk.Label(frame, text="SHARP", font=("Segoe UI", root.scale_value(16)), foreground="green").pack(pady=8)
ttk.Label(frame, text="Using scale_geometry()", font=("Segoe UI", root.scale_value(12))).pack(pady=5)
ttk.Label(frame, text="abcdefghijklmnopqrstuvwxyz\\nABCDEFGHIJKLMNOPQRSTUVWXYZ\\n0123456789",
          font=("Segoe UI", root.scale_value(14)), justify="center").pack(pady=8)

info = f"DPI: {root.dpi_x}x{root.dpi_y}  ({root.dpi_scaling:.0%})"
ttk.Label(frame, text=info, font=("Consolas", root.scale_value(10))).pack(pady=2)

button = ttk.Button(frame, text="Test Button", width=18)
button.configure(style="Scaled.TButton")
# Create a custom style with scaled font
style = ttk.Style()
style.configure("Scaled.TButton", font=("Segoe UI", root.scale_value(9)))
button.pack(pady=5)

root.mainloop()
"""

    # Window 3: DPI-aware Tk WITHOUT scaling
    unscaled_code = """
from tkinter import ttk
from tkinter_unblur import Tk

root = Tk()
root.title("3. Unblur Tk No Scaling (Sharp)")
root.geometry("450x400+1050+100")

frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="tkinter-unblur Tk", font=("Segoe UI", 28, "bold")).pack(pady=8)
ttk.Label(frame, text="SHARP", font=("Segoe UI", 16), foreground="blue").pack(pady=8)
ttk.Label(frame, text="No scale_geometry()", font=("Segoe UI", 12)).pack(pady=5)
ttk.Label(frame, text="abcdefghijklmnopqrstuvwxyz\\nABCDEFGHIJKLMNOPQRSTUVWXYZ\\n0123456789",
          font=("Segoe UI", 14), justify="center").pack(pady=8)

info = f"DPI: {root.dpi_x}x{root.dpi_y}  ({root.dpi_scaling:.0%})"
ttk.Label(frame, text=info, font=("Consolas", 10)).pack(pady=2)
ttk.Button(frame, text="Test Button", width=18).pack(pady=5)

root.mainloop()
"""

    # Write temporary scripts
    standard_script.write_text(standard_code, encoding="utf-8")
    scaled_script.write_text(scaled_code, encoding="utf-8")
    unscaled_script.write_text(unscaled_code, encoding="utf-8")

    try:
        # Launch all three processes
        proc1 = subprocess.Popen([sys.executable, str(standard_script)])
        proc2 = subprocess.Popen([sys.executable, str(scaled_script)])
        proc3 = subprocess.Popen([sys.executable, str(unscaled_script)])

        print("✓ All windows launched")
        print()
        print("COMPARISON:")
        print("-" * 70)
        print("Window 1 (LEFT):   Large, blurry text (avoid this!)")
        print("Window 2 (MIDDLE): Large, sharp text (recommended! ✓)")
        print("Window 3 (RIGHT):  Small, sharp text (need to scale manually)")
        print()
        print("RECOMMENDATION:")
        print("Use tkinter_unblur.Tk with scale_geometry() like Window 2")
        print()
        print("Example code:")
        print("  from tkinter_unblur import Tk")
        print("  root = Tk()")
        print('  root.geometry(root.scale_geometry("800x600+100+100"))')
        print()
        print("Close all windows to exit...")
        print("=" * 70)

        # Wait for all processes
        proc1.wait()
        proc2.wait()
        proc3.wait()

    finally:
        # Clean up
        standard_script.unlink(missing_ok=True)
        scaled_script.unlink(missing_ok=True)
        unscaled_script.unlink(missing_ok=True)
        print("\nTest complete.")


if __name__ == "__main__":
    main()
