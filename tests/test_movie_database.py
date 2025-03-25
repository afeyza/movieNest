import pytest
from unittest.mock import MagicMock
from movieNest.movie_database import Database

@pytest.fixture
def mock_db():
    """ Returns mocked database object"""
    db = Database()
    db.cursor = MagicMock()
    return db

def test_login_user_success(mock_db):
    """ Login must be successful with an existing username-password pair"""
    mock_db.cursor.fetchone.return_value = ("ahmet", "7575")  # User exists
    assert mock_db.login_user("ahmet", "7575") is True

def test_login_user_failure(mock_db):
    """ Login must fail with the wrong username-password pair"""
    mock_db.cursor.fetchone.return_value = None  # User not found
    assert mock_db.login_user("ali", "12345") is False

def test_login_user_db_error(mock_db, capsys):
    """ Should return False and print error message in case of a database error """
    mock_db.cursor.execute.side_effect = Exception("DB error")
    
    result = mock_db.login_user("ahmet", "7575")
    
    assert result is False
    captured = capsys.readouterr()
    assert "DB error" in captured.out
