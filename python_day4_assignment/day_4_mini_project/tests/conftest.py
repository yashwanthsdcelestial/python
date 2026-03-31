import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_loanhub.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# SQLite does not enforce foreign keys by default — enable them
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, _):
    dbapi_conn.execute("PRAGMA foreign_keys=ON")

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── App wiring ────────────────────────────────────────────────────────────────
# Import AFTER the engine is created so models register against Base correctly
from database import Base, get_db  # noqa: E402
from main import app                # noqa: E402

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions=False)


# ── Helpers ───────────────────────────────────────────────────────────────────

def register_and_login(client, username, email, password="password123",
                       phone="9876543210", income=60000):
    client.post("/auth/register", json={
        "username": username,
        "email": email,
        "password": password,
        "phone": phone,
        "monthly_income": income,
    })
    resp = client.post("/auth/login", json={"username": username, "password": password})
    assert resp.status_code == 200
    return resp.json()["token"]


def auth_headers(token: str) -> dict:
    return {"x-auth-token": token}


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def user_token(client):
    return register_and_login(client, "testuser", "testuser@mail.com")


@pytest.fixture
def admin_token(client):
    from services.user_service import UserService
    db = TestingSessionLocal()
    UserService(db).seed_admin("admin", "admin1234", "admin@loanhub.com")
    db.close()
    resp = client.post("/auth/login", json={"username": "admin", "password": "admin1234"})
    assert resp.status_code == 200
    return resp.json()["token"]


@pytest.fixture
def loan_payload():
    return {
        "amount": 500000,
        "purpose": "home",
        "tenure_months": 120,
        "employment_status": "employed",
    }
