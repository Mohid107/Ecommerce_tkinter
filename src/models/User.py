from src.db import db

class User:
    @staticmethod
    def create(username: str, password: str, first_name: str = None, last_name: str = None, phone: str = None, email: str = None, dob: str = None):
        query = "INSERT INTO Users (username, password, first_name, last_name, phone, email, dob) VALUES (?, ?, ?, ?, ?, ?, ?)"
        return db.execute(query, (username, password, first_name, last_name, phone, email, dob))

    @staticmethod
    def get_by_username(username: str):
        query = "SELECT user_id, username, password, first_name, last_name, phone, email, dob, role FROM Users WHERE username=?"
        rows = db.execute(query, (username,), fetch=True)
        if rows:
            row = rows[0]
            # Handle potential None for new columns if user was created before schema update (though we only have new users or empty db)
            return {
                "id": row[0], 
                "username": row[1], 
                "password": row[2],
                "first_name": row[3],
                "last_name": row[4],
                "phone": row[5],
                "email": row[6],
                "dob": row[7] if len(row) > 7 else None,
                "role": row[8] if len(row) > 8 else 'user' 
            }
        return None
