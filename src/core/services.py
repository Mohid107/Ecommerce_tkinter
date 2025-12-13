from src.data.models import User, Product, CartItem, Order, OrderItem
from src.data.db import db

# -------------------------------
# GLOBAL CART (for current session)
# -------------------------------
current_user = None
cart = []   # list of CartItem objects


# -------------------------------
# USER AUTHENTICATION
# -------------------------------
def login(username: str, password: str):
    global current_user
    # Get user from database
    user = User.get_by_username(username)
    if user is None:
        raise ValueError("User does not exist.")

    if user["password"] != password:
        raise ValueError("Incorrect password.")

    current_user = user
    return True


def signup(username: str, password: str):
    # Check if username already exists
    user = User.get_by_username(username)
    if user:
        raise ValueError("Username already exists.")

    # Create new user
    success = User.create(username, password)
    return success


# -------------------------------
# PRODUCT OPERATIONS
# -------------------------------
def get_all_products():
    return Product.get_all()


def get_product(product_id: int):
    product = Product.get(product_id)
    if not product:
        raise ValueError("Product not found.")
    return product


# -------------------------------
# CART OPERATIONS
# -------------------------------
def add_to_cart(product_id: int, quantity: int = 1):
    """Adds item to in-memory cart"""
    product = Product.get(product_id)
    if not product:
        raise ValueError("Product does not exist.")

    # Check if already in cart
    for item in cart:
        if item.product_id == product_id:
            item.quantity += quantity
            return True

    # Add as new item
    cart.append(CartItem(product_id, quantity))
    return True


def remove_from_cart(product_id: int):
    global cart
    cart = [item for item in cart if item.product_id != product_id]


def update_cart_quantity(product_id: int, new_quantity: int):
    for item in cart:
        if item.product_id == product_id:
            if new_quantity <= 0:
                remove_from_cart(product_id)
            else:
                item.quantity = new_quantity
            return True
    raise ValueError("Item not found in cart.")


def get_cart_items():
    """Return cart items with full product details."""
    detailed = []
    for item in cart:
        p = Product.get(item.product_id)
        detailed.append({
            "product_id": item.product_id,
            "name": p["name"],
            "price": p["price"],
            "quantity": item.quantity,
            "total": p["price"] * item.quantity
        })
    return detailed


def get_cart_total():
    return sum(item["total"] for item in get_cart_items())


# -------------------------------
# CHECKOUT OPERATIONS
# -------------------------------
def checkout():
    if current_user is None:
        raise ValueError("User not logged in.")

    if not cart:
        raise ValueError("Cart is empty.")

    total_amount = get_cart_total()

    # Create order record
    order_id = Order.create(current_user["id"], total_amount)
    if not order_id:
        raise RuntimeError("Failed to create order.")

    # Insert each cart item
    for item in cart:
        OrderItem.create(order_id, item.product_id, item.quantity)

    # Clear cart after checkout
    cart.clear()

    return order_id


# -------------------------------
# USER ORDER HISTORY
# -------------------------------
def get_user_orders():
    if current_user is None:
        raise ValueError("User not logged in.")
    return Order.get_by_user(current_user["id"])


# Add these methods to services.py

def update_password(new_password):
    """Update current user's password"""
    global current_user
    if current_user is None:
        raise ValueError("No user logged in")

    # Update in database
    query = "UPDATE Users SET password = ? WHERE user_id = ?"
    from src.data.db import db
    db.execute(query, (new_password, current_user["id"]))

    # Update current_user in memory
    current_user["password"] = new_password
    return True


def get_current_user():
    """Get current logged in user"""
    return current_user
