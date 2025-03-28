import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from jose import jwt
import auth
from auth import UserCreate, UserInDB, TokenData
from fastapi import HTTPException

class TestAuth:
    def setup_method(self):
        auth.users_db = {}  # Reset database before each test
        self.test_user = {
            "username": "testuser",
            "password": "testpass123"
        }
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "testpass123"
        hashed = auth.get_password_hash(password)
        assert hashed != password
        assert auth.verify_password(password, hashed) == True
        assert auth.verify_password("wrongpass", hashed) == False

    def test_get_user(self):
        """Test user retrieval"""
        # Test with non-existent user
        assert auth.get_user("nonexistent") is None
        
        # Test with existing user
        hashed_password = auth.get_password_hash(self.test_user["password"])
        auth.users_db[self.test_user["username"]] = {
            "username": self.test_user["username"],
            "hashed_password": hashed_password
        }
        user = auth.get_user(self.test_user["username"])
        assert user is not None
        assert user.username == self.test_user["username"]

    def test_authenticate_user(self):
        """Test user authentication"""
        # Create test user
        hashed_password = auth.get_password_hash(self.test_user["password"])
        auth.users_db[self.test_user["username"]] = {
            "username": self.test_user["username"],
            "hashed_password": hashed_password
        }
        
        # Test valid credentials
        user = auth.authenticate_user(self.test_user["username"], self.test_user["password"])
        assert isinstance(user, UserInDB)
        assert user.username == self.test_user["username"]
        
        # Test invalid password
        assert auth.authenticate_user(self.test_user["username"], "wrongpass") == False
        
        # Test non-existent user
        assert auth.authenticate_user("nonexistent", "anypass") == False

    def test_create_access_token(self):
        """Test JWT token creation"""
        data = {"sub": self.test_user["username"]}
        
        # Test with default expiration
        token = auth.create_access_token(data)
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        assert payload["sub"] == self.test_user["username"]
        assert "exp" in payload
        
        # Test with custom expiration
        expires = timedelta(minutes=5)
        token = auth.create_access_token(data, expires)
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        assert payload["sub"] == self.test_user["username"]
        assert "exp" in payload

    @pytest.mark.asyncio
    async def test_get_current_user(self):
        """Test current user retrieval from token"""
        # Create test user
        hashed_password = auth.get_password_hash(self.test_user["password"])
        auth.users_db[self.test_user["username"]] = {
            "username": self.test_user["username"],
            "hashed_password": hashed_password
        }
        
        # Create valid token
        token = auth.create_access_token({"sub": self.test_user["username"]})
        user = await auth.get_current_user(token)
        assert user.username == self.test_user["username"]
        
        # Test invalid token
        with pytest.raises(HTTPException) as exc_info:
            await auth.get_current_user("invalid_token")
        assert exc_info.value.status_code == 401
        
        # Test expired token
        expired_token = auth.create_access_token(
            {"sub": self.test_user["username"]},
            timedelta(minutes=-1)
        )
        with pytest.raises(HTTPException) as exc_info:
            await auth.get_current_user(expired_token)
        assert exc_info.value.status_code == 401

    def test_register_endpoint(self, test_client):
        """Test registration endpoint"""
        response = test_client.post(
            "/auth/register",
            json=self.test_user
        )
        assert response.status_code == 200
        assert response.json() == {"message": "User created successfully"}
        
        # Test duplicate registration
        response = test_client.post(
            "/auth/register",
            json=self.test_user
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_login_endpoint(self, test_client):
        """Test login endpoint"""
        # Register user first
        test_client.post("/auth/register", json=self.test_user)
        
        # Test valid login
        response = test_client.post(
            "/auth/token",
            data=self.test_user
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"
        
        # Test invalid password
        response = test_client.post(
            "/auth/token",
            data={
                "username": self.test_user["username"],
                "password": "wrongpass"
            }
        )
        assert response.status_code == 401

    def test_protected_endpoint(self, test_client):
        """Test protected endpoint"""
        # Register and login
        test_client.post("/auth/register", json=self.test_user)
        response = test_client.post("/auth/token", data=self.test_user)
        token = response.json()["access_token"]
        
        # Test with valid token
        response = test_client.get(
            "/auth/protected",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["message"] == f"Hello {self.test_user['username']}"
        
        # Test without token
        response = test_client.get("/auth/protected")
        assert response.status_code == 401
        
        # Test with invalid token
        response = test_client.get(
            "/auth/protected",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401

@pytest.fixture
def test_client():
    from main import app
    return TestClient(app)