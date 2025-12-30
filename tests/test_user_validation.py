import pytest
from src.core.services import login, signup, current_user
import src.core.services as services

@pytest.fixture
def mock_user_model(mocker):
    return mocker.patch('src.core.services.User')

def test_login_success(mock_user_model):
    """Test successful login"""
    mock_user_model.get_by_username.return_value = {
        "id": 1, "username": "testuser", "password": "password123"
    }
    
    assert login("testuser", "password123") is True
    assert services.current_user is not None
    assert services.current_user["username"] == "testuser"

def test_login_invalid_user(mock_user_model):
    """Test login with non-existent user"""
    mock_user_model.get_by_username.return_value = None
    
    with pytest.raises(ValueError, match="User does not exist"):
        login("unknown", "pass")

def test_login_wrong_password(mock_user_model):
    """Test login with incorrect password"""
    mock_user_model.get_by_username.return_value = {
        "id": 1, "username": "testuser", "password": "password123"
    }
    
    with pytest.raises(ValueError, match="Incorrect password"):
        login("testuser", "wrongpass")

def test_signup_success(mock_user_model):
    """Test successful signup"""
    mock_user_model.get_by_username.return_value = None # User doesn't exist
    mock_user_model.create.return_value = True
    
    assert signup("newuser", "password123") is True
    mock_user_model.create.assert_called_with("newuser", "password123")

def test_signup_existing_user(mock_user_model):
    """Test signup with existing username"""
    mock_user_model.get_by_username.return_value = {"id": 1}
    
    with pytest.raises(ValueError, match="Username already exists"):
        signup("existinguser", "pass")
