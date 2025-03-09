import customtkinter as ctk

DEFAULT_BTN = {
    "fg_color": "transparent",
    "hover": False,
    "compound": "left",
    "anchor": "w",
}

LINK_BTN = {**DEFAULT_BTN, "width": 70, "height": 25, "text_color": "#3574F0"}
BTN_LINK = {**DEFAULT_BTN, "width": 20, "height": 20, "text_color": "#3574F0", "font": ("", 13, "underline")}
ICON_BTN = {**DEFAULT_BTN, "width": 30, "height": 30}
BTN_OPTION = {**DEFAULT_BTN, "text_color": ("black", "white"), "corner_radius": 5, "hover_color": ("gray90", "gray25")}
btn = {**DEFAULT_BTN, "width": 230, "height": 50, "text_color": ("#000000", "#FFFFFF"), "font": ("", 13)}
btn_active = {**btn, "fg_color": (ctk.ThemeManager.theme["CTkButton"]["fg_color"]), "hover": True}
btn_footer = {**btn, "fg_color": ("#EBECF0", "#393B40"), "hover_color": ("#DFE1E5", "#43454A"), "corner_radius": 0}

DEFAULT_ICON_ONLY_BTN = {**DEFAULT_BTN, "height": 50, "text_color": ("#000000", "#FFFFFF"), "anchor": "center"}
btn_icon_only = {**DEFAULT_ICON_ONLY_BTN, "width": 70}
btn_icon_only_active = {**btn_icon_only, "fg_color": (ctk.ThemeManager.theme["CTkButton"]["fg_color"]), "hover": True}
btn_icon_only_footer = {**DEFAULT_ICON_ONLY_BTN, "width": 80, "fg_color": ("#EBECF0", "#393B40"),
                        "hover_color": ("#DFE1E5", "#43454A"), "corner_radius": 0}