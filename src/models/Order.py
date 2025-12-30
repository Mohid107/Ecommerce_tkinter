from src.db import db

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
