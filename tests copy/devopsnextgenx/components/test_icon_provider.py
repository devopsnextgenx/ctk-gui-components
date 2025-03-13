import os
import sys

# Add src directory to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))
sys.path.append(src_path)

import pytest
from devopsnextgenx.utils import list_icons, get_icon_path
from collections.abc import dict_keys
def test_list_icons():
    """Test the list_icons function"""
    icons = list_icons()
    assert isinstance(icons, dict_keys)
    assert "close" in icons
    assert "images" in icons
    assert "eye1" in icons
    assert "info" in icons

def test_get_icon_path_dark_theme():
    """Test get_icon_path function with dark theme"""
    assert get_icon_path("close", "dark") == os.path.join("icons", "close_black.png")
    assert get_icon_path("eye1", "dark") == os.path.join("icons", "eye1_black.png")
    assert get_icon_path("info", "dark") == os.path.join("icons", "info.png")

def test_get_icon_path_light_theme():
    """Test get_icon_path function with light theme"""
    assert get_icon_path("close", "light") == os.path.join("icons", "close_white.png")
    assert get_icon_path("eye1", "light") == os.path.join("icons", "eye1_white.png")

def test_get_icon_path_no_theme():
    """Test get_icon_path function with no theme specified"""
    assert get_icon_path("info") == os.path.join("icons", "info.png")
    assert get_icon_path("warning") == os.path.join("icons", "warning.png")

def test_get_icon_path_invalid_icon():
    """Test get_icon_path function with invalid icon name"""
    assert get_icon_path("nonexistent") is None