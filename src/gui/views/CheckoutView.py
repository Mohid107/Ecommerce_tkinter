import tkinter as tk
from tkinter import ttk, messagebox
from src.core.constants import AppConstants, Messages, ViewNames
from src.gui import theme

class CheckoutView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.cart_service = self.controller.cart_service
        self.order_service = self.controller.order_service
        self.user_service = self.controller.user_service
        
        theme.setup_styles(self)
        self._setup_ui()

    def _setup_ui(self):
        ttk.Label(self, text="Checkout", style="Title.TLabel").pack(pady=20)
        
        self.summary_frame = ttk.Frame(self, style="Card.TFrame", padding=20)
        self.summary_frame.pack(fill="x", padx=50, pady=10)
        
        self.total_label = ttk.Label(self.summary_frame, text="Total: $0.00", style="Header.TLabel")
        self.total_label.pack(pady=10)

        ttk.Button(self, text="Confirm Order", style="Primary.TButton",
                   command=self.process_checkout).pack(pady=20)
        
        ttk.Button(self, text="Back to Cart", style="Secondary.TButton",
                   command=lambda: self.controller.show_view(ViewNames.CART)).pack()

    def refresh(self):
        total = self.cart_service.get_cart_total()
        self.total_label.config(text=f"Total: ${total:.2f}")

    def process_checkout(self):
        try:
            # Pass Dependencies if needed or use injected services
            order_id = self.order_service.checkout(self.user_service, self.cart_service)
            messagebox.showinfo("Success", Messages.CHECKOUT_SUCCESS.format(order_id=order_id))
            self.controller.show_view(ViewNames.PRODUCT_LIST)
        except ValueError as e:
            messagebox.showerror("Checkout Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Checkout failed: {e}")
