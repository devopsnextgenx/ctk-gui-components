import os
import sys

# Add src directory to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))
sys.path.append(src_path)

import pytest
import warnings
from devopsnextgenx.utils.style import change_title_color, convert_color, apply_style
import os
import sys
import pytest
from devopsnextgenx.components.messageHub import Alert, Banner, Notification
import os
import sys
import pytest
from devopsnextgenx.utils.guiUtils import center_window, place_window_bottom_right, place_frame
import os
import sys
import pytest
from devopsnextgenx.components.Carousel import Carousel

# filepath: /home/kira/git/devopsnextgenx/ctk-gui-components/tests/test_style.py

# Add src directory to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_path)


def test_change_title_color_initialization():
    """Test the initialization of change_title_color class"""
    window = 12345  # Mock window ID
    color = "#ff0000"
    title_color = change_title_color(window, color)
    assert title_color.HWND == window

def test_change_title_color_windows():
    """Test the color conversion and application for Windows"""
    if sys.platform.startswith("win"):
        window = 12345  # Mock window ID
        color = "#ff0000"
        title_color = change_title_color(window, color)
        assert title_color.color == int(convert_color(color), 16)

def test_change_title_color_unsupported_platform():
    """Test the warning for unsupported platforms"""
    if not sys.platform.startswith("win"):
        window = 12345  # Mock window ID
        color = "#ff0000"
        with pytest.warns(UserWarning, match="Titlebar text color customization has limited support on Linux"):
            change_title_color(window, color)

def test_convert_color():
    """Test the convert_color function"""
    assert convert_color("red") == "#ff0000"
    assert convert_color("#ff0000") == "#ff0000"
    assert convert_color("grey50") == "#505050"
    with pytest.raises(ValueError):
        convert_color("invalidcolor")

def test_apply_style_windows():
    """Test the apply_style class for Windows styles"""
    if sys.platform.startswith("win"):
        window = 12345  # Mock window ID
        style = apply_style(window, "dark")
        assert style.HWND == window

def test_apply_style_linux():
    """Test the apply_style class for Linux styles"""
    if sys.platform.startswith("linux"):
        window = 12345  # Mock window ID
        style = apply_style(window, "dark")
        assert style.HWND == window

# filepath: /home/kira/git/devopsnextgenx/ctk-gui-components/tests/test_messageHub.py

# Add src directory to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_path)


def test_alert_initialization():
    """Test the initialization of Alert class"""
    alert = Alert(state="info", title="Test Alert", body_text="This is a test alert")
    assert alert.title_label.cget("text") == "  Test Alert"

def test_banner_initialization():
    """Test the initialization of Banner class"""
    banner = Banner(master=None, state="info", title="Test Banner")
    assert banner.title_label.cget("text") == "  Test Banner"

def test_notification_initialization():
    """Test the initialization of Notification class"""
    notification = Notification(master=None, state="info", message="Test Notification")
    assert notification.message_label.cget("text") == "  Test Notification"

# filepath: /home/kira/git/devopsnextgenx/ctk-gui-components/tests/test_guiUtils.py

# Add src directory to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_path)


def test_center_window():
    """Test the center_window function"""
    class MockRoot:
        def winfo_screenwidth(self):
            return 800
        def winfo_screenheight(self):
            return 600
        def geometry(self, geometry_str):
            self.geometry_str = geometry_str

    root = MockRoot()
    center_window(root, 400, 300)
    assert root.geometry_str == "400x300+200+150"

def test_place_window_bottom_right():
    """Test the place_window_bottom_right function"""
    class MockRoot:
        def update(self):
            pass
        def winfo_width(self):
            return 800
        def winfo_height(self):
            return 600
        def winfo_rootx(self):
            return 0
        def winfo_rooty(self):
            return 0

    class MockChild:
        def geometry(self, geometry_str):
            self.geometry_str = geometry_str

    root = MockRoot()
    child = MockChild()
    place_window_bottom_right(root, child, 200, 100)
    assert child.geometry_str == "200x100+580+480"

def test_place_frame():
    """Test the place_frame function"""
    class MockMaster:
        def winfo_width(self):
            return 800
        def winfo_height(self):
            return 600

    class MockFrame:
        def winfo_reqwidth(self):
            return 200
        def winfo_reqheight(self):
            return 100
        def place(self, x, y):
            self.x = x
            self.y = y

    master = MockMaster()
    frame = MockFrame()
    place_frame(master, frame, horizontal="right", vertical="bottom")
    assert frame.x == 580
    assert frame.y == 480

# filepath: /home/kira/git/devopsnextgenx/ctk-gui-components/tests/test_carousel.py

# Add src directory to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_path)


def test_carousel_initialization():
    """Test the initialization of Carousel class"""
    carousel = Carousel(master=None, img_list=["path/to/image1.png", "path/to/image2.png"])
    assert carousel.img_list == ["path/to/image1.png", "path/to/image2.png"]

def test_carousel_next_callback():
    """Test the next_callback method of Carousel class"""
    carousel = Carousel(master=None, img_list=["path/to/image1.png", "path/to/image2.png"])
    carousel.next_callback()
    assert carousel.image_index == 1

def test_carousel_previous_callback():
    """Test the previous_callback method of Carousel class"""
    carousel = Carousel(master=None, img_list=["path/to/image1.png", "path/to/image2.png"])
    carousel.previous_callback()
    assert carousel.image_index == 1