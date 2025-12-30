import tkinter as tk
from tkinter import ttk, messagebox
from src.constants import AppConstants, Messages, ViewNames
from src import theme
from src.utils import setup_scroll, load_local_image

class ProductView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.product_service = self.controller.product_service
        self.cart_service = self.controller.cart_service
        
        self.configure(style="TFrame")
        self._setup_ui()
        self.load_products()

    def _setup_ui(self):
        # Nav Header
        nav_frame = ttk.Frame(self, style="TFrame")
        nav_frame.pack(fill="x", padx=20, pady=10)

        buttons = [
            ("🏠 Home", ViewNames.HOME), # Note: HomeView might need creation or reuse
            ("🛒 Cart", ViewNames.CART),
            ("👤 Profile", ViewNames.PROFILE),
            ("📋 Orders", ViewNames.ORDER_HISTORY),
            ("🛒 Checkout", ViewNames.CHECKOUT)
        ]
        
        for text, view_name in buttons:
             ttk.Button(nav_frame, text=text,
                       command=lambda vn=view_name: self.controller.show_view(vn)).pack(side="left", padx=5)

        # Title
        ttk.Label(self, text="📦 Products", style="Title.TLabel").pack(pady=10)

        # Content Area
        self.products_canvas = tk.Canvas(self, bg=theme.Colors.BACKGROUND, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.products_canvas.yview)
        self.products_frame = ttk.Frame(self.products_canvas, style="TFrame")

        self.products_frame.bind(
            "<Configure>",
            lambda e: self.products_canvas.configure(scrollregion=self.products_canvas.bbox("all"))
        )
        
        self.window_id = self.products_canvas.create_window((0, 0), window=self.products_frame, anchor="n")
        self.products_canvas.bind("<Configure>", lambda e: self.products_canvas.itemconfig(self.window_id, width=e.width))
        self.products_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        setup_scroll(self.products_canvas)
        
        self.products_canvas.pack(side="left", fill="both", expand=True, padx=(20, 0))
        self.scrollbar.pack(side="right", fill="y", padx=(0, 20))

    def load_products(self):
        try:
            products = self.product_service.get_all_products()
            self._display_products(products)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load products: {e}")

    def _display_products(self, products):
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        if not products:
            ttk.Label(self.products_frame, text="No products available", style="CardDesc.TLabel").pack(pady=20)
            return

        row, col = 0, 0
        for p in products:
            self._create_product_card(p, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1
        
        # Configure weights
        for i in range(3):
            self.products_frame.grid_columnconfigure(i, weight=1)

    def _create_product_card(self, p, row, col):
        card = ttk.Frame(self.products_frame, style="Card.TFrame", padding=15)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # Icon
        icon_frame = ttk.Frame(card, style="Card.TFrame")
        icon_frame.pack(pady=(0, 10))
        
        img_label = tk.Label(icon_frame, bg="#eee", width=20, height=10)
        img_label.pack()
        photo = load_local_image(p['image_url'], size=(150, 150))
        if photo:
            img_label.config(image=photo, width=0, height=0)
            img_label.image = photo 
        else:
            img_label.config(text="No Image")

        # Info
        info_frame = ttk.Frame(card, style="TFrame")
        info_frame.pack(fill="both", expand=True)
        
        name = p["name"]
        if len(name) > 25: name = name[:22] + "..."
        ttk.Label(info_frame, text=name, style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(info_frame, text=f"💰 ${p['price']:.2f}", style="CardPrice.TLabel").pack(anchor="w", pady=5)
        
        stock = p.get("stock", 0)
        stock_text = f"📦 {stock} left" if stock > 0 else "❌ Out of Stock"
        ttk.Label(info_frame, text=stock_text, style="CardDesc.TLabel", 
                 foreground=theme.Colors.SUCCESS if stock > 0 else theme.Colors.ERROR).pack(anchor="w", pady=(0, 10))

        # Buttons
        btn_frame = ttk.Frame(card, style="TFrame")
        btn_frame.pack(fill="x", pady=(5, 0))
        
        ttk.Button(btn_frame, text="🛒 Add to Cart", style="Primary.TButton",
                  command=lambda pid=p['id']: self.add_to_cart(pid)).pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ttk.Button(btn_frame, text="👁️", style="Secondary.TButton", width=3,
                  command=lambda pid=p['id']: self.view_details(pid)).pack(side="right")

    def add_to_cart(self, product_id):
        try:
            self.cart_service.add_to_cart(product_id)
            messagebox.showinfo("Success", Messages.ADD_TO_CART_SUCCESS)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_details(self, product_id):
        self.controller.current_product_id = product_id
        self.controller.show_view(ViewNames.PRODUCT_DETAIL)
    
    def refresh(self):
        self.load_products()
