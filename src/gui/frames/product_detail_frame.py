import tkinter as tk
from tkinter import ttk, messagebox
from src.core import services
from src.gui import theme
from src.gui.utils import load_local_image

class ProductDetailFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Main container
        self.container = ttk.Frame(self, style="Card.TFrame", padding=20)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        self.container.columnconfigure(0, weight=1) # Image column
        self.container.columnconfigure(1, weight=1) # Details column

        # --- LEFT COLUMN: IMAGE ---
        self.image_frame = ttk.Frame(self.container, style="Card.TFrame")
        self.image_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        self.image_label = ttk.Label(self.image_frame, text="No Image")
        self.image_label.pack(expand=True)

        # --- RIGHT COLUMN: DETAILS ---
        self.details_frame = ttk.Frame(self.container, style="Card.TFrame")
        self.details_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Title
        self.title_label = ttk.Label(self.details_frame, text="", style="Header.TLabel", wraplength=400)
        self.title_label.pack(anchor="w", pady=(0, 10))

        # Price
        self.price_label = tk.Label(self.details_frame, text="", font=("Helvetica", 24, "bold"), 
                                    fg=theme.Colors.PRIMARY, bg=theme.Colors.CARD_BG)
        self.price_label.pack(anchor="w", pady=(0, 20))

        # Description
        self.desc_label = ttk.Label(self.details_frame, text="", style="Card.TLabel", 
                                    wraplength=400, justify="left")
        self.desc_label.pack(anchor="w", pady=(0, 20))

        # Quantity and Actions
        action_frame = ttk.Frame(self.details_frame, style="Card.TFrame")
        action_frame.pack(anchor="w", pady=20)

        ttk.Label(action_frame, text="Quantity:", style="Card.TLabel").pack(side="left", padx=(0, 10))
        
        self.quantity_var = tk.IntVar(value=1)
        self.quantity_spinbox = ttk.Spinbox(action_frame, from_=1, to=10, textvariable=self.quantity_var, width=5)
        self.quantity_spinbox.pack(side="left", padx=(0, 20))
        
        self.add_cart_btn = ttk.Button(action_frame, text="🛒 Add to Cart", style="Primary.TButton", 
                                       command=self.add_to_cart)
        self.add_cart_btn.pack(side="left")

        # Back button at top-left of the main frame
        self.back_btn = ttk.Button(self, text="← Back to Products", style="Secondary.TButton",
                                   command=lambda: controller.show_frame("ProductListFrame"))
        self.back_btn.place(x=20, y=10) # Fixed position for back button

        # Current product
        self.current_product = None

    def show_product(self, product_id):
        try:
            product = services.get_product(product_id)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load product: {e}")
            return

        self.current_product = product
        self.title_label.config(text=product["name"])
        self.price_label.config(text=f"${product['price']:.2f}")
        self.desc_label.config(text=product["description"])

        # Reset quantity
        self.quantity_var.set(1)

        # Load local image
        self.image_label.config(image="", text="Loading...")
        
        image_url = product.get("image_url", None)
        # Use a larger size for detail view
        photo = load_local_image(image_url, size=(500, 500))
        
        if photo:
            self.product_image = photo # Keep reference
            self.image_label.config(image=photo, text="")
        else:
            self.image_label.config(text="No Image", image="")

    def add_to_cart(self):
        if self.current_product is None:
            return
        try:
            qty = self.quantity_var.get()
            services.add_to_cart(self.current_product["id"], qty)
            messagebox.showinfo("Success", "Product added to cart!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh(self):
        """Called when frame is shown"""
        if hasattr(self.controller, 'current_product_id'):
            product_id = self.controller.current_product_id
            if product_id:
                self.show_product(product_id)
