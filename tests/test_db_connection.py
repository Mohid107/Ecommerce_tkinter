import pytest
from src.data.db import Database

def test_database_connect_success(mock_pyodbc):
    """Test successful database connection"""
    db = Database()
    mock_pyodbc.connect.assert_called_once()
    assert db.connection is not None

def test_database_connect_failure(mock_pyodbc, capsys):
    """Test database connection failure"""
    mock_pyodbc.connect.side_effect = Exception("Connection failed")
    db = Database()
    captured = capsys.readouterr()
    assert "Database connection error" in captured.out
    assert db.connection is None

def test_execute_query_no_params(mock_pyodbc):
    """Test executing a query without parameters"""
    db = Database()
    mock_cursor = db.connection.cursor.return_value
    
    db.execute("SELECT * FROM Users")
    mock_cursor.execute.assert_called_with("SELECT * FROM Users")
    db.connection.commit.assert_called_once()

def test_execute_query_with_params(mock_pyodbc):
    """Test executing a query with parameters"""
    db = Database()
    mock_cursor = db.connection.cursor.return_value
    
    db.execute("INSERT INTO Users VALUES (?)", ("test",))
    mock_cursor.execute.assert_called_with("INSERT INTO Users VALUES (?)", ("test",))
    db.connection.commit.assert_called_once()

def test_execute_fetch_results(mock_pyodbc):
    """Test executing a query that returns results"""
    db = Database()
    mock_cursor = db.connection.cursor.return_value
    mock_cursor.fetchall.return_value = [("user1",)]
    
    result = db.execute("SELECT username FROM Users", fetch=True)
    assert result == [("user1",)]
    mock_cursor.fetchall.assert_called_once()


# ----------------------------------------------------------------
# Extended Model Tests (User, Product, Order)
# ----------------------------------------------------------------
from src.data.models import User, Product, Order

def test_user_creation(mock_db):
    """Test User.create method"""
    # Reset not strictly needed due to fresh mock per test, but we can do:
    mock_db.execute.reset_mock()

    
    mock_db.execute.return_value = True
    result = User.create("newuser", "pass123")
    
    assert result is True
    mock_db.execute.assert_called_with(
        "INSERT INTO Users (username, password) VALUES (?, ?)", 
        ("newuser", "pass123")
    )

def test_user_get_by_username_found(mock_db):
    """Test retrieving an existing user"""
    # Mock return value: list of tuples (id, username, password)
    mock_db.execute.return_value = [(1, "user1", "pass1")]
    
    user = User.get_by_username("user1")
    assert user is not None
    assert user["id"] == 1
    assert user["username"] == "user1"

def test_user_get_by_username_not_found(mock_db):
    """Test retrieving a non-existent user"""
    mock_db.execute.return_value = [] # Empty list
    
    user = User.get_by_username("ghost")
    assert user is None

def test_product_create(mock_db):
    """Test Product.create"""
    mock_db.execute.return_value = True
    Product.create("P1", 10.0, "Desc", 5, "img.jpg")
    
    # Verify call args roughly (checking first arg contains INSERT)
    args = mock_db.execute.call_args[0]
    assert "INSERT INTO Products" in args[0]
    assert args[1] == ("P1", 10.0, "Desc", 5, "img.jpg")

def test_product_get_all(mock_db):
    """Test retrieving all products"""
    mock_db.execute.return_value = [
        (1, "Store Item", 99.99, "Description", 10, "url.jpg")
    ]
    
    products = Product.get_all()
    assert len(products) == 1
    assert products[0]["name"] == "Store Item"

def test_order_create(mock_db):
    """Test creating an order"""
    # Mocking that the query returns the new ID
    mock_db.execute.return_value = [(100,)] 
    
    order_id = Order.create(user_id=1, total_amount=50.0)
    assert order_id == 100

