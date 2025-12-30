import pytest
from unittest.mock import MagicMock
import sys
import os

# Add src to path if not already handled by pytest
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture
def mock_db(mocker):
    """Mock the global database object in src.data.db"""
    # Mock the pyodbc connection first so Database() init doesn't fail
    mocker.patch('src.data.db.pyodbc.connect')
    
    # Now mock the db object in all locations where it is imported
    mock_db_instance = MagicMock()
    
    # Patch the original definition
    mocker.patch('src.data.db.db', mock_db_instance)
    
    # Patch the references in other modules
    # Since we refactored models into submodules, we must patch each one
    mocker.patch('src.data.models.User.db', mock_db_instance)
    mocker.patch('src.data.models.Product.db', mock_db_instance)
    mocker.patch('src.data.models.Order.db', mock_db_instance)
    
    # Also patch services if they use it (UserService does)
    mocker.patch('src.core.services.UserService.db', mock_db_instance)
    
    return mock_db_instance

@pytest.fixture
def mock_pyodbc(mocker):
    """Mock the low-level pyodbc module"""
    return mocker.patch('src.data.db.pyodbc')

@pytest.fixture(autouse=True)
def reset_services():
    """
    Since services are now instantiable classes, we don't need to weirdly reset globals.
    But for safety with any legacy singleton usage (if any), we can just pass.
    Ideally tests should now instantiate fresh services.
    """
    pass
