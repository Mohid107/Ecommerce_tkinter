from src.models import Order, OrderItem

class OrderService:
    def checkout(self, user_service, cart_service):
        user = user_service.get_current_user()
        if user is None:
            raise ValueError("User not logged in.")

        cart_items = cart_service.cart
        if not cart_items:
            raise ValueError("Cart is empty.")

        total_amount = cart_service.get_cart_total()

        # Create order
        order_id = Order.create(user["id"], total_amount)
        if not order_id:
            raise RuntimeError("Failed to create order.")

        # Insert items
        for item in cart_items:
            OrderItem.create(order_id, item.product_id, item.quantity)

        # Clear cart
        cart_service.clear_cart()
        return order_id

    def get_user_orders(self, user_service):
        user = user_service.get_current_user()
        if user is None:
            raise ValueError("User not logged in.")
        return Order.get_by_user(user["id"])
