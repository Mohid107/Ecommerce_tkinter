import tkinter as tk
from tkinter import ttk
from src.gui.theme import Colors, Fonts
from src.gui.frames.login_frame import LoginFrame
from src.gui.frames.signup_frame import SignupFrame
from src.gui.frames.product_list_frame import ProductListFrame
from src.gui.frames.product_detail_frame import ProductDetailFrame
from src.gui.frames.cart_frame import CartFrame
from src.gui.frames.checkout_frame import CheckoutFrame
from src.gui.frames.order_history_frame import OrderHistoryFrame
from src.gui.frames.profile_frame import ProfileFrame
from src.gui.frames.home_frame import HomeFrame


class EcommerceApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Main window properties
        self.title("ShopEasy Desktop App")
        # Center the window
        window_width = 1024
        window_height = 768
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        center_x = int((screen_width / 2) - (window_width / 2))
        center_y = int((screen_height / 2) - (window_height / 2))
        
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.configure(bg=Colors.BACKGROUND)  # Changed from PRIMARY to BACKGROUND

        # Container to hold all frames
        self.container = tk.Frame(self, bg=Colors.BACKGROUND)  # Changed to BACKGROUND
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Dictionary to store all frames
        self.frames = {}

        # Initialize frames
        frame_classes = (
            LoginFrame,
            SignupFrame,
            HomeFrame,
            ProductListFrame,
            ProductDetailFrame,
            CartFrame,
            CheckoutFrame,
            OrderHistoryFrame,
            ProfileFrame,
        )

        for F in frame_classes:
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the initial frame
        self.show_frame(LoginFrame)

    def show_frame(self, frame_class):
        """Bring the specified frame to the front"""
        if isinstance(frame_class, str):
            # Convert string to class
            frame_mapping = {
                "LoginFrame": LoginFrame,
                "SignupFrame": SignupFrame,
                "HomeFrame": HomeFrame,
                "ProductListFrame": ProductListFrame,
                "ProductDetailFrame": ProductDetailFrame,
                "CartFrame": CartFrame,
                "CheckoutFrame": CheckoutFrame,
                "OrderHistoryFrame": OrderHistoryFrame,
                "ProfileFrame": ProfileFrame,
            }
            frame_class = frame_mapping[frame_class]

        frame = self.frames[frame_class]
        frame.tkraise()

        # Refresh frames that need updating when shown
        if hasattr(frame, 'refresh'):
            frame.refresh()
        elif hasattr(frame, 'load_products'):
            frame.load_products()
        elif hasattr(frame, 'load_cart'):
            frame.load_cart()
        elif hasattr(frame, 'load_profile'):
            frame.load_profile()


# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    app = EcommerceApp()
    app.mainloop()