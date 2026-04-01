"""Tests for smart_crop.auth module."""
import pytest
import os
import tempfile
from smart_crop.auth import AuthManager


class TestAuthManager:
    """Test cases for AuthManager class."""

    def test_init(self):
        """Test AuthManager initialization."""
        auth = AuthManager()
        assert auth is not None
        assert hasattr(auth, 'users_file')

    def test_hash_password(self):
        """Test password hashing."""
        auth = AuthManager()
        password = "test_password_123"
        hashed = auth.hash_password(password)
        assert hashed != password
        assert len(hashed) > 0

    def test_verify_password(self):
        """Test password verification."""
        auth = AuthManager()
        password = "test_password_123"
        hashed = auth.hash_password(password)
        assert auth.verify_password(password, hashed) is True
        assert auth.verify_password("wrong_password", hashed) is False

    def test_create_user(self):
        """Test user creation."""
        auth = AuthManager()
        username = "testuser"
        password = "testpass123"
        result = auth.create_user(username, password)
        assert result is True

    def test_authenticate_user(self):
        """Test user authentication."""
        auth = AuthManager()
        username = "testuser2"
        password = "testpass456"
        auth.create_user(username, password)
        assert auth.authenticate_user(username, password) is True
        assert auth.authenticate_user(username, "wrongpass") is False

    def test_get_user(self):
        """Test getting user information."""
        auth = AuthManager()
        username = "testuser3"
        password = "testpass789"
        auth.create_user(username, password)
        user = auth.get_user(username)
        assert user is not None
        assert user['username'] == username
