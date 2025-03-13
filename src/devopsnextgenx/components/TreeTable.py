import ttkbootstrap as ttk
from PIL import Image, ImageTk
from devopsnextgenx.utils.iconProvider import ICON_PATH
from enum import Enum
from .PreviewFrame import PreviewFrame

class PreviewSide(Enum):
    TOP = 'top'
    BOTTOM = 'bottom'
    LEFT = 'left'
    RIGHT = 'right'

class Treeview(ttk.Frame):
    def __init__(self, master: any, items, previewSide: PreviewSide = PreviewSide.RIGHT, key: str = 'name', style="darkly", height: int = 300):
        super().__init__(master)
        
        self.key = key
        self.items = items
        self.style = ttk.Style()
        self.previewSide = previewSide
        self.height = height
        
        # Configure treeview style with darkly theme
        self.style.configure(
            "Treeview",
            background="#2a2d2e",
            foreground="white",
            fieldbackground="#2a2d2e",
            borderwidth=0,
            font=("TkDefaultFont", 10)
        )
        
        # Configure selection colors
        self.style.map(
            "Treeview",
            background=[("selected", "#404040")],
            foreground=[("selected", "#00bc8c")]
        )

        # Style for the sash (divider)
        self.style.configure("TPanedwindow", background="#555555", sashwidth=5, sashpad=1)
        self.style.map("TPanedwindow", background=[("active", "#777777")])

        # Setup tree icons
        self.im_open = Image.open(ICON_PATH["arrow"])
        self.im_close = self.im_open.rotate(90)
        self.im_empty = Image.new('RGBA', (15, 15), (0, 0, 0, 0))

        self.img_open = ImageTk.PhotoImage(self.im_open, size=(15, 15))
        self.img_close = ImageTk.PhotoImage(self.im_close, size=(15, 15))
        self.img_empty = ImageTk.PhotoImage(self.im_empty, size=(15, 15))

        # Create custom tree indicator elements
        self.style.configure("Treeview", indent=15)

        # Configure tree layout
        self.style.layout(
            'Treeview.Item',
            [
                ('Treeitem.padding',
                {'sticky': 'nsew',
                'children': [
                    ('CustomTreeitem.indicator', {'side': 'left', 'sticky': 'nsew'}),
                    ('Treeitem.image', {'side': 'left', 'sticky': 'nsew'}),
                    ('Treeitem.focus',
                    {'side': 'left',
                        'sticky': 'nsew',
                        'children': [
                            ('Treeitem.text', {'side': 'left', 'sticky': 'nsew'})
                        ]})
                ]})
            ]
        )

        # Create a PanedWindow with proper orientation based on previewSide
        if self.previewSide in [PreviewSide.LEFT, PreviewSide.RIGHT]:
            self.paned_window = ttk.PanedWindow(self, orient="horizontal", height=self.height)
        else:
            self.paned_window = ttk.PanedWindow(self, orient="vertical", height=self.height)
        
        self.paned_window.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Create frames to hold each component
        self.tree_container = ttk.Frame(self.paned_window)
        self.preview_container = ttk.Frame(self.paned_window)

        # Create treeview widget inside its container
        self.treeview = ttk.Treeview(
            self.tree_container,
            show="tree",
            style="primary.Treeview",
        )
        
        self.treeview.tag_configure("leaf", image=self.img_empty)
        self.treeview.tag_configure("open", image=self.img_open)
        self.treeview.tag_configure("closed", image=self.img_close)
        # Set up scrollbar for treeview
        self.scrollbar = ttk.Scrollbar(self.tree_container, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        
        # Grid layout with scrollbar
        self.treeview.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure grid weights for tree_container
        self.tree_container.grid_columnconfigure(0, weight=1)
        self.tree_container.grid_rowconfigure(0, weight=1)
        
        # Explicitly set the height of tree_container (in pixels)
        self.tree_container.configure(height=self.height)
        # Prevent the container from changing size
        self.tree_container.pack_propagate(False)

        # Create preview frame inside its container
        if self.previewSide in [PreviewSide.LEFT, PreviewSide.RIGHT]:
            self.preview_frame = PreviewFrame(self.preview_container, self.previewSide)
        else:
            self.preview_frame = PreviewFrame(self.preview_container, self.previewSide)
        
        self.preview_frame.pack(fill="both", expand=True)

        # Add containers to paned window based on previewSide
        if self.previewSide == PreviewSide.LEFT or self.previewSide == PreviewSide.TOP:
            self.paned_window.add(self.preview_container, weight=1)
            self.paned_window.add(self.tree_container, weight=1)
        elif self.previewSide == PreviewSide.RIGHT or self.previewSide == PreviewSide.BOTTOM:
            self.paned_window.add(self.tree_container, weight=1)
            self.paned_window.add(self.preview_container, weight=1)

        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Insert items
        self.insert_items(self.items)

        # Bind selection event
        self.treeview.bind("<<TreeviewSelect>>", self._handle_selection)

        # Bind mouse wheel events for scrolling
        self.treeview.bind("<MouseWheel>", self._on_mouse_wheel)
        self.treeview.bind("<Button-4>", self._on_mouse_wheel)  # For Linux
        self.treeview.bind("<Button-5>", self._on_mouse_wheel)  # For Linux

    def insert_items(self, items, parent=''):
        """Insert items into treeview and start in a closed state"""
        for item in items:
            item['open'] = False
            
            if isinstance(item, dict) and 'children' in item and item['children']:
                # Insert parent node with proper tag
                item_id = self.treeview.insert(parent, 'end', text=item[self.key], tags=["closed"])
                # Insert children recursively
                self.insert_items(item['children'], item_id)
            else:
                # Insert leaf node with leaf tag (no children)
                self.treeview.insert(parent, 'end', text=item[self.key], tags=["leaf"])

    def _find_item(self, items, key, value):
        """Recursively find item in nested items by key and value"""
        for item in items:
            if item.get(key) == value:
                return item
            if 'children' in item:
                found = self._find_item(item['children'], key, value)
                if found:
                    return found
        return None
    
    def _handle_selection(self, event):
        """Handle tree item selection"""
        selected_items = self.treeview.selection()
        if selected_items:
            selected_item = selected_items[0]
            item_data = self.treeview.item(selected_item)
            item_name = item_data['text']
            
            # Find the corresponding data item
            item = self._find_item(self.items, self.key, item_name)
            
            # Check if this is a leaf node (no children)
            is_leaf = not (isinstance(item, dict) and 'children' in item and item['children'])
            
            if not is_leaf:
                # Toggle the item's open state in the treeview
                current_open_state = self.treeview.item(selected_item, 'open')
                self.treeview.item(selected_item, open=not current_open_state)
                
                # Update tags based on the new state
                if not current_open_state:  # Will be opened
                    self.treeview.item(selected_item, tags=["open"])
                else:  # Will be closed
                    self.treeview.item(selected_item, tags=["closed"])
                
                # Update the corresponding data item
                if item:
                    item['open'] = not current_open_state
            else:
                # Ensure leaf nodes stay tagged as leaves
                self.treeview.item(selected_item, tags=["leaf"])
            
            # Update preview for any selected item (leaf or non-leaf)
            if item:
                self.preview_frame.update_preview(item)

    def _on_mouse_wheel(self, event):
        if event.num == 5 or event.delta < 0:
            self.treeview.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.treeview.yview_scroll(-1, "units")
        return "break"  # Prevent the event from propagating to the parent