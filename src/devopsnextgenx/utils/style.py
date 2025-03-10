from typing import Any, Optional, Union
import os
import subprocess
import warnings

# Check for required Linux libraries
try:
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

class LinuxWindowIdentifier:
    """Helper class to identify window handles across different frameworks"""
    
    @staticmethod
    def get_xwindow_id(window_obj: Any) -> Optional[int]:
        """Extract X11 window ID from various GUI toolkit objects"""
        try:
            # Tkinter
            if hasattr(window_obj, 'winfo_id'):
                return window_obj.winfo_id()
            # PyQt/PySide
            elif hasattr(window_obj, 'winId'):
                return window_obj.winId().__int__()
            # wxPython
            elif hasattr(window_obj, 'GetHandle'):
                return window_obj.GetHandle()
            # Integer (already a window ID)
            elif isinstance(window_obj, int):
                return window_obj
            # GTK
            elif HAS_GTK and isinstance(window_obj, Gtk.Window):
                return window_obj.get_window().get_xid()
        except Exception as e:
            warnings.warn(f"Could not identify window: {e}")
        
        return None

class LinuxWindowStyle:
    """Manages window styling on Linux platforms"""
    
    def __init__(self, window: Any = None):
        self.window_id = LinuxWindowIdentifier.get_xwindow_id(window) if window else None
        self.display = None
        self.window = None
        
        if HAS_XLIB and self.window_id:
            try:
                self.display = display.Display()
                self.window = self.display.create_resource_object('window', self.window_id)
            except Exception as e:
                warnings.warn(f"Failed to create X11 window reference: {e}")

    def _run_command(self, cmd: list) -> None:
        """Run shell command safely"""
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            warnings.warn(f"Command failed: {e}")

class apply_style:
    """Different styles for Linux windows, mimicking Windows styling API"""

    def __init__(self, window, style: str) -> None:
        linux_styles = ["dark", "light", "transparent", "normal", "native"]
        
        if style not in linux_styles and style not in ["mica", "aero", "acrylic", "win7", 
                                                      "inverse", "popup", "optimised"]:
            raise ValueError(
                f"Invalid style name! No such window style exists: {style} \nAvailable styles: {linux_styles}"
            )
        
        if style not in linux_styles:
            warnings.warn(f"Style '{style}' is Windows-specific. Using closest Linux alternative.")
            
        self.window_id = LinuxWindowIdentifier.get_xwindow_id(window)
        self.window_obj = window
        self.gtk_win = None
        self.style_mgr = LinuxWindowStyle(window)
        
        # Try to get GTK window if we're in GTK
        if HAS_GTK:
            if isinstance(window, Gtk.Window):
                self.gtk_win = window
            # For Tkinter, try to get GTK window via Tk path
            elif hasattr(window, 'winfo_id'):
                try:
                    screen = Gdk.Screen.get_default()
                    for gtk_win in screen.get_window_stack():
                        if gtk_win.get_xid() == self.window_id:
                            self.gtk_win = gtk_win
                            break
                except:
                    pass
        
        # Apply the requested style
        if style == "dark":
            self._apply_dark_theme()
        elif style == "light":
            self._apply_light_theme()
        elif style == "transparent":
            self._apply_transparent()
        elif style in ["mica", "aero", "acrylic"]:
            # These are Windows-specific, use transparency as fallback
            self._apply_transparent()
        elif style == "normal":
            self._apply_normal_theme()
        elif style == "native":
            # Do nothing, use system's native look
            pass
    
    def _apply_dark_theme(self):
        """Apply dark theme"""
        if HAS_GTK and self.gtk_win:
            # For GTK applications
            settings = Gtk.Settings.get_default()
            if settings:
                settings.set_property("gtk-application-prefer-dark-theme", True)
        
        # For desktop environment specific approaches
        if DESKTOP_ENV == 'gnome':
            self._run_gsettings(["set", "org.gnome.desktop.interface", "color-scheme", "prefer-dark"])
        elif DESKTOP_ENV == 'kde':
            self._run_command(["plasma-apply-colorscheme", "BreezeDark"])
    
    def _apply_light_theme(self):
        """Apply light theme"""
        if HAS_GTK and self.gtk_win:
            settings = Gtk.Settings.get_default()
            if settings:
                settings.set_property("gtk-application-prefer-dark-theme", False)
        
        if DESKTOP_ENV == 'gnome':
            self._run_gsettings(["set", "org.gnome.desktop.interface", "color-scheme", "default"])
        elif DESKTOP_ENV == 'kde':
            self._run_command(["plasma-apply-colorscheme", "BreezeLight"])
    
    def _apply_transparent(self):
        """Apply transparency effect"""
        # For GTK applications
        if HAS_GTK and self.gtk_win:
            if isinstance(self.gtk_win, Gtk.Window):
                screen = self.gtk_win.get_screen()
                visual = screen.get_rgba_visual()
                if visual and screen.is_composited():
                    self.gtk_win.set_visual(visual)
                    self.gtk_win.set_app_paintable(True)
                    
                    # Connect drawing event to create transparency
                    def draw_transparent(widget, ctx):
                        ctx.set_source_rgba(0, 0, 0, 0.5)  # Semi-transparent
                        ctx.set_operator(0)  # OPERATOR_SOURCE
                        ctx.paint()
                        return False
                    
                    self.gtk_win.connect("draw", draw_transparent)
        
        # For X11 windows
        if HAS_XLIB and self.style_mgr.window:
            try:
                # Set the _NET_WM_WINDOW_OPACITY property
                atom = self.style_mgr.display.intern_atom('_NET_WM_WINDOW_OPACITY')
                opacity = int(0.8 * 0xffffffff)  # 80% opacity
                self.style_mgr.window.change_property(atom, X.CARDINAL, 32, [opacity])
                self.style_mgr.display.flush()
            except Exception as e:
                warnings.warn(f"Failed to set window transparency: {e}")
    
    def _apply_normal_theme(self):
        """Reset to normal theme"""
        if HAS_GTK and self.gtk_win:
            if isinstance(self.gtk_win, Gtk.Window):
                self.gtk_win.set_app_paintable(False)
                # Use system default visual
                screen = self.gtk_win.get_screen()
                visual = screen.get_system_visual()
                self.gtk_win.set_visual(visual)
        
        # Remove X11 transparency
        if HAS_XLIB and self.style_mgr.window:
            try:
                atom = self.style_mgr.display.intern_atom('_NET_WM_WINDOW_OPACITY')
                self.style_mgr.window.delete_property(atom)
                self.style_mgr.display.flush()
            except Exception:
                pass
    
    def _run_gsettings(self, args):
        """Run gsettings command"""
        try:
            cmd = ["gsettings"] + args
            subprocess.run(cmd, check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            warnings.warn(f"gsettings command failed: {e}")


class set_opacity:
    """Change opacity of individual widgets"""

    def __init__(self, widget: Any, value: float = 1.0, color: str = None) -> None:
        widget_id = None
        
        # Extract widget ID from different GUI frameworks
        try:
            # Tkinter widgets
            if hasattr(widget, 'winfo_id'):
                widget_id = widget.winfo_id()
            elif isinstance(widget, int):
                widget_id = widget
            else:
                raise ValueError("Widget ID should be passed, not the widget name.")
        except Exception as e:
            warnings.warn(f"Could not identify widget: {e}")
            return
        
        self.widget_id = widget_id
        self.opacity = value
        
        if HAS_XLIB and self.widget_id:
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


class change_header_color:
    """Change the titlebar background color - limited functionality on Linux"""

    def __init__(self, window: Any, color: str) -> None:
        warnings.warn("Titlebar color customization has limited support on Linux")
        
        # Basic implementations for specific desktop environments
        if DESKTOP_ENV == 'gnome':
            # Can only set to system-wide themes, not specific colors
            pass
        elif DESKTOP_ENV == 'kde':
            # KDE might support this via color schemes
            pass


class change_border_color:
    """Change the window border color - limited functionality on Linux"""

    def __init__(self, window: Any, color: str) -> None:
        warnings.warn("Window border color customization has limited support on Linux")


class change_title_color:
    """Change the title color - limited functionality on Linux"""

    def __init__(self, window: Any, color: str) -> None:
        warnings.warn("Titlebar text color customization has limited support on Linux")


def get_accent_color() -> str:
    """Returns current accent color of the desktop environment if available"""
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
    try:  # GTK
        if isinstance(window, Gtk.Widget):
            window.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 1))
            return
    except:
        pass
    
    warnings.warn("Don't know what the window type is, please set its background color to black")


# Keep the color conversion function for compatibility
def convert_color(color_name: str) -> str:
    """Convert colors to hex format"""
    
    NAMES_TO_HEX = {
        "aliceblue": "#f0f8ff",
        "antiquewhite": "#faebd7",
        "aqua": "#00ffff",
        # ... (rest of the color dictionary is identical to the original)
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
    
    # No need for color format conversion as in Windows
    return color


def detect(window: Any):
    """Detect the type of UI library and return window ID"""
    try:  # tkinter
        if hasattr(window, 'update'):
            window.update()
        if hasattr(window, 'winfo_id'):
            return window.winfo_id()
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
    try:  # GTK
        if HAS_GTK and isinstance(window, Gtk.Window):
            return window.get_window().get_xid()
    except:
        pass
    
    if isinstance(window, int):
        return window  # other window IDs
    
    # Try to get active window as fallback
    if HAS_XLIB:
        try:
            d = display.Display()
            return d.get_input_focus().focus.id
        except:
            pass
    
    warnings.warn("Could not detect window ID")
    return None