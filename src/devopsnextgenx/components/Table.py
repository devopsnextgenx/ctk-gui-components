import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from typing import List, Any, Optional, Callable
from pydantic import BaseModel
from enum import Enum
from tkinter import BooleanVar

class WidgetType(Enum):
    TEXT = "TEXT"
    CHECKBOX = "CHECKBOX"
    SQTOGGLE = "SQTOGGLE"
    RNDTOGGLE = "RNDTOGGLE"
    RADIOBTN = "RADIOBTN"
    ENTRY = "ENTRY"
    BUTTON = "BUTTON"

class Header(BaseModel):
    """
    Represents a table header configuration.
    text: str - The header text
    type: WidgetType - The widget type for the column
    - TEXT: Default text label
    - CHECKBOX: Checkbox
    - SQTOGGLE: Square toggle switch
    - RNDTOGGLE: Round toggle switch
    - RADIOBTN: Radio button
    - ENTRY: Text entry
    - BUTTON: Button
    text_color: str - Text color (default: white)
    fg_color: str - Foreground color (default: dark)
    bg_color: str - Background color (default: None)
    font_size: int - Font size (default: 14)
    weight: int - Column weight (default: 0)
    align: str - Text alignment (default: left)
    editable: bool - Whether the column is editable (default: False)
    style: Optional[str] - Custom style for the widget (default: None)
    colNo: Optional[int] - Column number (default: None)
    action: Optional[Callable] - Action callback for header click (default: None)
    on_change: Optional[Callable] - On change callback for cell value change (default: None)
    """
    text: str
    type: WidgetType = WidgetType.TEXT
    text_color: str = None
    fg_color: str = None
    bg_color: str = None
    font_size: int = 14
    weight: int = 0
    align: str = "left"
    editable: bool = False
    style: Optional[str] = None
    colNo: Optional[int] = None
    action: Optional[Callable] = None
    on_change: Optional[Callable] = None

class Table(ttk.Frame):
    """
    A table widget that displays data in rows and columns.
    master: any - The parent widget
    headers: List[Header] - List of table headers
    data: List[List[Any]] - List of data rows
    row_height: int - Row height (default: 30)
    header_color: str - Header color (default: primary)
    row_color: str - Row color (default: dark)
    alternate_row_color: str - Alternate row color (default: secondary)
    highlight_color: str - Highlight color (default: info)
    hover_color: str - Hover color (default: #404040)
    """
    def __init__(
        self,
        master: any,
        headers: List[Header],
        data: List[List[Any]],
        row_height: int = 30,
        header_color: str = "primary",
        row_color: str = "dark",
        alternate_row_color: str = "secondary",
        highlight_color: str = "info",
        hover_color: str = "#404040",  # Add hover color parameter
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        self.headers = headers
        self.data = data
        self.row_height = row_height
        self.header_color = header_color
        self.row_color = row_color
        self.alternate_row_color = alternate_row_color
        self.highlight_color = highlight_color
        self.hover_color = hover_color  # Store hover color
        self._sort_ascending = {}
        self.selected_row = None
        self.selected_cell = None
        self._cells = {}

        # Define custom styles
        style = ttk.Style()
        
        # Configure header style
        style.configure(
            "Header.TLabel",
            background="#00008B",  # Dark blue
            foreground="white",
            padding=5,
            anchor="center",
            font=("TkDefaultFont", 10, "bold")
        )
        
        # Configure row styles
        style.configure("Row.TLabel", padding=5)
        style.configure("Alt.TLabel", padding=5)
        
        # Use ttk built-in styles instead of creating custom ones
        # ttkbootstrap already has predefined styles we can use:
        # - For checks: primary.TCheckbutton, secondary.TCheckbutton, etc.
        # - For toggles: primary-toggle.Toolbutton, round-toggle.Toolbutton, etc.
        
        self._create_table()

    def _get_header_text(self, header: Header) -> str:
        """Get header text with sort indicator if applicable"""
        if not header.action:
            return header.text
            
        if header.colNo not in self._sort_ascending:
            return f"{header.text} ↕"
        
        return f"{header.text} {'↑' if self._sort_ascending[header.colNo] else '↓'}"

    def _create_table(self):
        # Create headers
        for col, header in enumerate(self.headers):
            header_label = ttk.Label(
                self,
                text=self._get_header_text(header),
                style="Header.TLabel",
                anchor="center",
                font=("TkDefaultFont", 10, "bold")
            )
            header.colNo = col
            
            # Add click binding if header has action
            if header.action:
                header_label.bind("<Button-1>", lambda e, h=header: self._handle_header_click(h))
                header_label.configure(cursor="hand2")  # Change cursor to hand when hoverable
                
            header_label.grid(row=0, column=col, padx=1, pady=1, sticky="nsew")
            self.grid_columnconfigure(col, weight=header.weight)
        
        # Create data rows
        for row_idx, row_data in enumerate(self.data, start=1):
            bg_color = self.alternate_row_color if row_idx % 2 == 0 else self.row_color
            
            for col_idx, cell_data in enumerate(row_data):
                bg_color = self.alternate_row_color if row_idx % 2 == 0 else self.row_color
                
                cell_widget = self._create_cell_widget(
                    row_idx, 
                    col_idx, 
                    cell_data, 
                    self.headers[col_idx],
                    bg_color
                )
                
                # Store cell reference
                self._cells[(row_idx, col_idx)] = cell_widget
                
                # Bind events (only for TEXT widgets, others handle events differently)
                if self.headers[col_idx].type == WidgetType.TEXT:
                    cell_widget.bind("<Button-1>", lambda e, r=row_idx, c=col_idx: self._handle_cell_click(r, c))
                    if self.headers[col_idx].editable:
                        cell_widget.bind("<Double-Button-1>", lambda e, r=row_idx, c=col_idx: self._make_cell_editable(r, c))
                
                cell_widget.grid(row=row_idx, column=col_idx, padx=1, pady=1, sticky="nsew")

    def _create_cell_widget(self, row_idx, col_idx, cell_data, header, bg_color):
        fg_color = "dark"
        text_color = header.text_color if header.text_color is not None else "white"
        fg_color = header.fg_color if header.fg_color is not None else fg_color
        bg_color = header.bg_color if header.bg_color is not None else bg_color
        
        # Handle alignment
        anchor = "w"
        match header.align.lower():
            case "w":
                anchor = "w"
            case "left":
                anchor = "w"
            case "e":
                anchor = "e"
            case "right":
                anchor = "e"
            case "center":
                anchor = "center"
            case _:
                anchor = "w"  # default to left alignment
                
        # Determine cell widget type based on header.type
        match header.type:
            case WidgetType.TEXT:
                # Text is the default type - uses Label
                cell_widget = ttk.Label(
                    self,
                    text=str(cell_data),
                    style="Row.TLabel" if row_idx % 2 == 0 else "Alt.TLabel",
                    anchor=anchor
                )
                
            case WidgetType.CHECKBOX:
                # Create checkbox widget
                var = BooleanVar()
                cell_widget = ttk.Checkbutton(
                    self,
                    text="",
                    # Fix: Use a standard ttkbootstrap style instead of a custom one
                    style="success.TCheckbutton",
                    variable=var
                )
                
                # Set initial value
                if isinstance(cell_data, bool):
                    var.set(cell_data)
                elif isinstance(cell_data, (int, float)):
                    var.set(bool(cell_data))
                elif isinstance(cell_data, str) and cell_data.lower() in ('true', 'yes', '1'):
                    var.set(True)
                else:
                    var.set(False)
                
                # Store the BooleanVar reference
                cell_widget.var = var
                
                # Add event handling
                cell_widget.configure(command=lambda r=row_idx-1, c=col_idx, cb=cell_widget: 
                    self._handle_checkbox_change(r, c, cb))
                
            case WidgetType.SQTOGGLE:
                # Create toggle/switch widget
                var = BooleanVar()
                # Fix: Use standard ttkbootstrap style for toggles
                cell_widget = ttk.Checkbutton(
                    self,
                    text="",
                    style="primary-square-toggle.Toolbutton",  # Use Toolbutton style class which supports toggles
                    variable=var
                )
                
                # Set initial value
                if isinstance(cell_data, bool):
                    var.set(cell_data)
                elif isinstance(cell_data, (int, float)):
                    var.set(bool(cell_data))
                elif isinstance(cell_data, str) and cell_data.lower() in ('true', 'yes', '1'):
                    var.set(True)
                else:
                    var.set(False)
                
                # Store the BooleanVar reference
                cell_widget.var = var
                
                # Add event handling
                cell_widget.configure(command=lambda r=row_idx-1, c=col_idx, sw=cell_widget: 
                    self._handle_toggle_change(r, c, sw))
                
            case WidgetType.RNDTOGGLE:
                # Create toggle/switch widget
                var = BooleanVar()
                # Fix: Use standard ttkbootstrap style for round toggles
                cell_widget = ttk.Checkbutton(
                    self,
                    text="",
                    style="primary-round-toggle.Toolbutton",  # Use Toolbutton style class with round-toggle 
                    variable=var
                )
                
                # Set initial value
                if isinstance(cell_data, bool):
                    var.set(cell_data)
                elif isinstance(cell_data, (int, float)):
                    var.set(bool(cell_data))
                elif isinstance(cell_data, str) and cell_data.lower() in ('true', 'yes', '1'):
                    var.set(True)
                else:
                    var.set(False)
                
                # Store the BooleanVar reference
                cell_widget.var = var
                
                # Add event handling
                cell_widget.configure(command=lambda r=row_idx-1, c=col_idx, sw=cell_widget: 
                    self._handle_toggle_change(r, c, sw))
                
            case WidgetType.RADIOBTN:
                # Create radio button widget
                var = BooleanVar()
                cell_widget = ttk.Radiobutton(
                    self,
                    text="",
                    style="primary.TRadiobutton",
                    variable=var
                )
                
                # Set initial value
                if isinstance(cell_data, bool):
                    var.set(cell_data)
                elif isinstance(cell_data, (int, float)):
                    var.set(bool(cell_data))
                elif isinstance(cell_data, str) and cell_data.lower() in ('true', 'yes', '1'):
                    var.set(True)
                else:
                    var.set(False)
                
                # Store the BooleanVar reference
                cell_widget.var = var
                
                # Add event handling
                cell_widget.configure(command=lambda r=row_idx-1, c=col_idx, sw=cell_widget: 
                    self._handle_toggle_change(r, c, sw))
                
            case WidgetType.ENTRY:
                # Create entry widget
                cell_widget = ttk.Entry(
                    self,
                    # Fix: Use standard ttkbootstrap styles
                    style="primary.TEntry",
                )
                
                # Set initial value
                cell_widget.insert(0, str(cell_data))
                
                # Enable/disable based on editable
                if not header.editable:
                    cell_widget.configure(state="readonly")
                
                # Add event handling
                if header.editable:
                    cell_widget.bind("<FocusOut>", lambda e, r=row_idx-1, c=col_idx, entry=cell_widget: 
                        self._handle_entry_change(r, c, entry))
                    cell_widget.bind("<Return>", lambda e, r=row_idx-1, c=col_idx, entry=cell_widget: 
                        self._handle_entry_change(r, c, entry))
                
            case WidgetType.BUTTON:
                # Create button widget
                cell_widget = ttk.Button(
                    self,
                    text=str(cell_data),
                    style=header.style if header.style is not None else "primary.TButton",
                )
                
                # Add event handling
                cell_widget.configure(command=lambda r=row_idx-1, c=col_idx: 
                    self._handle_button_click(r, c))
                
            case _:
                # Default to text if unknown widget type
                cell_widget = ttk.Label(
                    self,
                    text=str(cell_data),
                    style="Row.TLabel" if row_idx % 2 == 0 else "Alt.TLabel",
                    anchor=anchor
                )
        
        return cell_widget

    def _handle_checkbox_change(self, row: int, col: int, checkbox):
        """Handle checkbox value change"""
        # Update data
        new_value = checkbox.var.get()
        self.data[row][col] = new_value
        
        # Trigger on_change callback if exists
        if self.headers[col].on_change:
            self.headers[col].on_change(self.data, row, col)

    def _handle_toggle_change(self, row: int, col: int, switch):
        """Handle toggle/switch value change"""
        # Update data
        new_value = switch.var.get()
        self.data[row][col] = new_value
        
        # Trigger on_change callback if exists
        if self.headers[col].on_change:
            self.headers[col].on_change(self.data, row, col)

    def _handle_entry_change(self, row: int, col: int, entry):
        """Handle entry value change"""
        # Update data
        new_value = entry.get()
        self.data[row][col] = new_value
        
        # Trigger on_change callback if exists
        if self.headers[col].on_change:
            self.headers[col].on_change(self.data, row, col)

    def _handle_button_click(self, row: int, col: int):
        """Handle button click"""
        # For buttons, we just trigger the on_change callback
        if self.headers[col].on_change:
            self.headers[col].on_change(self.data, row, col)

    def update_data(self, new_data: List[List[Any]]):
        """Update table with new data"""
        # Clear existing data cells
        for widget in self.winfo_children():
            widget.destroy()
            
        self.data = new_data
        self._create_table()

    def _handle_header_click(self, header: Header):
        """Handle header click events"""
        if header.action:
            # Toggle ascending/descending
            if not hasattr(self, '_sort_ascending'):
                self._sort_ascending = {}
            self._sort_ascending[header.colNo] = not self._sort_ascending.get(header.colNo, True)
            header.action(self._sort_ascending[header.colNo])

    def _handle_cell_click(self, row: int, col: int):
        """Handle cell click for selection"""
        # Reset previous selections
        if self.selected_row:
            self._update_row_colors(self.selected_row)
        if self.selected_cell:
            self._update_cell_color(*self.selected_cell)

        # Update new selections
        self.selected_row = row
        self.selected_cell = (row, col)
        
        # Highlight selected row
        for c in range(len(self.headers)):
            cell = self._cells.get((row, c))
            if cell and hasattr(cell, 'configure') and callable(getattr(cell, 'configure')):
                if self.headers[c].type == WidgetType.TEXT:
                    cell.configure(style="info.TLabel")
        
        # Extra highlight for selected cell
        selected_cell = self._cells.get((row, col))
        if selected_cell and hasattr(selected_cell, 'configure') and callable(getattr(selected_cell, 'configure')):
            if self.headers[col].type == WidgetType.TEXT:
                selected_cell.configure(style="info.TLabel")

    def _make_cell_editable(self, row: int, col: int):
        """Make cell editable on double click (for TEXT type only)"""
        if not self.headers[col].editable or self.headers[col].type != WidgetType.TEXT:
            return
            
        cell = self._cells.get((row, col))
        if not cell:
            return
            
        current_text = cell.cget("text")
        
        # Create entry widget
        entry = ttk.Entry(self)
        entry.insert(0, current_text)
        entry.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
        entry.focus_set()
        
        def save_changes(event=None):
            new_value = entry.get()
            self.data[row-1][col] = new_value
            cell.configure(text=new_value)
            entry.destroy()
            
            # Trigger on_change callback if exists
            if self.headers[col].on_change:
                self.headers[col].on_change(self.data, row-1, col)
        
        entry.bind("<Return>", save_changes)
        entry.bind("<FocusOut>", save_changes)

    def _update_row_colors(self, row: int):
        """Reset row colors to default"""
        bg_color = self.alternate_row_color if row % 2 == 0 else self.row_color
        for col in range(len(self.headers)):
            cell = self._cells.get((row, col))
            if cell and hasattr(cell, 'configure') and callable(getattr(cell, 'configure')):
                if self.headers[col].type == WidgetType.TEXT:
                    cell.configure(style="Row.TLabel" if row % 2 == 0 else "Alt.TLabel")

    def _update_cell_color(self, row: int, col: int):
        """Reset cell color to match its row"""
        cell = self._cells.get((row, col))
        if cell and hasattr(cell, 'configure') and callable(getattr(cell, 'configure')):
            bg_color = self.alternate_row_color if row % 2 == 0 else self.row_color
            if self.headers[col].type == WidgetType.TEXT:
                cell.configure(style="Row.TLabel" if row % 2 == 0 else "Alt.TLabel")

    def _lighten_color(self, color: str, factor: float = 1.2) -> str:
        """Lighten a hex color"""
        # Convert hex to RGB
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        
        # Lighten
        rgb = tuple(min(int(c * factor), 255) for c in rgb)
        
        # Convert back to hex
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

    def _handle_row_enter(self, row: int):
        """Handle mouse enter event for row hover effect"""
        if row != self.selected_row:  # Don't apply hover to selected row
            for col in range(len(self.headers)):
                cell = self._cells.get((row, col))
                if cell and hasattr(cell, 'configure'):
                    if self.headers[col].type == WidgetType.TEXT:
                        cell.configure(background=self.hover_color)

    def _handle_row_leave(self, row: int):
        """Handle mouse leave event to restore original row color"""
        if row != self.selected_row:  # Don't remove highlight from selected row
            self._update_row_colors(row)