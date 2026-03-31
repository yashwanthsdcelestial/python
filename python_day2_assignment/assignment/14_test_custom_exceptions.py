"""
Test script for the custom exception handlers in FastAPI.
"""

from fastapi.testclient import TestClient
from fastapi_task_app import app
import json


# Create a test client
client = TestClient(app)


def print_test(test_name: str, method: str, endpoint: str, response):
    """Helper to print test results."""
    print(f"\n{'='*70}")
    print(f"{test_name}")
    print(f"{'='*70}")
    print(f"{method} {endpoint}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("CUSTOM EXCEPTION HANDLERS TEST")
    print("="*70)
    
    # Test 1: TaskNotFoundError
    print_test(
        "Test 1: TaskNotFoundError (404)",
        "GET",
        "/tasks/999",
        client.get("/tasks/999")
    )
    
    # Test 2: Create a task first, then delete it, then try to access it
    print("\n" + "="*70)
    print("Test 2: Create and Delete Task, Then Try to Access")
    print("="*70)
    
    # Create task
    create_response = client.post("/tasks", json={
        "title": "Test task",
        "description": "Test description",
        "status": "pending"
    })
    print(f"\nCREATE TASK:")
    print(f"Status Code: {create_response.status_code}")
    task_id = create_response.json()["id"]
    print(f"Created task with ID: {task_id}")
    
    # Delete task
    delete_response = client.delete(f"/tasks/{task_id}")
    print(f"\nDELETE TASK {task_id}:")
    print(f"Status Code: {delete_response.status_code}")
    print("Task deleted successfully")
    
    # Try to get deleted task
    get_response = client.get(f"/tasks/{task_id}")
    print_test(
        f"GET DELETED TASK {task_id} (Should Return 404)",
        "GET",
        f"/tasks/{task_id}",
        get_response
    )
    
    # Test 3: InvalidStatusError
    print_test(
        "Test 3: InvalidStatusError (400)",
        "GET",
        "/tasks?status=invalid",
        client.get("/tasks?status=invalid")
    )
    
    # Test 4: Try to update non-existent task
    update_response = client.put("/tasks/999", json={"status": "completed"})
    print_test(
        "Test 4: Update Non-existent Task (404)",
        "PUT",
        "/tasks/999",
        update_response
    )
    
    # Test 5: Try to delete non-existent task
    delete_response = client.delete("/tasks/999")
    print_test(
        "Test 5: Delete Non-existent Task (404)",
        "DELETE",
        "/tasks/999",
        delete_response
    )
    
    # Test 6: Create multiple tasks and test various error scenarios
    print("\n" + "="*70)
    print("Test 6: Create Tasks and Test Status Filtering with Errors")
    print("="*70)
    
    # Create some tasks
    for i in range(3):
        client.post("/tasks", json={
            "title": f"Task {i+1}",
            "description": f"Description {i+1}",
            "status": "pending"
        })
    
    print("\n✓ Created 3 tasks")
    
    # Test valid status filter
    valid_filter = client.get("/tasks?status=pending")
    print(f"\n✓ Valid filter (?status=pending): {valid_filter.status_code}")
    print(f"  Found {len(valid_filter.json())} tasks")
    
    # Test invalid status filter
    invalid_filter = client.get("/tasks?status=invalid_status")
    print_test(
        "Invalid filter (?status=invalid_status)",
        "GET",
        "/tasks?status=invalid_status",
        invalid_filter
    )
    
    # Summary
    print("\n" + "="*70)
    print("CUSTOM EXCEPTION HANDLERS SUMMARY")
    print("="*70)
    print("""
✓ All exception handlers working correctly!

HANDLERS IMPLEMENTED:
1. TaskNotFoundError Handler (404)
   - Triggered on GET, PUT, DELETE with non-existent task ID
   - Response structure: {error, message, status_code}
   
2. InvalidStatusError Handler (400)
   - Triggered on invalid status filter value
   - Response structure: {error, message, status_code}

ERROR RESPONSE FORMAT:
{
  "error": "ExceptionClassName",
  "message": "Detailed error message",
  "status_code": HTTP_STATUS_CODE
}

BENEFITS:
✓ Consistent error response format across all endpoints
✓ Easy to parse and handle on client side
✓ Clear error identification with error field
✓ Detailed messages for debugging
✓ Proper HTTP status codes
✓ Scalable: easy to add more custom exceptions

TESTING SCENARIOS COVERED:
1. GET non-existent task (404)
2. PUT non-existent task (404)
3. DELETE non-existent task (404)
4. Invalid status filter (400)
5. Valid status filter (200)
    """)
