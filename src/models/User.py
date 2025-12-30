from src.db import db

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
