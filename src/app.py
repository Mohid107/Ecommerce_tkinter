import tkinter as tk
from src.constants import AppConstants, ViewNames
from src.theme import Colors

# Services
from src.services.UserService import UserService
from src.services.ProductService import ProductService
from src.services.CartService import CartService
from src.services.OrderService import OrderService

# Views
from src.views.LoginView import LoginView
from src.views.SignupView import SignupView
from src.views.HomeView import HomeView
from src.views.ProductView import ProductView
from src.views.ProductDetailView import ProductDetailView
from src.views.CartView import CartView
from src.views.CheckoutView import CheckoutView
from src.views.OrderHistoryView import OrderHistoryView
from src.views.ProfileView import ProfileView

class EcommerceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # 1. Initialize Services (Dependency Injection Container)
        self.user_service = UserService()
        self.product_service = ProductService()
        self.cart_service = CartService()
        self.order_service = OrderService()
        
        # Shared State for Navigation
        self.current_product_id = None

        # 2. Window Setup
        self.title(AppConstants.APP_TITLE)
        self._center_window(AppConstants.WINDOW_WIDTH, AppConstants.WINDOW_HEIGHT)
        self.configure(bg=Colors.BACKGROUND)

        # 3. View Container
        self.container = tk.Frame(self, bg=Colors.BACKGROUND)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # 4. Initialize Views
        self.views = {}
        
        view_classes = {
            ViewNames.LOGIN: LoginView,
            ViewNames.SIGNUP: SignupView,
            ViewNames.HOME: HomeView,
            ViewNames.PRODUCT_LIST: ProductView,
            ViewNames.PRODUCT_DETAIL: ProductDetailView,
            ViewNames.CART: CartView,
            ViewNames.CHECKOUT: CheckoutView,
            ViewNames.ORDER_HISTORY: OrderHistoryView,
            ViewNames.PROFILE: ProfileView,
        }

        for name, ViewClass in view_classes.items():
            # Inject controller (self) which provides access to services
            view = ViewClass(self.container, self)
            self.views[name] = view
            view.grid(row=0, column=0, sticky="nsew")

        # 5. Start
        self.show_view(ViewNames.LOGIN)

    def show_view(self, view_name):
        """Switch to a different view"""
        if view_name not in self.views:
            raise ValueError(f"View {view_name} not found")
            
        view = self.views[view_name]
        view.tkraise()
        
        # Refresh if view has a refresh method
        if hasattr(view, 'refresh'):
            view.refresh()

    def _center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    app = EcommerceApp()
    app.mainloop()
