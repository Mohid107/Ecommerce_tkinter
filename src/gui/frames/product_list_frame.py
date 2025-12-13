# src/gui/frames/product_list_frame.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from src.core import services
from src.gui import theme
import requests
from io import BytesIO
import threading


from src.gui.utils import setup_scroll, load_local_image

class ProductListFrame(ttk.Frame):
    def __init__(self, parent, controller):
        # Store controller reference
        self.controller = controller
        self.current_product_id = None
        super().__init__(parent)
        self.configure(style="TFrame")
        self.product_images = {}  # Store references to prevent garbage collection

        # Navigation header
        nav_frame = ttk.Frame(self, style="TFrame")
        nav_frame.pack(fill="x", padx=20, pady=10)

        ttk.Button(nav_frame, text="🏠 Home",
                   command=lambda: controller.show_frame("HomeFrame")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="🛒 Cart",
                   command=lambda: controller.show_frame("CartFrame")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="👤 Profile",
                   command=lambda: controller.show_frame("ProfileFrame")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="📋 Orders",
                   command=lambda: controller.show_frame("OrderHistoryFrame")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="🛒 Checkout",
                   command=lambda: controller.show_frame("CheckoutFrame")).pack(side="left", padx=5)

        # Title
        title = ttk.Label(self, text="📦 Products", style="Title.TLabel")
        title.pack(pady=10)

        # Scrollable canvas for product cards
        self.products_canvas = tk.Canvas(self, bg=theme.Colors.BACKGROUND, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.products_canvas.yview)
        self.products_frame = ttk.Frame(self.products_canvas, style="TFrame")

        self.products_frame.bind(
            "<Configure>",
            lambda e: self.products_canvas.configure(scrollregion=self.products_canvas.bbox("all"))
        )
        
        # Center the window in the canvas
        self.window_id = self.products_canvas.create_window((0, 0), window=self.products_frame, anchor="n")
        
        def _configure_window(event):
            # Update the window width to match the canvas width
            self.products_canvas.itemconfig(self.window_id, width=event.width)
        
        self.products_canvas.bind("<Configure>", _configure_window)
        
        self.products_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Enable mouse wheel scrolling
        setup_scroll(self.products_canvas)
        
        self.products_canvas.pack(side="left", fill="both", expand=True, padx=(20, 0))
        self.scrollbar.pack(side="right", fill="y", padx=(0, 20))

        # Load products immediately (local images are fast)
        self.load_products()

    def load_products(self):
        try:
            products = services.get_all_products()
            self.display_products(products)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load products: {e}")

    def display_products(self, products):
        """Display loaded products in the UI"""
        # Clear existing
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        if not products:
            ttk.Label(self.products_frame, text="No products available",
                      style="CardDesc.TLabel").pack(pady=20)
            return

        # Create grid layout for products (3 per row)
        row, col = 0, 0

        for p in products:
            # Create product card
            card = ttk.Frame(self.products_frame, style="Card.TFrame", padding=15)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            # Configure grid weights
            self.products_frame.grid_columnconfigure(col, weight=1)

            # Product Image
            icon_frame = ttk.Frame(card, style="Card.TFrame")
            icon_frame.pack(pady=(0, 10))

            # Load local image
            # Expecting p['image_url'] to be just the filename now
            img_label = tk.Label(icon_frame, bg="#eee", width=20, height=10)
            img_label.pack()
            
            photo = load_local_image(p['image_url'], size=(150, 150))
            if photo:
                img_label.config(image=photo, width=0, height=0)
                img_label.image = photo 
            else:
                img_label.config(text="No Image")

            # Product Info
            info_frame = ttk.Frame(card, style="TFrame")
            info_frame.pack(fill="both", expand=True)

            # Product name (truncate if too long)
            name = p["name"]
            if len(name) > 25:
                name = name[:22] + "..."
            name_label = ttk.Label(info_frame, text=name, style="CardTitle.TLabel")
            name_label.pack(anchor="w")

            # Price
            price_label = ttk.Label(info_frame, text=f"💰 ${p['price']:.2f}",
                                    style="CardPrice.TLabel")
            price_label.pack(anchor="w", pady=(5, 5))

            # Stock info
            stock = p.get("stock", 0)
            stock_color = theme.Colors.SUCCESS if stock > 10 else theme.Colors.ERROR
            stock_text = f"📦 {stock} left" if stock > 0 else "❌ Out of Stock"
            stock_label = ttk.Label(info_frame, text=stock_text,
                                    style="CardDesc.TLabel", foreground=stock_color)
            stock_label.pack(anchor="w", pady=(0, 10))

            # Buttons frame
            btn_frame = ttk.Frame(card, style="TFrame")
            btn_frame.pack(fill="x", pady=(5, 0))

            # Add to Cart button
            add_btn = ttk.Button(btn_frame, text="🛒 Add to Cart", style="Primary.TButton",
                                 command=lambda pid=p['id']: self.add_to_cart(pid))
            add_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

            # View Details button
            view_btn = ttk.Button(btn_frame, text="👁️", style="Secondary.TButton",
                                  command=lambda pid=p['id']: self.view_product_details(pid),
                                  width=3)
            view_btn.pack(side="right")

            # Configure grid weights for 3 columns (0, 1, 2)
            self.products_frame.grid_columnconfigure(0, weight=1)
            self.products_frame.grid_columnconfigure(1, weight=1)
            self.products_frame.grid_columnconfigure(2, weight=1)

            # Update grid position
            col += 1
            if col >= 3:  # 3 products per row
                col = 0
                row += 1

    def add_to_cart(self, product_id):
        """Add product to cart"""
        try:
            services.add_to_cart(product_id)
            messagebox.showinfo("Success", "✅ Product added to cart!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add to cart: {str(e)}")

    def view_product_details(self, product_id):
        """Navigate to product detail frame"""
        # Store the product ID to view
        self.controller.current_product_id = product_id
        # Navigate to detail frame
        self.controller.show_frame("ProductDetailFrame")

    def refresh(self):
        """Refresh product list"""
        self.load_products()