# DevOpsNextGenX GUI Components

A collection of modern, customizable GUI components built with ttkbootstrap for Python desktop applications.

## Installation

```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.x
- customtkinter
- ttkbootstrap
- pydantic

## Demo

Run the included demo to see all components in action:

```bash
python src/demo.py
```

![demo.gif](https://github.com/devopsnextgenx/ctk-gui-components/blob/main/docs/imgs/demo.gif)


## Features

### StatusBar Component
A responsive status bar widget that includes:
- Status text display with progress bar
- User information display
- Access rights indicator
- Progress bar with percentage
- Auto-resizing capabilities

### StatusBar Example

```python
import ttkbootstrap as ttk
from devopsnextgenx.components import StatusBar

app = ttk.Window()

# Create status bar with custom height and progress bar thickness
status_bar = StatusBar(
    app,
    height=30,               # Custom height
    progress_thickness=3     # Thin progress bar
)
status_bar.pack(fill="x", side="bottom", padx=10, pady=5)

# Update status with text and progress
status_bar.update_status("Processing...", 0.5)  # 50% progress

# Reset status bar
status_bar.reset()  # Returns to "Ready" state with 0% progress
```

### Table Component
A feature-rich table widget offering:
- Customizable headers with multiple column types
- Support for different widget types per column:
  - TEXT: Regular text display
  - CHECKBOX: Boolean value selector
  - SQTOGGLE: Square toggle switch
  - RNDTOGGLE: Round toggle switch
  - ENTRY: Editable text field
  - BUTTON: Clickable button
- Sortable columns
- Row selection and highlighting
- Cell editing capabilities
- Custom styling options
- Responsive layout

### Table Example

```python
import ttkbootstrap as ttk
from devopsnextgenx.components import Table, Header, WidgetType

app = ttk.Window()

# Define headers with advanced options
headers = [
    Header(
        text="ID",
        editable=False,
        type=WidgetType.TEXT,
        align="left"
    ),
    Header(
        text="Name",
        editable=True,
        type=WidgetType.ENTRY,
        weight=1,
        text_color="white",
        font_size=14,
        on_change=lambda data, row, col: print(f"Changed: {data[row][col]}")
    ),
    Header(
        text="Active",
        type=WidgetType.RNDTOGGLE,
        align="center",
        weight=1,
        fg_color="#2a2d2e",
        bg_color="#000000"
    ),
    Header(
        text="Actions",
        type=WidgetType.BUTTON,
        align="center",
        weight=1,
        style="primary"
    )
]

# Sample data
data = [
    [1, "John Doe", True, "Edit"],
    [2, "Jane Smith", False, "Edit"]
]

# Create table with custom styling
table = Table(
    app,
    headers=headers,
    data=data,
    row_height=30,
    header_color="primary",
    row_color="dark",
    alternate_row_color="secondary",
    highlight_color="info",
    hover_color="#404040"
)
table.pack(fill="both", expand=True)
```

## Customization

Both components support extensive customization through their constructor parameters and methods:

- Colors and themes
- Sizes and proportions
- Event callbacks
- Visual styles

## Build and Publish
```bash
pip install setuptools wheel
python setup.py sdist bdist_wheel
pip install twine
twine upload dist/*
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```

## License

[LICENSE](https://github.com/devopsnextgenx/ctk-gui-components/blob/main/LICENSE.md)