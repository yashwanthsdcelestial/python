"""
Q16 - ENVIRONMENT VARIABLES AND CONFIG MANAGEMENT
==================================================

Topics: Config, Environment Variables, Pydantic

Problem Statement:
Create a Settings class using Pydantic's BaseSettings that loads
APP_NAME, DEBUG, JSON_DB_PATH, and LOG_LEVEL from a .env file.
Use these settings in your FastAPI app startup.

Expected Output:
App: TaskAPI | Debug: True | DB: ./data/tasks.json

Constraints:
✓ Use pydantic-settings package
✓ Do NOT hardcode any config values in source code
✓ Load settings using model_config = SettingsConfigDict(env_file=".env")
✓ Settings must be a singleton used across the app


IMPLEMENTATION DETAILS
======================

1. ENVIRONMENT FILE (.env)
   Location: Project root
   Purpose: Store configuration values

   Content:
   --------
   APP_NAME=TaskAPI
   DEBUG=true
   JSON_DB_PATH=./data/tasks.json
   LOG_LEVEL=INFO

2. SETTINGS CLASS (settings.py)
   - Inherits from pydantic_settings.BaseSettings
   - Defines all configuration fields with types
   - Uses SettingsConfigDict to specify .env file
   - Sets frozen=True for immutability
   - Acts as singleton when instantiated once

   Key Features:
   - Automatic type conversion (true -> True, etc.)
   - Case-insensitive environment variable matching
   - Fallback to default values if not in .env
   - Validation of configuration values

3. SINGLETON PATTERN
   Implementation:
   ---------------
   # Create singleton instance at module level
   settings = Settings()

   # Import and use throughout app
   from settings import settings

   Benefits:
   - Single instance loaded once at startup
   - Guaranteed same reference across imports
   - Efficient caching of environment reading
   - Immutable configuration prevents accidents

4. FASTAPI APP INTEGRATION
   - Import settings singleton: from settings import settings
   - Use in startup event for logging
   - Pass settings to endpoints as needed
   - Configure loggers with settings.log_level
   - Expose settings via /config endpoint

5. STARTUP MESSAGE
   The @app.on_event("startup") function logs:
   "App: {name} | Debug: {debug} | DB: {path}"

   Example:
   "App: TaskAPI | Debug: True | DB: ./data/tasks.json"


FILES CREATED
=============

1. .env
   - Configuration file with environment variables
   - NOT committed to version control
   - Local per environment (dev, staging, prod)

2. settings.py
   - Settings class definition
   - Singleton instance
   - Type-safe configuration
   - Immutable to prevent runtime changes

3. fastapi_config_app.py
   - FastAPI application using settings
   - Startup event that logs settings
   - /config endpoint returning current settings
   - /health endpoint using app_name from settings
   - Root endpoint displaying settings
   - Logger configured with settings.log_level

4. test_config_management.py
   - Comprehensive test suite
   - Verifies .env file loading
   - Validates singleton pattern
   - Tests immutability
   - Confirms settings used in endpoints
   - Checks logging configuration

5. Q16_CONFIG_DEMO.py
   - Simple demonstration
   - Shows startup output
   - Displays required format


CONFIGURATION FIELDS
====================

APP_NAME (string)
  - Purpose: Application display name
  - Default: "TaskAPI"
  - Usage: FastAPI title, logs, endpoints
  - Example: "TaskAPI", "MyApp", "ProductionAPI"

DEBUG (boolean)
  - Purpose: Debug mode flag
  - Default: False
  - Usage: Error details, logging verbosity
  - Values: true/false (converted to True/False)

JSON_DB_PATH (string)
  - Purpose: Path to JSON database file
  - Default: "./data/tasks.json"
  - Usage: File storage location
  - Example: "./data/tasks.json", "/var/data/db.json"

LOG_LEVEL (string)
  - Purpose: Python logging level
  - Default: "INFO"
  - Valid: DEBUG, INFO, WARNING, ERROR, CRITICAL
  - Usage: Logger configuration


PYDANTIC-SETTINGS FEATURES
===========================

1. ENVIRONMENT VARIABLE LOADING
   from pydantic_settings import BaseSettings

   class MySettings(BaseSettings):
       app_name: str = "Default"
       debug: bool = False

   # Loads from APP_NAME and DEBUG env vars
   settings = MySettings()

2. .ENV FILE SUPPORT
   model_config = SettingsConfigDict(
       env_file=".env",
       env_file_encoding="utf-8",
       case_sensitive=False,
       frozen=True
   )

   - Reads .env file instead of environment
   - Case-insensitive matching (APP_NAME = app_name)
   - Frozen=True prevents modification
   - Encoding specified for compatibility

3. TYPE CONVERSION
   - "true" string -> True boolean
   - "123" string -> 123 integer
   - Automatic validation
   - Type-safe access

4. DEFAULT VALUES
   app_name: str = "DefaultApp"  # Used if not in .env
   debug: bool = False            # Used if not specified


USAGE THROUGHOUT APP
====================

1. FASTAPI APP INITIALIZATION
   app = FastAPI(
       title=settings.app_name,  # Uses loaded value
       ...
   )

2. STARTUP EVENT
   @app.on_event("startup")
   async def startup_event():
       message = f"App: {settings.app_name} | Debug: {settings.debug} ..."
       logger.info(message)

3. ENDPOINTS
   @app.get("/config")
   async def get_config():
       return ConfigResponse(
           app_name=settings.app_name,
           debug=settings.debug,
           json_db_path=settings.json_db_path,
           log_level=settings.log_level
       )

4. LOGGING CONFIGURATION
   logging.basicConfig(
       level=getattr(logging, settings.log_level),
       ...
   )

5. CONDITIONAL LOGIC
   if settings.debug:
       # Enable detailed error responses
       pass
   
   if settings.json_db_path:
       # Use specified database path
       pass


TEST RESULTS
============

✅ All Tests Passed:

1. .env File Verification
   ✓ File found and readable
   ✓ All variables present

2. Settings Loading
   ✓ APP_NAME=TaskAPI loaded
   ✓ DEBUG=True loaded
   ✓ JSON_DB_PATH=./data/tasks.json loaded
   ✓ LOG_LEVEL=INFO loaded

3. Singleton Pattern
   ✓ Same instance on multiple imports
   ✓ ID matches across imports
   ✓ Memory efficient

4. Immutability
   ✓ frozen=True prevents modifications
   ✓ ValidationError raised on change attempt
   ✓ Protected configuration

5. FastAPI Integration
   ✓ Settings accessible in endpoints
   ✓ Startup event logs configuration
   ✓ /config endpoint returns settings

6. Logging
   ✓ Logger configured with settings.log_level
   ✓ Console output uses log level
   ✓ File logging respects configuration


EXAMPLE ENVIRONMENT SETUP
=========================

Development (.env.dev):
APP_NAME=TaskAPI-Dev
DEBUG=true
JSON_DB_PATH=./data/dev_tasks.json
LOG_LEVEL=DEBUG

Staging (.env.staging):
APP_NAME=TaskAPI-Staging
DEBUG=false
JSON_DB_PATH=/data/staging/tasks.json
LOG_LEVEL=INFO

Production (.env.prod):
APP_NAME=TaskAPI
DEBUG=false
JSON_DB_PATH=/data/prod/tasks.json
LOG_LEVEL=ERROR


RUNNING EXAMPLES
================

Test suite:
python test_config_management.py

Demo:
python Q16_CONFIG_DEMO.py

Run FastAPI app:
uvicorn fastapi_config_app:app --reload

Access API:
GET http://localhost:8000/config
GET http://localhost:8000/health
GET http://localhost:8000/


BEST PRACTICES
==============

1. ENVIRONMENT FILE MANAGEMENT
   ✓ .env in .gitignore (DON'T commit)
   ✓ Create .env.example with template
   ✓ Document all variables in README
   ✓ Different files per environment

2. CONFIGURATION TYPES
   ✓ Use type hints for validation
   ✓ Provide sensible defaults
   ✓ Document valid values (e.g., "pending|in_progress|completed")
   ✓ Validate at import time (fail fast)

3. SECURITY
   ✓ Never hardcode secrets
   ✓ Use environment variables for sensitive data
   ✓ Load from secure vaults in production
   ✓ Log sanitized config only

4. IMMUTABILITY
   ✓ frozen=True prevents runtime changes
   ✓ No risk of configuration modification
   ✓ Easier testing and debugging
   ✓ Better code safety

5. SINGLETON PATTERN
   ✓ Single import point at module level
   ✓ Consistent access throughout app
   ✓ Efficient (loaded once)
   ✓ Thread-safe Pydantic models


TROUBLESHOOTING
===============

Issue: ModuleNotFoundError: No module named 'pydantic_settings'
Solution: pip install pydantic-settings

Issue: Variables not loading from .env
Solution: 
- Check .env file in project root
- Verify variable names match class attributes
- Check case sensitivity setting matches usage

Issue: Settings values not updating
Solution:
- Settings are cached at startup
- Restart application to reload
- Check that frozen=True is intended behavior

Issue: Default values not used
Solution:
- Ensure .env values actually loaded
- Check env_file path is correct
- Use model_dump() to inspect values
"""

# This is a reference documentation file
# The actual implementation is in settings.py and fastapi_config_app.py
