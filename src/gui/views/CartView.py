import tkinter as tk
from tkinter import ttk, messagebox
from src.core.constants import AppConstants, Messages, ViewNames
from src.gui import theme

class CartView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.cart_service = self.controller.cart_service
        self.configure(style="TFrame")
        self._setup_ui()

    def _setup_ui(self):
        ttk.Label(self, text="🛒 Shopping Cart", style="Title.TLabel").pack(pady=20)

        self.cart_container = ttk.Frame(self, style="TFrame")
        self.cart_container.pack(fill="both", expand=True, padx=20)

        # Footer Actions
        btn_frame = ttk.Frame(self, style="TFrame")
        btn_frame.pack(fill="x", pady=20, padx=30)

        ttk.Button(btn_frame, text="Continue Shopping", style="Secondary.TButton",
                   command=lambda: self.controller.show_view(ViewNames.PRODUCT_LIST)).pack(side="left")
        
        self.checkout_btn = ttk.Button(btn_frame, text="Proceed to Checkout", style="Primary.TButton",
                   command=lambda: self.controller.show_view(ViewNames.CHECKOUT))
        self.checkout_btn.pack(side="right")

        self.load_cart()

    def load_cart(self):
        for widget in self.cart_container.winfo_children():
            widget.destroy()

        items = self.cart_service.get_cart_items()
        
        if not items:
            ttk.Label(self.cart_container, text="Your cart is empty", style="Label.TLabel").pack(pady=50)
            self.checkout_btn.config(state="disabled")
            return

        self.checkout_btn.config(state="normal")
        
        total_price = 0
        for item in items:
            self._create_cart_item_row(item)
            total_price += item['total']

        # Total
        ttk.Separator(self.cart_container, orient='horizontal').pack(fill='x', pady=10)
        total_frame = ttk.Frame(self.cart_container, style="TFrame")
        total_frame.pack(fill="x", pady=10)
        ttk.Label(total_frame, text=f"Total: ${total_price:.2f}", style="Header.TLabel").pack(side="right")

    def _create_cart_item_row(self, item):
        row = ttk.Frame(self.cart_container, style="Card.TFrame", padding=10)
        row.pack(fill="x", pady=5)
        
        # Product Name
        ttk.Label(row, text=item['name'], style="CardTitle.TLabel", width=30).pack(side="left")
        
        # Quantity Controls
        q_frame = ttk.Frame(row, style="TFrame")
        q_frame.pack(side="left", padx=20)
        
        ttk.Button(q_frame, text="-", width=2, 
                  command=lambda: self.update_quantity(item['product_id'], item['quantity'] - 1)).pack(side="left")
        ttk.Label(q_frame, text=str(item['quantity']), style="Label.TLabel").pack(side="left", padx=10)
        ttk.Button(q_frame, text="+", width=2, 
                  command=lambda: self.update_quantity(item['product_id'], item['quantity'] + 1)).pack(side="left")

        # Price
        ttk.Label(row, text=f"${item['total']:.2f}", style="CardPrice.TLabel").pack(side="right", padx=20)

        # Remove
        ttk.Button(row, text="Remove", style="Link.TButton",
                  command=lambda: self.remove_item(item['product_id'])).pack(side="right")

    def update_quantity(self, product_id, new_quantity):
        try:
            self.cart_service.update_cart_quantity(product_id, new_quantity)
            self.load_cart()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def remove_item(self, product_id):
        self.cart_service.remove_from_cart(product_id)
        self.load_cart()

    def refresh(self):
        self.load_cart()
