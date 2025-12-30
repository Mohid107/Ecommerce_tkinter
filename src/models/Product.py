from src.db import db

class Product:
    @staticmethod
    def create(name: str, price: float, description: str, stock: int, image_url: str):
        query = """
            INSERT INTO Products (name, price, description, stock, image_url) 
            VALUES (?, ?, ?, ?, ?)
        """
        return db.execute(query, (name, price, description, stock, image_url))

    @staticmethod
    def get(product_id: int):
        query = "SELECT * FROM Products WHERE product_id=?"
        rows = db.execute(query, (product_id,), fetch=True)
        if rows:
            row = rows[0]
            return {
                "id": row[0],
                "name": row[1],
                "price": row[2],
                "description": row[3],
                "stock": row[4],
                "image_url": row[5],
            }
        return None

    @staticmethod
    def get_all():
        query = "SELECT * FROM Products"
        rows = db.execute(query, fetch=True)
        products = []
        for row in rows:
            products.append({
                "id": row[0],
                "name": row[1],
                "price": row[2],
                "description": row[3],
                "stock": row[4],
                "image_url": row[5],
            })
        return products
