import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import customtkinter as ctk

class StatusBar(ttk.Frame):
    """
    A custom status bar with a progress bar.
    master: Parent widget
    height: Height of the status bar
    progress_thickness: Thickness of the progress bar
    """
    def __init__(
        self,
        master=None,
        height=30,
        progress_thickness=3,  # Set default to a thin strip
        **kwargs
    ):
        super().__init__(master, height=height, **kwargs)
        
        self.progress_thickness = progress_thickness
        
        self.label_width_ratio = 15
        self.user_width_ratio = 3
        self.access_width_ratio = 1
        self.progress_width_ratio = 5
        self.total_width = (self.label_width_ratio + self.user_width_ratio +
                            self.access_width_ratio + self.progress_width_ratio)
        
        self.progress_label = ttk.Label(
            self,
            text="Ready",
            anchor="w",
            padding=(10, 0),
            # bootstyle="inverse-dark"
        )
        self.progress_label.pack(side="left", fill="both", expand=True, padx=(0, 2))
        
        self.user_label = ttk.Label(self,
            text="User", 
            # bootstyle="inverse-dark"
        )
        self.user_label.pack(side="left", fill="y", padx=(0, 2))
        
        self.access_label = ttk.Label(self,
            text="RW",
            # bootstyle="inverse-dark"
        )
        self.access_label.pack(side="left", fill="y", padx=(0, 2))
        
        self.progress_frame = ttk.Frame(self, height=self.progress_thickness, bootstyle="dark")
        self.progress_frame.pack(side="left", fill="x", expand=True, padx=(5, 10), pady=(10, 10))
        style = ttk.Style()
        style.configure(
            "Custom.Horizontal.TProgressbar",
            thickness=self.progress_thickness,
            troughcolor="#333333",
            background="#007BFF",
            troughrelief="flat",
        )
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode="determinate",
            bootstyle=(PRIMARY, STRIPED),
            style="Custom.Horizontal.TProgressbar",
            length=100,  
        )
        self.progress_bar["value"] = 0

        self.progress_bar.pack(fill="x", expand=False)
        
        self.bind("<Configure>", self.on_resize)
        self.update_idletasks()
        self.on_initial_display()

    def on_initial_display(self):
        self.on_resize(None)

    def on_resize(self, event):
        frame_width = self.winfo_width() if event is None else event.width
        usable_width = frame_width * 0.95
        
        self.user_label.configure(width=max(5, int((self.user_width_ratio/self.total_width) * usable_width / 10)))
        self.access_label.configure(width=max(2, int((self.access_width_ratio/self.total_width) * usable_width / 10)))
        
        progress_width = max(100, int((self.progress_width_ratio/self.total_width) * usable_width))
        self.progress_bar.configure(length=progress_width)

    def update_status(self, text, progress=None):
        """
        Update the status bar with a new message and progress.
        text: New status message
        progress: Progress value between 0 and 1
        """
        self.progress_label.configure(text=text)
        if progress is not None:
            self.progress_bar["value"] = progress * 100
            self.progress_bar.update_idletasks()

    def reset(self):
        """Reset the status bar to its initial state."""
        self.progress_label.configure(text="Ready")
        self.progress_bar["value"] = 0


if __name__ == "__main__":
    app = ttk.Window(themename="darkly")
    app.title("StatusBar Demo")
    app.geometry("800x400")
    
    main_frame = ttk.Frame(app)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    test_button = ttk.Button(
        main_frame, 
        text="Test Status Update", 
        command=lambda: app.status_bar.update_status("Processing...", 0.75)
    )
    test_button.pack(pady=20)
    
    reset_button = ttk.Button(
        main_frame, 
        text="Reset Status", 
        command=lambda: app.status_bar.reset()
    )
    reset_button.pack(pady=10)
    
    app.status_bar = StatusBar(app, progress_thickness=3)  # Set thin progress bar
    app.status_bar.pack(fill="x", side="bottom", padx=10, pady=5)
    
    app.mainloop()
