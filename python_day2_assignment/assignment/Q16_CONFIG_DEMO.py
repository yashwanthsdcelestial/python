"""
Q16 - Environment Variables and Config Demonstration

This script demonstrates loading settings from .env file at startup
and displays the required output format.
"""

from fastapi.testclient import TestClient
from Q16_fastapi_config_app import app

print("\n" + "=" * 70)
print("Q16 - ENVIRONMENT VARIABLES AND CONFIG MANAGEMENT")
print("=" * 70)
print("\nStartup Output (from app startup event):")
print("-" * 70)

# The startup event was already triggered when importing the app
# Let's show it again for clarity and also verify with TestClient

client = TestClient(app)

# Make a request to trigger full startup if needed
response = client.get("/config")

print("\nConfiguration Verification:")
print("-" * 70)

config = response.json()
print(f"✓ Configuration loaded from .env file:")
print(f"  - APP_NAME: {config['app_name']}")
print(f"  - DEBUG: {config['debug']}")
print(f"  - JSON_DB_PATH: {config['json_db_path']}")
print(f"  - LOG_LEVEL: {config['log_level']}")

print("\n✅ REQUIRED OUTPUT FORMAT:")
print("-" * 70)
print(f"App: {config['app_name']} | Debug: {config['debug']} | DB: {config['json_db_path']}")

print("\n" + "=" * 70)
