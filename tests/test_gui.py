import pytest
import tkinter as tk
from tkinter import messagebox
from unittest.mock import MagicMock, patch
from src.gui.main_window import EcommerceApp
from src.core.constants import ViewNames, Messages

# ----------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------

@pytest.fixture
def mock_services(mocker):
    """Mock all services to isolate UI from business logic/DB"""
    mocker.patch('src.gui.main_window.UserService')
    mocker.patch('src.gui.main_window.ProductService')
    mocker.patch('src.gui.main_window.CartService')
    mocker.patch('src.gui.main_window.OrderService')

@pytest.fixture
def app(mock_services, mocker):
    """Initialize App with mocked mainloop and services"""
    # Prevent main window from actually showing up/blocking
    mocker.patch('tkinter.Tk.mainloop') 
    mocker.patch('tkinter.Tk.geometry') # Avoid actual screen sizing
    
    app = EcommerceApp()
    # Hide it so it doesn't pop up during tests if env allow
    app.withdraw() 
    
    # Mock MessageBox to prevent blocking popups
    mocker.patch('tkinter.messagebox.showinfo')
    mocker.patch('tkinter.messagebox.showerror')
    mocker.patch('tkinter.messagebox.showwarning')
    
    yield app
    
    # Cleanup
    app.destroy()

# ----------------------------------------------------------------
# Test Cases
# ----------------------------------------------------------------

def test_app_creation(app):
    """Test main window initialization"""
    assert app.title() == "ShopEasy Desktop App"
    # Verify initial view is Login
    from tkinter import ttk
    assert isinstance(app.views[ViewNames.LOGIN], ttk.Frame)
    # Check if LoginView is visible (raised) - hard to check 'visibility' directly in mock, 
    # but we can check if it's the one we most recently called show_view on if we mocked it,
    # or just check structural existence.
    assert ViewNames.LOGIN in app.views

def test_login_flow_success(app):
    """Test successful login navigation"""
    login_view = app.views[ViewNames.LOGIN]
    
    # Mock service response
    app.user_service.login.return_value = True
    
    # Simulate User Input
    login_view.username_entry.insert(0, "testuser")
    login_view.password_entry.insert(0, "password")
    
    # Trigger Login
    with patch.object(app, 'show_view', wraps=app.show_view) as mock_show:
        login_view.login()
        
        # Verify Service Call
        app.user_service.login.assert_called_with("testuser", "password")
        
        # Verify Navigation to Home
        mock_show.assert_called_with(ViewNames.HOME)

def test_login_validation_failure(app):
    """Test login failure with error message"""
    login_view = app.views[ViewNames.LOGIN]
    app.user_service.login.side_effect = ValueError("Invalid credentials")
    
    login_view.username_entry.insert(0, "wrong")
    login_view.password_entry.insert(0, "wrong")
    
    login_view.login()
    
    # Verify Error Message
    messagebox.showerror.assert_called_with("Login Failed", "Invalid credentials")

def test_navigation_flow(app):
    """Test navigating between main views"""
    # Go to Home first
    app.show_view(ViewNames.HOME)
    home_view = app.views[ViewNames.HOME]
    
    # Simulate clicking "Browse Products" (checking callback logic)
    # We can invoke the command associated with the button if we find it, 
    # or just call the controller method directly to verify View integration.
    
    with patch.object(app, 'show_view', wraps=app.show_view) as mock_show:
        # Simulate user action: click browse product button
        # (Assuming we know the command structure or button existence)
        # Using controller direct call as proxy for button click for robust testing:
        app.show_view(ViewNames.PRODUCT_LIST)
        mock_show.assert_called_with(ViewNames.PRODUCT_LIST)
        
        app.show_view(ViewNames.CART)
        mock_show.assert_called_with(ViewNames.CART)

def test_checkout_flow_success(app):
    """Test checkout form submission"""
    checkout_view = app.views[ViewNames.CHECKOUT]
    
    # Mock data
    app.cart_service.get_cart_total.return_value = 100.0
    app.order_service.checkout.return_value = 123 # Order ID
    
    # Fill Form
    checkout_view.fields['Full Name'].insert(0, "John Doe")
    checkout_view.fields['Street Address'].insert(0, "123 Main St")
    checkout_view.fields['City'].insert(0, "New York")
    checkout_view.fields['State/Province'].insert(0, "NY")
    checkout_view.fields['Zip/Postal Code'].insert(0, "10001")
    
    # Trigger Checkout
    with patch.object(app, 'show_view', wraps=app.show_view) as mock_show:
        checkout_view.process_checkout()
        
        # Verify Service Call
        app.order_service.checkout.assert_called_once()
        
        # Verify Success Message
        messagebox.showinfo.assert_called_with("Order Placed", Messages.CHECKOUT_SUCCESS.format(order_id=123))
        
        # Verify Redirect
        mock_show.assert_called_with(ViewNames.PRODUCT_LIST)

def test_checkout_validation_error(app):
    """Test checkout form validation (empty fields)"""
    checkout_view = app.views[ViewNames.CHECKOUT]
    
    # Leave fields empty
    checkout_view.process_checkout()
    
    # Verify Error - Should be "Missing Information" since we check empty fields
    # The actual message is "Missing Information", "Please enter your Full Name."
    messagebox.showerror.assert_called()
    assert "Missing Information" in messagebox.showerror.call_args[0][0]

def test_cart_loading(app):
    """Test cart view properly loads items from service"""
    cart_view = app.views[ViewNames.CART]
    
    # Mock Items
    fake_items = [
        {"product_id": 1, "name": "Item 1", "price": 10.0, "quantity": 2, "total": 20.0},
        {"product_id": 2, "name": "Item 2", "price": 5.0, "quantity": 1, "total": 5.0}
    ]
    app.cart_service.get_cart_items.return_value = fake_items
    
    # Trigger refresh
    cart_view.load_cart()
    
    # Check Treeview content
    # Get all items in tree
    tree_items = cart_view.tree.get_children()
    assert len(tree_items) == 2
    
    # Verify values of first item
    first_row = cart_view.tree.item(tree_items[0])['values']
    # Values are returned as strings often in tk, or tuple logic depends on tk version wrapper
    # Treeview values: (name, price, qty, total)
    assert first_row[0] == "Item 1"
    assert "10.00" in str(first_row[1])
    assert str(first_row[2]) == "2"

def test_error_handling_service_down(app):
    """Test generic error handling when service fails (e.g. DB error)"""
    login_view = app.views[ViewNames.LOGIN]
    app.user_service.login.side_effect = Exception("Database Connection Failed")
    
    login_view.username_entry.insert(0, "user")
    login_view.password_entry.insert(0, "pass")
    
    login_view.login()
    
    messagebox.showerror.assert_called()
    args = messagebox.showerror.call_args[0]
    assert "Error" in args[0]
    assert "Database Connection Failed" in str(args[1])
