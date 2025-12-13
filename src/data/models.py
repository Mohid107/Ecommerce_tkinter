from src.data.db import db

# -------------------------------
# USER MODEL
# -------------------------------
class User:
    @staticmethod
    def create(username: str, password: str):
        query = "INSERT INTO Users (username, password) VALUES (?, ?)"
        return db.execute(query, (username, password))

    @staticmethod
    def get_by_username(username: str):
        query = "SELECT user_id, username, password FROM Users WHERE username=?"
        rows = db.execute(query, (username,), fetch=True)
        if rows:
            row = rows[0]
            return {"id": row[0], "username": row[1], "password": row[2]}
        return None


# -------------------------------
# PRODUCT MODEL
# -------------------------------
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


# -------------------------------
# CART ITEM (In-memory)
# -------------------------------
class CartItem:
    def __init__(self, product_id: int, quantity: int = 1):
        self.product_id = product_id
        self.quantity = quantity


# -------------------------------
# ORDER MODEL
# -------------------------------
class Order:
    @staticmethod
    def create(user_id: int, total_amount: float):
        query = """
            INSERT INTO Orders (user_id, total_amount)
            OUTPUT INSERTED.order_id
            VALUES (?, ?)
        """
        rows = db.execute(query, (user_id, total_amount), fetch=True)
        if rows:
            return rows[0][0]  # new order ID
        return None

    @staticmethod
    def get_by_user(user_id: int):
        query = "SELECT order_id, user_id, total_amount, date FROM Orders WHERE user_id=?"
        rows = db.execute(query, (user_id,), fetch=True)
        orders = []
        for row in rows:
            orders.append({
                "id": row[0],
                "user_id": row[1],
                "total_amount": row[2],
                "date": row[3],
            })
        return orders


# -------------------------------
# ORDER ITEM MODEL
# -------------------------------
class OrderItem:
    @staticmethod
    def create(order_id: int, product_id: int, quantity: int):
        # Must match your SQL table name: Order_Items
        query = """
            INSERT INTO Order_Items (order_id, product_id, quantity, price)
            VALUES (
                ?, ?, ?, 
                (SELECT price FROM Products WHERE product_id = ?)
            )
        """
        return db.execute(query, (order_id, product_id, quantity, product_id))
