import os
import sys
import time
import tkinter as tk  # Add this import for Canvas and Scrollbar

# Add src directory to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_path)

import customtkinter as ctk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from devopsnextgenx.components.StatusBar import StatusBar
from devopsnextgenx.components.Table import Table, Header, WidgetType
from devopsnextgenx.components.messageHub import Alert, Banner, Notification
from devopsnextgenx.components.Carousel import Carousel, image_list_provider
from devopsnextgenx.utils import get_icon_path

closeDark = get_icon_path("close", "dark")
print(f"Icon path for 'close' icon in dark theme: {closeDark}")
if os.path.exists(closeDark):
    print("Icon file exists!")
else:
    print("Icon file not found!")

def alert():
    alertx = Alert(state="info", title="Title", body_text="How do I get to top on AI?", btn1="Ok", btn2="Cancel")

def banner():
    bannerx = Banner(master=preview_frame, state="info", title="Title",
                          btn1="Action 1", btn2="Action 2", side="right_bottom")

def notification():
    Notification(master=preview_frame, state="info", message="message", side="right_bottom")

def carousel():
    carousel = Carousel(preview_frame, img_radius=25)
    carousel.grid(padx=20, pady=20)

WIDGETS = {
    "Alert": alert,
    "Banner": banner,
    "Notification": notification,
#    "Card": card,
    "Carousel": carousel,
#    "Input1": ctk_input_1,
#    "Input2": ctk_input_2,
#    "Loader": loader,
#    "PopupMenu": ctk_popup,
#    "ProgressPopup": progress_popup,
#    "Treeview": treeview
}


def toggle_widgets(widget):
    for widgets in preview_frame.winfo_children():
        widgets.destroy()

    var = WIDGETS[widget]
    var()

class Demo(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")

        self.title("Component Demo")
        self.geometry("600x400")

        # Add status bar at the bottom
        self.status_bar = StatusBar(self, progress_thickness=5)
        self.status_bar.pack(fill="x", side="bottom", padx=10, pady=5)
        self.status_bar.update_user("Amit")
        self.status_bar.update_access("Admin")

        # Create a canvas and a vertical scrollbar
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Configure scrollable frame to resize with canvas
        self.scrollable_frame.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Bind canvas resize to adjust scrollable frame width
        self.canvas.bind("<Configure>", 
            lambda e: self.canvas.itemconfig(
                "all",  # Update all canvas items (only the scrollable_frame window)
                width=e.width
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.winfo_width())
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        options = ["Alert", "Banner", "Notification", "Carousel"]
        option = ctk.CTkOptionMenu(self.scrollable_frame, values=options, width=200, command=toggle_widgets)
        option.pack(pady=20)
        option.set("None")

        # Add some demo buttons
        ttk.Button(
            self.scrollable_frame, 
            text="Start Process", 
            command=self.simulate_process,
            bootstyle="primary"
        ).pack(pady=10)

        ttk.Button(
            self.scrollable_frame, 
            text="Reset Status", 
            command=self.reset_status,
            bootstyle="secondary"
        ).pack(pady=10)

        # Add carousel to display images
        self.carouselFrame = ttk.Frame(self.scrollable_frame)
        self.carouselFrame.pack(fill="both", expand=True, pady=10)
        CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
        ICON_DIR = os.path.join(CURRENT_PATH, "imgs", "carousel")
        imgList = image_list_provider(ICON_DIR, imgOptions = {"imgPrefix":"sun", "suffix":"png", "start":1, "end":15})
        self.carousel = Carousel(self.carouselFrame, img_radius=5, img_list = imgList)
        self.carousel.grid(padx=20, pady=20)
        
        # Add table for user info
        self.add_user_info_table(self.scrollable_frame)

    def add_user_info_table(self, parent):
        """Add a table to display user info"""
        header1 = Header(text="ID", editable=False)
        header2 = Header(
            text="Name", 
            editable=True, 
            weight=1,
            on_change=lambda data, row, col: print(f"Changed cell ({row},{col}) to {data[row][col]}"),
            style="Bevel.TLabel"
        )
        header3 = Header(
            text="Age", 
            fg_color="#2a2d2e", 
            bg_color="#000000", 
            font_size=14, 
            weight=1, 
            align="right",
            action=self.sort_by_age,
            style="Bevel.TLabel"
        )
        header4 = Header(
            text="Email", 
            fg_color="#2a2d2e", 
            bg_color="#000000", 
            text_color="blue", 
            font_size=14, 
            weight=5, 
            align="center",
            action=self.sort_by_email,
            style="Bevel.TLabel"
        )
        header5 = Header(
            text="Active", 
            type=WidgetType.RNDTOGGLE,
            align="center",
            fg_color="#2a2d2e",
            bg_color="#000000",
            font_size=14,
            weight=1,
            on_change=lambda data, row, col: print(f"Changed cell ({row},{col}) to {data[row][col]}"),
            style="Bevel.TLabel"
        )
        header6 = Header(
            text="Notify", 
            type=WidgetType.SQTOGGLE,
            align="center",
            fg_color="#2a2d2e",
            bg_color="#000000",
            font_size=14,
            weight=1,
            on_change=lambda data, row, col: print(f"Changed cell ({row},{col}) to {data[row][col]}"),
            style="Bevel.TLabel"
        )
        header7 = Header(
            text="isPremium", 
            type=WidgetType.CHECKBOX,
            align="center",
            fg_color="#2a2d2e",
            bg_color="#000000",
            font_size=14,
            weight=1,
            on_change=lambda data, row, col: print(f"Changed cell ({row},{col}) to {data[row][col]}"),
            style="Bevel.TLabel"
        )
        header8 = Header(
            text="isBlocked", 
            type=WidgetType.RADIOBTN,
            align="center",
            fg_color="#2a2d2e",
            bg_color="#000000",
            font_size=14,
            weight=1,
            on_change=lambda data, row, col: print(f"Changed cell ({row},{col}) to {data[row][col]}"),
            style="Bevel.TLabel"
        )
        
        # Add new header for remove button
        remove_button_style = ttk.Style()
        remove_button_style.configure("Remove.TButton",
                        foreground="black",  # Text color
                        background="red",    # Not directly used in ttk
                        borderwidth=1,
                        focusthickness=3,
                        relief="flat")
        remove_button_style.map("Remove.TButton",
                background=[("active", "#cc0000"), ("pressed", "#990000")],
                foreground=[("active", "white"), ("pressed", "white")])
        header9 = Header(
            text="Actions",
            type=WidgetType.BUTTON,
            align="center",
            fg_color="#2a2d2e",
            bg_color="#000000",
            font_size=14,
            weight=1,
            button_text="Remove",
            on_click=self.remove_user,
            style="Remove.TButton",
        )

        headers = [header1, header2, header3, header4, header5, header6, header7, header8, header9]

        # Add sample data with placeholder for remove button
        users = [
            [1, "Alice", 30, "alice@example.com", True, True, True, False, "Remove"],
            [2, "Bob", 25, "bob@example.com", False, False, True, True, "Remove"],
            [3, "Charlie", 35, "charlie@example.com", True, True, False, False, "Remove"],
            [4, "David", 28, "david@example.com", True, False, True, True, "Remove"],
            [5, "Eve", 22, "eve@example.com", True, True, False, False, "Remove"],
        ]

        self.table = Table(parent, headers=headers, data=users)
        self.table.pack(fill="both", expand=True, pady=10)

        # Add style for bevel border
        style = ttk.Style()
        style.configure("Bevel.TLabel", relief="raised", borderwidth=2)

    def simulate_process(self):
        """Simulate a process with progress updates"""
        steps = 10
        for i in range(steps + 1):
            progress = i / steps
            self.status_bar.update_status(f"Processing... {i*10}%", progress)
            self.update()
            time.sleep(0.5)
        self.status_bar.update_status("Process completed!", 1.0)

    def reset_status(self):
        """Reset the status bar"""
        self.status_bar.reset()

    def sort_by_age(self, ascending=True):
        """Sort table data by age"""
        sorted_data = sorted(self.table.data, key=lambda x: x[2], reverse=not ascending)
        self.table.update_data(sorted_data)

    def sort_by_email(self, ascending=True):
        """Sort table data by email"""
        sorted_data = sorted(self.table.data, key=lambda x: x[3], reverse=not ascending)
        self.table.update_data(sorted_data)

    def remove_user(self, row):
        """Remove a user from the table"""
        if row < len(self.table.data):
            data = self.table.data.copy()
            data.pop(row)
            self.table.update_data(data)

if __name__ == "__main__":
    app = Demo()

    # Customize the preview_frame with border color and thickness
    preview_frame = ctk.CTkFrame(app.scrollable_frame, fg_color="transparent", border_color="black", border_width=2)
    preview_frame.pack(fill="both", expand=True)

    app.mainloop()