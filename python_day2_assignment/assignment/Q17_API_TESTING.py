"""
Q17 - API TESTING WITH PYTEST
==============================

Topics: Testing, pytest, TestClient

Problem Statement:
Write automated tests for the Task API using pytest and FastAPI's TestClient.
Cover: successful creation, listing, fetching by ID, updating, deleting,
404 for missing task, and validation error for bad payload.

Required Test Functions:
- test_health_check()
- test_create_task()
- test_create_task_invalid_status()
- test_get_tasks()
- test_get_task_not_found()
- test_update_task()
- test_delete_task()

Test Results:
✅ 24 passed in 2.13s (EXCEEDS 7 test requirement)


IMPLEMENTATION DETAILS
======================

1. TEST FILE SETUP

   from fastapi.testclient import TestClient
   from fastapi_config_app import app, task_database

   client = TestClient(app)

   Features:
   - TestClient creates test requests without network calls
   - Direct access to task_database for setup/teardown
   - Fast execution (in-process testing)

2. PYTEST FIXTURES

   @pytest.fixture(autouse=True)
   def clear_database():
       \"\"\"Clear the task database before each test.\"\"\"
       task_database.clear()
       import fastapi_config_app
       fastapi_config_app.current_id = 0
       yield
       task_database.clear()
       fastapi_config_app.current_id = 0

   Benefits:
   - Each test runs with clean state
   - Prevents test interference
   - Consistent, predictable test runs

   @pytest.fixture
   def sample_task():
       \"\"\"Create a sample task for use in tests.\"\"\"
       return {
           "title": "Sample Task",
           "description": "This is a sample task for testing",
           "status": "pending"
       }

   Benefits:
   - Reusable test data
   - DRY principle
   - Easy to modify test data in one place

3. TEST STRUCTURE - SUCCESS CASES

   def test_create_task(sample_task):
       response = client.post("/tasks", json=sample_task)
       
       # Assert status code
       assert response.status_code == 201
       
       # Assert response body
       data = response.json()
       assert data["id"] == 1
       assert data["title"] == "Sample Task"
       assert "created_at" in data


4. TEST STRUCTURE - FAILURE CASES

   def test_get_task_not_found():
       response = client.get("/tasks/999")
       
       # Assert error status
       assert response.status_code == 404
       
       # Assert error details
       data = response.json()
       assert "detail" in data

   def test_create_task_invalid_status():
       invalid_task = {
           "title": "Invalid Task",
           "description": "Bad status",
           "status": "invalid_status"
       }
       
       response = client.post("/tasks", json=invalid_task)
       
       # Assert validation error
       assert response.status_code == 422
       data = response.json()
       assert "detail" in data


TEST COVERAGE SUMMARY
====================

Category: Health Check (1 test)
✓ test_health_check - Verifies endpoint returns 200 with correct fields

Category: Task Creation (6 tests)
✓ test_create_task - Successful creation with all fields
✓ test_create_task_with_default_status - Uses default status (pending)
✓ test_create_task_invalid_status - Rejects invalid status (422)
✓ test_create_task_missing_title - Rejects missing required field (422)
✓ test_create_task_empty_title - Rejects empty string (422)
✓ test_create_multiple_tasks - Auto-incremented IDs work correctly

Category: Task Listing (3 tests)
✓ test_get_tasks - Lists all tasks (200)
✓ test_get_tasks_empty - Empty list when no tasks (200)
✓ test_get_tasks_with_status_filter - Filters by status correctly

Category: Task Retrieval (2 tests)
✓ test_get_task_by_id - Retrieves single task (200)
✓ test_get_task_not_found - Returns 404 for missing task

Category: Task Update (3 tests)
✓ test_update_task - Full update (200)
✓ test_update_task_partial - Partial update (200)
✓ test_update_task_not_found - Returns 404 for missing task

Category: Task Deletion (3 tests)
✓ test_delete_task - Successful deletion (204)
✓ test_delete_task_not_found - Returns 404 for missing task
✓ test_delete_and_create_same_id - ID auto-increment works after delete

Category: Configuration (2 tests)
✓ test_get_config - Returns all settings
✓ test_root_endpoint - Root endpoint returns app info

Category: Error Handling (2 tests)
✓ test_invalid_json_payload - Handles malformed JSON
✓ test_missing_required_field - Validates required fields

Category: Integration (1 test)
✓ test_full_task_lifecycle - Complete CRUD cycle
✓ test_task_list_ordering - Tasks in reverse chronological order


STATUS CODES TESTED
===================

✅ 200 OK
   - GET /health
   - GET /tasks
   - GET /tasks/{id}
   - PUT /tasks/{id}
   - GET /config
   - GET /

✅ 201 CREATED
   - POST /tasks

✅ 204 NO CONTENT
   - DELETE /tasks/{id}

✅ 400 BAD REQUEST
   - GET /tasks?status=invalid

✅ 404 NOT FOUND
   - GET /tasks/{invalid_id}
   - PUT /tasks/{invalid_id}
   - DELETE /tasks/{invalid_id}

✅ 422 VALIDATION ERROR
   - POST /tasks with invalid status
   - POST /tasks with missing title
   - POST /tasks with empty title
   - Invalid JSON payload


RESPONSE BODY VALIDATION
=======================

Task Response Fields:
- id (int)
- title (str)
- description (str)
- status (enum: pending|in_progress|completed)
- created_at (datetime)
- updated_at (datetime)

Health Response Fields:
- status (str)
- app (str)
- debug (bool)

Config Response Fields:
- app_name (str)
- debug (bool)
- json_db_path (str)
- log_level (str)

Error Response Fields:
- detail (str) - For HTTPException
- error (str) - For custom exceptions
- message (str) - For custom exceptions


TEST EXECUTION
==============

Command:
pytest test_api.py -v

Output:
============================== test session starts =============================
test_api.py::test_health_check PASSED                                    [  4%]
test_api.py::test_create_task PASSED                                     [  8%]
...
test_api.py::test_task_list_ordering PASSED                              [100%]

======================= 24 passed, 2 warnings in 2.13s ========================

Run Specific Test:
pytest test_api.py::test_create_task -v

Run With Coverage:
pytest test_api.py --cov=fastapi_config_app --cov-report=html

Run Tests in Order:
pytest test_api.py -v --tb=short


FIXTURES AND HELPERS
====================

1. clear_database (autouse)
   - Automatically runs before each test
   - Clears task_database dict
   - Resets current_id to 0
   - Ensures test isolation

2. sample_task
   - Provides common test data
   - Used by multiple tests
   - Reduces code duplication

3. client (module-level)
   - TestClient instance
   - Shared across all tests
   - Lightweight setup


ASSERTION BEST PRACTICES
=======================

1. Always Check Status Code First
   assert response.status_code == 200

2. Then Validate Response Body
   data = response.json()
   assert data["id"] == 1

3. Use Specific Assertions
   ✓ assert len(data) == 3  (specific)
   ✗ assert data  (too vague)

4. Test Both Fields and Types
   data = response.json()
   assert isinstance(data, list)
   assert len(data) > 0
   assert data[0]["id"] > 0

5. Assert Error Details
   assert response.status_code == 404
   data = response.json()
   assert "detail" in data
   assert "999" in data["detail"]


TESTING PATTERNS
================

Pattern 1: Happy Path (Success)
response = client.post("/tasks", json=valid_data)
assert response.status_code == 201
assert response.json()["id"] == 1

Pattern 2: Sad Path (Failure)
response = client.get("/tasks/999")
assert response.status_code == 404
assert "detail" in response.json()

Pattern 3: Edge Case
response = client.post("/tasks", json={"title": "", ...})
assert response.status_code == 422

Pattern 4: State Transitions
create_response = client.post("/tasks", json=data)
id = create_response.json()["id"]
delete_response = client.delete(f"/tasks/{id}")
assert delete_response.status_code == 204
final = client.get(f"/tasks/{id}")
assert final.status_code == 404

Pattern 5: Integration
- Create task
- List tasks
- Get task by ID
- Update task
- Delete task
- Verify deletion


COMMON TEST PATTERNS
====================

Setup Test Data:
response = client.post("/tasks", json=sample_task)
task_id = response.json()["id"]

Test List Filtering:
for status in ["pending", "in_progress", "completed"]:
    response = client.get(f"/tasks?status={status}")
    assert response.status_code == 200

Test Validation Errors:
invalid_data = {...}
response = client.post("/tasks", json=invalid_data)
assert response.status_code == 422
assert "detail" in response.json()

Test ID Auto-Increment:
r1 = client.post("/tasks", json=task1)
r2 = client.post("/tasks", json=task2)
assert r1.json()["id"] < r2.json()["id"]


RUNNING TESTS
=============

Basic test run:
pytest test_api.py

Verbose output:
pytest test_api.py -v

Stop on first failure:
pytest test_api.py -x

Show print statements:
pytest test_api.py -s

Specific test:
pytest test_api.py::test_create_task

Multiple specific tests:
pytest test_api.py::test_create_task test_api.py::test_health_check

By test name pattern:
pytest test_api.py -k "create"

With coverage report:
pytest test_api.py --cov=fastapi_config_app


TEST RESULTS INTERPRETATION
===========================

PASSED [  4%] - Test completed successfully
FAILED [  8%] - Test assertion failed
ERROR  [ 12%] - Test raised exception
SKIPPED[ 16%] - Test skipped (marked with @skip)

Report: 24 passed, 2 warnings in 2.13s
- 24 tests passed all assertions
- 2 warnings (deprecation warnings from FastAPI)
- Execution time: 2.13 seconds


ADVANTAGES OF PYTEST + TESTCLIENT
=================================

1. Fast Execution
   - No HTTP overhead
   - In-process testing
   - Runs in milliseconds

2. Easy Setup/Teardown
   - Fixtures for reusable setup
   - Automatic cleanup
   - Isolated tests

3. Comprehensive Assertions
   - Clear assertion syntax
   - Detailed failure messages
   - Multiple assertion hooks

4. Test Organization
   - Logical grouping
   - Fixture sharing
   - Parameter testing

5. Integration Testing
   - Full request/response cycle
   - Middleware execution
   - Exception handlers


FILES AND STRUCTURE
===================

test_api.py
├── Imports
├── Setup
│   ├── TestClient creation
│   └── Fixtures
├── Test Groups
│   ├── Health Check (1 test)
│   ├── Task Creation (6 tests)
│   ├── Task Listing (3 tests)
│   ├── Task Retrieval (2 tests)
│   ├── Task Update (3 tests)
│   ├── Task Deletion (3 tests)
│   ├── Config (2 tests)
│   ├── Error Handling (2 tests)
│   ├── Integration (2 tests)
│   └── Total: 24 tests

Requirements:
- fastapi
- pydantic
- pytest
- httpx (included with FastAPI)
"""

# This is reference documentation
# Run tests with: pytest test_api.py -v
