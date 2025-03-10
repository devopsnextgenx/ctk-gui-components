import tkinter as tk
from ttkbootstrap import Style, Frame, Scrollbar

class ScrollFrame(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Create a canvas and a vertical scrollbar with custom style
        self.canvas = tk.Canvas(self)
        
        # Define custom style for the scrollbar
        style = Style()
        style.configure("Custom.Vertical.TScrollbar", 
                        troughcolor="gray", 
                        background="black", 
                        arrowcolor="white", 
                        bordercolor="black", 
                        lightcolor="black", 
                        darkcolor="black")

        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview, style="Custom.Vertical.TScrollbar")
        self.scrollable_frame = Frame(self.canvas)

        # Configure scrollable frame to resize with canvas
        self.scrollable_frame.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Bind canvas resize to adjust scrollable frame width
        self.canvas.bind("<Configure>", 
            lambda e: self.canvas.itemconfig(
                "all",  # Update all canvas items (only the scrollable_frame window)
                width=e.width
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.winfo_width())
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def get_scrollable_frame(self):
        return self.scrollable_frame