import pytest
from unittest.mock import MagicMock, patch
from src.exceptions import DatabaseError, AuthenticationError
from src.db import Database
from src.services.UserService import UserService

# ----------------------------------------------------------------
# Database Tests
# ----------------------------------------------------------------

def test_db_retry_success(mocker):
    """Test that DB connects eventually after retries"""
    # 1. Instantiate DB without triggering the real connect()
    with patch("src.db.Database.connect"):
        db = Database()
        
    # 2. Setup the mock for the actual test
    mock_odbc_connect = mocker.patch("pyodbc.connect")
    # Fail twice, then succeed
    mock_odbc_connect.side_effect = [Exception("Fail 1"), Exception("Fail 2"), MagicMock()]
    
    # 3. Call connect() manually and verify retries
    with patch("time.sleep"): # Don't wait in tests
        db.connect(retries=3)
        
    assert mock_odbc_connect.call_count == 3

def test_db_retry_failure(mocker):
    """Test that DB raises DatabaseError after max retries"""
    with patch("src.db.Database.connect"):
        db = Database()

    mock_odbc_connect = mocker.patch("pyodbc.connect")
    mock_odbc_connect.side_effect = Exception("Always Fail")
    
    with patch("time.sleep"): 
        with pytest.raises(DatabaseError) as exc:
            db.connect(retries=3)
    
    assert "Failed to connect" in str(exc.value)

# ----------------------------------------------------------------
# Service Tests
# ----------------------------------------------------------------

def test_user_service_auth_error(mocker):
    """Test UserService raises AuthenticationError"""
    mock_user_model = mocker.patch("src.services.UserService.User")
    mock_user_model.get_by_username.return_value = None # User not found
    
    service = UserService()
    
    with pytest.raises(AuthenticationError) as exc:
        service.login("unknown", "password")
        
    assert "User does not exist" in str(exc.value)
