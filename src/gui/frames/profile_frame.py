# src/gui/frames/profile_frame.py
import tkinter as tk
from tkinter import ttk, messagebox
from src.gui import theme
from src.core import services

class ProfileFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="User Profile", style="Title.TLabel").pack(pady=20)

        # Profile form frame
        self.form_frame = ttk.Frame(self, style="Frame.TFrame")
        self.form_frame.pack(padx=20, pady=10, fill="x")

        ttk.Label(self.form_frame, text="Username:", style="Label.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(self.form_frame, textvariable=self.username_var, state="readonly")
        self.username_entry.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(self.form_frame, text="Password:", style="Label.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.form_frame, textvariable=self.password_var, show="*")
        self.password_entry.grid(row=1, column=1, sticky="ew", pady=5)

        # Update button
        ttk.Button(self, text="Update Password", style="Primary.TButton", command=self.update_password).pack(pady=15)

        # Back button
        ttk.Button(self, text="Back to Home", style="Secondary.TButton",
                   command=lambda: controller.show_frame("HomeFrame")).pack(pady=10)

        self.load_profile()

    def load_profile(self):
        """Load current user's profile details"""
        user = services.current_user
        if user:
            self.username_var.set(user["username"])
            self.password_var.set(user["password"])

    def update_password(self):
        """Update password functionality"""
        new_password = self.password_var.get()
        if not new_password:
            messagebox.showerror("Error", "Password cannot be empty!")
            return

        # Here you can call a service to update password in DB
        try:
            services.update_password(new_password)
            messagebox.showinfo("Success", "Password updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
