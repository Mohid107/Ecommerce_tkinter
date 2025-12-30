import tkinter as tk
from tkinter import ttk, messagebox
from src.core.constants import ViewNames
from src.gui import theme

class ProfileView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user_service = self.controller.user_service
        self.configure(style="TFrame")
        
        self._setup_ui()

    def _setup_ui(self):
        # Nav
        nav = ttk.Frame(self, style="TFrame")
        nav.pack(fill="x", padx=20, pady=10)
        ttk.Button(nav, text="← Back", style="Secondary.TButton",
                  command=lambda: self.controller.show_view(ViewNames.PRODUCT_LIST)).pack(side="left")

        ttk.Label(self, text="My Profile", style="Title.TLabel").pack(pady=20)
        
        content = ttk.Frame(self, style="Card.TFrame", padding=30)
        content.pack(pady=20)
        
        self.info_label = ttk.Label(content, text="", style="Header.TLabel")
        self.info_label.pack(pady=10)
        
        ttk.Button(content, text="Logout", style="Secondary.TButton",
                  command=self.logout).pack(pady=20)

    def load_profile(self):
        user = self.user_service.get_current_user()
        if user:
            self.info_label.config(text=f"Username: {user['username']}")
        else:
            self.info_label.config(text="Not Logged In")

    def logout(self):
        self.user_service.logout()
        self.controller.show_view(ViewNames.LOGIN)

    def refresh(self):
        self.load_profile()
