import tkinter as tk
from tkinter import ttk
from src.constants import AppConstants, Messages, ViewNames
from src import theme

class HomeView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="TFrame")
        
        self._setup_ui()

    def _setup_ui(self):
        # 1. Hero Section (Banner)
        hero_frame = tk.Frame(self, bg=theme.Colors.PRIMARY, height=250)
        hero_frame.pack(fill="x", side="top")
        hero_frame.pack_propagate(False)  # Enforce height

        # Hero Content
        hero_content = tk.Frame(hero_frame, bg=theme.Colors.PRIMARY)
        hero_content.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(hero_content, text="Welcome to ShopEasy", 
                 font=theme.Fonts.TITLE, bg=theme.Colors.PRIMARY, fg="white").pack(pady=(0, 10))
        
        tk.Label(hero_content, text="Discover the best products at unbeatable prices.",
                 font=theme.Fonts.SUBTITLE, bg=theme.Colors.PRIMARY, fg="#E0E0E0").pack(pady=(0, 20))

        cta_btn = tk.Button(hero_content, text="Shop Now",
                            font=("Segoe UI", 12, "bold"), bg="white", fg=theme.Colors.PRIMARY,
                            relief="flat", padx=20, pady=10, cursor="hand2",
                            command=lambda: self.controller.show_view(ViewNames.PRODUCT_LIST))
        cta_btn.pack()

        # 2. Main Content Area
        content_frame = ttk.Frame(self, style="TFrame", padding=30)
        content_frame.pack(fill="both", expand=True)

        # Quick Actions Grid
        ttk.Label(content_frame, text="Quick Actions", style="Header.TLabel").pack(pady=(0, 20))

        actions_grid = ttk.Frame(content_frame, style="TFrame")
        actions_grid.pack()

        self._create_action_card(actions_grid, "📦", "Browse Products", "Explore our full catalog", 
                                 ViewNames.PRODUCT_LIST, 0, 0)
        self._create_action_card(actions_grid, "👤", "My Profile", "Manage details & password", 
                                 ViewNames.PROFILE, 0, 1)
        self._create_action_card(actions_grid, "📋", "Order History", "Track your purchases", 
                                 ViewNames.ORDER_HISTORY, 0, 2)
        self._create_action_card(actions_grid, "🛒", "View Cart", "Ready to checkout?", 
                                 ViewNames.CART, 0, 3)

        # Footer
        footer = ttk.Frame(self, style="TFrame", padding=10)
        footer.pack(side="bottom", fill="x")
        ttk.Label(footer, text="© 2025 ShopEasy Inc.", style="Label.TLabel", foreground=theme.Colors.TEXT_SECONDARY).pack()

    def _create_action_card(self, parent, icon, title, desc, view_name, row, col):
        card = ttk.Frame(parent, style="Card.TFrame", padding=20)
        card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        # Icon
        ttk.Label(card, text=icon, font=("Segoe UI Emoji", 32), background="white").pack(pady=(0, 10))
        
        # Text
        ttk.Label(card, text=title, style="CardTitle.TLabel").pack()
        ttk.Label(card, text=desc, style="CardDesc.TLabel", wraplength=150, justify="center").pack(pady=(5, 15))
        
        # Button
        ttk.Button(card, text="Go", style="Secondary.TButton",
                   command=lambda: self.controller.show_view(view_name)).pack()

    def refresh(self):
        pass
