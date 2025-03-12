import ttkbootstrap as ttk
from PIL import Image, ImageTk
from devopsnextgenx.utils.iconProvider import ICON_PATH

class Treeview(ttk.Frame):
    def __init__(self, master: any, items, key: str = 'name', style="darkly"):
        super().__init__(master)
        
        self.key = key
        self.items = items
        self.style = ttk.Style()
        
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

        # Header styling
        self.header = ttk.Label(
            self,
            text="Treeview",
            style="primary.Inverse.TLabel",
            font=("TkDefaultFont", 16)
        )
        self.header.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Setup tree icons
        self.im_open = Image.open(ICON_PATH["arrow"])
        self.im_close = self.im_open.rotate(90)
        self.im_empty = Image.new('RGBA', (15, 15), (0, 0, 0, 0))

        self.img_open = ImageTk.PhotoImage(self.im_open, size=(15, 15))
        self.img_close = ImageTk.PhotoImage(self.im_close, size=(15, 15))
        self.img_empty = ImageTk.PhotoImage(self.im_empty, size=(15, 15))

        # Create custom tree indicator elements
        self.style.element_create(
            'CustomTreeitem.indicator',  # Using a unique name here
            'image',
            self.img_close,
            ('user1', '!user2', self.img_open),
            ('user2', self.img_empty),
            sticky='w',
            width=15,
            height=15
        )

        # Configure tree layout
        self.style.layout(
            'Treeview.Item',
            [
                ('Treeitem.padding',
                {'sticky': 'nsew',
                'children': [
                    ('CustomTreeitem.indicator', {'side': 'left', 'sticky': 'nsew'}),  # Updated here
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

        # Create treeview widget
        self.treeview = ttk.Treeview(
            self,
            show="tree",
            style="primary.Treeview"
        )
        self.treeview.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        
        # Insert items
        self.insert_items(self.items)

        # Bind selection event
        self.treeview.bind("<<TreeviewSelect>>", self._handle_selection)

    def insert_items(self, items, parent=''):
        """Insert items into treeview"""
        for item in items:
            if isinstance(item, dict) and 'children' in item:
                item_id = self.treeview.insert(parent, 'end', text=item[self.key])
                self.insert_items(item['children'], item_id)
            else:
                self.treeview.insert(parent, 'end', text=item[self.key])

    def _handle_selection(self, event):
        """Handle tree item selection"""
        self.focus_set()
