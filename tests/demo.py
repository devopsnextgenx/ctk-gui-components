import os
import sys

# Add src directory to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_path)

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from devopsnextgenx.components.StatusBar import StatusBar
from devopsnextgenx.components.Table import Table, Header, WidgetType
import time
class Demo(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")

        self.title("Component Demo")
        self.geometry("600x400")

        # Create main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Add some demo buttons
        ttk.Button(
            main_frame, 
            text="Start Process", 
            command=self.simulate_process,
            bootstyle="primary"
        ).pack(pady=10)

        ttk.Button(
            main_frame, 
            text="Reset Status", 
            command=self.reset_status,
            bootstyle="secondary"
        ).pack(pady=10)

        # Add table for user info
        self.add_user_info_table(main_frame)

        # Add status bar at the bottom
        self.status_bar = StatusBar(self, progress_thickness=5)
        self.status_bar.pack(fill="x", side="bottom", padx=10, pady=5)

    def add_user_info_table(self, parent):
        """Add a table to display user info"""
        header1 = Header(text="ID", editable=False)
        header2 = Header(
            text="Name", 
            editable=True, 
            weight=1,
            on_change=lambda data, row, col: print(f"Changed cell ({row},{col}) to {data[row][col]}")
        )
        header3 = Header(
            text="Age", 
            fg_color="#2a2d2e", 
            bg_color="#000000", 
            font_size=14, 
            weight=1, 
            align="right",
            action=self.sort_by_age
        )
        header4 = Header(
            text="Email", 
            fg_color="#2a2d2e", 
            bg_color="#000000", 
            text_color="blue", 
            font_size=14, 
            weight=5, 
            align="center",
            action=self.sort_by_email
        )
        header5 = Header(
            text="Active", 
            type=WidgetType.RNDTOGGLE,
            align="center",
            fg_color="#2a2d2e",
            bg_color="#000000",
            font_size=14,
            weight=1,
            on_change=lambda data, row, col: print(f"Changed cell ({row},{col}) to {data[row][col]}")
        )
        header6 = Header(
            text="Notify", 
            type=WidgetType.SQTOGGLE,
            align="center",
            fg_color="#2a2d2e",
            bg_color="#000000",
            font_size=14,
            weight=1,
            on_change=lambda data, row, col: print(f"Changed cell ({row},{col}) to {data[row][col]}")
        )
        header7 = Header(
            text="isPremium", 
            type=WidgetType.CHECKBOX,
            align="center",
            fg_color="#2a2d2e",
            bg_color="#000000",
            font_size=14,
            weight=1,
            on_change=lambda data, row, col: print(f"Changed cell ({row},{col}) to {data[row][col]}")
        )
        header8 = Header(
            text="isBlocked", 
            type=WidgetType.RADIOBTN,
            align="center",
            fg_color="#2a2d2e",
            bg_color="#000000",
            font_size=14,
            weight=1,
            on_change=lambda data, row, col: print(f"Changed cell ({row},{col}) to {data[row][col]}")
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
    app.mainloop()