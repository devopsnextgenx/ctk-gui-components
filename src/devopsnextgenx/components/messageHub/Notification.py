import customtkinter as ctk
from PIL import Image
from devopsnextgenx.utils import place_frame
from devopsnextgenx.utils.iconProvider import ICON_PATH

class Notification(ctk.CTkFrame):
    def __init__(self, master, state: str = "info", message: str = "message", side: str = "right_bottom", destroy_delay: int = 10000):
        self.root = master
        self.width = 400
        self.height = 60
        super().__init__(self.root, width=self.width, height=self.height, corner_radius=5, border_width=1)
        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.horizontal, self.vertical = side.split("_")

        if state not in ICON_PATH or ICON_PATH[state] is None:
            self.icon = ctk.CTkImage(Image.open(ICON_PATH["info"]), Image.open(ICON_PATH["info"]), (24, 24))
        else:
            self.icon = ctk.CTkImage(Image.open(ICON_PATH[state]), Image.open(ICON_PATH[state]), (24, 24))

        self.close_icon = ctk.CTkImage(Image.open(ICON_PATH["close"][0]), Image.open(ICON_PATH["close"][1]), (20, 20))

        self.message_label = ctk.CTkLabel(self, text=f"  {message}", font=("", 13), image=self.icon, compound="left")
        self.message_label.grid(row=0, column=0, sticky="nsw", padx=15, pady=10)

        self.close_btn = ctk.CTkButton(self, text="", image=self.close_icon, width=20, height=20, hover=False,
                                       fg_color="transparent", command=self.close_notification)
        self.close_btn.grid(row=0, column=1, sticky="nse", padx=10, pady=10)

        place_frame(self.root, self, self.horizontal, self.vertical)
        self.root.bind("<Configure>", self.update_position, add="+")

        self.after(destroy_delay, self.close_notification)

    def update_position(self, event):
        place_frame(self.root, self, self.horizontal, self.vertical)
        self.update_idletasks()
        self.root.update_idletasks()

    def close_notification(self):
        self.root.unbind("<Configure>")
        self.destroy()
