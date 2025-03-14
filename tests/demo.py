import os
import sys
import time
import tkinter as tk  # Add this import for Canvas and Scrollbar

# Add src directory to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_path)

import customtkinter as ctk
import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY, SECONDARY, INFO
from devopsnextgenx.utils import get_icon_path
from devopsnextgenx.components.StatusBar import StatusBar
from devopsnextgenx.components.Table import Table, Header, WidgetType
from devopsnextgenx.components.Carousel import Carousel, image_list_provider
from devopsnextgenx.components.ScrollFrame import ScrollFrame
from devopsnextgenx.components.messageHub.provider import show_alert, show_banner, show_notification
from devopsnextgenx.components import Treeview, PreviewSide
from EmployeeTreeDataProvider import create_org_structure

closeDark = get_icon_path("close", "dark")
print(f"Icon path for 'close' icon in dark theme: {closeDark}")
if os.path.exists(closeDark):
    print("Icon file exists!")
else:
    print("Icon file not found!")

def alert():
    alertx = show_alert(state="info", title="Title", body_text="How do I get to top on AI?", btn1="Ok", btn2="Cancel")

def banner():
    bannerx = show_banner(state="info", title="Title")

def notification():
    notificationx = show_notification(state="info", message="message", side="right_top")

WIDGETS = {
    "Alert": alert,
    "Banner": banner,
    "Notification": notification,
#    "Card": card,
#    "Input1": ctk_input_1,
#    "Input2": ctk_input_2,
#    "Loader": loader,
#    "PopupMenu": ctk_popup,
#    "ProgressPopup": progress_popup,
#    "Treeview": treeview
}


def toggle_widgets(widget):
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

        # Use ScrollFrame component
        self.scroll_frame = ScrollFrame(self)
        self.scrollable_frame = self.scroll_frame.get_scrollable_frame()
        self.scroll_frame.pack(side="top", fill="both", expand=True)

        # Create a frame to hold the option menu and buttons
        button_frame = ttk.Frame(self.scrollable_frame)
        button_frame.pack(side="top", pady=20, fill="x")

        options = ["Alert", "Banner", "Notification"]
        option = ctk.CTkOptionMenu(button_frame, values=options, width=200, command=toggle_widgets)
        option.pack(side="left", padx=5)
        option.set("None")

        ttk.Button(
            button_frame, 
            text="Start Process", 
            command=self.simulate_process,
            bootstyle="primary"
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame, 
            text="Reset Status", 
            command=self.reset_status,
            bootstyle="secondary"
        ).pack(side="left", padx=5)

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

        # Add employee tree
        self.add_employee_tree(self.scrollable_frame)


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

    def add_employee_tree(self, parent):
        """Add organizational tree view"""
        org_structure = create_org_structure()
        
        # Convert employee structure to tree items format
        def convert_to_tree_items(employee):
            item = {
                "name": employee.name,
                "gender": employee.gender,
                "age": employee.age,
                "email": employee.email,
                "designation": employee.designation,
                "salary": employee.salary,
                "location": employee.location,
                "years_of_service": employee.years_of_service,
                "property1": "value1",
                "property2": "value2",
                "property3": "value3",
                "property4": "value4",
                "property5": "value5",
                "property6": "value6",
                "property7": "value7",
                "property8": "value8",
                "property9": "value9",
                "property10": "value10",
                "property11": "value11",
                "property12": "value12",
                "property13": "value13",
                "property14": "value14",
                "property15": "value15",
                "property16": "value16",
                "property17": "value17",
                "property18": "value18",
                "property19": "value19",
                "property20": "value20",
                "property21": "value21",
                "property22": "value22",
                "property23": "value23",
                "property24": "value24",
                "property25": "value25",
                "property26": "value26",
                "property27": "value27",
                "property28": "value28",
                "property29": "value29",
                "property30": "value30"
            }
            if employee.subordinates:
                item["children"] = [convert_to_tree_items(sub) for sub in employee.subordinates]
            return item
        
        tree_items = [convert_to_tree_items(org_structure)]
        
        rootFrame = ttk.Frame(parent)
        rootFrame.pack(fill="both", expand=False, pady=10)
        self.employee_tree = Treeview(rootFrame, items=tree_items, previewSide=PreviewSide.RIGHT, height=400)
        self.employee_tree.pack(fill="both", expand=False, pady=10)

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
