import tkinter as tk
from tkinter import ttk, messagebox
from src.core.constants import ViewNames, Messages
from src.gui import theme
from src.gui.utils import load_local_image

class ProductDetailView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.product_service = self.controller.product_service
        self.cart_service = self.controller.cart_service
        self.configure(style="TFrame")
        self._setup_ui()

    def _setup_ui(self):
        # Back Button
        ttk.Button(self, text="← Back to Products", style="Secondary.TButton",
                   command=lambda: self.controller.show_view(ViewNames.PRODUCT_LIST)).pack(anchor="w", padx=20, pady=20)

        # Content Container
        self.content_frame = ttk.Frame(self, style="TFrame")
        self.content_frame.pack(fill="both", expand=True, padx=40)

    def load_product_details(self):
        # Clear previous
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        product_id = self.controller.current_product_id
        if not product_id:
            return

        try:
            product = self.product_service.get_product(product_id)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        # Layout: Image (Left), Info (Right)
        
        # Image
        img_frame = ttk.Frame(self.content_frame, style="Card.TFrame", padding=10)
        img_frame.pack(side="left", anchor="n", padx=(0, 40))
        
        img_label = tk.Label(img_frame, bg="white", width=40, height=20)
        img_label.pack()
        
        photo = load_local_image(product['image_url'], size=(300, 300))
        if photo:
            img_label.config(image=photo, width=0, height=0)
            img_label.image = photo 
        else:
            img_label.config(text="No Image")

        # Details
        details_frame = ttk.Frame(self.content_frame, style="TFrame")
        details_frame.pack(side="left", fill="both", expand=True)

        ttk.Label(details_frame, text=product['name'], style="Title.TLabel").pack(anchor="w", pady=(0, 10))
        ttk.Label(details_frame, text=f"Price: ${product['price']:.2f}", style="Header.TLabel", foreground=theme.Colors.PRIMARY).pack(anchor="w", pady=(0, 20))
        
        # Description
        ttk.Label(details_frame, text="Description:", style="Label.TLabel").pack(anchor="w")
        
        desc_text = tk.Text(details_frame, height=5, width=40, font=theme.Fonts.BODY, 
                           bg=theme.Colors.BACKGROUND, relief="flat", wrap="word")
        desc_text.insert("1.0", product['description'])
        desc_text.configure(state="disabled")
        desc_text.pack(anchor="w", pady=(5, 20))

        # Stock
        stock = product.get('stock', 0)
        stock_msg = f"In Stock: {stock}" if stock > 0 else "Out of Stock"
        ttk.Label(details_frame, text=stock_msg, style="Label.TLabel").pack(anchor="w", pady=(0, 20))

        # Add to Cart
        if stock > 0:
            ttk.Button(details_frame, text="Add to Cart", style="Primary.TButton",
                      command=lambda: self.add_to_cart(product['id'])).pack(anchor="w")

    def add_to_cart(self, product_id):
        try:
            self.cart_service.add_to_cart(product_id)
            messagebox.showinfo("Success", Messages.ADD_TO_CART_SUCCESS)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh(self):
        self.load_product_details()
