import tkinter as tk
from tkinter import ttk, messagebox
from src.constants import AppConstants, Messages, ViewNames
from src import theme
from src.exceptions import AuthenticationError

class LoginView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Access UserService from controller
        self.user_service = self.controller.user_service

        theme.setup_styles(self)
        self._setup_ui()

    def _setup_ui(self):
        # Card Container
        card_frame = ttk.Frame(self, style="Card.TFrame", padding=40)
        card_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Header
        ttk.Label(card_frame, text="Welcome Back", style="Header.TLabel").pack(pady=(0, 10))
        ttk.Label(card_frame, text="Please login to your account", 
                 style="Card.TLabel", foreground=theme.Colors.TEXT_SECONDARY).pack(pady=(0, 30))

        # Inputs
        user_container = ttk.Frame(card_frame, style="Card.TFrame")
        user_container.pack(fill="x", pady=(0, 15))
        ttk.Label(user_container, text="Username", style="Card.TLabel").pack(anchor="w", pady=(0, 5))
        self.username_entry = ttk.Entry(user_container, font=theme.Fonts.BODY, width=30)
        self.username_entry.pack(fill="x", ipady=5)

        pass_container = ttk.Frame(card_frame, style="Card.TFrame")
        pass_container.pack(fill="x", pady=(0, 25))
        ttk.Label(pass_container, text="Password", style="Card.TLabel").pack(anchor="w", pady=(0, 5))
        self.password_entry = ttk.Entry(pass_container, show="*", font=theme.Fonts.BODY, width=30)
        self.password_entry.pack(fill="x", ipady=5)

        # Actions
        login_btn = ttk.Button(card_frame, text="LOGIN", command=self.login, style="TButton")
        login_btn.pack(fill="x", pady=(0, 15), ipady=5)

        footer_frame = ttk.Frame(card_frame, style="Card.TFrame")
        footer_frame.pack(fill="x", pady=(10, 0))
        ttk.Label(footer_frame, text="Don't have an account?", 
                 style="Card.TLabel", foreground=theme.Colors.TEXT_SECONDARY).pack(side="left")
        
        # Navigate to SignupView
        signup_btn = ttk.Button(footer_frame, text="Sign Up", 
                               command=lambda: self.controller.show_view(ViewNames.SIGNUP), 
                               style="Link.TButton", cursor="hand2")
        signup_btn.pack(side="left", padx=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            if self.user_service.login(username, password):
                self.controller.show_view(ViewNames.HOME)
        except AuthenticationError as e:
            messagebox.showerror("Login Failed", str(e))
        except Exception as e:
            from src.logger import app_logger
            app_logger.error(f"Login Error: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
