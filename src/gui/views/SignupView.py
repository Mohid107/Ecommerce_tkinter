import tkinter as tk
from tkinter import ttk, messagebox
from src.core.constants import AppConstants, Messages, ViewNames
from src.gui import theme

class SignupView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user_service = self.controller.user_service
        
        theme.setup_styles(self)
        self._setup_ui()

    def _setup_ui(self):
        theme.setup_styles(self)
        ttk.Label(self, text="Sign Up", style="Title.TLabel").pack(pady=20)

        form_frame = ttk.Frame(self, style="Frame.TFrame")
        form_frame.pack(padx=30, pady=10, fill="x")

        # Username
        ttk.Label(form_frame, text="Username:", style="Label.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        self.username_var = tk.StringVar()
        entry_user = ttk.Entry(form_frame, textvariable=self.username_var)
        entry_user.grid(row=0, column=1, sticky="ew", pady=5)

        # Password
        ttk.Label(form_frame, text="Password:", style="Label.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        self.password_var = tk.StringVar()
        entry_pass = ttk.Entry(form_frame, textvariable=self.password_var, show="*")
        entry_pass.grid(row=1, column=1, sticky="ew", pady=5)

        # Confirm
        ttk.Label(form_frame, text="Confirm Password:", style="Label.TLabel").grid(row=2, column=0, sticky="w", pady=5)
        self.confirm_var = tk.StringVar()
        entry_confirm = ttk.Entry(form_frame, textvariable=self.confirm_var, show="*")
        entry_confirm.grid(row=2, column=1, sticky="ew", pady=5)

        ttk.Button(self, text="Sign Up", style="Primary.TButton", command=self.signup).pack(pady=15)

        ttk.Button(self, text="Back to Login", style="Secondary.TButton",
                   command=lambda: self.controller.show_view(ViewNames.LOGIN)).pack(pady=10)

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
            self.user_service.signup(username, password)
            messagebox.showinfo("Success", Messages.SIGNUP_SUCCESS)
            self.controller.show_view(ViewNames.LOGIN)
        except Exception as e:
            messagebox.showerror("Error", str(e))
