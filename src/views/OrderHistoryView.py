import tkinter as tk
from tkinter import ttk, messagebox
from src.constants import ViewNames
from src import theme
from src.utils import setup_scroll

class OrderHistoryView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.order_service = self.controller.order_service
        self.user_service = self.controller.user_service
        self.configure(style="TFrame")
        
        self._setup_ui()

    def _setup_ui(self):
        # Nav Header
        nav = ttk.Frame(self, style="TFrame")
        nav.pack(fill="x", padx=20, pady=10)
        ttk.Button(nav, text="← Back to Products", style="Secondary.TButton",
                   command=lambda: self.controller.show_view(ViewNames.PRODUCT_LIST)).pack(side="left")

        ttk.Label(self, text="My Orders", style="Title.TLabel").pack(pady=10)

        # Scrollable container
        self.canvas_container = ttk.Frame(self, style="TFrame")
        self.canvas_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.canvas = tk.Canvas(self.canvas_container, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.canvas_container, orient="vertical", command=self.canvas.yview)
        
        self.list_frame = ttk.Frame(self.canvas, style="TFrame")
        
        # Configure scroll
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack scrolling elements
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create window in canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        
        # Bind events
        self.list_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Enable mousewheel
        setup_scroll(self.canvas)

    def _on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        # Resize list_frame to match canvas width
        width = event.width
        self.canvas.itemconfigure(self.canvas_window, width=width)

    def load_orders(self):
        for w in self.list_frame.winfo_children(): w.destroy()
        
        try:
            orders = self.order_service.get_user_orders(self.user_service)
        except Exception as e:
            ttk.Label(self.list_frame, text=f"Error: {e}", style="Label.TLabel").pack()
            return

        if not orders:
            ttk.Label(self.list_frame, text="No orders found.", style="Label.TLabel").pack(pady=20)
            return

        for order in orders:
            card = ttk.Frame(self.list_frame, style="Card.TFrame", padding=15)
            card.pack(fill="x", pady=5)
            
            # Header
            header = ttk.Frame(card, style="TFrame")
            header.pack(fill="x")
            
            ttk.Label(header, text=f"Order #{order['id']}", style="CardTitle.TLabel").pack(side="left")
            ttk.Label(header, text=str(order['date']), style="Label.TLabel").pack(side="right")
            
            # Details
            ttk.Separator(card, orient="horizontal").pack(fill="x", pady=5)
            ttk.Label(card, text=f"Total Amount: ${order['total_amount']:.2f}", style="CardPrice.TLabel").pack(anchor="e")

    def refresh(self):
        self.load_orders()
