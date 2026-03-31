"""Task endpoint tests."""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture(scope="module")
def test_owner():
    """Create a test user."""
    response = client.post(
        "/users/register",
        json={
            "username": "taskowner",
            "email": "taskowner@mail.com",
            "password": "securepass123"
        }
    )
    return response.json()["username"]


class TestTaskCreation:
    """Test task creation endpoint."""
    
    def test_create_task(self, test_owner):
        """Test successful task creation."""
        response = client.post(
            "/tasks",
            json={
                "title": "Write report",
                "description": "Q2 summary report",
                "priority": "high",
                "status": "pending",
                "owner": test_owner
            }
        )
        assert response.status_code == 201
        assert response.json()["title"] == "Write report"
        assert response.json()["status"] == "pending"
    
    def test_create_task_invalid_title(self, test_owner):
        """Test short title rejection."""
        response = client.post(
            "/tasks",
            json={
                "title": "ab",
                "description": "Test description",
                "priority": "high",
                "owner": test_owner
            }
        )
        assert response.status_code == 422


class TestTaskList:
    """Test task list endpoint."""
    
    def test_list_tasks(self, test_owner):
        """Test listing tasks."""
        # Create some tasks
        for i in range(3):
            client.post(
                "/tasks",
                json={
                    "title": f"Task {i}",
                    "description": f"Description {i}",
                    "priority": "medium",
                    "owner": test_owner
                }
            )
        
        response = client.get("/tasks")
        assert response.status_code == 200
        assert len(response.json()["data"]) == 3
    
    def test_list_tasks_with_filter(self, test_owner):
        """Test filtering tasks by priority."""
        # Create tasks with different priorities
        client.post(
            "/tasks",
            json={
                "title": "High priority task",
                "priority": "high",
                "status": "pending",
                "owner": test_owner
            }
        )
        client.post(
            "/tasks",
            json={
                "title": "Low priority task",
                "priority": "low",
                "status": "pending",
                "owner": test_owner
            }
        )
        
        # Filter by priority
        response = client.get("/tasks?priority=high")
        assert response.status_code == 200
        assert len(response.json()["data"]) >= 1


class TestTaskUpdate:
    """Test task update endpoint."""
    
    def test_full_update_task(self, test_owner):
        """Test full task update."""
        # Create task
        create_response = client.post(
            "/tasks",
            json={
                "title": "Original title",
                "priority": "low",
                "owner": test_owner
            }
        )
        task_id = create_response.json()["id"]
        
        # Update task
        response = client.put(
            f"/tasks/{task_id}",
            json={
                "title": "Updated title",
                "priority": "high",
                "status": "completed"
            }
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Updated title"
        assert response.json()["priority"] == "high"
    
    def test_partial_update_task(self, test_owner):
        """Test partial task update."""
        # Create task
        create_response = client.post(
            "/tasks",
            json={
                "title": "Original title",
                "description": "Original description",
                "priority": "low",
                "owner": test_owner
            }
        )
        task_id = create_response.json()["id"]
        
        # Partial update
        response = client.patch(
            f"/tasks/{task_id}",
            json={
                "priority": "high"
            }
        )
        assert response.status_code == 200
        assert response.json()["priority"] == "high"
        assert response.json()["title"] == "Original title"


class TestTaskDelete:
    """Test task delete endpoint."""
    
    def test_delete_task(self, test_owner):
        """Test deleting a task."""
        # Create task
        create_response = client.post(
            "/tasks",
            json={
                "title": "Task to delete",
                "owner": test_owner
            }
        )
        task_id = create_response.json()["id"]
        
        # Delete task
        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 200
        
        # Verify deleted
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 404
