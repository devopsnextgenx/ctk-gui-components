import customtkinter as ctk
from PIL import Image
from devopsnextgenx.utils.iconProvider import ICON_PATH
from devopsnextgenx.utils import place_frame

class ProgressPopup(ctk.CTkFrame):
    def __init__(self, master, title: str = "Background Tasks", label: str = "Label...",
                 message: str = "Do something...", side: str = "right_bottom"):
        self.root = master
        self.width = 420
        self.height = 120
        super().__init__(self.root, width=self.width, height=self.height, corner_radius=5, border_width=1)
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)

        self.cancelled = False

        self.title = ctk.CTkLabel(self, text=title, font=("", 16))
        self.title.grid(row=0, column=0, sticky="ew", padx=20, pady=10, columnspan=2)

        self.label = ctk.CTkLabel(self, text=label, height=0)
        self.label.grid(row=1, column=0, sticky="sw", padx=20, pady=0)

        self.progressbar = ctk.CTkProgressBar(self)
        self.progressbar.set(0)
        self.progressbar.grid(row=2, column=0, sticky="ew", padx=20, pady=0)

        self.close_icon = ctk.CTkImage(Image.open(ICON_PATH["close"][0]),
                                       Image.open(ICON_PATH["close"][1]),
                                       (16, 16))

        self.cancel_btn = ctk.CTkButton(self, text="", width=16, height=16, fg_color="transparent",
                                        command=self.cancel_task, image=self.close_icon)
        self.cancel_btn.grid(row=2, column=1, sticky="e", padx=10, pady=0)

        self.message = ctk.CTkLabel(self, text=message, height=0)
        self.message.grid(row=3, column=0, sticky="nw", padx=20, pady=(0, 10))

        self.horizontal, self.vertical = side.split("_")
        place_frame(self.root, self, self.horizontal, self.vertical)
        self.root.bind("<Configure>", self.update_position, add="+")

    def update_position(self, event):
        place_frame(self.root, self, self.horizontal, self.vertical)
        self.update_idletasks()
        self.root.update_idletasks()

    def update_progress(self, progress):
        if self.cancelled:
            return "Cancelled"

        self.progressbar.set(progress)
        self.update_progress_bar_color(progress)

        # Check if the progress is complete and close the popup after 5 seconds
        if progress >= 1.0:
            self.after(5000, self.close_progress_popup)
            
    def update_message(self, message):
        self.message.configure(text=message)

    def update_label(self, label):
        self.label.configure(text=label)

    def update_status(self, text, progress):
        """Update the status of the progress popup."""
        self.update_label(text)
        self.update_progress(progress)

    def cancel_task(self):
        self.cancelled = True
        self.close_progress_popup()

    def close_progress_popup(self):
        self.root.unbind("<Configure>")
        self.destroy()

    def update_progress_bar_color(self, progress):
        if progress < 0.3:
            color = "#FF0000"
        elif progress < 0.7:
            color = "#0000FF"
        else:
            color = "#00FF00"
        self.progressbar.configure(fg_color=color)
