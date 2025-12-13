# src/gui/frames/checkout_frame.py
import tkinter as tk
from tkinter import ttk, messagebox
from src.core import services
from src.gui import theme

class CheckoutFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        theme.setup_styles(self)
        
        # Main wrapper for centering
        self.main_container = ttk.Frame(self, style="Card.TFrame", padding=30)
        self.main_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Initialize the view
        self.setup_checkout_view()

    def refresh(self):
        """Called when frame is shown to reload cart data"""
        # If we are in success state, reset to checkout view
        # (Simple heuristic: checks if we have the checkout widgets or success widgets)
        # For simplicity, always rebuild checkout view on refresh if items exist
        self.setup_checkout_view()

    def setup_checkout_view(self):
        # Clear existing widgets
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # Check if cart is empty
        items = services.get_cart_items()
        if not items:
            ttk.Label(self.main_container, text="Your Carts Empty", style="Header.TLabel").pack(pady=20)
            ttk.Button(self.main_container, text="Go Shopping", command=lambda: self.controller.show_frame("ProductListFrame")).pack(pady=10)
            return

        # ---------------------------
        # HEADER
        # ---------------------------
        ttk.Label(self.main_container, text="Checkout", style="Header.TLabel").pack(pady=(0, 20))

        # ---------------------------
        # COLUMNS CONTAINER
        # ---------------------------
        # We'll use a frame to hold two side-by-side sections if space permits, 
        # or just stack them. For standard dialog size, stacking is safer.
        content_frame = ttk.Frame(self.main_container, style="Card.TFrame")
        content_frame.pack(fill="x")

        # --- SECTION 1: ADDRESS DETAILS ---
        details_frame = ttk.Frame(content_frame, style="Card.TFrame")
        details_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(details_frame, text="Shipping Details", style="Card.TLabel", font=theme.Fonts.SUBHEADER).pack(anchor="w", pady=(0, 10))
        
        # Address
        ttk.Label(details_frame, text="Full Address", style="Card.TLabel").pack(anchor="w")
        self.address_entry = ttk.Entry(details_frame, width=40, font=theme.Fonts.BODY)
        self.address_entry.pack(fill="x", pady=(5, 10), ipady=3)

        # Phone
        ttk.Label(details_frame, text="Phone Number", style="Card.TLabel").pack(anchor="w")
        self.phone_entry = ttk.Entry(details_frame, width=40, font=theme.Fonts.BODY)
        self.phone_entry.pack(fill="x", pady=(5, 10), ipady=3)

        # --- SECTION 2: PAYMENT METHOD ---
        payment_frame = ttk.Frame(content_frame, style="Card.TFrame")
        payment_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(payment_frame, text="Payment Method", style="Card.TLabel", font=theme.Fonts.SUBHEADER).pack(anchor="w", pady=(0, 10))
        
        self.payment_var = tk.StringVar(value="Cash")
        
        # Custom style for radio buttons needed? Default usually OK, but let's ensure background matches
        style = ttk.Style()
        style.configure("TRadiobutton", background=theme.Colors.CARD_BG, font=theme.Fonts.BODY)
        
        ttk.Radiobutton(payment_frame, text="Cash on Delivery", variable=self.payment_var, value="Cash", style="TRadiobutton").pack(anchor="w", pady=2)
        ttk.Radiobutton(payment_frame, text="Credit Card", variable=self.payment_var, value="Card", style="TRadiobutton").pack(anchor="w", pady=2)

        # --- SECTION 3: ORDER SUMMARY ---
        summary_frame = ttk.Frame(content_frame, style="Card.TFrame")
        summary_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(summary_frame, text="Order Summary", style="Card.TLabel", font=theme.Fonts.SUBHEADER).pack(anchor="w", pady=(0, 10))
        
        total = services.get_cart_total()
        ttk.Label(summary_frame, text=f"Total Items: {len(items)}", style="Card.TLabel").pack(anchor="w")
        ttk.Label(summary_frame, text=f"Total Amount: ${total:.2f}", style="Header.TLabel", font=("Helvetica", 14, "bold")).pack(anchor="w", pady=(5, 0))

        # ---------------------------
        # ACTIONS
        # ---------------------------
        btn_frame = ttk.Frame(self.main_container, style="Card.TFrame")
        btn_frame.pack(fill="x", pady=(10, 0))

        ttk.Button(btn_frame, text="PLACE ORDER", command=self.place_order, style="TButton").pack(side="right", fill="x", expand=True, padx=(5, 0), ipady=5)
        ttk.Button(btn_frame, text="Cancel", command=lambda: self.controller.show_frame("CartFrame"), style="Link.TButton").pack(side="left", padx=(0, 5))

    def setup_success_view(self, order_id):
        # Clear existing widgets
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # Success Icon/Text
        ttk.Label(self.main_container, text="🎉", font=("Helvetica", 48), background=theme.Colors.CARD_BG).pack(pady=(0, 10))
        ttk.Label(self.main_container, text="Order Placed Successfully!", style="Header.TLabel").pack(pady=(0, 10))
        
        ttk.Label(self.main_container, text=f"Order ID: #{order_id}", style="Card.TLabel", font=theme.Fonts.SUBHEADER).pack(pady=(0, 20))
        
        ttk.Label(self.main_container, text="Thank you for shopping with us.", style="Card.TLabel").pack(pady=(0, 30))

        ttk.Button(self.main_container, text="Continue Shopping", 
                   command=lambda: self.controller.show_frame("ProductListFrame"), 
                   style="TButton").pack(fill="x", ipady=5)

    def place_order(self):
        # 1. Validate Form
        address = self.address_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not address or not phone:
            messagebox.showwarning("Missing Details", "Please provide your shipping address and phone number.")
            return

        # 2. Process Order
        try:
            # In a real app, we'd save address/phone to the Order record here
            order_id = services.checkout()
            
            # 3. Show Success Screen
            self.setup_success_view(order_id)
            
        except Exception as e:
            messagebox.showerror("Checkout Failed", str(e))

