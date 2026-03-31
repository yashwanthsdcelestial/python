"""
Q17 - API Testing with pytest

Comprehensive test suite for the Task Management API using pytest and TestClient.

Test Coverage:
- Health check endpoint
- Task creation (success and validation error)
- List tasks
- Get task by ID (success and 404)
- Update task
- Delete task
- Invalid status validation
"""

import pytest
from fastapi.testclient import TestClient
from Q16_fastapi_config_app import app, task_database

# Create TestClient for the FastAPI app
client = TestClient(app)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture(autouse=True)
def clear_database():
    """Clear the task database before each test."""
    task_database.clear()
    # Reset current_id
    import questions.Q16_fastapi_config_app as Q16_fastapi_config_app
    Q16_fastapi_config_app.current_id = 0
    yield
    task_database.clear()
    Q16_fastapi_config_app.current_id = 0


@pytest.fixture
def sample_task():
    """Create a sample task for use in tests."""
    return {
        "title": "Sample Task",
        "description": "This is a sample task for testing",
        "status": "pending"
    }


# ============================================================================
# HEALTH CHECK TESTS
# ============================================================================

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    
    # Assert status code
    assert response.status_code == 200
    
    # Assert response body
    data = response.json()
    assert data["status"] == "healthy"
    assert "app" in data
    assert "debug" in data
    assert data["app"] == "TaskAPI"


# ============================================================================
# TASK CREATION TESTS
# ============================================================================

def test_create_task(sample_task):
    """Test successful task creation."""
    response = client.post("/tasks", json=sample_task)
    
    # Assert status code for creation
    assert response.status_code == 201
    
    # Assert response body
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Sample Task"
    assert data["description"] == "This is a sample task for testing"
    assert data["status"] == "pending"
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_with_default_status():
    """Test task creation with default status."""
    task_data = {
        "title": "Task without status",
        "description": "Default status should be pending"
    }
    
    response = client.post("/tasks", json=task_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "pending"


def test_create_task_invalid_status():
    """Test task creation with invalid status (validation error)."""
    invalid_task = {
        "title": "Invalid Task",
        "description": "This has an invalid status",
        "status": "invalid_status"
    }
    
    response = client.post("/tasks", json=invalid_task)
    
    # Assert error status code
    assert response.status_code == 422  # Validation error
    
    # Assert error details in response
    data = response.json()
    assert "detail" in data
    assert isinstance(data["detail"], list)


def test_create_task_missing_title():
    """Test task creation with missing required field."""
    incomplete_task = {
        "description": "Missing title"
    }
    
    response = client.post("/tasks", json=incomplete_task)
    
    # Assert validation error
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_create_task_empty_title():
    """Test task creation with empty title."""
    task_data = {
        "title": "",
        "description": "Empty title"
    }
    
    response = client.post("/tasks", json=task_data)
    
    # Assert validation error
    assert response.status_code == 422


def test_create_multiple_tasks():
    """Test creating multiple tasks with auto-increment IDs."""
    task1 = {"title": "Task 1", "description": "First task"}
    task2 = {"title": "Task 2", "description": "Second task"}
    task3 = {"title": "Task 3", "description": "Third task"}
    
    response1 = client.post("/tasks", json=task1)
    response2 = client.post("/tasks", json=task2)
    response3 = client.post("/tasks", json=task3)
    
    data1 = response1.json()
    data2 = response2.json()
    data3 = response3.json()
    
    # Assert IDs are auto-incremented
    assert data1["id"] == 1
    assert data2["id"] == 2
    assert data3["id"] == 3
    
    # Assert all status codes
    assert response1.status_code == 201
    assert response2.status_code == 201
    assert response3.status_code == 201


# ============================================================================
# TASK LISTING TESTS
# ============================================================================

def test_get_tasks():
    """Test listing all tasks."""
    # Create some tasks first
    client.post("/tasks", json={"title": "Task 1", "description": "First"})
    client.post("/tasks", json={"title": "Task 2", "description": "Second"})
    
    response = client.get("/tasks")
    
    # Assert status code
    assert response.status_code == 200
    
    # Assert response is a list
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    
    # Assert task structure
    for task in data:
        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "status" in task
        assert "created_at" in task
        assert "updated_at" in task


def test_get_tasks_empty():
    """Test listing tasks when none exist."""
    response = client.get("/tasks")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_get_tasks_with_status_filter():
    """Test listing tasks with status filter."""
    # Create tasks with different statuses
    client.post("/tasks", json={"title": "Task 1", "description": "Desc", "status": "pending"})
    client.post("/tasks", json={"title": "Task 2", "description": "Desc", "status": "in_progress"})
    client.post("/tasks", json={"title": "Task 3", "description": "Desc", "status": "completed"})
    
    # Filter by pending
    response = client.get("/tasks?status=pending")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "pending"


# ============================================================================
# TASK RETRIEVAL BY ID TESTS
# ============================================================================

def test_get_task_by_id(sample_task):
    """Test fetching a task by ID."""
    # Create a task
    create_response = client.post("/tasks", json=sample_task)
    task_id = create_response.json()["id"]
    
    # Fetch the task
    response = client.get(f"/tasks/{task_id}")
    
    # Assert status code
    assert response.status_code == 200
    
    # Assert response body
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Sample Task"
    assert data["description"] == "This is a sample task for testing"


def test_get_task_not_found():
    """Test fetching a task that doesn't exist (404)."""
    response = client.get("/tasks/999")
    
    # Assert 404 status
    assert response.status_code == 404
    
    # Assert error in response
    data = response.json()
    assert "detail" in data


# ============================================================================
# TASK UPDATE TESTS
# ============================================================================

def test_update_task(sample_task):
    """Test updating a task."""
    # Create a task
    create_response = client.post("/tasks", json=sample_task)
    task_id = create_response.json()["id"]
    
    # Update the task
    update_data = {
        "title": "Updated Title",
        "status": "completed"
    }
    response = client.put(f"/tasks/{task_id}", json=update_data)
    
    # Assert status code
    assert response.status_code == 200
    
    # Assert updated data
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Updated Title"
    assert data["status"] == "completed"
    # Description should remain unchanged
    assert data["description"] == "This is a sample task for testing"


def test_update_task_partial():
    """Test partial update of a task."""
    # Create a task
    create_response = client.post("/tasks", json={
        "title": "Original Title",
        "description": "Original Description",
        "status": "pending"
    })
    task_id = create_response.json()["id"]
    
    # Update only the status
    update_data = {"status": "in_progress"}
    response = client.put(f"/tasks/{task_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    
    # Status should be updated
    assert data["status"] == "in_progress"
    # Others should remain unchanged
    assert data["title"] == "Original Title"
    assert data["description"] == "Original Description"


def test_update_task_not_found():
    """Test updating a task that doesn't exist."""
    update_data = {"title": "Updated"}
    response = client.put("/tasks/999", json=update_data)
    
    # Assert 404 status
    assert response.status_code == 404


# ============================================================================
# TASK DELETION TESTS
# ============================================================================

def test_delete_task(sample_task):
    """Test deleting a task."""
    # Create a task
    create_response = client.post("/tasks", json=sample_task)
    task_id = create_response.json()["id"]
    
    # Delete the task
    response = client.delete(f"/tasks/{task_id}")
    
    # Assert status code (204 No Content)
    assert response.status_code == 204
    
    # Verify task is deleted by trying to fetch it
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found():
    """Test deleting a task that doesn't exist."""
    response = client.delete("/tasks/999")
    
    # Assert 404 status
    assert response.status_code == 404


def test_delete_and_create_same_id():
    """Test creating, deleting, and creating again."""
    task1 = {"title": "Task 1", "description": "First"}
    task2 = {"title": "Task 2", "description": "Second"}
    
    # Create task 1
    response1 = client.post("/tasks", json=task1)
    id1 = response1.json()["id"]
    assert id1 == 1
    
    # Delete task 1
    client.delete(f"/tasks/{id1}")
    
    # Create task 2 - should get ID 2 (auto-increment)
    response2 = client.post("/tasks", json=task2)
    id2 = response2.json()["id"]
    assert id2 == 2  # Not 1, because ID auto-increments


# ============================================================================
# CONFIG ENDPOINT TESTS
# ============================================================================

def test_get_config():
    """Test retrieving application configuration."""
    response = client.get("/config")
    
    assert response.status_code == 200
    data = response.json()
    
    # Assert config values
    assert data["app_name"] == "TaskAPI"
    assert data["debug"] == True
    assert data["json_db_path"] == "./data/tasks.json"
    assert data["log_level"] == "INFO"


# ============================================================================
# ROOT ENDPOINT TEST
# ============================================================================

def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    
    # Assert response structure
    assert "message" in data
    assert "version" in data
    assert "endpoints" in data
    assert data["message"] == "TaskAPI"


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

def test_invalid_json_payload():
    """Test sending invalid JSON."""
    response = client.post(
        "/tasks",
        content="invalid json",
        headers={"Content-Type": "application/json"}
    )
    
    # Should return 422 or 400
    assert response.status_code in [400, 422]


def test_missing_required_field():
    """Test creating task with missing required field."""
    task_data = {
        "title": "No description"
        # Missing 'description' field
    }
    
    response = client.post("/tasks", json=task_data)
    
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

def test_full_task_lifecycle():
    """Test complete task lifecycle: create, read, update, delete."""
    # 1. Create
    create_data = {
        "title": "Lifecycle Test",
        "description": "Full lifecycle test",
        "status": "pending"
    }
    create_response = client.post("/tasks", json=create_data)
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]
    
    # 2. Read
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Lifecycle Test"
    
    # 3. Update
    update_data = {"status": "completed"}
    update_response = client.put(f"/tasks/{task_id}", json=update_data)
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "completed"
    
    # 4. Delete
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204
    
    # 5. Verify deletion
    final_get = client.get(f"/tasks/{task_id}")
    assert final_get.status_code == 404


def test_task_list_ordering():
    """Test that tasks are returned in reverse chronological order."""
    # Create tasks
    client.post("/tasks", json={"title": "Task 1", "description": "First"})
    client.post("/tasks", json={"title": "Task 2", "description": "Second"})
    client.post("/tasks", json={"title": "Task 3", "description": "Third"})
    
    # Get all tasks
    response = client.get("/tasks")
    tasks = response.json()
    
    # Should be in reverse order (most recent first)
    assert tasks[0]["title"] == "Task 3"
    assert tasks[1]["title"] == "Task 2"
    assert tasks[2]["title"] == "Task 1"
