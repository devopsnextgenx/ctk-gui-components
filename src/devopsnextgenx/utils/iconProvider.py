import os

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
# ICON_DIR = os.path.join(CURRENT_PATH, "src", "icons")
ICON_DIR = os.path.join(CURRENT_PATH, "icons")
ICON_PATH = {
    "close": (os.path.join(ICON_DIR, "close_black.png"), os.path.join(ICON_DIR, "close_white.png")),
    "images": list(os.path.join(ICON_DIR, f"sun{i}.png") for i in range(1, 15)),
    "eye1": (os.path.join(ICON_DIR, "eye1_black.png"), os.path.join(ICON_DIR, "eye1_white.png")),
    "eye2": (os.path.join(ICON_DIR, "eye2_black.png"), os.path.join(ICON_DIR, "eye2_white.png")),
    "info": os.path.join(ICON_DIR, "info.png"),
    "warning": os.path.join(ICON_DIR, "warning.png"),
    "error": os.path.join(ICON_DIR, "error.png"),
    "left": os.path.join(ICON_DIR, "left.png"),
    "right": os.path.join(ICON_DIR, "right.png"),
    "warning2": os.path.join(ICON_DIR, "warning2.png"),
    "loader": os.path.join(ICON_DIR, "loader.gif"),
    "icon": os.path.join(ICON_DIR, "icon.png"),
    "arrow": os.path.join(ICON_DIR, "arrow.png"),
    "image": os.path.join(ICON_DIR, "image.png"),
}

def list_icons():
    """List all available icons"""
    return ICON_PATH.keys()

def get_icon_path(icon_name, theme="dark"):
    """Return the icon path based on the icon name and theme"""
    if icon_name in ICON_PATH:
        if isinstance(ICON_PATH[icon_name], tuple):
            return ICON_PATH[icon_name][0] if theme == "dark" else ICON_PATH[icon_name][1]
        return ICON_PATH[icon_name]
    return None