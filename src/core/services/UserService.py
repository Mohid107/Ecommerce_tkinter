from src.data.models import User
from src.data.db import db
from src.core.exceptions import AuthenticationError, ValidationError

class UserService:
    def __init__(self):
        self.current_user = None

    def login(self, username, password):
        user = User.get_by_username(username)
        if user is None:
            raise AuthenticationError("User does not exist.")
        if user["password"] != password:
            raise AuthenticationError("Incorrect password.")
        self.current_user = user
        return True

    def signup(self, username, password):
        if not username or not password:
             raise ValidationError("Username and password cannot be empty.")
        user = User.get_by_username(username)
        if user:
            raise ValidationError("Username already exists.")
        return User.create(username, password)

    def get_current_user(self):
        return self.current_user

    def logout(self):
        self.current_user = None

    def update_password(self, new_password):
        if self.current_user is None:
            raise ValueError("No user logged in")
        
        query = "UPDATE Users SET password = ? WHERE user_id = ?"
        db.execute(query, (new_password, self.current_user["id"]))
        self.current_user["password"] = new_password
        return True
