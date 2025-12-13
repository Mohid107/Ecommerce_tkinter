# src/gui/frames/signup_frame.py
import tkinter as tk
from tkinter import ttk, messagebox
from src.gui import theme
from src.core import services

class SignupFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Sign Up", style="Title.TLabel").pack(pady=20)

        # Form Frame
        self.form_frame = ttk.Frame(self, style="Frame.TFrame")
        self.form_frame.pack(padx=30, pady=10, fill="x")

        # Username
        ttk.Label(self.form_frame, text="Username:", style="Label.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(self.form_frame, textvariable=self.username_var)
        self.username_entry.grid(row=0, column=1, sticky="ew", pady=5)

        # Password
        ttk.Label(self.form_frame, text="Password:", style="Label.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.form_frame, textvariable=self.password_var, show="*")
        self.password_entry.grid(row=1, column=1, sticky="ew", pady=5)

        # Confirm Password
        ttk.Label(self.form_frame, text="Confirm Password:", style="Label.TLabel").grid(row=2, column=0, sticky="w", pady=5)
        self.confirm_var = tk.StringVar()
        self.confirm_entry = ttk.Entry(self.form_frame, textvariable=self.confirm_var, show="*")
        self.confirm_entry.grid(row=2, column=1, sticky="ew", pady=5)

        # Signup Button
        ttk.Button(self, text="Sign Up", style="Primary.TButton", command=self.signup).pack(pady=15)

        # Back to Login Button
        ttk.Button(self, text="Back to Login", style="Secondary.TButton",
                   command=lambda: controller.show_frame("LoginFrame")).pack(pady=10)

    def signup(self):
        username = self.username_var.get()
        password = self.password_var.get()
        confirm = self.confirm_var.get()

        if not username or not password or not confirm:
            messagebox.showerror("Error", "All fields are required!")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        try:
            services.signup(username, password)
            messagebox.showinfo("Success", "User registered! Please login.")
            self.controller.show_frame("LoginFrame")
        except Exception as e:
            messagebox.showerror("Error", str(e))
