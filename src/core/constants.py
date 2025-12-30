class AppConstants:
    APP_TITLE = "ShopEasy Desktop App"
    APP_VERSION = "1.0.0"
    WINDOW_WIDTH = 1024
    WINDOW_HEIGHT = 768
    
class Messages:
    LOGIN_SUCCESS = "Successfully logged in!"
    LOGIN_FAILED = "Invalid username or password."
    SIGNUP_SUCCESS = "Account created successfully!"
    SIGNUP_FAILED = "Username already exists."
    ADD_TO_CART_SUCCESS = "✅ Product added to cart!"
    ADD_TO_CART_FAILED = "Failed to add to cart"
    CHECKOUT_SUCCESS = "Order placed successfully! Order ID: {order_id}"
    CHECKOUT_EMPTY = "Cart is empty."
    CHECKOUT_NO_USER = "User not logged in."
    
class ViewNames:
    LOGIN = "LoginView"
    SIGNUP = "SignupView"
    HOME = "HomeView"
    PRODUCT_LIST = "ProductListView"
    PRODUCT_DETAIL = "ProductDetailView"
    CART = "CartView"
    CHECKOUT = "CheckoutView"
    ORDER_HISTORY = "OrderHistoryView"
    PROFILE = "ProfileView"
