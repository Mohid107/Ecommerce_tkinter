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
        # Header
        header = ttk.Frame(self, style="TFrame")
        header.pack(fill="x", padx=30, pady=20)
        ttk.Label(header, text="🛒 Shopping Cart", style="Title.TLabel").pack(side="left")

        # Main Layout: Left (Table), Right (Summary)
        main_frame = ttk.Frame(self, style="TFrame")
        main_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        main_frame.grid_columnconfigure(0, weight=3) # Cart Table
        main_frame.grid_columnconfigure(1, weight=1) # Summary
        main_frame.grid_rowconfigure(0, weight=1)

        # --- LEFT: Cart Items (Treeview) ---
        table_frame = ttk.Frame(main_frame, style="TFrame")
        table_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        # Treeview setup
        columns = ("name", "price", "qty", "total")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("name", text="Product")
        self.tree.heading("price", text="Price")
        self.tree.heading("qty", text="Quantity")
        self.tree.heading("total", text="Total")
        
        self.tree.column("name", width=300)
        self.tree.column("price", width=100, anchor="e")
        self.tree.column("qty", width=80, anchor="center")
        self.tree.column("total", width=100, anchor="e")

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Treeview Actions (Remove/Edit)
        actions_frame = ttk.Frame(table_frame, style="TFrame")
        actions_frame.pack(fill="x", pady=10)
        
        ttk.Button(actions_frame, text="➖ Decrease Qty", style="Secondary.TButton", 
                   command=lambda: self._adjust_qty(-1)).pack(side="left", padx=5)
        ttk.Button(actions_frame, text="➕ Increase Qty", style="Secondary.TButton", 
                   command=lambda: self._adjust_qty(1)).pack(side="left", padx=5)
        ttk.Button(actions_frame, text="❌ Remove Item", style="Secondary.TButton", 
                   command=self._remove_selected).pack(side="left", padx=5)


        # --- RIGHT: Order Summary ---
        summary_card = ttk.Frame(main_frame, style="Card.TFrame", padding=25)
        summary_card.grid(row=0, column=1, sticky="nw")

        ttk.Label(summary_card, text="Order Summary", style="Header.TLabel").pack(anchor="w", pady=(0, 15))
        
        # Details
        self.summary_content = ttk.Frame(summary_card, style="TFrame")
        self.summary_content.pack(fill="x", pady=10)
        
        # (Populated efficiently in refresh)
        self.lbl_subtotal = ttk.Label(self.summary_content, text="Subtotal: $0.00", style="Label.TLabel")
        self.lbl_subtotal.pack(anchor="e")
        
        ttk.Separator(summary_card, orient="horizontal").pack(fill="x", pady=15)
        
        self.lbl_total = ttk.Label(summary_card, text="Total: $0.00", style="Header.TLabel")
        self.lbl_total.pack(anchor="e", pady=(0, 20))

        # Checkout Button
        self.btn_checkout = ttk.Button(summary_card, text="🔒 Proceed to Checkout", style="Primary.TButton",
                   command=lambda: self.controller.show_view(ViewNames.CHECKOUT))
        self.btn_checkout.pack(fill="x")
        
        ttk.Button(summary_card, text="← Continue Shopping", style="Link.TButton",
                   command=lambda: self.controller.show_view(ViewNames.PRODUCT_LIST)).pack(pady=10)

    def load_cart(self):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        items = self.cart_service.get_cart_items()
        
        total_price = 0
        for item in items:
            self.tree.insert("", "end", iid=item['product_id'], values=(
                item['name'],
                f"${item['price']:.2f}",
                item['quantity'],
                f"${item['total']:.2f}"
            ))
            total_price += item['total']

        # Update Summary
        self.lbl_subtotal.config(text=f"Subtotal: ${total_price:.2f}")
        self.lbl_total.config(text=f"Total: ${total_price:.2f}")

        # Disable checkout if empty
        if not items:
            self.btn_checkout.config(state="disabled")
        else:
            self.btn_checkout.config(state="normal")

    def _adjust_qty(self, change):
        selected = self.tree.selection()
        if not selected: return
        
        pid = int(selected[0])
        # Find current qty
        # Ideally we ask service, or read from tree values
        # Reading from service is safer
        for item in self.cart_service.cart:
            if item.product_id == pid:
                new_qty = item.quantity + change
                try:
                    self.cart_service.update_cart_quantity(pid, new_qty)
                    self.load_cart()
                    # Reselect
                    if new_qty > 0: self.tree.selection_set(str(pid))
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                return

    def _remove_selected(self):
        selected = self.tree.selection()
        if not selected: return
        pid = int(selected[0])
        self.cart_service.remove_from_cart(pid)
        self.load_cart()

    def refresh(self):
        self.load_cart()
