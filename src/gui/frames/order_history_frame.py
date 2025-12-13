# src/gui/frames/order_history_frame.py
import tkinter as tk
from tkinter import ttk
from src.gui import theme
from src.core import services


class OrderHistoryFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="TFrame")

        # Navigation header
        nav_frame = ttk.Frame(self, style="TFrame")
        nav_frame.pack(fill="x", padx=20, pady=10)

        ttk.Button(nav_frame, text="🏠 Home",
                   command=lambda: controller.show_frame("HomeFrame")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="📦 Products",
                   command=lambda: controller.show_frame("ProductListFrame")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="🛒 Cart",
                   command=lambda: controller.show_frame("CartFrame")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="👤 Profile",
                   command=lambda: controller.show_frame("ProfileFrame")).pack(side="left", padx=5)

        # Title
        ttk.Label(self, text="📋 Order History", style="Title.TLabel").pack(pady=20)

        # Main content frame
        self.content_frame = ttk.Frame(self, style="Frame.TFrame")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Load orders
        self.load_orders()

    def load_orders(self):
        """Load and display user orders"""
        # Clear previous content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        try:
            orders = services.get_user_orders()
        except ValueError as e:
            # User not logged in
            ttk.Label(self.content_frame, text="🔒 Please login to view orders",
                      style="SubTitle.TLabel").pack(pady=50)
            ttk.Button(self.content_frame, text="Go to Login",
                       command=lambda: self.controller.show_frame("LoginFrame")).pack(pady=10)
            return
        except Exception as e:
            ttk.Label(self.content_frame, text=f"❌ Error loading orders: {str(e)}",
                      style="SubTitle.TLabel").pack(pady=50)
            return

        if not orders:
            ttk.Label(self.content_frame, text="📭 No orders placed yet",
                      style="SubTitle.TLabel").pack(pady=50)
            ttk.Button(self.content_frame, text="Browse Products",
                       command=lambda: self.controller.show_frame("ProductListFrame")).pack(pady=10)
            return

        # Create scrollable frame for orders
        canvas = tk.Canvas(self.content_frame, bg=theme.Colors.BACKGROUND, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="TFrame")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Display orders
        for order in orders:
            order_frame = ttk.Frame(scrollable_frame, style="Card.TFrame", padding=15)
            order_frame.pack(fill="x", padx=5, pady=10)

            # Order header
            header_frame = ttk.Frame(order_frame, style="TFrame")
            header_frame.pack(fill="x", pady=(0, 10))

            ttk.Label(header_frame, text=f"Order #{order['id']}",
                      style="CardTitle.TLabel").pack(side="left")

            ttk.Label(header_frame, text=f"${order['total_amount']:.2f}",
                      style="CardPrice.TLabel").pack(side="right")

            # Order details
            details_frame = ttk.Frame(order_frame, style="TFrame")
            details_frame.pack(fill="x")

            # Date
            date_str = order.get('date', 'N/A')
            if hasattr(date_str, 'strftime'):  # If it's a datetime object
                date_str = date_str.strftime("%Y-%m-%d %H:%M")

            ttk.Label(details_frame, text=f"📅 Date: {date_str}",
                      style="CardDesc.TLabel").pack(anchor="w")

            ttk.Label(details_frame, text=f"👤 User ID: {order['user_id']}",
                      style="CardDesc.TLabel").pack(anchor="w")

    def refresh(self):
        """Refresh order history"""
        self.load_orders()