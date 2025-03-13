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

        # Create custom tree indicator elements - FIX: Swap the image assignments to match open/close states
        self.style.configure("Treeview", indent=15)
        # Create custom tree indicator elements - FIXED: Proper image assignments for open/close states
        # self.style.element_create(
        #     'CustomTreeitem.indicator',
        #     'image',
        #     self.img_close,  # Default (collapsed)
        #     ('open', self.img_open),  # When expanded - arrow pointing down
        #     ('!open', self.img_close),  # When collapsed - arrow pointing right
        #     sticky='w',
        #     width=15,
        #     height=15
        # )

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
            self.paned_window = ttk.PanedWindow(self, orient="horizontal")
        else:
            self.paned_window = ttk.PanedWindow(self, orient="vertical")
        
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

        # Set the initial sash position (divider) to be in the middle
        # This is done after the widget is fully created and visible
        self.after(100, self._set_initial_sash_position)

        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Insert items
        self.insert_items(self.items)

        # Bind selection event
        self.treeview.bind("<<TreeviewSelect>>", self._handle_selection)

    def _set_initial_sash_position(self):
        """Set the initial sash position after widget is visible"""
        try:
            self.update_idletasks()  # Ensure layout calculations are complete

            if self.previewSide in [PreviewSide.LEFT, PreviewSide.RIGHT]:
                total_width = self.paned_window.winfo_width()
                if total_width > 0:  # Ensure valid width
                    print(f"Total Width: {total_width}")  # Debugging
                    self.paned_window.sashpos(0, total_width // 2)
                else:
                    self.after(100, self._set_initial_sash_position)  # Retry later
                    return
            else:
                total_height = self.paned_window.winfo_height()
                if total_height > 0:  # Ensure valid height
                    print(f"Total Height: {total_height}")  # Debugging
                    self.paned_window.sashpos(0, total_height // 2)
                else:
                    self.after(100, self._set_initial_sash_position)  # Retry later
                    return

        except Exception as e:
            print(f"Error setting sash position: {e}")  # Print error for debugging
            self.after(100, self._set_initial_sash_position)  # Retry later

    def insert_items(self, items, parent=''):
        """Insert items into treeview and start in a closed state"""
        for item in items:
            item['open'] = False
            if isinstance(item, dict) and 'children' in item:
                item_id = self.treeview.insert(parent, 'end', text=item[self.key], tags=["closed"])
                self.insert_items(item['children'], item_id)
            else:
                self.treeview.insert(parent, 'end', text=item[self.key])

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
            
            # Toggle the item's open state in the treeview
            current_open_state = self.treeview.item(selected_item, 'open')
            self.treeview.item(selected_item, open=not current_open_state)
            
            # Update tags based on the new state
            if not current_open_state:  # Will be opened
                self.treeview.item(selected_item, tags=["open"])
            else:  # Will be closed
                self.treeview.item(selected_item, tags=["closed"])
            
            # Find and update the corresponding data item
            item = self._find_item(self.items, self.key, item_name)
            if item:
                item['open'] = not current_open_state
                self.preview_frame.update_preview(item)