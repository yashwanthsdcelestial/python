"""Test configuration and fixtures."""
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from main import app
from config import settings
from repositories.json_repository import JSONRepository

# Override settings for testing
settings.json_db_path = "./test_data"


@pytest.fixture(scope="session")
def test_client():
    """Provide test client."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_test_data():
    """Cleanup test data before each test."""
    test_data_dir = Path("./test_data")
    if test_data_dir.exists():
        import shutil
        shutil.rmtree(test_data_dir)
    test_data_dir.mkdir(exist_ok=True)
    yield
    # Cleanup after test
    if test_data_dir.exists():
        import shutil
        shutil.rmtree(test_data_dir)
