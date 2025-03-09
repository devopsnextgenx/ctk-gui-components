import sys
import customtkinter as ctk
from PIL import Image
from devopsnextgenx.utils import center_window
from devopsnextgenx.utils.iconProvider import ICON_PATH

class Alert(ctk.CTkToplevel):
    def __init__(self, state: str = "info", title: str = "Title",
                 body_text: str = "Body text", btn1: str = "OK", btn2: str = "Cancel"):
        super().__init__()
        self.old_y = None
        self.old_x = None
        self.width = 420
        self.height = 200
        center_window(self, self.width, self.height)
        self.resizable(False, False)
        self.overrideredirect(True)
        self.lift()

        self.x = self.winfo_x()
        self.y = self.winfo_y()
        self.event = None

        # Set transparent_color properly for all platforms
        if sys.platform.startswith("win"):
            self.transparent_color = self._apply_appearance_mode(self.cget("fg_color"))
            self.attributes("-transparentcolor", self.transparent_color)
        else:
            # Use 'transparent' instead of None
            self.transparent_color = 'transparent'

        self.bg_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame_top = ctk.CTkFrame(self, corner_radius=5, width=self.width,
                                      border_width=1,
                                      bg_color=self.transparent_color, fg_color=self.bg_color)
        self.frame_top.grid(sticky="nsew")
        self.frame_top.bind("<B1-Motion>", self.move_window)
        self.frame_top.bind("<ButtonPress-1>", self.old_xy_set)
        self.frame_top.grid_columnconfigure(0, weight=1)
        self.frame_top.grid_rowconfigure(1, weight=1)

        if state not in ICON_PATH or ICON_PATH[state] is None:
            self.icon = ctk.CTkImage(Image.open(ICON_PATH["info"]), Image.open(ICON_PATH["info"]), (30, 30))
        else:
            self.icon = ctk.CTkImage(Image.open(ICON_PATH[state]), Image.open(ICON_PATH[state]), (30, 30))

        self.close_icon = ctk.CTkImage(Image.open(ICON_PATH["close"][0]), Image.open(ICON_PATH["close"][1]), (20, 20))

        self.title_label = ctk.CTkLabel(self.frame_top, text=f"  {title}", font=("", 18), image=self.icon,
                                        compound="left")
        self.title_label.grid(row=0, column=0, sticky="w", padx=15, pady=20)
        self.title_label.bind("<B1-Motion>", self.move_window)
        self.title_label.bind("<ButtonPress-1>", self.old_xy_set)

        self.close_btn = ctk.CTkButton(self.frame_top, text="", image=self.close_icon, width=20, height=20, hover=False,
                                       fg_color="transparent", command=self.button_event)
        self.close_btn.grid(row=0, column=1, sticky="ne", padx=10, pady=10)

        self.message = ctk.CTkLabel(self.frame_top,
                                    text=body_text,
                                    justify="left", anchor="w", wraplength=self.width - 30)
        self.message.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew", columnspan=2)

        self.btn_1 = ctk.CTkButton(self.frame_top, text=btn1, width=120, command=lambda: self.button_event(btn1),
                                   text_color="white")
        self.btn_1.grid(row=2, column=0, padx=(10, 5), pady=20, sticky="e")

        self.btn_2 = ctk.CTkButton(self.frame_top, text=btn2, width=120, fg_color="transparent", border_width=1,
                                   command=lambda: self.button_event(btn2), text_color=("black", "white"))
        self.btn_2.grid(row=2, column=1, padx=(5, 10), pady=20, sticky="e")

        self.bind("<Escape>", lambda e: self.button_event())

    def get(self):
        if self.winfo_exists():
            self.master.wait_window(self)
        return self.event

    def old_xy_set(self, event):
        self.old_x = event.x
        self.old_y = event.y

    def move_window(self, event):
        self.y = event.y_root - self.old_y
        self.x = event.x_root - self.old_x
        self.geometry(f'+{self.x}+{self.y}')

    def button_event(self, event=None):
        self.grab_release()
        self.destroy()
        self.event = event