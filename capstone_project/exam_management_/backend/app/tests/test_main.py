"""
Tests for auth service, exam service, and API endpoints.
Run: pytest app/tests/ -v --cov=app --cov-report=term-missing
"""
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import Base, get_db
from app.core.config import settings
from app.core.security import get_password_hash, verify_password, create_access_token, decode_token
from app.models.models import User, Exam, RoleEnum, ExamStatusEnum
from app.services.auth_service import AuthService
from app.schemas.schemas import UserRegisterRequest, UserLoginRequest

# ── Test DB Setup ──────────────────────────────────────────────────────────────

TEST_DB_URL = settings.TEST_DATABASE_URL

@pytest.fixture(scope="session")
def engine():
    eng = create_engine(TEST_DB_URL)
    Base.metadata.create_all(bind=eng)
    yield eng
    Base.metadata.drop_all(bind=eng)


@pytest.fixture(scope="function")
def db(engine):
    TestSession = sessionmaker(bind=engine)
    session = TestSession()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ── Security Tests ─────────────────────────────────────────────────────────────

class TestSecurity:
    def test_password_hash_and_verify(self):
        pw = "MySecret@123"
        hashed = get_password_hash(pw)
        assert hashed != pw
        assert verify_password(pw, hashed)
        assert not verify_password("wrong", hashed)

    def test_create_and_decode_access_token(self):
        token = create_access_token(subject=42, extra_data={"role": "student"})
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "42"
        assert payload["type"] == "access"
        assert payload["role"] == "student"

    def test_invalid_token_returns_none(self):
        result = decode_token("this.is.not.valid")
        assert result is None

    def test_access_token_has_expiry(self):
        token = create_access_token(subject=1)
        payload = decode_token(token)
        assert "exp" in payload


# ── Auth Service Tests ─────────────────────────────────────────────────────────

class TestAuthService:
    def test_register_new_user(self, db):
        import uuid
        service = AuthService(db)
        unique_email = f"test_{uuid.uuid4().hex[:8]}@test.com"
        data = UserRegisterRequest(email=unique_email, password="Pass@1234", full_name="Test User")
        user = service.register(data)
        assert user.id is not None
        assert user.email == unique_email
        assert user.hashed_password != "Pass@1234"
        assert user.role == RoleEnum.student

    def test_register_duplicate_email_raises(self, db):
        from fastapi import HTTPException
        import uuid
        service = AuthService(db)
        unique_email = f"dup_{uuid.uuid4().hex[:8]}@test.com"
        data = UserRegisterRequest(email=unique_email, password="Pass@1234", full_name="Dup User")
        service.register(data)
        with pytest.raises(HTTPException) as exc:
            service.register(data)
        assert exc.value.status_code == 400

    def test_login_valid_credentials(self, db):
        import uuid
        service = AuthService(db)
        email = f"login_{uuid.uuid4().hex[:8]}@test.com"
        service.register(UserRegisterRequest(email=email, password="Pass@1234", full_name="Login User"))
        tokens = service.login(UserLoginRequest(email=email, password="Pass@1234"))
        assert tokens.access_token
        assert tokens.refresh_token
        assert tokens.token_type == "bearer"

    def test_login_wrong_password_raises(self, db):
        from fastapi import HTTPException
        import uuid
        service = AuthService(db)
        email = f"badpw_{uuid.uuid4().hex[:8]}@test.com"
        service.register(UserRegisterRequest(email=email, password="Pass@1234", full_name="Bad PW"))
        with pytest.raises(HTTPException) as exc:
            service.login(UserLoginRequest(email=email, password="WrongPassword"))
        assert exc.value.status_code == 401


# ── API Integration Tests ──────────────────────────────────────────────────────

class TestAuthAPI:
    def test_register_endpoint(self, client):
        import uuid
        email = f"api_{uuid.uuid4().hex[:8]}@test.com"
        response = client.post("/api/auth/register", json={
            "email": email,
            "password": "Pass@1234",
            "full_name": "API User",
            "role": "student",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == email
        assert data["role"] == "student"
        assert "hashed_password" not in data

    def test_login_endpoint(self, client):
        import uuid
        email = f"login_api_{uuid.uuid4().hex[:8]}@test.com"
        client.post("/api/auth/register", json={"email": email, "password": "Pass@1234", "full_name": "Login API"})
        response = client.post("/api/auth/login", json={"email": email, "password": "Pass@1234"})
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    def test_me_endpoint_requires_auth(self, client):
        response = client.get("/api/auth/me")
        assert response.status_code == 403  # No auth header

    def test_me_endpoint_with_valid_token(self, client):
        import uuid
        email = f"me_{uuid.uuid4().hex[:8]}@test.com"
        client.post("/api/auth/register", json={"email": email, "password": "Pass@1234", "full_name": "Me User"})
        login_resp = client.post("/api/auth/login", json={"email": email, "password": "Pass@1234"})
        token = login_resp.json()["access_token"]
        response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.json()["email"] == email


class TestExamsAPI:
    def _get_admin_token(self, client):
        import uuid
        email = f"adm_{uuid.uuid4().hex[:8]}@test.com"
        client.post("/api/auth/register", json={"email": email, "password": "Pass@1234", "full_name": "Admin", "role": "admin"})
        resp = client.post("/api/auth/login", json={"email": email, "password": "Pass@1234"})
        return resp.json()["access_token"]

    def _get_student_token(self, client):
        import uuid
        email = f"stu_{uuid.uuid4().hex[:8]}@test.com"
        client.post("/api/auth/register", json={"email": email, "password": "Pass@1234", "full_name": "Student", "role": "student"})
        resp = client.post("/api/auth/login", json={"email": email, "password": "Pass@1234"})
        return resp.json()["access_token"]

    def test_create_exam_as_admin(self, client):
        token = self._get_admin_token(client)
        response = client.post("/api/exams", json={
            "title": "Test Exam",
            "description": "A test",
            "duration_minutes": 30,
            "pass_percentage": 50.0,
            "max_attempts": 1,
            "questions": [
                {"text": "Q1?", "options": ["A", "B", "C", "D"], "correct_answer": "A", "marks": 10},
                {"text": "Q2?", "options": ["X", "Y"], "correct_answer": "X", "marks": 10},
            ],
        }, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Exam"

    def test_create_exam_as_student_forbidden(self, client):
        token = self._get_student_token(client)
        response = client.post("/api/exams", json={
            "title": "Student Attempt",
            "questions": [{"text": "Q?", "options": ["A", "B"], "correct_answer": "A", "marks": 5}],
        }, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 403

    def test_list_exams(self, client):
        token = self._get_student_token(client)
        response = client.get("/api/exams", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data


class TestCustomHook:
    """Tests for the custom hook / utility"""
    def test_password_validation_schema(self):
        with pytest.raises(Exception):
            UserRegisterRequest(email="a@b.com", password="short", full_name="Test")

    def test_full_name_validation_schema(self):
        with pytest.raises(Exception):
            UserRegisterRequest(email="a@b.com", password="Pass@1234", full_name="X")
