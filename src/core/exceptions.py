class AppError(Exception):
    """Base exception for the application."""
    def __init__(self, message, original_exception=None):
        super().__init__(message)
        self.original_exception = original_exception

class DatabaseError(AppError):
    """Raised when a database operation fails."""
    pass

class ValidationError(AppError):
    """Raised when input validation fails."""
    pass

class AuthenticationError(AppError):
    """Raised when authentication fails."""
    pass

class StockError(AppError):
    """Raised when there are inventory issues."""
    pass

class PaymentError(AppError):
    """Raised when payment processing fails."""
    pass
