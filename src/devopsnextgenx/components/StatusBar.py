import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class StatusBar(ttk.Frame):
    def __init__(
        self,
        master=None,
        height=30,
        **kwargs
    ):
        super().__init__(master, height=height, **kwargs)
        
        # Define the ratios
        access_width_ratio = 0
        user_width_ratio = 1
        progress_width_ratio = 1
        label_width_ratio = 5
        
        total_width = label_width_ratio + user_width_ratio + access_width_ratio + progress_width_ratio
        
        self.progress_label = ttk.Label(
            self,
            text="Ready",
            anchor="w",
            padding=(10, 0),
            width=int((label_width_ratio/total_width) * self.winfo_width()),
            bootstyle="inverse-dark"
        )
        self.progress_label.pack(side="left", fill="both", expand=True, padx=(0, 2))
        
        self.user_label = ttk.Label(
            self,
            text="User",
            width=int((user_width_ratio/total_width) * self.winfo_width()),
            bootstyle="inverse-dark"
        )
        self.user_label.pack(side="left", padx=(0, 2))
        
        self.access_label = ttk.Label(
            self,
            text="RW",
            width=int((access_width_ratio/total_width) * self.winfo_width()),
            bootstyle="inverse-dark"
        )
        self.access_label.pack(side="left", padx=(0, 2))
        
        self.progress_bar = ttk.Progressbar(
            self,
            mode="determinate",
            bootstyle="success-striped",
            length=int((progress_width_ratio/total_width) * self.winfo_width())
        )
        self.progress_bar.pack(side="left", padx=(5, 10))
        self.progress_bar["value"] = 0
        
        # Bind resize event to update widget widths
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        """Update widget widths when frame is resized"""
        # Recalculate widget widths based on ratios
        access_width_ratio = 1
        user_width_ratio = 3
        progress_width_ratio = 5
        label_width_ratio = 15
        total_width = label_width_ratio + user_width_ratio + access_width_ratio + progress_width_ratio
        
        frame_width = event.width
        
        # Update widget widths
        self.progress_label.configure(width=int((label_width_ratio/total_width) * frame_width * 0.9))
        self.user_label.configure(width=int((user_width_ratio/total_width) * frame_width * 0.9))
        self.access_label.configure(width=int((access_width_ratio/total_width) * frame_width * 0.9))
        self.progress_bar.configure(length=int((progress_width_ratio/total_width) * frame_width * 0.9))

    def update_status(self, text, progress=None):
        """Update status text and progress bar value.
        
        Args:
            text (str): Status text to display
            progress (float): Progress value between 0 and 1 (optional)
        """
        self.progress_label.configure(text=text)
        if progress is not None:
            self.progress_bar["value"] = progress * 100

    def update_user(self, user):
        """Update the user label.
        
        Args:
            user (str): User name to display
        """
        self.user_label.configure(text=user)
    
    def update_access(self, access):
        """Update the access label.
        
        Args:
            access (str): Access permissions to display
        """
        self.access_label.configure(text=access)

    def reset(self):
        """Reset the status bar to initial state."""
        self.progress_label.configure(text="Ready")
        self.progress_bar["value"] = 0


if __name__ == "__main__":
    app = ttk.Window(themename="darkly")
    app.title("StatusBar Demo")
    app.geometry("800x400")
    
    main_frame = ttk.Frame(app)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Add status bar at the bottom
    app.status_bar = StatusBar(app)
    app.status_bar.pack(fill="x", side="bottom", padx=10, pady=5)
    
    # Add a test button to show updating status
    test_button = ttk.Button(
        main_frame, 
        text="Test Status Update", 
        command=lambda: app.status_bar.update_status("Processing...", 0.75)
    )
    test_button.pack(pady=20)
    
    app.mainloop()