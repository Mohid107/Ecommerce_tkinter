
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from src.gui import theme
from src.core import services
from src.gui.utils import setup_scroll, load_local_image

class HomeFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # --- TOP HEADER (Hero Section) ---
        hero_frame = tk.Frame(self, bg=theme.Colors.PRIMARY, height=150)
        hero_frame.pack(fill="x")
        hero_frame.pack_propagate(False) # Force height

        # Hero Content
        hero_content = tk.Frame(hero_frame, bg=theme.Colors.PRIMARY)
        hero_content.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(hero_content, text="SUMMER COLLECTION 2024", 
                 font=("Helvetica", 24, "bold"), fg="white", bg=theme.Colors.PRIMARY).pack(pady=(0, 10))
        tk.Label(hero_content, text="Discover the latest trends in fashion and technology.",
                 font=("Helvetica", 14), fg="#EAECEE", bg=theme.Colors.PRIMARY).pack(pady=(0, 20))
        
        shop_btn = tk.Button(hero_content, text="SHOP NOW", 
                             font=("Helvetica", 12, "bold"), bg=theme.Colors.ACCENT, fg="white",
                             activebackground="#CA6F1E", activeforeground="white", relief="flat",
                             padx=20, pady=10, command=lambda: controller.show_frame("ProductListFrame"))
        shop_btn.pack()

        # --- QUICK NAV ---
        # (Optional, maybe below hero or just rely on hero button. Let's keep it simple and clean as requested)

        # --- FEATURED PRODUCTS SECTION ---
        # Scrollable Container for Featured Products
        container = ttk.Frame(self, style="TFrame")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        self.canvas = tk.Canvas(container, bg=theme.Colors.BACKGROUND, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.featured_frame = ttk.Frame(self.canvas, style="TFrame")

        self.featured_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        
        # Center content
        self.window_id = self.canvas.create_window((0, 0), window=self.featured_frame, anchor="n")
        
        def _configure_window(event):
            self.canvas.itemconfig(self.window_id, width=event.width)
        self.canvas.bind("<Configure>", _configure_window)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Enable mouse wheel scrolling
        setup_scroll(self.canvas)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.load_featured_products()

    def load_featured_products(self):
        for widget in self.featured_frame.winfo_children():
            widget.destroy()

        # Load more products (e.g. 10)
        products = services.get_all_products()
        if not products:
            return

        # Shuffle or just take first 10
        import random
        random.shuffle(products)
        products = products[:10]
        
        # Grid layout for Featured (2 columns)
        for i, p in enumerate(products):
            row = i // 2
            col = i % 2
            
            # Card Frame
            card = ttk.Frame(self.featured_frame, style="Card.TFrame", padding=15)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.featured_frame.columnconfigure(0, weight=1)
            self.featured_frame.columnconfigure(1, weight=1)

            # Horizontal Layout inside card
            # Left: Image placeholder
            img_label = tk.Label(card, bg="#eee", width=15, height=8)
            img_label.pack(side="left", padx=(0, 15))
            
            # Load local image directly
            # Expecting p['image_url'] to be just the filename now (e.g., "headphones.jpg")
            photo = load_local_image(p['image_url'], size=(100, 100))
            if photo:
                img_label.config(image=photo, width=0, height=0)
                img_label.image = photo # Keep reference
            else:
                img_label.config(text="No Image")

            # Right: Info
            info = ttk.Frame(card, style="Card.TFrame")
            info.pack(side="left", fill="both", expand=True)
            
            ttk.Label(info, text=p['name'], style="CardTitle.TLabel").pack(anchor="w")
            ttk.Label(info, text=f"${p['price']:.2f}", style="CardPrice.TLabel").pack(anchor="w", pady=(5, 10))
            
            ttk.Button(info, text="Add to Cart", style="Primary.TButton",
                       command=lambda pid=p['id']: self.add_to_cart(pid)).pack(anchor="w")

    def add_to_cart(self, product_id):
        try:
            services.add_to_cart(product_id)
            messagebox.showinfo("Cart", "Product added to cart!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
