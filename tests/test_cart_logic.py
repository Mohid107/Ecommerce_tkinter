import pytest
from src.services.CartService import CartService
from src.services.OrderService import OrderService
from src.services.UserService import UserService
from src.models import Product

@pytest.fixture
def product_service_mock(mocker):
    return mocker.patch('src.services.CartService.ProductService')

@pytest.fixture
def cart_service(product_service_mock):
    # We mock the ProductService that CartService uses internally
    service = CartService()
    service.product_service = mocker_product_service_instance(product_service_mock)
    return service

def mocker_product_service_instance(mock_class):
    # Helper to setup the mock instance returned by the class constructor
    instance = mock_class.return_value
    return instance

@pytest.fixture
def mock_product(mocker):
    # This mocks the Product model itself if needed, but CartService uses ProductService
    # In integration we'd mock ProductService to return dicts simulating products
    pass

def test_add_to_cart_new_item(cart_service):
    """Test adding a new item to the cart"""
    # Setup mock product service response
    cart_service.product_service.get_product.return_value = {"id": 1, "name": "Test Product", "price": 100}
    
    assert cart_service.add_to_cart(1, 2) is True
    assert len(cart_service.cart) == 1
    assert cart_service.cart[0].product_id == 1
    assert cart_service.cart[0].quantity == 2

def test_add_to_cart_existing_item(cart_service):
    """Test adding an item that is already in the cart"""
    cart_service.product_service.get_product.return_value = {"id": 1, "name": "Test Product", "price": 100}
    
    cart_service.add_to_cart(1, 1)
    cart_service.add_to_cart(1, 2)
    
    assert len(cart_service.cart) == 1
    assert cart_service.cart[0].quantity == 3

def test_add_to_cart_invalid_product(cart_service):
    """Test adding a non-existent product"""
    cart_service.product_service.get_product.return_value = None
    
    with pytest.raises(ValueError, match="Product does not exist"):
        cart_service.add_to_cart(999)

def test_remove_from_cart(cart_service):
    """Test removing an item from the cart"""
    cart_service.product_service.get_product.return_value = {"id": 1, "name": "Product", "price": 10}
    cart_service.add_to_cart(1)
    
    cart_service.remove_from_cart(1)
    assert len(cart_service.cart) == 0

def test_update_cart_quantity(cart_service):
    """Test updating item quantity"""
    cart_service.product_service.get_product.return_value = {"id": 1, "name": "Product", "price": 10}
    cart_service.add_to_cart(1, 1)
    
    cart_service.update_cart_quantity(1, 5)
    assert cart_service.cart[0].quantity == 5
    
    # Test setting to 0 removes item
    cart_service.update_cart_quantity(1, 0)
    assert len(cart_service.cart) == 0

def test_get_cart_items(cart_service):
    """Test retrieving detailed cart items"""
    cart_service.product_service.get_product.return_value = {"id": 1, "name": "Test Product", "price": 100}
    cart_service.add_to_cart(1, 2)
    
    items = cart_service.get_cart_items()
    assert len(items) == 1
    assert items[0]['name'] == "Test Product"
    assert items[0]['total'] == 200

def test_cart_total_calculation(cart_service):
    """Test cart total calculation with multiple items"""
    # Mock product returns based on input ID
    def get_product_side_effect(product_id):
        products = {
            1: {"id": 1, "name": "P1", "price": 10.0},
            2: {"id": 2, "name": "P2", "price": 20.0}
        }
        return products.get(product_id)
    
    cart_service.product_service.get_product.side_effect = get_product_side_effect
    
    cart_service.add_to_cart(1, 2) # 2 * 10 = 20
    cart_service.add_to_cart(2, 1) # 1 * 20 = 20
    
    total = cart_service.get_cart_total()
    assert total == 40.0

def test_cart_clearing(cart_service):
    """Test explicit cart clearing"""
    cart_service.cart.append("item")
    assert len(cart_service.cart) > 0
    
    cart_service.clear_cart()
    
    assert len(cart_service.cart) == 0

def test_checkout_success(mocker, cart_service):
    """Test successful checkout"""
    # Mocks
    mock_order = mocker.patch('src.services.OrderService.Order')
    mock_order_item = mocker.patch('src.services.OrderService.OrderItem')
    
    user_service = mocker.Mock(spec=UserService)
    user_service.get_current_user.return_value = {"id": 1, "username": "testuser"}
    
    # Setup Cart
    cart_service.product_service.get_product.side_effect = lambda pid: {"id": pid, "name": "P", "price": 100}
    cart_service.add_to_cart(1, 2)
    
    # Mock order creation
    mock_order.create.return_value = 1001 # Order ID
    
    order_service = OrderService()
    order_id = order_service.checkout(user_service, cart_service)
    
    assert order_id == 1001
    assert len(cart_service.cart) == 0  # Cart should be empty
    mock_order.create.assert_called_once()
    mock_order_item.create.assert_called_once()

def test_checkout_not_logged_in(mocker, cart_service):
    """Test checkout fails when not logged in"""
    user_service = mocker.Mock(spec=UserService)
    user_service.get_current_user.return_value = None
    
    order_service = OrderService()
    
    with pytest.raises(ValueError, match="User not logged in"):
        order_service.checkout(user_service, cart_service)

def test_checkout_empty_cart(mocker, cart_service):
    """Test checkout with empty cart raises error"""
    user_service = mocker.Mock(spec=UserService)
    user_service.get_current_user.return_value = {"id": 1}
    cart_service.clear_cart()
    
    order_service = OrderService()
    
    with pytest.raises(ValueError, match="Cart is empty"):
        order_service.checkout(user_service, cart_service)
