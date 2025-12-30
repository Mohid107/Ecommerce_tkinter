import tkinter as tk
from tkinter import ttk
from src.core.constants import AppConstants, Messages, ViewNames
from src.gui import theme

class HomeView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ttk.Label(self, text="Welcome to ShopEasy!", style="Title.TLabel").pack(pady=50)
        
        ttk.Button(self, text="Browse Products", style="Primary.TButton",
                   command=lambda: self.controller.show_view(ViewNames.PRODUCT_LIST)).pack(pady=10)
        
        ttk.Button(self, text="My Profile", style="Secondary.TButton",
                   command=lambda: self.controller.show_view(ViewNames.PROFILE)).pack(pady=10)

    def refresh(self):
        pass
