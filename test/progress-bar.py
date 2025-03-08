import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def create_progress_bar(master, thickness=20):
    """Creates a progressbar with a custom thickness."""

    style = ttk.Style()
    style.configure("Custom.Horizontal.TProgressbar", thickness=thickness)

    progress_bar = ttk.Progressbar(
        master,
        mode="determinate",
        bootstyle="primary",
        style="Custom.Horizontal.TProgressbar",
        length=200,  # Example length
    )
    return progress_bar

def main():
    root = ttk.Window(themename="flatly")  # Choose a theme
    root.title("Custom Progressbar Thickness")

    # Example: Progressbar with thickness 20
    progress_bar1 = create_progress_bar(root, thickness=20)
    progress_bar1.pack(pady=20)

    # Example: Progressbar with thickness 5
    progress_bar2 = create_progress_bar(root, thickness=5)
    progress_bar2.pack(pady=20)

    # Example: Progressbar with thickness 40
    progress_bar3 = create_progress_bar(root, thickness=40)
    progress_bar3.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()