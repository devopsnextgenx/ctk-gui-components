import os
import sys

# Add src directory to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_path)

import pytest
import ttkbootstrap as ttk
from devopsnextgenx.components.StatusBar import StatusBar

@pytest.fixture
def status_bar():
    """Fixture to create a fresh StatusBar instance for each test"""
    root = ttk.Window()
    status_bar = StatusBar(root)
    return status_bar

def test_status_bar_creation(status_bar):
    """Test the creation of a StatusBar object"""
    assert isinstance(status_bar, StatusBar)

def test_status_bar_progress(status_bar):
    """Test the progress method of StatusBar"""
    status_bar.update_status("Progressing...")
    assert status_bar.progress_label.cget("text") == "Progressing..."
    status_bar.update_status("Progressing...!!!", 0.5)
    assert status_bar.progress_label.cget("text") == "Progressing...!!!"
    assert status_bar.progress_bar.cget("value") == 50

def test_status_bar_reset(status_bar):
    """Test the reset method of StatusBar"""
    status_bar.update_status("Ready", 0.5)
    status_bar.reset()
    assert status_bar.progress_label.cget("text") == "Ready"
    assert status_bar.progress_bar.cget("value") == 0

def test_status_bar_initial_display(status_bar):
    """Test the initial display method of StatusBar"""
    status_bar.on_initial_display()
    assert status_bar.user_label.cget("width") == 5
    assert status_bar.access_label.cget("width") == 2
    assert status_bar.progress_bar.cget("length") == 100

def test_status_bar_complete(status_bar):
    """Test the complete StatusBar object"""
    status_bar.update_status("Ready", 1)
    assert status_bar.progress_label.cget("text") == "Ready"
    assert status_bar.progress_bar.cget("value") == 100

def test_status_bar_resize(status_bar):
    """Test the resize method of StatusBar"""
    # Test with None event (initial sizing)
    status_bar.on_resize(None)
    assert status_bar.user_label.cget("width") == 5  # Minimum width
    assert status_bar.access_label.cget("width") == 2  # Minimum width
    assert status_bar.progress_bar.cget("length") == 100  # Minimum length

    # Create mock event with specific width
    class MockEvent:
        def __init__(self, width):
            self.width = width

    # Test with wider window (800px)
    wide_event = MockEvent(800)
    status_bar.on_resize(wide_event)
    
    # Calculate expected values based on the StatusBar's ratio calculations
    usable_width = 800 * 0.95  # 95% of total width
    total_ratio = status_bar.total_width
    
    expected_user_width = max(5, int((status_bar.user_width_ratio/total_ratio) * usable_width / 10))
    expected_access_width = max(2, int((status_bar.access_width_ratio/total_ratio) * usable_width / 10))
    expected_progress_width = max(100, int((status_bar.progress_width_ratio/total_ratio) * usable_width))

    assert status_bar.user_label.cget("width") == expected_user_width
    assert status_bar.access_label.cget("width") == expected_access_width
    assert status_bar.progress_bar.cget("length") == expected_progress_width

    # Test with narrow window (300px)
    narrow_event = MockEvent(300)
    status_bar.on_resize(narrow_event)
    
    # Should maintain minimum values for narrow window
    assert status_bar.user_label.cget("width") == 5
    assert status_bar.access_label.cget("width") == 2
    assert status_bar.progress_bar.cget("length") == 100