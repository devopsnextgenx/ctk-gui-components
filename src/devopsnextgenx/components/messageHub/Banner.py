import time
import customtkinter as ctk
from PIL import Image
from devopsnextgenx.utils import place_frame
from devopsnextgenx.utils.iconProvider import ICON_PATH
from devopsnextgenx.utils import LINK_BTN

class Banner(ctk.CTkFrame):
    def __init__(self, master, state: str = "info", title: str = "Title", btn1: str = "Action A",
                 btn2: str = "Action B", side: str = "right_bottom", destroy_delay: int = 10000):
        self.root = master
        self.width = 400
        self.height = 100
        super().__init__(self.root, width=self.width, height=self.height, corner_radius=5, border_width=1)

        self.grid_propagate(False)
        self.grid_columnconfigure(1, weight=1)
        self.event = None

        self.horizontal, self.vertical = side.split("_")

        if state not in ICON_PATH or ICON_PATH[state] is None:
            self.icon = ctk.CTkImage(Image.open(ICON_PATH["info"]), Image.open(ICON_PATH["info"]), (24, 24))
        else:
            self.icon = ctk.CTkImage(Image.open(ICON_PATH[state]), Image.open(ICON_PATH[state]), (24, 24))

        self.close_icon = ctk.CTkImage(Image.open(ICON_PATH["close"][0]), Image.open(ICON_PATH["close"][1]), (20, 20))

        self.title_label = ctk.CTkLabel(self, text=f"  {title}", font=("", 16), image=self.icon,
                                        compound="left")
        self.title_label.grid(row=0, column=0, sticky="w", padx=15, pady=10)

        self.close_btn = ctk.CTkButton(self, text="", image=self.close_icon, width=20, height=20, hover=False,
                                       fg_color="transparent", command=self.button_event)
        self.close_btn.grid(row=0, column=1, sticky="ne", padx=10, pady=10)

        self.btn_1 = ctk.CTkButton(self, text=btn1, **LINK_BTN, command=lambda: self.button_event(btn1))
        self.btn_1.grid(row=1, column=0, padx=(40, 5), pady=10, sticky="w")

        self.btn_2 = ctk.CTkButton(self, text=btn2, **LINK_BTN,
                                   command=lambda: self.button_event(btn2))
        self.btn_2.grid(row=1, column=1, padx=5, pady=10, sticky="w")

        # Add progress bar
        self.progress_bar = ctk.CTkProgressBar(self, width=self.width - 20)
        self.progress_bar.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        self.progress_bar.set(1.0)  # Set initial progress to 100%

        place_frame(self.root, self, self.horizontal, self.vertical)
        self.root.bind("<Configure>", self.update_position, add="+")

        # Schedule the banner to be destroyed after the specified delay
        self.destroy_delay = destroy_delay
        self.start_time = time.time()
        self.update_progress_bar()
        self.root.after(destroy_delay, self.button_event)

    def update_position(self, event):
        place_frame(self.root, self, self.horizontal, self.vertical)
        self.update_idletasks()
        self.root.update_idletasks()

    def get(self):
        if self.winfo_exists():
            self.master.wait_window(self)
        return self.event

    def button_event(self, event=None):
        self.root.unbind("<Configure>")
        self.grab_release()
        self.destroy()
        self.event = event

    def update_progress_bar(self):
        if not self.winfo_exists():
            return

        current_time = time.time()
        elapsed_time = current_time - self.start_time
        elapsed_time = max(1, elapsed_time)  # Ensure elapsed_time is at least 1 second
        progress = (elapsed_time * 1000) / self.destroy_delay

        if progress < 0.3:
            self.progress_bar.configure(fg_color="#00FF00")
        elif 0.3 <= progress < 0.7:
            self.progress_bar.configure(fg_color="blue")
        else:
            self.progress_bar.configure(fg_color="red")

        if progress < 1:
            self.progress_bar.set(progress)
        if progress > 0:
            self.root.after(1000, self.update_progress_bar)