[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=devopsnextgenx_ctk-gui-components&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=devopsnextgenx_ctk-gui-components) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=devopsnextgenx_ctk-gui-components&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=devopsnextgenx_ctk-gui-components)

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
- pytest-cov

## Test and Coverage
```bash
pytest tests/devopsnextgenx/utils/test_style.py
pytest tests/devopsnextgenx/utils/test_style.py::test_change_title_color_initialization
pytest --cov=src --cov-report=term-missing
```

## Demo

Run the included demo to see all components in action:

```bash
python tests/demo.py

ffmpeg -i input.webm demo.gif

```

![demo.gif](https://raw.githubusercontent.com/devopsnextgenx/ctk-gui-components/refs/heads/main/docs/imgs/demo.gif)


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

### MessageHub Components

#### Alert Example

```python
import customtkinter as ctk
from devopsnextgenx.components.messageHub import Alert

app = ctk.CTk()

def show_alert():
    alert = Alert(state="info", title="Information", body_text="This is an alert message.", btn1="OK", btn2="Cancel")
    alert.get()

button = ctk.CTkButton(app, text="Show Alert", command=show_alert)
button.pack(pady=20)

app.mainloop()
```

#### Banner Example

```python
import customtkinter as ctk
from devopsnextgenx.components.messageHub import Banner

app = ctk.CTk()

banner = Banner(master=app, state="info", title="Information", btn1="Action 1", btn2="Action 2", side="right_bottom")
banner.pack(pady=20)

app.mainloop()
```

#### Notification Example

```python
import customtkinter as ctk
from devopsnextgenx.components.messageHub import Notification

app = ctk.CTk()

notification = Notification(master=app, state="info", message="This is a notification.", side="right_bottom")
notification.pack(pady=20)

app.mainloop()
```

### Carousel Component

A customizable carousel widget that displays a series of images.

#### Carousel Example

```python
import customtkinter as ctk
from devopsnextgenx.components import Carousel, image_list_provider

app = ctk.CTk()

# Provide a list of image paths
image_paths = image_list_provider("path/to/images", imgOptions={"imgPrefix":"image", "suffix":"png", "start":1, "end":5})

carousel = Carousel(app, img_radius=25, img_list=image_paths)
carousel.pack(pady=20)

app.mainloop()
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



        # Create a canvas and a scrollbar
        canvas = ctk.CTkCanvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.pack(fill="both", expand=True)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="both")

        # Create main frame inside the scrollable frame
        # main_frame = ttk.Frame(scrollable_frame, style="TFrame", padding=10)
        # self.style.configure("TFrame", background="#343A40")
        # main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        options = ["Alert", "Banner", "Notification", "Carousel"]
        option = ctk.CTkOptionMenu(scrollable_frame, values=options, width=200, command=toggle_widgets)
        option.pack(pady=20)
        option.set("None")

        # Add some demo buttons
        ttk.Button(
            scrollable_frame, 
            text="Start Process", 
            command=self.simulate_process,
            bootstyle="primary"
        ).pack(pady=10)

        ttk.Button(
            scrollable_frame, 
            text="Reset Status", 
            command=self.reset_status,
            bootstyle="secondary"
        ).pack(pady=10)

        # Add carousel to display images
        self.carouselFrame = ttk.Frame(scrollable_frame)
        self.carouselFrame.pack(fill="both", expand=True, pady=10)
        CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
        ICON_DIR = os.path.join(CURRENT_PATH, "imgs", "carousel")
        imgList = image_list_provider(ICON_DIR, imgOptions = {"imgPrefix":"sun", "suffix":"png", "start":1, "end":15})
        self.carousel = Carousel(self.carouselFrame, img_radius=5, img_list = imgList)
        self.carousel.grid(padx=20, pady=20)
        
        # Add table for user info
        self.add_user_info_table(scrollable_frame)
