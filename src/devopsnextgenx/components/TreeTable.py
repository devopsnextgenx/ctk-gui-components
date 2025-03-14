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
        self.resizing = False
        self.start_y = 0
        self.start_height = self.height
        
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

        # Custom style for the paned window divider (sash)
        self.style.configure("CustomPane.TPanedwindow", background="#555555", sashwidth=5, sashpad=1)
        self.style.map("CustomPane.TPanedwindow", 
                       background=[("active", "#00bc8c"), ("hover", "#999999")],
                       sashrelief=[("active", "sunken")])
        
        # Set hover cursor for paned window sash
        self.style.element_create("CustomSash", "from", "default")
        if self.previewSide in [PreviewSide.LEFT, PreviewSide.RIGHT]:
            self.style.configure("CustomPane.TPanedwindow", sashcursor="sb_h_double_arrow")
        else:
            self.style.configure("CustomPane.TPanedwindow", sashcursor="sb_v_double_arrow")

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
        self.tree_container = ttk.Frame(self.paned_window, style="CustomPane.TPanedwindow")
        self.preview_container = ttk.Frame(self.paned_window, style="CustomPane.TPanedwindow")

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
        # self.tree_container.pack_configure(padx=5, pady=5)
        # Prevent the container from changing size
        self.tree_container.pack_propagate(False)

        # Create preview frame inside its container
        if self.previewSide in [PreviewSide.LEFT, PreviewSide.RIGHT]:
            self.preview_frame = PreviewFrame(self.preview_container, self.previewSide)
        else:
            self.preview_frame = PreviewFrame(self.preview_container, self.previewSide)
        
        # self.preview_container.pack_configure(padx=5, pady=5)
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
        
        # Create a resizer frame at the bottom
        self.resizer = ttk.Frame(self, height=8, cursor="sb_v_double_arrow")
        self.resizer.grid(row=2, column=0, sticky="ew")
        self.resizer.configure(style="Resizer.TFrame")
        
        # Create a custom style for the resizer
        self.style.configure("Resizer.TFrame", background="#777777")
        self.style.map("Resizer.TFrame", background=[("active", "#999999")])
        
        # Bind events for resizing
        self.resizer.bind("<Enter>", self._on_resizer_enter)
        self.resizer.bind("<Leave>", self._on_resizer_leave)
        self.resizer.bind("<ButtonPress-1>", self._on_resizer_press)
        self.resizer.bind("<ButtonRelease-1>", self._on_resizer_release)
        self.resizer.bind("<B1-Motion>", self._on_resizer_motion)
        
        # Update grid weight for resizer row
        self.grid_rowconfigure(2, weight=0)

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
    
    def _on_resizer_enter(self, event):
        """Visual feedback when mouse enters the resizer area"""
        self.resizer.configure(style="ResizerHover.TFrame")
        self.style.configure("ResizerHover.TFrame", background="#999999")
    
    def _on_resizer_leave(self, event):
        """Reset visual feedback when mouse leaves the resizer area"""
        if not self.resizing:
            self.resizer.configure(style="Resizer.TFrame")
    
    def _on_resizer_press(self, event):
        """Start the resizing operation"""
        self.resizing = True
        self.start_y = event.y_root
        self.start_height = self.winfo_height()
        self.resizer.configure(style="ResizerActive.TFrame")
        self.style.configure("ResizerActive.TFrame", background="#00bc8c")
    
    def _on_resizer_release(self, event):
        """End the resizing operation"""
        self.resizing = False
        self.resizer.configure(style="Resizer.TFrame")
    
    def _on_resizer_motion(self, event):
        """Handle resizing during mouse motion"""
        if self.resizing:
            # Calculate new height
            delta_y = event.y_root - self.start_y
            new_height = max(100, self.start_height + delta_y)  # Minimum height of 100px
            
            # Update the height of the component
            self.height = new_height
            self.configure(height=new_height)
            
            # Update the height of the paned window to match
            self.paned_window.configure(height=new_height - 28)  # Adjust for padding and resizer
            
            # Update the tree container's height
            self.tree_container.configure(height=new_height - 28)
            
            # Force update of layout
            self.update_idletasks()