import pytest
from src.core.services.UserService import UserService

@pytest.fixture
def mock_user_model(mocker):
    return mocker.patch('src.core.services.UserService.User')

def test_login_success(mock_user_model):
    """Test successful login"""
    mock_user_model.get_by_username.return_value = {
        "id": 1, "username": "testuser", "password": "password123"
    }
    
    service = UserService()
    assert service.login("testuser", "password123") is True
    assert service.get_current_user() is not None
    assert service.get_current_user()["username"] == "testuser"

def test_login_invalid_user(mock_user_model):
    """Test login with non-existent user"""
    mock_user_model.get_by_username.return_value = None
    
    service = UserService()
    with pytest.raises(ValueError, match="User does not exist"):
        service.login("unknown", "pass")

def test_login_wrong_password(mock_user_model):
    """Test login with incorrect password"""
    mock_user_model.get_by_username.return_value = {
        "id": 1, "username": "testuser", "password": "password123"
    }
    
    service = UserService()
    with pytest.raises(ValueError, match="Incorrect password"):
        service.login("testuser", "wrongpass")

def test_signup_success(mock_user_model):
    """Test successful signup"""
    mock_user_model.get_by_username.return_value = None # User doesn't exist
    mock_user_model.create.return_value = True
    
    service = UserService()
    assert service.signup("newuser", "password123") is True
    mock_user_model.create.assert_called_with("newuser", "password123")

def test_signup_existing_user(mock_user_model):
    """Test signup with existing username"""
    mock_user_model.get_by_username.return_value = {"id": 1}
    
    service = UserService()
    with pytest.raises(ValueError, match="Username already exists"):
        service.signup("existinguser", "pass")
