from typing import Any, Optional, Union
import os
import warnings
import platform

# Determine the current operating system
PLATFORM = platform.system().lower()

# Windows-specific imports
if PLATFORM == 'windows':
    try:
        import winreg
        from ctypes import (POINTER, Structure, byref, c_int, pointer, sizeof, windll)
        from ctypes.wintypes import DWORD, ULONG
        HAS_WINDOWS_API = True
    except ImportError:
        HAS_WINDOWS_API = False
        warnings.warn("Windows API imports failed despite being on Windows.")
else:
    HAS_WINDOWS_API = False

# Linux-specific imports
if PLATFORM == 'linux':
    try:
        import subprocess
        import gi
        gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk, Gdk
        HAS_GTK = True
    except (ImportError, ValueError):
        HAS_GTK = False
        warnings.warn("GTK libraries not found. Some styling features will be limited.")
    
    try:
        import Xlib
        from Xlib import display, X
        import Xlib.protocol.event
        HAS_XLIB = True
    except ImportError:
        HAS_XLIB = False
        warnings.warn("Xlib not found. Some window styling features will be limited.")
    
    # Determine desktop environment
    def get_desktop_environment():
        desktop = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
        if desktop:
            return desktop
        # Fallback checks
        if os.environ.get('GNOME_DESKTOP_SESSION_ID'):
            return 'gnome'
        elif os.environ.get('KDE_FULL_SESSION'):
            return 'kde'
        # Default to generic X11
        return 'unknown'
    
    DESKTOP_ENV = get_desktop_environment()
else:
    HAS_GTK = False
    HAS_XLIB = False
    DESKTOP_ENV = None

# Windows specific classes
if HAS_WINDOWS_API:
    class ACCENT_POLICY(Structure):
        _fields_ = [
            ("AccentState", DWORD),
            ("AccentFlags", DWORD),
            ("GradientColor", DWORD),
            ("AnimationId", DWORD),
        ]

    class WINDOW_COMPOSITION_ATTRIBUTES(Structure):
        _fields_ = [
            ("Attribute", DWORD),
            ("Data", POINTER(ACCENT_POLICY)),
            ("SizeOfData", ULONG),
        ]

    class MARGINS(Structure):
        _fields_ = [
            ("cxLeftWidth", c_int),
            ("cxRightWidth", c_int),
            ("cyTopHeight", c_int),
            ("cyBottomHeight", c_int),
        ]

# Cross-platform window/widget detection
def detect(window: Any):
    """Detect the type of UI library and return window handle/ID"""
    try:  # tkinter
        if hasattr(window, 'update'):
            window.update()
        if hasattr(window, 'winfo_id'):
            win_id = window.winfo_id()
            if PLATFORM == 'windows':
                return windll.user32.GetParent(win_id)
            return win_id
    except:
        pass
    
    try:  # pyqt/pyside
        return window.winId().__int__()
    except:
        pass
    
    try:  # wxpython
        return window.GetHandle()
    except:
        pass
    
    # GTK (Linux only)
    if PLATFORM == 'linux' and HAS_GTK:
        try:
            if isinstance(window, Gtk.Window):
                return window.get_window().get_xid()
        except:
            pass
    
    if isinstance(window, int):
        return window  # assume it's already a window handle/ID
    
    # Fallback: get active window
    if PLATFORM == 'windows' and HAS_WINDOWS_API:
        return windll.user32.GetActiveWindow()
    elif PLATFORM == 'linux' and HAS_XLIB:
        try:
            d = display.Display()
            return d.get_input_focus().focus.id
        except:
            pass
    
    warnings.warn("Could not detect window ID")
    return None

# Cross-platform paint function
def paint(window: Any) -> None:
    """Paint background for transparency effects"""
    try:  # tkinter
        window.config(bg="black")
        return
    except:
        pass
    
    try:  # pyqt/pyside
        window.setStyleSheet("background-color: transparent;")
        return
    except:
        pass
    
    try:  # wxpython
        window.SetBackgroundColour("black")
        return
    except:
        pass
    
    # GTK (Linux only)
    if PLATFORM == 'linux' and HAS_GTK:
        try:
            if isinstance(window, Gtk.Widget):
                window.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 1))
                return
        except:
            pass
    
    warnings.warn("Don't know what the window type is, please set its background color to black")

# Color conversion utility
def convert_color(color_name: str) -> str:
    """Convert colors to the required format based on platform"""
    
    NAMES_TO_HEX = {
        "aliceblue": "#f0f8ff",
        "antiquewhite": "#faebd7",
        "aqua": "#00ffff",
        "aquamarine": "#7fffd4",
        "azure": "#f0ffff",
        "beige": "#f5f5dc",
        "bisque": "#ffe4c4",
        "black": "#000000",
        "blanchedalmond": "#ffebcd",
        "blue": "#0000ff",
        "blueviolet": "#8a2be2",
        "brown": "#a52a2a",
        "burlywood": "#deb887",
        "cadetblue": "#5f9ea0",
        "chartreuse": "#7fff00",
        "chocolate": "#d2691e",
        "coral": "#ff7f50",
        "cornflowerblue": "#6495ed",
        "cornsilk": "#fff8dc",
        "crimson": "#dc143c",
        "cyan": "#00ffff",
        "darkblue": "#00008b",
        "darkcyan": "#008b8b",
        "darkgoldenrod": "#b8860b",
        "darkgray": "#a9a9a9",
        "darkgrey": "#a9a9a9",
        "darkgreen": "#006400",
        "darkkhaki": "#bdb76b",
        "darkmagenta": "#8b008b",
        "darkolivegreen": "#556b2f",
        "darkorange": "#ff8c00",
        "darkorchid": "#9932cc",
        "darkred": "#8b0000",
        "darksalmon": "#e9967a",
        "darkseagreen": "#8fbc8f",
        "darkslateblue": "#483d8b",
        "darkslategray": "#2f4f4f",
        "darkslategrey": "#2f4f4f",
        "darkturquoise": "#00ced1",
        "darkviolet": "#9400d3",
        "deeppink": "#ff1493",
        "deepskyblue": "#00bfff",
        "dimgray": "#696969",
        "dimgrey": "#696969",
        "dodgerblue": "#1e90ff",
        "firebrick": "#b22222",
        "floralwhite": "#fffaf0",
        "forestgreen": "#228b22",
        "fuchsia": "#ff00ff",
        "gainsboro": "#dcdcdc",
        "ghostwhite": "#f8f8ff",
        "gold": "#ffd700",
        "goldenrod": "#daa520",
        "gray": "#808080",
        "grey": "#808080",
        "green": "#008000",
        "greenyellow": "#adff2f",
        "honeydew": "#f0fff0",
        "hotpink": "#ff69b4",
        "indianred": "#cd5c5c",
        "indigo": "#4b0082",
        "ivory": "#fffff0",
        "khaki": "#f0e68c",
        "lavender": "#e6e6fa",
        "lavenderblush": "#fff0f5",
        "lawngreen": "#7cfc00",
        "lemonchiffon": "#fffacd",
        "lightblue": "#add8e6",
        "lightcoral": "#f08080",
        "lightcyan": "#e0ffff",
        "lightgoldenrodyellow": "#fafad2",
        "lightgray": "#d3d3d3",
        "lightgrey": "#d3d3d3",
        "lightgreen": "#90ee90",
        "lightpink": "#ffb6c1",
        "lightsalmon": "#ffa07a",
        "lightseagreen": "#20b2aa",
        "lightskyblue": "#87cefa",
        "lightslategray": "#778899",
        "lightslategrey": "#778899",
        "lightsteelblue": "#b0c4de",
        "lightyellow": "#ffffe0",
        "lime": "#00ff00",
        "limegreen": "#32cd32",
        "linen": "#faf0e6",
        "magenta": "#ff00ff",
        "maroon": "#800000",
        "mediumaquamarine": "#66cdaa",
        "mediumblue": "#0000cd",
        "mediumorchid": "#ba55d3",
        "mediumpurple": "#9370db",
        "mediumseagreen": "#3cb371",
        "mediumslateblue": "#7b68ee",
        "mediumspringgreen": "#00fa9a",
        "mediumturquoise": "#48d1cc",
        "mediumvioletred": "#c71585",
        "midnightblue": "#191970",
        "mintcream": "#f5fffa",
        "mistyrose": "#ffe4e1",
        "moccasin": "#ffe4b5",
        "navajowhite": "#ffdead",
        "navy": "#000080",
        "oldlace": "#fdf5e6",
        "olive": "#808000",
        "olivedrab": "#6b8e23",
        "orange": "#ffa500",
        "orangered": "#ff4500",
        "orchid": "#da70d6",
        "palegoldenrod": "#eee8aa",
        "palegreen": "#98fb98",
        "paleturquoise": "#afeeee",
        "palevioletred": "#db7093",
        "papayawhip": "#ffefd5",
        "peachpuff": "#ffdab9",
        "peru": "#cd853f",
        "pink": "#ffc0cb",
        "plum": "#dda0dd",
        "powderblue": "#b0e0e6",
        "purple": "#800080",
        "red": "#ff0000",
        "rosybrown": "#bc8f8f",
        "royalblue": "#4169e1",
        "saddlebrown": "#8b4513",
        "salmon": "#fa8072",
        "sandybrown": "#f4a460",
        "seagreen": "#2e8b57",
        "seashell": "#fff5ee",
        "sienna": "#a0522d",
        "silver": "#c0c0c0",
        "skyblue": "#87ceeb",
        "slateblue": "#6a5acd",
        "slategray": "#708090",
        "slategrey": "#708090",
        "snow": "#fffafa",
        "springgreen": "#00ff7f",
        "steelblue": "#4682b4",
        "tan": "#d2b48c",
        "teal": "#008080",
        "thistle": "#d8bfd8",
        "tomato": "#ff6347",
        "turquoise": "#40e0d0",
        "violet": "#ee82ee",
        "wheat": "#f5deb3",
        "white": "#ffffff",
        "whitesmoke": "#f5f5f5",
        "yellow": "#ffff00",
        "yellowgreen": "#9acd32",
    }

    if not color_name.startswith("#"):
        if color_name in NAMES_TO_HEX:
            color = NAMES_TO_HEX[color_name]
        elif color_name.startswith("grey") or color_name.startswith("gray"):
            color = f"#{color_name[-2:]}{color_name[-2:]}{color_name[-2:]}"
        else:
            raise ValueError(f"Invalid color passed: {color_name}")
    else:
        color = color_name

    # For Windows, convert to BGR format
    if PLATFORM == 'windows':
        color = f"{color[5:7]}{color[3:5]}{color[1:3]}"
    
    return color

# Windows-specific functions
if HAS_WINDOWS_API:
    def ChangeDWMAttrib(hWnd: int, attrib: int, color) -> None:
        """Change DWM window attribute (Windows only)"""
        windll.dwmapi.DwmSetWindowAttribute(hWnd, attrib, byref(color), sizeof(c_int))

    def ChangeDWMAccent(hWnd: int, attrib: int, state: int, color: str | None = None) -> None:
        """Change DWM window accent (Windows only)"""
        accentPolicy = ACCENT_POLICY()

        winCompAttrData = WINDOW_COMPOSITION_ATTRIBUTES()
        winCompAttrData.Attribute = attrib
        winCompAttrData.SizeOfData = sizeof(accentPolicy)
        winCompAttrData.Data = pointer(accentPolicy)

        accentPolicy.AccentState = state
        if color:
            accentPolicy.GradientColor = color

        windll.user32.SetWindowCompositionAttribute(hWnd, pointer(winCompAttrData))

    def ExtendFrameIntoClientArea(HWND: int) -> None:
        """Extend window frame into client area (Windows only)"""
        margins = MARGINS(-1, -1, -1, -1)
        windll.dwmapi.DwmExtendFrameIntoClientArea(HWND, byref(margins))

    def get_accent_color_windows() -> str:
        """Returns current accent color of Windows"""
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\DWM")
        value, type = winreg.QueryValueEx(key, "ColorizationAfterglow")
        winreg.CloseKey(key)
        color = f"#{str(hex(value))[4:]}"
        return color

# Linux helper functions
if PLATFORM == 'linux':
    def run_command(cmd: list) -> None:
        """Run shell command safely"""
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            warnings.warn(f"Command failed: {e}")
    
    def get_accent_color_linux() -> str:
        """Returns current accent color on Linux if available"""
        if DESKTOP_ENV == 'gnome':
            try:
                result = subprocess.run(
                    ["gsettings", "get", "org.gnome.desktop.interface", "accent-color"],
                    capture_output=True, text=True, check=True
                )
                if result.stdout.strip():
                    return result.stdout.strip().strip("'")
                return "#3584e4"  # Default GNOME blue
            except:
                pass
        
        # Default fallback color
        return "#3584e4"

# Cross-platform get_accent_color function
def get_accent_color() -> str:
    """Returns current accent color based on the platform"""
    if PLATFORM == 'windows' and HAS_WINDOWS_API:
        try:
            return get_accent_color_windows()
        except:
            return "#0078d7"  # Default Windows blue
    elif PLATFORM == 'linux':
        return get_accent_color_linux()
    else:
        return "#0078d7"  # Default fallback

# Main cross-platform styling class
class apply_style():
    """Different styles for windows - cross-platform implementation"""

    def __init__(self, window, style: str) -> None:
        # Available styles
        windows_styles = ["dark", "mica", "aero", "transparent", "acrylic", "win7",
                          "inverse", "popup", "native", "optimised", "light", "normal"]
        
        linux_styles = ["dark", "light", "transparent", "normal", "native"]
        
        all_styles = list(set(windows_styles + linux_styles))
        
        if style not in all_styles:
            raise ValueError(
                f"Invalid style name! No such window style exists: {style} \nAvailable styles: {all_styles}"
            )
        
        self.HWND = detect(window)
        self.window_obj = window
        
        # Apply style based on platform
        if PLATFORM == 'windows' and HAS_WINDOWS_API:
            self._apply_windows_style(style)
        elif PLATFORM == 'linux':
            self._apply_linux_style(style, window)
        else:
            warnings.warn(f"Platform {PLATFORM} not fully supported for window styling.")
    
    def _apply_windows_style(self, style: str) -> None:
        """Apply Windows-specific styles"""
        if style == "mica":
            ChangeDWMAttrib(self.HWND, 19, c_int(1))
            ChangeDWMAttrib(self.HWND, 1029, c_int(0x01))
        elif style == "optimised":
            ChangeDWMAccent(self.HWND, 30, 1)
        elif style == "dark":
            ChangeDWMAttrib(self.HWND, 19, c_int(1))
            ChangeDWMAttrib(self.HWND, 20, c_int(1))
        elif style == "light":
            ChangeDWMAttrib(self.HWND, 19, c_int(0))
            ChangeDWMAttrib(self.HWND, 20, c_int(0))
        elif style == "inverse":
            ChangeDWMAccent(self.HWND, 6, 1)
        elif style == "win7":
            ChangeDWMAccent(self.HWND, 11, 1)
        elif style == "aero":
            paint(self.window_obj)
            ChangeDWMAccent(self.HWND, 30, 2)
            ChangeDWMAccent(self.HWND, 19, 3, color=0x000000)
        elif style == "acrylic":
            paint(self.window_obj)
            ChangeDWMAttrib(self.HWND, 20, c_int(1))
            ChangeDWMAccent(self.HWND, 30, 3, color=0x292929)
            ExtendFrameIntoClientArea(self.HWND)
        elif style == "popup":
            ChangeDWMAccent(self.HWND, 4, 1)
        elif style == "native":
            ChangeDWMAccent(self.HWND, 30, 2)
            ChangeDWMAccent(self.HWND, 19, 2)
        elif style == "transparent":
            paint(self.window_obj)
            ChangeDWMAccent(self.HWND, 30, 2)
            ChangeDWMAccent(self.HWND, 19, 4, color=0)
        elif style == "normal":
            ChangeDWMAccent(self.HWND, 6, 0)
            ChangeDWMAccent(self.HWND, 4, 0)
            ChangeDWMAccent(self.HWND, 11, 0)
            ChangeDWMAttrib(self.HWND, 19, c_int(0))
            ChangeDWMAttrib(self.HWND, 20, c_int(0))
            ChangeDWMAccent(self.HWND, 30, 0)
            ChangeDWMAccent(self.HWND, 19, 0)
    
    def _apply_linux_style(self, style: str, window: Any) -> None:
        """Apply Linux-specific styles"""
        # For GTK applications in Linux
        if HAS_GTK:
            gtk_win = None
            if isinstance(window, Gtk.Window):
                gtk_win = window
            
            # Get GTK settings
            settings = Gtk.Settings.get_default() if HAS_GTK else None
            
            if style == "dark":
                # Apply dark theme
                if settings:
                    settings.set_property("gtk-application-prefer-dark-theme", True)
                
                # GNOME specific
                if DESKTOP_ENV == 'gnome':
                    run_command(["gsettings", "set", "org.gnome.desktop.interface", "color-scheme", "prefer-dark"])
                elif DESKTOP_ENV == 'kde':
                    run_command(["plasma-apply-colorscheme", "BreezeDark"])
            
            elif style == "light":
                # Apply light theme
                if settings:
                    settings.set_property("gtk-application-prefer-dark-theme", False)
                
                # GNOME specific
                if DESKTOP_ENV == 'gnome':
                    run_command(["gsettings", "set", "org.gnome.desktop.interface", "color-scheme", "default"])
                elif DESKTOP_ENV == 'kde':
                    run_command(["plasma-apply-colorscheme", "BreezeLight"])
            
            elif style == "transparent":
                # Apply transparency
                paint(window)
                
                if gtk_win:
                    screen = gtk_win.get_screen()
                    visual = screen.get_rgba_visual()
                    if visual and screen.is_composited():
                        gtk_win.set_visual(visual)
                        gtk_win.set_app_paintable(True)
                        
                        # Connect drawing event to create transparency
                        def draw_transparent(widget, ctx):
                            ctx.set_source_rgba(0, 0, 0, 0.5)  # Semi-transparent
                            ctx.set_operator(0)  # OPERATOR_SOURCE
                            ctx.paint()
                            return False
                        
                        gtk_win.connect("draw", draw_transparent)
                
                # X11 transparency
                if HAS_XLIB and self.HWND:
                    try:
                        d = display.Display()
                        win = d.create_resource_object('window', self.HWND)
                        atom = d.intern_atom('_NET_WM_WINDOW_OPACITY')
                        opacity = int(0.8 * 0xffffffff)  # 80% opacity
                        win.change_property(atom, X.CARDINAL, 32, [opacity])
                        d.flush()
                    except Exception as e:
                        warnings.warn(f"Failed to set X11 transparency: {e}")
            
            elif style == "normal":
                # Reset to normal
                if gtk_win:
                    gtk_win.set_app_paintable(False)
                    # Use system default visual
                    screen = gtk_win.get_screen()
                    visual = screen.get_system_visual()
                    gtk_win.set_visual(visual)
                
                # Remove X11 transparency
                if HAS_XLIB and self.HWND:
                    try:
                        d = display.Display()
                        win = d.create_resource_object('window', self.HWND)
                        atom = d.intern_atom('_NET_WM_WINDOW_OPACITY')
                        win.delete_property(atom)
                        d.flush()
                    except Exception:
                        pass
            
            # Map Windows-specific styles to Linux alternatives
            elif style in ["mica", "aero", "acrylic"]:
                # Use transparency as fallback
                self._apply_linux_style("transparent", window)
            elif style in ["win7", "inverse", "popup", "optimised"]:
                # No direct equivalent, use normal
                warnings.warn(f"Style '{style}' is Windows-specific with no Linux equivalent.")
                self._apply_linux_style("normal", window)

# Cross-platform set_opacity class
class set_opacity():
    """Change opacity of individual widgets - cross-platform"""

    def __init__(self, widget: Any, value: float = 1.0, color: str = None) -> None:
        widget_id = None
        
        try:
            # Tkinter widgets
            if hasattr(widget, 'winfo_id'):
                widget_id = widget.winfo_id()
            elif isinstance(widget, int):
                widget_id = widget
            else:
                raise ValueError("Widget ID should be passed, not the widget name.")
        except:
            warnings.warn("Could not identify widget ID")
            return
        
        self.widget_id = widget_id
        self.opacity = value
        
        if PLATFORM == 'windows' and HAS_WINDOWS_API:
            # Windows implementation
            self.opacity_value = int(255 * value)
            self.color = 1 if color is None else DWORD(int(convert_color(color), base=16))
            wnd_exstyle = windll.user32.GetWindowLongA(self.widget_id, -20)
            new_exstyle = wnd_exstyle | 0x00080000
            windll.user32.SetWindowLongA(self.widget_id, -20, new_exstyle)
            windll.user32.SetLayeredWindowAttributes(
                self.widget_id, self.color, self.opacity_value, 3
            )
        
        elif PLATFORM == 'linux' and HAS_XLIB and self.widget_id:
            # Linux implementation using X11
            try:
                d = display.Display()
                win = d.create_resource_object('window', self.widget_id)
                
                # Set the _NET_WM_WINDOW_OPACITY property
                atom = d.intern_atom('_NET_WM_WINDOW_OPACITY')
                opacity_value = int(self.opacity * 0xffffffff)
                win.change_property(atom, X.CARDINAL, 32, [opacity_value])
                d.flush()
            except Exception as e:
                warnings.warn(f"Failed to set opacity: {e}")

# Cross-platform header color change class
class change_header_color():
    """Change the titlebar background color"""

    def __init__(self, window: Any, color: str) -> None:
        self.HWND = detect(window)
        
        if PLATFORM == 'windows' and HAS_WINDOWS_API:
            if color == "transparent":
                ChangeDWMAccent(self.HWND, 30, 2)
                return
            else:
                ChangeDWMAccent(self.HWND, 30, 0)

            self.color = DWORD(int(convert_color(color), base=16))
            self.attrib = 35
            ChangeDWMAttrib(self.HWND, self.attrib, self.color)
        
        elif PLATFORM == 'linux':
            warnings.warn("Titlebar color customization has limited support on Linux")
            # Basic implementations for specific desktop environments
            if DESKTOP_ENV == 'gnome':
                # Can only set to system-wide themes, not specific colors
                pass
            elif DESKTOP_ENV == 'kde':
                # KDE might support this via color schemes
                pass

# Cross-platform border color change class
class change_border_color():
    """Change the window border color"""

    def __init__(self, window: Any, color: str) -> None:
        self.HWND = detect(window)
        
        if PLATFORM == 'windows' and HAS_WINDOWS_API:
            self.color = DWORD(int(convert_color(color), base=16))
            self.attrib = 34
            ChangeDWMAttrib(self.HWND, self.attrib, self.color)
        
        elif PLATFORM == 'linux':
            warnings.warn("Window border color customization has limited support on Linux")

# Cross-platform title color change class
class change_title_color():
    """Change the title color"""

    def __init__(self, window: Any, color: str) -> None:
        self.HWND = detect(window)
        
        if PLATFORM == 'windows' and HAS_WINDOWS_API:
            self.color = DWORD(int(convert_color(color), base=16))
            self.attrib = 36
            ChangeDWMAttrib(self.HWND, self.attrib, self.color)
        
        elif PLATFORM == 'linux':
            warnings.warn("Titlebar text color customization has limited support on Linux")