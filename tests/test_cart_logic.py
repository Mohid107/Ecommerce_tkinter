import pytest
from src.core.services import (
    add_to_cart, remove_from_cart, update_cart_quantity, 
    get_cart_items, get_cart_total, checkout
)
import src.core.services as services

@pytest.fixture
def mock_product(mocker):
    return mocker.patch('src.core.services.Product')

@pytest.fixture
def mock_order(mocker):
    return mocker.patch('src.core.services.Order')

@pytest.fixture
def mock_order_item(mocker):
    return mocker.patch('src.core.services.OrderItem')

def test_add_to_cart_new_item(mock_product):
    """Test adding a new item to the cart"""
    # Setup mock product
    mock_product.get.return_value = {"id": 1, "name": "Test Product", "price": 100}
    
    assert add_to_cart(1, 2) is True
    assert len(services.cart) == 1
    assert services.cart[0].product_id == 1
    assert services.cart[0].quantity == 2

def test_add_to_cart_existing_item(mock_product):
    """Test adding an item that is already in the cart"""
    mock_product.get.return_value = {"id": 1, "name": "Test Product", "price": 100}
    
    add_to_cart(1, 1)
    add_to_cart(1, 2)
    
    assert len(services.cart) == 1
    assert services.cart[0].quantity == 3

def test_add_to_cart_invalid_product(mock_product):
    """Test adding a non-existent product"""
    mock_product.get.return_value = None
    
    with pytest.raises(ValueError, match="Product does not exist"):
        add_to_cart(999)

def test_remove_from_cart(mock_product):
    """Test removing an item from the cart"""
    mock_product.get.return_value = {"id": 1, "name": "Product", "price": 10}
    add_to_cart(1)
    
    remove_from_cart(1)
    assert len(services.cart) == 0

def test_update_cart_quantity(mock_product):
    """Test updating item quantity"""
    mock_product.get.return_value = {"id": 1, "name": "Product", "price": 10}
    add_to_cart(1, 1)
    
    update_cart_quantity(1, 5)
    assert services.cart[0].quantity == 5
    
    # Test setting to 0 removes item
    update_cart_quantity(1, 0)
    assert len(services.cart) == 0

def test_get_cart_items(mock_product):
    """Test retrieving detailed cart items"""
    mock_product.get.return_value = {"id": 1, "name": "Test Product", "price": 100}
    add_to_cart(1, 2)
    
    items = get_cart_items()
    assert len(items) == 1
    assert items[0]['name'] == "Test Product"
    assert items[0]['total'] == 200

def test_checkout_success(mock_product, mock_order, mock_order_item):
    """Test successful checkout"""
    # Login user
    services.current_user = {"id": 1, "username": "testuser"}
    
    # Add items
    mock_product.get.return_value = {"id": 1, "name": "Test Product", "price": 100}
    add_to_cart(1, 2)
    
    # Mock order creation
    mock_order.create.return_value = 1001 # Order ID
    
    order_id = checkout()
    
    assert order_id == 1001
    assert len(services.cart) == 0  # Cart should be empty
    mock_order.create.assert_called_once()
    mock_order_item.create.assert_called_once()

def test_checkout_not_logged_in():
    """Test checkout fails when not logged in"""
    services.current_user = None
    
    with pytest.raises(ValueError, match="User not logged in"):
        checkout()

def test_cart_total_calculation(mock_product):
    """Test cart total calculation with multiple items"""
    # Mock product returns based on input ID
    def get_product_side_effect(product_id):
        products = {
            1: {"id": 1, "name": "P1", "price": 10.0},
            2: {"id": 2, "name": "P2", "price": 20.0}
        }
        return products.get(product_id)
    
    mock_product.get.side_effect = get_product_side_effect
    
    add_to_cart(1, 2) # 2 * 10 = 20
    add_to_cart(2, 1) # 1 * 20 = 20
    
    total = get_cart_total()
    assert total == 40.0

def test_cart_clearing():
    """Test explicit cart clearing"""
    from src.core.services import cart
    # Setup
    services.cart.append("item")
    assert len(services.cart) > 0
    
    # Act
    services.cart.clear()
    
    # Assert
    assert len(services.cart) == 0

def test_checkout_empty_cart():
    """Test checkout with empty cart raises error"""
    services.current_user = {"id": 1}
    # Ensure cart is empty
    services.cart.clear()
    
    with pytest.raises(ValueError, match="Cart is empty"):
        checkout()

