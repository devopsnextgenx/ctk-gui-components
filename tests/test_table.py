import os
import sys

# Add src directory to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_path)

import pytest
import ttkbootstrap as ttk
from devopsnextgenx.components.Table import Table, Header, WidgetType

@pytest.fixture
def table():
    """Fixture to create a fresh Table instance for each test"""
    root = ttk.Window()
    
    headers = [
        Header(text="Text Column", type=WidgetType.TEXT, editable=True),
        Header(text="Checkbox", type=WidgetType.CHECKBOX),
        Header(text="Square Toggle", type=WidgetType.SQTOGGLE),
        Header(text="Round Toggle", type=WidgetType.RNDTOGGLE),
        Header(text="Radio", type=WidgetType.RADIOBTN),
        Header(text="Entry", type=WidgetType.ENTRY, editable=True),
        Header(text="Button", type=WidgetType.BUTTON)
    ]
    
    data = [
        ["Row 1", True, False, True, False, "Entry 1", "Click Me"],
        ["Row 2", False, True, False, True, "Entry 2", "Press Me"]
    ]
    
    table = Table(root, headers=headers, data=data)
    return table

def test_table_creation(table):
    """Test the creation of a Table object"""
    assert isinstance(table, Table)
    assert len(table.headers) == 7
    assert len(table.data) == 2

def test_header_types(table):
    """Test that headers have correct widget types"""
    assert isinstance(table, Table)
    assert table.headers[0].type == WidgetType.TEXT
    assert table.headers[1].type == WidgetType.CHECKBOX
    assert table.headers[2].type == WidgetType.SQTOGGLE
    assert table.headers[3].type == WidgetType.RNDTOGGLE
    assert table.headers[4].type == WidgetType.RADIOBTN
    assert table.headers[5].type == WidgetType.ENTRY
    assert table.headers[6].type == WidgetType.BUTTON

def test_update_data(table):
    """Test updating table data"""
    new_data = [
        ["New Row 1", True, False, True, False, "New Entry 1", "New Button 1"],
        ["New Row 2", False, True, False, True, "New Entry 2", "New Button 2"],
        ["New Row 3", True, True, False, False, "New Entry 3", "New Button 3"]
    ]
    table.update_data(new_data)
    assert len(table.data) == 3
    assert table.data[0][0] == "New Row 1"

def test_cell_selection(table):
    """Test cell selection functionality"""
    table._handle_cell_click(1, 0)
    assert table.selected_row == 1
    assert table.selected_cell == (1, 0)

def test_editable_cells(table):
    """Test editable cell functionality"""
    # Test TEXT type cell
    assert table.headers[0].editable == True
    # Test ENTRY type cell
    assert table.headers[5].editable == True

# Test uncommented as it should now work with fixed implementation
def test_checkbox_cell_change(table):
    """Test checkbox cell value change"""
    cell = table._cells.get((1, 1))  # Get first checkbox cell
    initial_value = table.data[0][1]
    cell.invoke()  # Simulate checkbox click
    assert table.data[0][1] != initial_value

# Test uncommented as it should now work with fixed implementation
def test_toggle_cell_change(table):
    """Test toggle cell value change"""
    cell = table._cells.get((1, 2))  # Get first toggle cell
    initial_value = table.data[0][2]
    cell.invoke()  # Simulate toggle click
    assert table.data[0][2] != initial_value

def test_entry_cell_content(table):
    """Test entry cell content"""
    cell = table._cells.get((1, 5))  # Get first entry cell
    assert cell.get() == "Entry 1"

def test_button_cell_exists(table):
    """Test button cell creation"""
    cell = table._cells.get((1, 6))  # Get first button cell
    assert isinstance(cell, ttk.Button)
    assert cell.cget("text") == "Click Me"

def test_header_click_sorting(table):
    """Test header click sorting functionality"""
    def sort_function(ascending):
        # Sort the table data based on the first column
        table.data.sort(key=lambda row: row[0], reverse=not ascending)
    
    table.headers[0].action = sort_function
    table._handle_header_click(table.headers[0])
    assert table._sort_ascending[0] == False
    assert table.data[0][0] == "Row 2"  # Assuming initial data is sorted ascending
    table._handle_header_click(table.headers[0])
    assert table._sort_ascending[0] == True
    assert table.data[0][0] == "Row 1"  # Assuming initial data is sorted ascending

# Test uncommented as it should now work with fixed implementation
def test_widget_styles(table):
    """Test that widgets have correct styles applied"""
    # Test checkbox style
    checkbox_cell = table._cells.get((1, 1))
    assert isinstance(checkbox_cell, ttk.Checkbutton)
    
    # Test toggle styles
    sq_toggle_cell = table._cells.get((1, 2))
    assert isinstance(sq_toggle_cell, ttk.Checkbutton)
    
    rnd_toggle_cell = table._cells.get((1, 3))
    assert isinstance(rnd_toggle_cell, ttk.Checkbutton)