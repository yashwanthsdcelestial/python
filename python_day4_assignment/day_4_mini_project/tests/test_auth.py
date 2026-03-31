"""5 auth tests: register success, duplicate username, invalid email, login success, wrong password."""
from tests.conftest import auth_headers


def test_register_success(client):
    resp = client.post("/auth/register", json={
        "username": "rahul",
        "email": "rahul@mail.com",
        "password": "secure1234",
        "phone": "9876543210",
        "monthly_income": 55000,
    })
    assert resp.status_code == 201
    body = resp.json()
    assert body["username"] == "rahul"
    assert body["role"] == "user"
    assert "password" not in body


def test_register_duplicate_username(client, user_token):
    resp = client.post("/auth/register", json={
        "username": "testuser",   # already taken by user_token fixture
        "email": "other@mail.com",
        "password": "password123",
        "phone": "9876543210",
        "monthly_income": 50000,
    })
    assert resp.status_code == 409
    assert resp.json()["error"] == "DuplicateUserError"


def test_register_invalid_email(client):
    resp = client.post("/auth/register", json={
        "username": "newuser2",
        "email": "notanemail",    # missing @ and .
        "password": "password123",
        "phone": "9876543210",
        "monthly_income": 50000,
    })
    assert resp.status_code == 422


def test_login_success(client, user_token):
    resp = client.post("/auth/login", json={
        "username": "testuser",
        "password": "password123",
    })
    assert resp.status_code == 200
    body = resp.json()
    assert body["message"] == "Login successful"
    assert body["username"] == "testuser"
    assert body["role"] == "user"
    assert "token" in body


def test_login_wrong_password(client, user_token):
    resp = client.post("/auth/login", json={
        "username": "testuser",
        "password": "wrongpassword",
    })
    assert resp.status_code == 401
    assert resp.json()["error"] == "InvalidCredentialsError"