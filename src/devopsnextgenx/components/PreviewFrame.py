import ttkbootstrap as ttk

class PreviewFrame(ttk.Frame):
    def __init__(self, master, previewSide, width=300):
        super().__init__(master)
        self.previewSide = previewSide

        # Create a container frame to hold both canvas and scrollbar
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Configure preview frame scrollable
        self.preview_canvas = ttk.Canvas(self.container)
        self.preview_scrollbar = ttk.Scrollbar(self.container, orient="vertical", 
                                              command=self.preview_canvas.yview)
        
        # Pack scrollbar to the right edge of container
        self.preview_scrollbar.pack(side="right", fill="y")
        
        # Pack canvas to fill the remaining space
        self.preview_canvas.pack(side="left", fill="both", expand=True)
        
        # Configure canvas to use scrollbar
        self.preview_canvas.configure(yscrollcommand=self.preview_scrollbar.set)
        
        # Create inner frame for content
        self.preview_inner_frame = ttk.Frame(self.preview_canvas)
        self.preview_canvas.create_window((0, 0), window=self.preview_inner_frame, anchor="nw")
        
        # Update scroll region when inner frame size changes
        self.preview_inner_frame.bind("<Configure>", 
                                     lambda e: self.preview_canvas.configure(
                                         scrollregion=self.preview_canvas.bbox("all")))

    def update_preview(self, item_data):
        """Update preview frame with selected item data"""
        # Clear existing widgets
        for widget in self.preview_inner_frame.winfo_children():
            widget.destroy()

        # Add new data labels
        for key, value in item_data.items():
            ttk.Label(self.preview_inner_frame, text=f"{key}: {value}").pack(anchor="w")

        # Position the frame according to previewSide
        if self.previewSide == 'top':
            self.grid(row=0, column=0, columnspan=2, sticky="nsew")
        elif self.previewSide == 'bottom':
            self.grid(row=2, column=0, columnspan=2, sticky="nsew")
        elif self.previewSide == 'left':
            self.grid(row=1, column=0, sticky="nsew")
        elif self.previewSide == 'right':
            self.grid(row=1, column=1, sticky="nsew")