from src.data.models import Product

class ProductService:
    def get_all_products(self):
        return Product.get_all()

    def get_product(self, product_id):
        product = Product.get(product_id)
        if not product:
            raise ValueError("Product not found.")
        return product
