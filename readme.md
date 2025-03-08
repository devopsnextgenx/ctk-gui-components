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

![demo.gif](./docs/imgs/demo.gif)


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
status_bar = StatusBar(app)
status_bar.pack(fill="x", side="bottom")

# Update status
status_bar.update_status("Processing...", 0.5)  # 50% progress
status_bar.update_user("Admin")
status_bar.update_access("RW")

# Reset status
status_bar.reset()
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

# Define headers
headers = [
    Header(text="ID", editable=False),
    Header(text="Name", editable=True, weight=1),
    Header(
        text="Active",
        type=WidgetType.RNDTOGGLE,
        align="center",
        weight=1
    )
]

# Sample data
data = [
    [1, "John Doe", True],
    [2, "Jane Smith", False]
]

# Create table
table = Table(app, headers=headers, data=data)
table.pack(fill="both", expand=True)
```

## Customization

Both components support extensive customization through their constructor parameters and methods:

- Colors and themes
- Sizes and proportions
- Event callbacks
- Visual styles

## License

[Add your license information here]