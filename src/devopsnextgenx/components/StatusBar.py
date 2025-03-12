import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import customtkinter as ctk
from devopsnextgenx.components.messageHub.provider import set_root_frame, show_alert
from devopsnextgenx.components.ProgressPopup import ProgressPopup


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
        super().__init__(master, height=height, bootstyle="dark", relief="sunken", **kwargs)
        set_root_frame(master)
        self.progress_thickness = progress_thickness
        
        self.grid_columnconfigure(1, weight=12)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=2)
        
        self.progress_label = ttk.Label(
            self,
            text="Ready",
            anchor="w",
            padding=(10, 0),
            bootstyle="inverse-dark",
            relief="sunken",  # Add bevel border
            borderwidth=2     # Set border width
        )
        self.progress_label.grid(row=0, column=1, sticky="ew", padx=(5, 2))
        
        self.user_label = ttk.Label(self,
            text="User", 
            bootstyle="inverse-dark",
            relief="sunken",  # Add bevel border
            borderwidth=2     # Set border width
        )
        self.user_label.grid(row=0, column=2, sticky="ew", padx=(5, 2))
        self.user_label.bind("<Double-1>", self.show_user_alert)  # Bind double-click event
        
        self.access_label = ttk.Label(self,
            text=" RW ",
            bootstyle="inverse-dark",
            relief="sunken",  # Add bevel border
            borderwidth=2     # Set border width
        )
        self.access_label.grid(row=0, column=3, sticky="ew", padx=(5, 2))
        self.access_label.bind("<Double-1>", self.show_access_alert)  # Bind double-click event
        
        self.progress_frame = ttk.Frame(self, height=self.progress_thickness, bootstyle="dark", relief="sunken", borderwidth=2)  # Add bevel border
        self.progress_frame.grid(row=0, column=4, sticky="ew", padx=(5, 10), pady=(8, 8))
        progressStyle = ttk.Style()
        progressStyle.configure(
            "Custom.Horizontal.TProgressbar",
            thickness=self.progress_thickness,
            troughcolor="#333333",
            background="#00FF00",
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
        self.progress_bar.bind("<Double-1>", self.show_progress_popup)  # Bind double-click event
        
        self.bind("<Configure>", self.on_resize)
        self.update_idletasks()
        self.on_initial_display()

    def on_initial_display(self):
        self.on_resize(None)

    def on_resize(self, event):
        # Intentionally left empty to handle resize events
        pass

    def update_status(self, text, progress=None):
        """
        Update the status bar with a new message and progress.
        text: New status message
        progress: Progress value between 0 and 1
        """
        self.progress_label.configure(text=text)
        if progress is not None:
            self.progress_bar["value"] = progress * 100
            
            # Update progress bar color based on progress value
            if progress < 0.3:
                color = "#FF0000"  # Red
            elif 0.3 <= progress <= 0.7:
                color = "#0000FF"  # Blue
            else:
                color = "#00FF00"  # Green
            
            progressStyle = ttk.Style()
            progressStyle.configure(
                "Custom.Horizontal.TProgressbar",
                thickness=self.progress_thickness,
                troughcolor="#333333",
                background=color,
                troughrelief="flat",
            )
            
            self.progress_bar.update_idletasks()
        
        # Update ProgressPopup if it is open
        if hasattr(self, 'progress_popup') and self.progress_popup.winfo_exists():
            self.progress_popup.update_status(text, progress)

    def reset(self):
        """Reset the status bar to its initial state."""
        self.progress_label.configure(text="Ready")
        self.progress_bar["value"] = 0

    def update_user(self, user_text):
        """Update the user label text."""
        self.user_label.configure(text=user_text)

    def update_access(self, access_text):
        """Update the access label text."""
        self.access_label.configure(text=access_text)

    def show_user_alert(self, event):
        """Show an alert with the user name."""
        show_alert(state="info", title="User Info", body_text=f"User: {self.user_label.cget('text')}")

    def show_access_alert(self, event):
        """Show an alert with the access information."""
        show_alert(state="info", title="Access Info", body_text=f"Access: {self.access_label.cget('text')}")

    def show_progress_popup(self, event):
        """Show the ProgressPopup when the progress bar is double-clicked."""
        self.progress_popup = ProgressPopup(self.master)
        self.progress_popup.update_status(self.progress_label.cget("text"), self.progress_bar["value"] / 100)


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
