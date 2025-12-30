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
        # 1. Navigation Header
        nav = ttk.Frame(self, style="TFrame")
        nav.pack(fill="x", padx=20, pady=10)
        ttk.Button(nav, text="← Home", style="Secondary.TButton",
                  command=lambda: self.controller.show_view(ViewNames.HOME)).pack(side="left")

        # 2. Main Content
        container = ttk.Frame(self, style="TFrame")
        container.pack(fill="both", expand=True, padx=40, pady=20)

        ttk.Label(container, text="My Profile", style="Title.TLabel").pack(anchor="w", pady=(0, 20))

        # Two Column Layout
        grid = ttk.Frame(container, style="TFrame")
        grid.pack(fill="x")
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)

        # --- LEFT: User Details ---
        details_card = ttk.Frame(grid, style="Card.TFrame", padding=30)
        details_card.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        ttk.Label(details_card, text="Account Details", style="Header.TLabel").pack(anchor="w", pady=(0, 20))
        
        self.info_label = ttk.Label(details_card, text="", style="Label.TLabel", font=("Segoe UI", 12))
        self.info_label.pack(anchor="w", pady=5)
        
        ttk.Separator(details_card, orient="horizontal").pack(fill="x", pady=20)
        
        ttk.Button(details_card, text="📜 View Order History", style="Secondary.TButton",
                  command=lambda: self.controller.show_view(ViewNames.ORDER_HISTORY)).pack(fill="x", pady=5)
        
        ttk.Button(details_card, text="🚪 Logout", style="Secondary.TButton",
                  command=self.logout).pack(fill="x", pady=5)


        # --- RIGHT: Change Password ---
        pwd_card = ttk.Frame(grid, style="Card.TFrame", padding=30)
        pwd_card.grid(row=0, column=1, sticky="nsew", padx=(15, 0))

        ttk.Label(pwd_card, text="Security Settings", style="Header.TLabel").pack(anchor="w", pady=(0, 20))
        ttk.Label(pwd_card, text="Update Password", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 15))

        # New Password
        ttk.Label(pwd_card, text="New Password", style="Label.TLabel").pack(anchor="w")
        self.new_pass = ttk.Entry(pwd_card, show="*", font=theme.Fonts.BODY)
        self.new_pass.pack(fill="x", pady=(5, 15))

        # Confirm Password
        ttk.Label(pwd_card, text="Confirm New Password", style="Label.TLabel").pack(anchor="w")
        self.confirm_pass = ttk.Entry(pwd_card, show="*", font=theme.Fonts.BODY)
        self.confirm_pass.pack(fill="x", pady=(5, 20))

        ttk.Button(pwd_card, text="Update Password", style="Primary.TButton",
                  command=self.update_password).pack(fill="x")

    def load_profile(self):
        user = self.user_service.get_current_user()
        if user:
            self.info_label.config(text=f"👤 Username: {user['username']}\n🆔 User ID: {user['id']}")
        else:
            self.info_label.config(text="Not Logged In")
            
    def update_password(self):
        new_p = self.new_pass.get()
        confirm_p = self.confirm_pass.get()
        
        if not new_p:
            messagebox.showwarning("Input Required", "Please enter a new password.")
            return
            
        if new_p != confirm_p:
            messagebox.showerror("Error", "Passwords do not match.")
            return
            
        try:
            # Assuming UserService has an update_password method (we added it in step 180)
            self.user_service.update_password(new_p)
            messagebox.showinfo("Success", "Password updated successfully!")
            self.new_pass.delete(0, 'end')
            self.confirm_pass.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def logout(self):
        self.user_service.logout()
        self.controller.show_view(ViewNames.LOGIN)

    def refresh(self):
        self.load_profile()
