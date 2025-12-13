# src/gui/login_frame.py
import tkinter as tk
from tkinter import ttk, messagebox
from src.core import services
from src.gui import theme

class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Set up the theme styles (ensure they are loaded)
        theme.setup_styles(self)

        # Main container (Full background) can just be 'self' (TFrame default is background color)

        # ---------------------------------------------------------
        # CARD CONTAINER (Centered White Box)
        # ---------------------------------------------------------
        card_frame = ttk.Frame(self, style="Card.TFrame", padding=40)
        card_frame.place(relx=0.5, rely=0.5, anchor="center")

        # ---------------------------------------------------------
        # HEADER
        # ---------------------------------------------------------
        # "Welcome Back" title
        title_label = ttk.Label(card_frame, text="Welcome Back", style="Header.TLabel")
        title_label.pack(pady=(0, 10))

        # "Please login..." subtitle
        subtitle_label = ttk.Label(card_frame, text="Please login to your account", style="Card.TLabel", foreground=theme.Colors.TEXT_SECONDARY)
        subtitle_label.pack(pady=(0, 30))

        # ---------------------------------------------------------
        # INPUT FIELDS
        # ---------------------------------------------------------
        
        # Username
        user_container = ttk.Frame(card_frame, style="Card.TFrame")
        user_container.pack(fill="x", pady=(0, 15))
        
        ttk.Label(user_container, text="Username", style="Card.TLabel").pack(anchor="w", pady=(0, 5))
        self.username_entry = ttk.Entry(user_container, font=theme.Fonts.BODY, width=30)
        self.username_entry.pack(fill="x", ipady=5) # ipady for taller input

        # Password
        pass_container = ttk.Frame(card_frame, style="Card.TFrame")
        pass_container.pack(fill="x", pady=(0, 25))

        ttk.Label(pass_container, text="Password", style="Card.TLabel").pack(anchor="w", pady=(0, 5))
        self.password_entry = ttk.Entry(pass_container, show="*", font=theme.Fonts.BODY, width=30)
        self.password_entry.pack(fill="x", ipady=5)

        # ---------------------------------------------------------
        # ACTIONS
        # ---------------------------------------------------------
        
        # Login Button (Primary Action)
        login_btn = ttk.Button(card_frame, text="LOGIN", command=self.login, style="TButton")
        login_btn.pack(fill="x", pady=(0, 15), ipady=5) # ipady to make button taller

        # Sign Up Link (Secondary Action)
        # Using a Frame to hold the "Don't have an account?" text and the Link Button
        footer_frame = ttk.Frame(card_frame, style="Card.TFrame")
        footer_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Label(footer_frame, text="Don't have an account?", style="Card.TLabel", foreground=theme.Colors.TEXT_SECONDARY).pack(side="left")
        
        signup_btn = ttk.Button(footer_frame, text="Sign Up", command=self.signup, style="Link.TButton", cursor="hand2")
        signup_btn.pack(side="left", padx=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            services.login(username, password)
            # messagebox.showinfo("Success", "Logged in successfully!") 
            # (Optional: Skip success popup for smoother flow)
            self.controller.show_frame("ProductListFrame")
        except Exception as e:
            messagebox.showerror("Login Failed", str(e))

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
             messagebox.showwarning("Input Required", "Please enter a username and password to sign up.")
             return

        try:
            services.signup(username, password)
            messagebox.showinfo("Account Created", "User registered successfully! You can now login.")
        except Exception as e:
            messagebox.showerror("Registration Error", str(e))
