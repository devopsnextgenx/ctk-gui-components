import os
import customtkinter as ctk
from PIL import Image, ImageDraw
from devopsnextgenx.utils import set_opacity, ICON_BTN
from devopsnextgenx.utils.iconProvider import ICON_PATH

def image_list_provider(ICON_DIR, imgOptions = {"imgPrefix":"sun", "suffix":".png", "start":1, "end":15}):
    return list(os.path.join(ICON_DIR, f"{imgOptions['imgPrefix']}{i}.{imgOptions['suffix']}") for i in range(imgOptions['start'], imgOptions['end']))

class Carousel(ctk.CTkFrame):
    def __init__(self, master: any, img_list=None, width=None, height=None, img_radius=5, **kwargs):
        if img_list is None:
            img_list = ICON_PATH["images"]

        self.img_list = img_list
        self.image_index = 0
        self.img_radius = img_radius

        if width and height:
            self.width = width
            self.height = height
            for path in self.img_list.copy():
                try:
                    Image.open(path)
                except Exception as e:
                    self.remove_path(path)
        else:
            self.width, self.height = self.get_dimensions()
        super().__init__(master, width=self.width, height=self.height, fg_color="transparent", **kwargs)

        self.prev_icon = ctk.CTkImage(Image.open(ICON_PATH["left"]), Image.open(ICON_PATH["left"]), (30, 30))
        self.next_icon = ctk.CTkImage(Image.open(ICON_PATH["right"]), Image.open(ICON_PATH["right"]), (30, 30))

        self.image_label = ctk.CTkLabel(self, text="")
        self.image_label.pack(expand=True, fill="both")

        self.button_bg = ctk.ThemeManager.theme["CTkButton"]["fg_color"]

        self.previous_button = ctk.CTkButton(self.image_label, text="", image=self.prev_icon, **ICON_BTN,
                                             command=self.previous_callback, bg_color=self.button_bg)
        self.previous_button.place(relx=0.0, rely=0.5, anchor='w')  # Adjusted position
        set_opacity(self.previous_button.winfo_id(), color=self.button_bg[0])  # Increased transparency
        # set_opacity(self.previous_button.winfo_id(), color=self.button_bg[0], alpha=0.2)  # Increased transparency

        self.next_button = ctk.CTkButton(self.image_label, text="", image=self.next_icon, **ICON_BTN,
                                         command=self.next_callback, bg_color=self.button_bg)
        self.next_button.place(relx=1.0, rely=0.5, anchor='e')  # Adjusted position
        set_opacity(self.next_button.winfo_id(), color=self.button_bg[0])  # Increased transparency
        # set_opacity(self.next_button.winfo_id(), color=self.button_bg[0], alpha=0.2)  # Increased transparency

        self.bind("<Left>", lambda event: self.previous_callback())
        self.bind("<Right>", lambda event: self.next_callback())
        self.focus_set()

        self.image_label.bind("<Button-1>", self.set_focus)

        self.next_callback()

    def set_focus(self, event=None):
        self.focus_set()

    def get_dimensions(self):
        max_width, max_height = 0, 0

        for path in self.img_list.copy():
            try:
                with Image.open(path) as img:
                    width, height = img.size

                    if width > max_width and height > max_height:
                        max_width, max_height = width, height
            except Exception as e:
                self.remove_path(path)

        return max_width, max_height

    def remove_path(self, path):
        self.img_list.remove(path)

    @staticmethod
    def add_corners(image, radius):
        circle = Image.new('L', (radius * 2, radius * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, radius * 2 - 1, radius * 2 - 1), fill=255)
        alpha = Image.new('L', image.size, 255)
        w, h = image.size
        alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
        alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
        alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
        alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))
        image.putalpha(alpha)
        return image

    def next_callback(self):
        self.image_index += 1

        if self.image_index > len(self.img_list) - 1:
            self.image_index = 0

        create_rounded = Image.open(self.img_list[self.image_index])
        create_rounded = self.add_corners(create_rounded, self.img_radius)

        next_image = ctk.CTkImage(create_rounded, create_rounded, (self.width, self.height))

        self.image_label.configure(image=next_image)

    def previous_callback(self):
        self.image_index -= 1

        if self.image_index < 0:
            self.image_index = len(self.img_list) - 1

        create_rounded = Image.open(self.img_list[self.image_index])
        create_rounded = self.add_corners(create_rounded, self.img_radius)

        next_image = ctk.CTkImage(create_rounded, create_rounded, (self.width, self.height))

        self.image_label.configure(image=next_image)
