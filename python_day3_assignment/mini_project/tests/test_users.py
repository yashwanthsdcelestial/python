"""User endpoint tests."""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestUserRegistration:
    """Test user registration endpoint."""
    
    def test_register_valid_user(self):
        """Test successful user registration."""
        response = client.post(
            "/users/register",
            json={
                "username": "alice",
                "email": "alice@mail.com",
                "password": "securepass123"
            }
        )
        assert response.status_code == 201
        assert response.json()["username"] == "alice"
        assert response.json()["email"] == "alice@mail.com"
    
    def test_register_duplicate_username(self):
        """Test duplicate username rejection."""
        # Register first user
        client.post(
            "/users/register",
            json={
                "username": "bob",
                "email": "bob@mail.com",
                "password": "securepass123"
            }
        )
        
        # Try to register with same username
        response = client.post(
            "/users/register",
            json={
                "username": "bob",
                "email": "bob2@mail.com",
                "password": "securepass123"
            }
        )
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]
    
    def test_register_invalid_email(self):
        """Test invalid email rejection."""
        response = client.post(
            "/users/register",
            json={
                "username": "charlie",
                "email": "invalid-email",
                "password": "securepass123"
            }
        )
        assert response.status_code == 422
    
    def test_register_short_password(self):
        """Test short password rejection."""
        response = client.post(
            "/users/register",
            json={
                "username": "diana",
                "email": "diana@mail.com",
                "password": "short"
            }
        )
        assert response.status_code == 422


class TestUserLogin:
    """Test user login endpoint."""
    
    def test_login_valid_credentials(self):
        """Test successful login."""
        # Register user first
        client.post(
            "/users/register",
            json={
                "username": "eve",
                "email": "eve@mail.com",
                "password": "securepass123"
            }
        )
        
        # Login
        response = client.post(
            "/users/login",
            json={
                "username": "eve",
                "password": "securepass123"
            }
        )
        assert response.status_code == 200
        assert response.json()["username"] == "eve"
    
    def test_login_invalid_password(self):
        """Test invalid password rejection."""
        # Register user
        client.post(
            "/users/register",
            json={
                "username": "frank",
                "email": "frank@mail.com",
                "password": "correctpass123"
            }
        )
        
        # Try to login with wrong password
        response = client.post(
            "/users/login",
            json={
                "username": "frank",
                "password": "wrongpass"
            }
        )
        assert response.status_code == 401


class TestUserList:
    """Test user list endpoint."""
    
    def test_list_users(self):
        """Test listing users."""
        # Register some users
        for i in range(3):
            client.post(
                "/users/register",
                json={
                    "username": f"user{i}",
                    "email": f"user{i}@mail.com",
                    "password": "securepass123"
                }
            )
        
        response = client.get("/users")
        assert response.status_code == 200
        assert len(response.json()) == 3


class TestUserDelete:
    """Test user delete endpoint."""
    
    def test_delete_user(self):
        """Test deleting a user."""
        # Register user
        register_response = client.post(
            "/users/register",
            json={
                "username": "george",
                "email": "george@mail.com",
                "password": "securepass123"
            }
        )
        user_id = register_response.json()["id"]
        
        # Delete user
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 200
        
        # Verify deleted
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 404
