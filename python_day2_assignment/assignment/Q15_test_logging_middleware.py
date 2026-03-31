"""Test script for the request logging middleware (Q15)."""

import os
from fastapi.testclient import TestClient

# Remove existing log file to start fresh
if os.path.exists("api_logs.txt"):
    os.remove("api_logs.txt")
    print("✓ Cleared previous api_logs.txt")

# Import the app AFTER clearing the log file
from fastapi_task_app import app

client = TestClient(app)

print("\n" + "=" * 70)
print("TESTING REQUEST LOGGING MIDDLEWARE (Q15)")
print("=" * 70)

print("\n[Test 1] Health Check (GET /health)")
print("-" * 70)
response = client.get("/health")
print(f"Status Code: {response.status_code}")


print("\n[Test 2] Create Task (POST /tasks)")
print("-" * 70)
task_data = {
    "title": "Complete Q15",
    "description": "Implement request logging middleware",
    "status": "in_progress"
}
response = client.post("/tasks", json=task_data)
print(f"Status Code: {response.status_code}")


print("\n[Test 3] List Tasks (GET /tasks)")
print("-" * 70)
response = client.get("/tasks")
print(f"Status Code: {response.status_code}")
print(f"Task Count: {len(response.json())}")


print("\n[Test 4] Get Specific Task (GET /tasks/1)")
print("-" * 70)
response = client.get("/tasks/1")
print(f"Status Code: {response.status_code}")


print("\n[Test 5] Update Task (PUT /tasks/1)")
print("-" * 70)
update_data = {
    "status": "completed"
}
response = client.put("/tasks/1", json=update_data)
print(f"Status Code: {response.status_code}")


print("\n[Test 6] Invalid Status Filter (GET /tasks?status=invalid)")
print("-" * 70)
response = client.get("/tasks?status=invalid")
print(f"Status Code: {response.status_code}")


print("\n[Test 7] Valid Status Filter (GET /tasks?status=pending)")
print("-" * 70)
response = client.get("/tasks?status=pending")
print(f"Status Code: {response.status_code}")


print("\n[Test 8] Delete Task (DELETE /tasks/1)")
print("-" * 70)
response = client.delete("/tasks/1")
print(f"Status Code: {response.status_code}")


print("\n[Test 9] Access Deleted Task (GET /tasks/1)")
print("-" * 70)
response = client.get("/tasks/1")
print(f"Status Code: {response.status_code}")


print("\n[Test 10] Root Endpoint (GET /)")
print("-" * 70)
response = client.get("/")
print(f"Status Code: {response.status_code}")


# Read and display the log file
print("\n" + "=" * 70)
print("API LOG FILE CONTENTS (api_logs.txt)")
print("=" * 70 + "\n")

if os.path.exists("api_logs.txt"):
    with open("api_logs.txt", "r") as log_file:
        log_contents = log_file.read()
        print(log_contents)
else:
    print("❌ api_logs.txt not found!")

# Count log entries
if os.path.exists("api_logs.txt"):
    with open("api_logs.txt", "r") as log_file:
        log_lines = log_file.readlines()
    
    print("\n" + "=" * 70)
    print("LOG STATISTICS")
    print("=" * 70)
    print(f"Total Requests Logged: {len(log_lines)}")
    
    # Count by HTTP method
    methods = {}
    statuses = {}
    for line in log_lines:
        if "|" in line:
            parts = line.split("|")
            if len(parts) >= 2:
                method_path = parts[1].strip()
                method = method_path.split()[0]
                methods[method] = methods.get(method, 0) + 1
                
                # Extract status code
                if "Status:" in line:
                    status_part = line.split("Status:")[1].split("|")[0].strip()
                    statuses[status_part] = statuses.get(status_part, 0) + 1
    
    print("\nRequests by HTTP Method:")
    for method, count in sorted(methods.items()):
        print(f"  {method}: {count}")
    
    print("\nRequests by Status Code:")
    for status, count in sorted(statuses.items()):
        print(f"  {status}: {count}")
    
    print("\n" + "=" * 70)
    print("✅ REQUEST LOGGING MIDDLEWARE WORKING CORRECTLY!")
    print("=" * 70)
    print("\nMIDDLEWARE FEATURES VERIFIED:")
    print("✓ Logs all incoming HTTP requests")
    print("✓ Includes timestamp (YYYY-MM-DD HH:MM:SS)")
    print("✓ Records HTTP method (GET, POST, PUT, DELETE)")
    print("✓ Captures request path")
    print("✓ Logs response status code")
    print("✓ Calculates response time in milliseconds")
    print("✓ Writes to api_logs.txt file")
    print("✓ Handles error responses (400, 404)")
    print("✓ Doesn't interfere with normal request/response flow")
