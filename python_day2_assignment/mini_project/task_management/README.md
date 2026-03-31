# FastAPI Task Management System

A production-style Task Management REST API built with FastAPI, Pydantic, and JSON file storage, fully following SOLID principles and OOP best practices.

## 📋 Project Overview

This is a complete Task Management System with:
- **User Management** (Registration, Login, CRUD operations)
- **Task Management** (Create, Read, Update, Delete with filtering and pagination)
- **JSON-based storage** (Persistent data across server restarts)
- **Structured logging** (File-based with timestamps)
- **Error handling** (Custom exceptions with proper HTTP status codes)
- **Environment configuration** (Pydantic Settings from .env)
- **Full test coverage** (pytest with TestClient)

## 🏗️ Project Structure

```
day_2_mini_project/
├── main.py                          # FastAPI application entry point
├── config.py                        # Environment & configuration settings
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables
│
├── models/
│   ├── __init__.py
│   ├── schemas.py                   # Pydantic request/response models
│   └── enums.py                     # Status and Priority enums
│
├── services/
│   ├── __init__.py
│   ├── user_service.py              # User business logic
│   └── task_service.py              # Task business logic
│
├── repositories/
│   ├── __init__.py
│   ├── base_repository.py           # Abstract interface (DIP)
│   └── json_repository.py           # JSON file implementation
│
├── routers/
│   ├── __init__.py
│   ├── user_router.py               # User endpoints
│   └── task_router.py               # Task endpoints
│
├── middleware/
│   ├── __init__.py
│   └── logging_middleware.py        # Request/response logging
│
├── exceptions/
│   ├── __init__.py
│   └── custom_exceptions.py         # Custom exception classes
│
├── utils/
│   ├── __init__.py
│   ├── logger.py                    # Structured logging setup
│   └── security.py                  # Password hashing utilities
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # pytest configuration
│   ├── test_users.py                # User endpoint tests
│   └── test_tasks.py                # Task endpoint tests
│
├── data/
│   ├── users.json                   # Users database (JSON)
│   └── tasks.json                   # Tasks database (JSON)
│
└── logs/
    └── app.log                      # Application logs
```

## 🎯 SOLID Principles Implementation

### ✅ Single Responsibility Principle (SRP)
- **Routers**: Only handle HTTP request/response mapping
- **Services**: Contain all business logic (validation, workflows)
- **Repositories**: Handle data persistence (JSON read/write)
- **Middleware**: Manage cross-cutting concerns (logging)

### ✅ Open/Closed Principle (OCP)
- Add new entities (e.g., Projects) without modifying existing code
- Just add new router, service, and repository files
- Existing code remains closed for modification

### ✅ Liskov Substitution Principle (LSP)
- `JSONRepository` is replaceable with any `BaseRepository` implementation
- Service layer uses abstraction, not concrete implementations

### ✅ Interface Segregation Principle (ISP)
- `BaseRepository` only defines data access methods
- No logging or validation in repository interface

### ✅ Dependency Inversion Principle (DIP)
- Services depend on `BaseRepository` (abstraction)
- Repositories injected via FastAPI `Depends()`
- Configuration injected at startup

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- pip package manager

### Installation

1. **Navigate to project directory**
   ```bash
   cd day_2_mini_project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify .env file** (already configured)
   ```
   APP_NAME=TaskAPI
   DEBUG=true
   LOG_LEVEL=INFO
   JSON_DB_PATH=./data
   LOG_FILE_PATH=./logs/app.log
   ```

### Running the Application

**Start development server:**
```bash
python main.py
```

**Or using uvicorn directly:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**API Documentation (auto-generated):**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_users.py

# Run with coverage
pytest --cov=.

# Run with verbose output
pytest -v
```

## 📚 API Endpoints

### User Endpoints

#### Register User
```
POST /users/register
Content-Type: application/json

{
  "username": "alice",
  "email": "alice@mail.com",
  "password": "securepass123"
}

Response: 201 Created
{
  "id": 1,
  "username": "alice",
  "email": "alice@mail.com",
  "created_at": "2026-03-20T09:00:00"
}
```

#### Login User
```
POST /users/login
Content-Type: application/json

{
  "username": "alice",
  "password": "securepass123"
}

Response: 200 OK
{
  "id": 1,
  "username": "alice",
  "email": "alice@mail.com",
  "created_at": "2026-03-20T09:00:00"
}
```

#### List All Users
```
GET /users

Response: 200 OK
[
  {
    "id": 1,
    "username": "alice",
    "email": "alice@mail.com",
    "created_at": "2026-03-20T09:00:00"
  }
]
```

#### Delete User
```
DELETE /users/{user_id}

Response: 200 OK
{
  "message": "User 1 deleted successfully"
}
```

### Task Endpoints

#### Create Task
```
POST /tasks
Content-Type: application/json

{
  "title": "Write report",
  "description": "Q2 summary",
  "priority": "high",
  "status": "pending",
  "owner": "alice"
}

Response: 201 Created
{
  "id": 1,
  "title": "Write report",
  "description": "Q2 summary",
  "status": "pending",
  "priority": "high",
  "owner": "alice",
  "created_at": "2026-03-20T10:00:00",
  "updated_at": "2026-03-20T10:00:00"
}
```

#### List Tasks (with filtering & pagination)
```
GET /tasks?status=pending&priority=high&owner=alice&page=1&limit=10

Response: 200 OK
{
  "data": [
    {
      "id": 1,
      "title": "Write report",
      "description": "Q2 summary",
      "status": "pending",
      "priority": "high",
      "owner": "alice",
      "created_at": "2026-03-20T10:00:00",
      "updated_at": "2026-03-20T10:00:00"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 1,
    "pages": 1
  }
}
```

#### Get Task by ID
```
GET /tasks/{task_id}

Response: 200 OK
{
  "id": 1,
  "title": "Write report",
  "description": "Q2 summary",
  "status": "pending",
  "priority": "high",
  "owner": "alice",
  "created_at": "2026-03-20T10:00:00",
  "updated_at": "2026-03-20T10:00:00"
}
```

#### Update Task (Full)
```
PUT /tasks/{task_id}
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description",
  "status": "in_progress",
  "priority": "medium"
}

Response: 200 OK
{
  "id": 1,
  "title": "Updated title",
  "description": "Updated description",
  "status": "in_progress",
  "priority": "medium",
  "owner": "alice",
  "created_at": "2026-03-20T10:00:00",
  "updated_at": "2026-03-20T10:05:00"
}
```

#### Partial Update Task
```
PATCH /tasks/{task_id}
Content-Type: application/json

{
  "status": "completed"
}

Response: 200 OK
{
  "id": 1,
  "title": "Updated title",
  "description": "Updated description",
  "status": "completed",
  "priority": "medium",
  "owner": "alice",
  "created_at": "2026-03-20T10:00:00",
  "updated_at": "2026-03-20T10:10:00"
}
```

#### Delete Task
```
DELETE /tasks/{task_id}

Response: 200 OK
{
  "message": "Task 1 deleted successfully"
}
```

## 🔍 Query Parameters

### Task Filtering
- `?status=pending` — Filter by status (pending, in_progress, completed, cancelled)
- `?priority=high` — Filter by priority (low, medium, high)
- `?owner=alice` — Filter by owner username

### Pagination
- `?page=1` — Page number (default: 1)
- `?limit=10` — Items per page (default: 10)

**Example:**
```
GET /tasks?status=pending&priority=high&owner=alice&page=1&limit=5
```

## 📊 Data Models

### User
```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@mail.com",
  "password": "hashed_password",
  "created_at": "2026-03-20T09:00:00"
}
```

### Task
```json
{
  "id": 1,
  "title": "Write report",
  "description": "Q2 summary",
  "status": "pending",
  "priority": "high",
  "owner": "alice",
  "created_at": "2026-03-20T10:00:00",
  "updated_at": "2026-03-20T10:00:00"
}
```

## 🔒 Error Handling

All errors return standardized JSON response:

```json
{
  "error": "ErrorClassName",
  "message": "Descriptive error message",
  "status_code": 404
}
```

### Error Codes

| Error | Status | Description |
|-------|--------|-------------|
| UserNotFoundError | 404 | User not found |
| TaskNotFoundError | 404 | Task not found |
| DuplicateUserError | 409 | Username already exists |
| InvalidCredentialsError | 401 | Wrong username/password |
| ValidationError | 422 | Invalid request data |

## 📝 Logging

Logs are written to `logs/app.log` with the format:

```
[TIMESTAMP] - LEVEL - MODULE - MESSAGE
```

### Example Log Entries

```
[2026-03-20 10:00:00] - INFO - user_service - User 'alice' registered successfully
[2026-03-20 10:05:00] - WARNING - user_service - Duplicate username: 'alice'
[2026-03-20 10:10:00] - ERROR - task_service - Task ID 999 not found
[2026-03-20 10:15:00] - INFO - middleware.logging_middleware - POST /tasks | 201 | 25ms
```

## 🧪 Testing with Postman

### Import Collection

1. Open Postman
2. Click **Import** → **Upload Files**
3. Select `postman_collection.json`

### Available Test Folders

- **Users**: Register, Login, List, Delete
- **Tasks**: Create, List, Get, Update (PUT), Partial Update (PATCH), Delete
- **Error Cases**: Invalid payload, Not found, Duplicate user, Bad credentials

### Example Postman Request

**Create Task:**
```
POST http://localhost:8000/tasks
Content-Type: application/json

{
  "title": "Write report",
  "description": "Q2 summary",
  "priority": "high",
  "status": "pending",
  "owner": "alice"
}
```

## 📦 Dependencies

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **pydantic**: Data validation
- **pydantic-settings**: Configuration management
- **pytest**: Testing framework
- **httpx**: HTTP client for testing

See `requirements.txt` for exact versions.

## 🔧 Configuration

### Environment Variables (.env)

```env
APP_NAME=TaskAPI              # Application name
DEBUG=true                    # Debug mode
LOG_LEVEL=INFO               # Logging level
JSON_DB_PATH=./data          # Data directory
LOG_FILE_PATH=./logs/app.log # Log file path
```

## 🎓 Learning Points

This project demonstrates:

1. **FastAPI**: Modern async web framework
2. **Pydantic**: Type hints and validation
3. **SOLID Principles**: Clean, maintainable code architecture
4. **Repository Pattern**: Abstraction for data persistence
5. **Dependency Injection**: Loose coupling
6. **Custom Exceptions**: Error handling patterns
7. **Structured Logging**: Production-ready logging
8. **Unit Testing**: Test-driven development with pytest

## 📄 License

This is an educational project for learning FastAPI and software design principles.

## 🤝 Support

For questions or issues:
1. Check if your Python version is 3.9+
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Check logs in `logs/app.log`
4. Run tests: `pytest -v`

---

**Created:** March 2026  
**Python Version:** 3.9+  
**FastAPI Version:** 0.104.1+
