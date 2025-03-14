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
        self.start_x = 0
        self.start_tree_size = 0
        self.total_size = 0
        
        # Configure treeview style
        self.style.configure("Treeview", background="#2a2d2e", foreground="white", fieldbackground="#2a2d2e", borderwidth=0, font=("TkDefaultFont", 10))
        self.style.map("Treeview", background=[("selected", "#404040")], foreground=[("selected", "#00bc8c")])

        # Divider style
        self.style.configure("Divider.TFrame", background="#777777")
        self.style.map("Divider.TFrame", background=[("active", "#999999")])

        # Tree icons
        self.im_open = Image.open(ICON_PATH["arrow"])
        self.im_close = self.im_open.rotate(90)
        self.im_empty = Image.new('RGBA', (15, 15), (0, 0, 0, 0))
        self.img_open = ImageTk.PhotoImage(self.im_open, size=(15, 15))
        self.img_close = ImageTk.PhotoImage(self.im_close, size=(15, 15))
        self.img_empty = ImageTk.PhotoImage(self.im_empty, size=(15, 15))

        self.style.configure("Treeview", indent=15)
        self.style.layout('Treeview.Item', [
            ('Treeitem.padding', {'sticky': 'nsew', 'children': [
                ('CustomTreeitem.indicator', {'side': 'left', 'sticky': 'nsew'}),
                ('Treeitem.image', {'side': 'left', 'sticky': 'nsew'}),
                ('Treeitem.focus', {'side': 'left', 'sticky': 'nsew', 'children': [
                    ('Treeitem.text', {'side': 'left', 'sticky': 'nsew'})
                ]})
            ]})
        ])

        # Create divider
        if self.previewSide in [PreviewSide.LEFT, PreviewSide.RIGHT]:
            self.divider = ttk.Frame(self, width=5, cursor="sb_h_double_arrow", style="Divider.TFrame")
        else:
            self.divider = ttk.Frame(self, height=5, cursor="sb_v_double_arrow", style="Divider.TFrame")

        # Create containers
        self.tree_container = ttk.Frame(self)
        self.preview_container = ttk.Frame(self)

        # Treeview setup
        self.treeview = ttk.Treeview(self.tree_container, show="tree", style="primary.Treeview")
        self.treeview.tag_configure("leaf", image=self.img_empty)
        self.treeview.tag_configure("open", image=self.img_open)
        self.treeview.tag_configure("closed", image=self.img_close)
        
        self.scrollbar = ttk.Scrollbar(self.tree_container, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        
        self.treeview.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree_container.grid_columnconfigure(0, weight=1)
        self.tree_container.grid_rowconfigure(0, weight=1)

        # Preview frame
        self.preview_frame = PreviewFrame(self.preview_container, self.previewSide)
        self.preview_frame.pack(fill="both", expand=True)

        # Layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        if self.previewSide in [PreviewSide.LEFT, PreviewSide.RIGHT]:
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=0)
            self.grid_columnconfigure(2, weight=1)
            if self.previewSide == PreviewSide.LEFT:
                self.preview_container.grid(row=0, column=0, sticky="nsew")
                self.divider.grid(row=0, column=1, sticky="ns")
                self.tree_container.grid(row=0, column=2, sticky="nsew")
            else:  # RIGHT
                self.tree_container.grid(row=0, column=0, sticky="nsew")
                self.divider.grid(row=0, column=1, sticky="ns")
                self.preview_container.grid(row=0, column=2, sticky="nsew")
        else:  # TOP or BOTTOM
            self.grid_rowconfigure(0, weight=1)
            self.grid_rowconfigure(1, weight=0)
            self.grid_rowconfigure(2, weight=1)
            if self.previewSide == PreviewSide.TOP:
                self.preview_container.grid(row=0, column=0, sticky="nsew")
                self.divider.grid(row=1, column=0, sticky="ew")
                self.tree_container.grid(row=2, column=0, sticky="nsew")
            else:  # BOTTOM
                self.tree_container.grid(row=0, column=0, sticky="nsew")
                self.divider.grid(row=1, column=0, sticky="ew")
                self.preview_container.grid(row=2, column=0, sticky="nsew")

        # Insert items
        self.insert_items(self.items)

        # Bind events
        self.treeview.bind("<<TreeviewSelect>>", self._handle_selection)
        self.divider.bind("<ButtonPress-1>", self._on_divider_press)
        self.divider.bind("<ButtonRelease-1>", self._on_divider_release)
        self.divider.bind("<B1-Motion>", self._on_divider_motion)
        self.treeview.bind("<MouseWheel>", self._on_mouse_wheel)
        self.treeview.bind("<Button-4>", self._on_mouse_wheel)
        self.treeview.bind("<Button-5>", self._on_mouse_wheel)

        # Bottom resizer
        self.resizer = ttk.Frame(self, height=8, cursor="sb_v_double_arrow")
        self.resizer.grid(row=3 if self.previewSide in [PreviewSide.TOP, PreviewSide.BOTTOM] else 1, 
                         column=0, sticky="ew", columnspan=3 if self.previewSide in [PreviewSide.LEFT, PreviewSide.RIGHT] else 1)
        self.resizer.configure(style="Resizer.TFrame")
        self.style.configure("Resizer.TFrame", background="#777777")
        self.style.map("Resizer.TFrame", background=[("active", "#999999")])
        
        self.resizer.bind("<Enter>", self._on_resizer_enter)
        self.resizer.bind("<Leave>", self._on_resizer_leave)
        self.resizer.bind("<ButtonPress-1>", self._on_resizer_press)
        self.resizer.bind("<ButtonRelease-1>", self._on_resizer_release)
        self.resizer.bind("<B1-Motion>", self._on_resizer_motion)
        
        self.grid_rowconfigure(3 if self.previewSide in [PreviewSide.TOP, PreviewSide.BOTTOM] else 1, weight=0)

        # Initial sizing
        self.update_idletasks()  # Ensure geometry is calculated
        self._set_initial_sizes()

    def _set_initial_sizes(self):
        """Set initial sizes for containers"""
        if self.previewSide in [PreviewSide.LEFT, PreviewSide.RIGHT]:
            total_width = self.winfo_width()
            if total_width <= 0:  # If not yet realized, use a default
                total_width = 600
            half_width = (total_width - 5) // 2  # 5 is divider width
            self.tree_container.configure(width=half_width)
            self.preview_container.configure(width=half_width)
        else:
            total_height = self.winfo_height()
            if total_height <= 0:  # If not yet realized, use a default
                total_height = self.height
            half_height = (total_height - 5) // 2  # 5 is divider height
            self.tree_container.configure(height=half_height)
            self.preview_container.configure(height=half_height)

    def insert_items(self, items, parent=''):
        for item in items:
            item['open'] = False
            if isinstance(item, dict) and 'children' in item and item['children']:
                item_id = self.treeview.insert(parent, 'end', text=item[self.key], tags=["closed"])
                self.insert_items(item['children'], item_id)
            else:
                self.treeview.insert(parent, 'end', text=item[self.key], tags=["leaf"])

    def _find_item(self, items, key, value):
        for item in items:
            if item.get(key) == value:
                return item
            if 'children' in item:
                found = self._find_item(item['children'], key, value)
                if found:
                    return found
        return None
    
    def _handle_selection(self, event):
        selected_items = self.treeview.selection()
        if selected_items:
            selected_item = selected_items[0]
            item_data = self.treeview.item(selected_item)
            item_name = item_data['text']
            item = self._find_item(self.items, self.key, item_name)
            is_leaf = not (isinstance(item, dict) and 'children' in item and item['children'])
            
            if not is_leaf:
                current_open_state = self.treeview.item(selected_item, 'open')
                self.treeview.item(selected_item, open=not current_open_state)
                if not current_open_state:
                    self.treeview.item(selected_item, tags=["open"])
                else:
                    self.treeview.item(selected_item, tags=["closed"])
                if item:
                    item['open'] = not current_open_state
            else:
                self.treeview.item(selected_item, tags=["leaf"])
            
            if item:
                self.preview_frame.update_preview(item)

    def _on_mouse_wheel(self, event):
        if event.num == 5 or event.delta < 0:
            self.treeview.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.treeview.yview_scroll(-1, "units")
        return "break"
    
    def _on_resizer_enter(self, event):
        self.resizer.configure(style="ResizerHover.TFrame")
        self.style.configure("ResizerHover.TFrame", background="#999999")
    
    def _on_resizer_leave(self, event):
        if not self.resizing:
            self.resizer.configure(style="Resizer.TFrame")
    
    def _on_resizer_press(self, event):
        self.resizing = True
        self.start_y = event.y_root
        self.start_height = self.winfo_height()
        self.resizer.configure(style="ResizerActive.TFrame")
        self.style.configure("ResizerActive.TFrame", background="#00bc8c")
    
    def _on_resizer_release(self, event):
        self.resizing = False
        self.resizer.configure(style="Resizer.TFrame")
    
    def _on_resizer_motion(self, event):
        if self.resizing:
            delta_y = event.y_root - self.start_y
            new_height = max(100, self.start_height + delta_y)
            self.height = new_height
            self.configure(height=new_height)
            self._set_initial_sizes()  # Recompute container sizes
            self.update_idletasks()

    def _on_divider_press(self, event):
        self.resizing = True
        self.start_y = event.y_root
        self.start_x = event.x_root
        if self.previewSide in [PreviewSide.LEFT, PreviewSide.RIGHT]:
            self.start_tree_size = self.tree_container.winfo_width()
            self.total_size = self.winfo_width()
        else:
            self.start_tree_size = self.tree_container.winfo_height()
            self.total_size = self.winfo_height()
        self.divider.configure(style="DividerActive.TFrame")
        self.style.configure("DividerActive.TFrame", background="#00bc8c")
        self.update_idletasks()  # Ensure sizes are current

    def _on_divider_release(self, event):
        self.resizing = False
        self.divider.configure(style="Divider.TFrame")

    def _on_divider_motion(self, event):
        if not self.resizing:
            return
        
        min_size = 100  # Minimum size for each container
        divider_size = 5
        
        if self.previewSide in [PreviewSide.LEFT, PreviewSide.RIGHT]:
            delta_x = event.x_root - self.start_x
            if self.previewSide == PreviewSide.LEFT:
                new_preview_width = max(min_size, min(self.total_size - min_size - divider_size, self.start_tree_size - delta_x))
                new_tree_width = self.total_size - new_preview_width - divider_size
            else:  # RIGHT
                new_tree_width = max(min_size, min(self.total_size - min_size - divider_size, self.start_tree_size + delta_x))
                new_preview_width = self.total_size - new_tree_width - divider_size
            
            # Apply sizes directly
            self.preview_container.configure(width=new_preview_width)
            self.tree_container.configure(width=new_tree_width)
            self.preview_container.grid_columnconfigure(0, weight=0)
            self.tree_container.grid_columnconfigure(0, weight=0)
        
        else:  # TOP or BOTTOM
            delta_y = event.y_root - self.start_y
            if self.previewSide == PreviewSide.TOP:
                new_preview_height = max(min_size, min(self.total_size - min_size - divider_size, self.start_tree_size - delta_y))
                new_tree_height = self.total_size - new_preview_height - divider_size
            else:  # BOTTOM
                new_tree_height = max(min_size, min(self.total_size - min_size - divider_size, self.start_tree_size + delta_y))
                new_preview_height = self.total_size - new_tree_height - divider_size
            
            # Apply sizes directly
            self.preview_container.configure(height=new_preview_height)
            self.tree_container.configure(height=new_tree_height)
            self.preview_container.grid_rowconfigure(0, weight=0)
            self.tree_container.grid_rowconfigure(0, weight=0)
        
        # Minimize flickering by batching updates
        self.update_idletasks()
