from src.models import CartItem, Product
from src.services.ProductService import ProductService

class CartService:
    def __init__(self):
        self.cart = [] # List of CartItem objects
        self.product_service = ProductService() # Or inject if preferred, but simple composition works here

    def add_to_cart(self, product_id: int, quantity: int = 1):
        product = self.product_service.get_product(product_id)
        if not product:
            raise ValueError("Product does not exist.")

        for item in self.cart:
            if item.product_id == product_id:
                item.quantity += quantity
                return True
        
        self.cart.append(CartItem(product_id, quantity))
        return True

    def remove_from_cart(self, product_id: int):
        self.cart = [item for item in self.cart if item.product_id != product_id]

    def update_cart_quantity(self, product_id: int, new_quantity: int):
        for item in self.cart:
            if item.product_id == product_id:
                if new_quantity <= 0:
                    self.remove_from_cart(product_id)
                else:
                    item.quantity = new_quantity
                return True
        raise ValueError("Item not found in cart.")

    def get_cart_items(self):
        detailed = []
        for item in self.cart:
            p = self.product_service.get_product(item.product_id)
            detailed.append({
                "product_id": item.product_id,
                "name": p["name"],
                "price": p["price"],
                "quantity": item.quantity,
                "total": p["price"] * item.quantity
            })
        return detailed

    def get_cart_total(self):
        return sum(item["total"] for item in self.get_cart_items())

    def clear_cart(self):
        self.cart.clear()
