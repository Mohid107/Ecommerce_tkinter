import tkinter as tk
from tkinter import ttk, messagebox
from src.constants import AppConstants, Messages, ViewNames
from src import theme

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
        # Nav Header
        nav = ttk.Frame(self, style="TFrame")
        nav.pack(fill="x", padx=30, pady=20)
        ttk.Button(nav, text="← Back to Cart", style="Secondary.TButton",
                  command=lambda: self.controller.show_view(ViewNames.CART)).pack(side="left")

        # Main Layout
        grid = ttk.Frame(self, style="TFrame")
        grid.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        grid.grid_columnconfigure(0, weight=2)
        grid.grid_columnconfigure(1, weight=1)

        # --- LEFT: Shipping Information ---
        form_card = ttk.Frame(grid, style="Card.TFrame", padding=30)
        form_card.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        ttk.Label(form_card, text="Shipping Information", style="Title.TLabel").pack(anchor="w", pady=(0, 20))

        # Form Fields
        self.fields = {}
        labels = ["Full Name", "Street Address", "City", "State/Province", "Zip/Postal Code"]
        
        for label in labels:
            lbl = ttk.Label(form_card, text=label, style="Label.TLabel")
            lbl.pack(anchor="w", pady=(5, 0))
            entry = ttk.Entry(form_card, font=theme.Fonts.BODY, width=40)
            entry.pack(fill="x", pady=(5, 15))
            self.fields[label] = entry

        # Payment Mock
        ttk.Label(form_card, text="Payment Method", style="Label.TLabel").pack(anchor="w", pady=(10, 0))
        self.payment_var = tk.StringVar(value="Credit Card")
        pay_box = ttk.Combobox(form_card, textvariable=self.payment_var, values=["Credit Card", "PayPal", "Bank Transfer"], state="readonly")
        pay_box.pack(fill="x", pady=5)


        # --- RIGHT: Order Summary ---
        summary_card = ttk.Frame(grid, style="Card.TFrame", padding=30)
        summary_card.grid(row=0, column=1, sticky="nw")

        ttk.Label(summary_card, text="Order Summary", style="Header.TLabel").pack(anchor="w", pady=(0, 20))

        self.summary_list = ttk.Frame(summary_card, style="TFrame")
        self.summary_list.pack(fill="x", pady=10)

        ttk.Separator(summary_card, orient="horizontal").pack(fill="x", pady=20)
        
        self.total_label = ttk.Label(summary_card, text="Total: $0.00", style="Header.TLabel")
        self.total_label.pack(anchor="e", pady=(0, 30))

        self.btn_confirm = ttk.Button(summary_card, text="Confirm Order", style="Primary.TButton",
                   command=self.process_checkout)
        self.btn_confirm.pack(fill="x")


    def refresh(self):
        # Update summary
        for w in self.summary_list.winfo_children(): w.destroy()
        
        items = self.cart_service.get_cart_items()
        
        if not items:
            ttk.Label(self.summary_list, text="Cart is empty").pack()
            self.total_label.config(text=f"Total: $0.00")
            self.btn_confirm.config(state="disabled")
            return
            
        self.btn_confirm.config(state="normal")
        
        for item in items:
            row = ttk.Frame(self.summary_list, style="TFrame")
            row.pack(fill="x", pady=2)
            ttk.Label(row, text=f"{item['quantity']}x {item['name'][:20]}..", style="Label.TLabel").pack(side="left")
            ttk.Label(row, text=f"${item['total']:.2f}", style="Label.TLabel").pack(side="right")
            
        total = self.cart_service.get_cart_total()
        self.total_label.config(text=f"Total: ${total:.2f}")

    def process_checkout(self):
        # Validation
        for lbl, entry in self.fields.items():
            if not entry.get().strip():
                messagebox.showerror("Missing Information", f"Please enter your {lbl}.")
                return

        try:
            # Pass Dependencies if needed or use injected services
            order_id = self.order_service.checkout(self.user_service, self.cart_service)
            messagebox.showinfo("Order Placed", Messages.CHECKOUT_SUCCESS.format(order_id=order_id))
            
            # Clear fields
            for entry in self.fields.values():
                entry.delete(0, 'end')
                
            self.controller.show_view(ViewNames.PRODUCT_LIST)
        except ValueError as e:
            messagebox.showerror("Checkout Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Checkout failed: {e}")
