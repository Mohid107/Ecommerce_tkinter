# src/gui/cart_frame.py
import tkinter as tk
from tkinter import ttk, messagebox
from src.core import services
from src.gui import theme


class CartFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(style="TFrame")
        theme.setup_styles(self)

        # ============================
        # NAVIGATION HEADER
        # ============================
        nav_frame = ttk.Frame(self, style="TFrame")
        nav_frame.pack(fill="x", padx=20, pady=10)

        ttk.Button(nav_frame, text="🏠 Home",
                   command=lambda: controller.show_frame("HomeFrame")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="📦 Products",
                   command=lambda: controller.show_frame("ProductListFrame")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="👤 Profile",
                   command=lambda: controller.show_frame("ProfileFrame")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="📋 Orders",
                   command=lambda: controller.show_frame("OrderHistoryFrame")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="✅ Checkout",
                   command=self.go_to_checkout).pack(side="left", padx=5)

        # ============================
        # PAGE HEADER
        # ============================
        header_frame = ttk.Frame(self, style="TFrame")
        header_frame.pack(fill="x", padx=20, pady=(0, 20))

        header = ttk.Label(header_frame, text="🛒 Your Shopping Cart",
                           font=theme.Fonts.HEADER, foreground=theme.Colors.PRIMARY)
        header.pack(side="left")

        # Cart summary badge
        self.cart_count = tk.StringVar(value="0 items")
        count_label = ttk.Label(header_frame, textvariable=self.cart_count,
                                font=("Helvetica", 10), foreground=theme.Colors.ACCENT)
        count_label.pack(side="right", padx=10)

        # ============================
        # BOTTOM ACTION BUTTONS (Footer)
        # ============================
        # Pack footer first (side=bottom) effectively pins it to the bottom
        btn_frame = ttk.Frame(self, style="TFrame")
        btn_frame.pack(side="bottom", fill="x", pady=20, padx=20)

        # Left side buttons
        left_btn_frame = ttk.Frame(btn_frame, style="TFrame")
        left_btn_frame.pack(side="left")

        ttk.Button(left_btn_frame, text="← Continue Shopping",
                   command=lambda: controller.show_frame("ProductListFrame")).pack(side="left", padx=5)

        ttk.Button(left_btn_frame, text="Clear Cart",
                   command=self.clear_cart, style="Secondary.TButton").pack(side="left", padx=5)

        # Right side buttons
        right_btn_frame = ttk.Frame(btn_frame, style="TFrame")
        right_btn_frame.pack(side="right")

        self.total_label = ttk.Label(right_btn_frame, text="Total: $0.00",
                                     font=theme.Fonts.SUBHEADER, foreground=theme.Colors.PRIMARY)
        self.total_label.pack(side="left", padx=10)

        self.checkout_btn = ttk.Button(right_btn_frame, text="Proceed to Checkout →",
                                       style="TButton", command=self.go_to_checkout)
        self.checkout_btn.pack(side="right")

        # ============================
        # CART ITEMS CONTAINER
        # ============================
        # Pack container last, so it takes up all remaining space between header and footer
        self.cart_container = tk.Frame(self, bg=theme.Colors.BACKGROUND)
        self.cart_container.pack(side="top", fill="both", expand=True, padx=20, pady=10)

        # Load cart items
        self.load_cart()

    def load_cart(self):
        """Load and display cart items"""
        # Clear previous content
        for widget in self.cart_container.winfo_children():
            widget.destroy()

        try:
            items = services.get_cart_items()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load cart: {e}")
            items = []

        if not items:
            # Empty cart message
            empty_frame = tk.Frame(self.cart_container, bg=theme.Colors.BACKGROUND)
            empty_frame.pack(expand=True, pady=100)

            ttk.Label(empty_frame, text="🛒", font=("Arial", 48),
                      background=theme.Colors.BACKGROUND).pack(pady=10)
            ttk.Label(empty_frame, text="Your cart is empty",
                      font=theme.Fonts.SUBHEADER, background=theme.Colors.BACKGROUND).pack(pady=5)
            ttk.Label(empty_frame, text="Add some products to get started!",
                      font=theme.Fonts.BODY, background=theme.Colors.BACKGROUND).pack(pady=5)

            ttk.Button(empty_frame, text="Browse Products",
                       command=lambda: self.controller.show_frame("ProductListFrame")).pack(pady=20)

            # Update UI
            self.cart_count.set("0 items")
            self.total_label.config(text="Total: $0.00")
            self.checkout_btn.config(state="disabled")
            return

        # ============================
        # CART ITEMS TABLE
        # ============================
        # Create a canvas for scrollable content
        canvas = tk.Canvas(self.cart_container, bg=theme.Colors.BACKGROUND, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.cart_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="TFrame")

        from src.gui.utils import setup_scroll
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Center content
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        
        def _configure_window(event):
            canvas.itemconfig(window_id, width=event.width)
        canvas.bind("<Configure>", _configure_window)

        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mouse wheel
        setup_scroll(canvas)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Table headers
        headers_frame = ttk.Frame(scrollable_frame, style="Card.TFrame", padding=10)
        headers_frame.pack(fill="x", padx=5, pady=(0, 10))

        headers = ["Product", "Price", "Quantity", "Total", "Actions"]
        for idx, h in enumerate(headers):
            lbl = ttk.Label(headers_frame, text=h, font=theme.Fonts.SUBHEADER,
                            foreground=theme.Colors.PRIMARY)
            lbl.grid(row=0, column=idx, padx=10, pady=5, sticky="w")

        # Cart items
        for i, item in enumerate(items, start=1):
            item_frame = ttk.Frame(scrollable_frame, style="Card.TFrame", padding=10)
            item_frame.pack(fill="x", padx=5, pady=5)

            # Product name
            ttk.Label(item_frame, text=item['name'], font=theme.Fonts.BODY,
                      wraplength=200, justify="left").grid(row=0, column=0, padx=10, pady=5, sticky="w")

            # Price
            ttk.Label(item_frame, text=f"${item['price']:.2f}", font=theme.Fonts.BODY).grid(
                row=0, column=1, padx=10, pady=5, sticky="w")

            # Quantity controls
            qty_frame = ttk.Frame(item_frame, style="TFrame")
            qty_frame.grid(row=0, column=2, padx=10, pady=5, sticky="w")

            # Decrease button
            ttk.Button(qty_frame, text="−", width=2,
                       command=lambda pid=item['product_id'], q=item['quantity'] - 1:
                       self.update_quantity(pid, q if q > 0 else 1)).pack(side="left")

            # Quantity display
            qty_var = tk.StringVar(value=str(item['quantity']))
            qty_entry = ttk.Entry(qty_frame, textvariable=qty_var, width=5, justify="center")
            qty_entry.pack(side="left", padx=2)
            qty_entry.bind("<Return>",
                           lambda e, pid=item['product_id'], var=qty_var:
                           self.update_quantity(pid, int(var.get()) if var.get().isdigit() else 1))

            # Increase button
            ttk.Button(qty_frame, text="+", width=2,
                       command=lambda pid=item['product_id'], q=item['quantity'] + 1:
                       self.update_quantity(pid, q)).pack(side="left")

            # Total for this item
            ttk.Label(item_frame, text=f"${item['total']:.2f}",
                      font=theme.Fonts.BODY, foreground=theme.Colors.ACCENT).grid(
                row=0, column=3, padx=10, pady=5, sticky="w")

            # Remove button
            ttk.Button(item_frame, text="🗑️ Remove", style="Secondary.TButton",
                       command=lambda pid=item['product_id']: self.remove_item(pid)).grid(
                row=0, column=4, padx=10, pady=5, sticky="e")

        # ============================
        # UPDATE SUMMARY
        # ============================
        total_amount = services.get_cart_total()
        item_count = sum(item['quantity'] for item in items)

        self.cart_count.set(f"{item_count} {'item' if item_count == 1 else 'items'}")
        self.total_label.config(text=f"Total: ${total_amount:.2f}")
        self.checkout_btn.config(state="normal")

    def remove_item(self, product_id):
        """Remove item from cart"""
        if messagebox.askyesno("Remove Item", "Are you sure you want to remove this item from your cart?"):
            try:
                services.remove_from_cart(product_id)
                self.load_cart()
                # messagebox.showinfo("Success", "Item removed from cart!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove item: {e}")

    def update_quantity(self, product_id, new_quantity):
        """Update item quantity"""
        try:
            if new_quantity < 1:
                messagebox.showwarning("Invalid Quantity", "Quantity must be at least 1")
                return

            services.update_cart_quantity(product_id, new_quantity)
            self.load_cart()  # Refresh display
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid quantity: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update quantity: {e}")

    def clear_cart(self):
        """Clear all items from cart"""
        if not services.get_cart_items():
            messagebox.showinfo("Cart Empty", "Your cart is already empty!")
            return

        if messagebox.askyesno("Clear Cart", "Are you sure you want to remove all items from your cart?"):
            try:
                # Remove each item individually
                items = services.get_cart_items()
                for item in items:
                    services.remove_from_cart(item['product_id'])
                self.load_cart()
                messagebox.showinfo("Success", "Cart cleared successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear cart: {e}")

    def go_to_checkout(self):
        """Navigate to checkout page"""
        try:
            items = services.get_cart_items()
            if not items:
                messagebox.showwarning("Empty Cart", "Your cart is empty!")
                # Optional: Navigate to product list if empty
                # self.controller.show_frame("ProductListFrame")
                return

            self.controller.show_frame("CheckoutFrame")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot proceed to checkout: {e}")

    def refresh(self):
        """Refresh cart display (called when frame is shown)"""
        self.load_cart()