# Day 3 Mini Project: Task Manager Migration to SQLAlchemy + Supabase

## Overview

This project migrates the Day-2 Task Management System from JSON file storage to SQLAlchemy ORM with a PostgreSQL/Supabase backend. All endpoints, schemas, and error handling remain identical, but data now persists in a real relational database.

## Architecture Changes

### What Changed:
| Component | Day 2 (JSON) | Day 3 (SQLAlchemy) |
|-----------|-------------|------------------|
| **Storage** | `json_repository.py` | `sqlalchemy_repository.py` |
| **Models** | Pydantic only | Pydantic schemas + SQLAlchemy ORM models |
| **DB Setup** | None | `database.py` (engine, session, Base) |
| **Migrations** | Manual | Alembic v1.14.1 with versioning |
| **Connection** | File I/O | Connection pool (5 connections, pool_pre_ping=True) |
| **Background Tasks** | None | Background task on task creation |

### What Stayed the Same:
- ✅ All API endpoints (same URLs, methods, status codes)
- ✅ Pydantic schemas (TaskCreate, TaskUpdate, TaskResponse, etc.)
- ✅ Custom exceptions (TaskNotFoundError, UserNotFoundError, etc.)
- ✅ Logging middleware
- ✅ Error handlers
- ✅ Router structure
- ✅ Service layer logic

## Project Structure

```
day_3_mini_project3/
├── main.py                          # Updated: DB initialization in lifespan
├── config.py                        # Updated: Added DATABASE_URL
├── database.py                      # NEW: SQLAlchemy engine, SessionLocal, Base, get_db()
├── alembic.ini                      # NEW: Alembic configuration
├── alembic/                         # NEW: Migrations directory
│   ├── env.py                       # Migration environment
│   ├── script.py.mako               # Migration template
│   └── versions/
│       └── 001_initial.py          # Initial schema migration
├── models/
│   ├── schemas.py                   # Unchanged: Pydantic schemas
│   ├── enums.py                     # Unchanged: TaskStatus, TaskPriority
│   └── db_models.py                # NEW: SQLAlchemy User & Task models
├── services/
│   ├── task_service.py              # Updated: Uses new repository
│   └── user_service.py              # Updated: Uses new repository
├── repositories/
│   ├── base_repository.py           # Unchanged: DIP interface
│   └── sqlalchemy_repository.py     # NEW: SQLAlchemy implementation
├── routers/
│   ├── task_router.py               # Updated: Added BackgroundTasks
│   └── user_router.py               # Updated: Uses SQLAlchemy repo
├── middleware/
│   └── logging_middleware.py        # NEW: HTTP request/response logging
├── exceptions/
│   └── custom_exceptions.py         # NEW: Custom exception classes
├── utils/
│   ├── logger.py                    # NEW: Logger setup utility
│   ├── security.py                  # NEW: Password hashing (PBKDF2+salt)
│   └── background_tasks.py          # NEW: Background task utilities
├── tests/
│   ├── test_tasks.py                # Updated: DB test fixtures
│   └── test_users.py                # Updated: DB test fixtures
├── logs/
│   ├── app.log                      # Application logs (with SQLAlchemy entries)
│   └── notifications.log            # Background task notifications
├── .env                             # Updated: DATABASE_URL added
├── requirements.txt                 # Updated: Added sqlalchemy, psycopg2-binary, alembic
└── README.md                        # This file
```

## Key Features

### 1. Database Configuration
- **Engine**: PostgreSQL with connection pool (pool_size=5, pool_pre_ping=True)
- **Session Management**: Dependency injection via `get_db()`
- **Pool Settings**: 
  - `pool_pre_ping=True`: Test connections before using
  - `pool_recycle=3600`: Recycle connections every hour
  - Prevents "connection lost" errors in long-running apps

### 2. SQLAlchemy Models
- **User Model**: username, email, password (hashed), created_at
- **Task Model**: title, description, status, priority, owner, created_at, updated_at
- **Relationships**: User has many Tasks (one-to-many)
- **Cascading**: Deleting user deletes their tasks (cascade delete)

### 3. Repository Pattern (DIP)
- `BaseRepository`: Abstract interface (unchanged from Day 2)
- `SQLAlchemyRepository`: Concrete implementation
- Services inject repository via DI → **swappable storage backends**

### 4. Alembic Migrations
- **Initial Migration** (`001_initial.py`): Creates users and tasks tables
- **Enum Types**: TaskStatus and TaskPriority as PostgreSQL ENUMs
- **Indexes**: On id, username, email, title, owner for performance
- **Foreign Keys**: Tasks.owner_id → Users.id with SET NULL on delete

### 5. Background Tasks
- **Feature**: Async notification logging on task creation
- **File**: `logs/notifications.log`
- **Format**: `[TIMESTAMP] Task '<title>' created by <owner> — notification sent`

### 6. Password Security
- **Algorithm**: PBKDF2-HMAC-SHA256 with 100,000 iterations
- **Salt**: Random 32-byte salt per password
- **Storage**: Base64-encoded (salt + hash)

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

**Key packages added:**
- `sqlalchemy==2.0.35`: ORM framework
- `psycopg2-binary==2.9.10`: PostgreSQL driver
- `alembic==1.14.1`: Database migrations

### 2. Configure Environment
Update `.env` with your Supabase credentials:
```env
APP_NAME=TaskAPI
DEBUG=true
LOG_LEVEL=INFO
DATABASE_URL=postgresql://postgres:<password>@<host>:5432/postgres
```

### 3. Run Database Migrations
```bash
# Create or update database schema
alembic upgrade head
```

This creates:
- `users` table with constraints
- `tasks` table with foreign key to users
- Indexes for performance
- Enum types for status and priority

### 4. Start Application
```bash
uvicorn main:app --reload
```

Visit: http://localhost:8000/docs

## API Endpoints

All endpoints work identically to Day 2:

### Users
- `POST /users/register` - Register new user
- `POST /users/login` - Login user
- `GET /users` - List all users
- `GET /users/{id}` - Get user by ID
- `DELETE /users/{id}` - Delete user

### Tasks
- `POST /tasks` - Create task (triggers background notification)
- `GET /tasks` - List tasks (with filtering & pagination)
- `GET /tasks/{id}` - Get task by ID
- `PUT /tasks/{id}` - Full task update
- `PATCH /tasks/{id}` - Partial task update
- `DELETE /tasks/{id}` - Delete task

### Health & Root
- `GET /health` - Health check
- `GET /` - Root endpoint

## Dependency Injection Strategy

### Service Layer
```python
# Services receive repository via dependency injection
class TaskService:
    def __init__(self, repository: BaseRepository):  # DIP
        self.repository = repository
```

### Router Layer
```python
# Routers inject SQLAlchemy repository
def get_task_repository(db: Session = Depends(get_db)):
    return SQLAlchemyRepository(Task, db)

def get_task_service(repo = Depends(get_task_repository)):
    return TaskService(repo)
```

### Key Benefit
To switch back to JSON storage:
1. Create `JsonRepository` implementing `BaseRepository`
2. Update only the dependency: `get_task_repository()`
3. **Zero changes** to services or business logic

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(30) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
-- Indexes: username, email, id
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    status task_status NOT NULL DEFAULT 'pending',
    priority task_priority NOT NULL DEFAULT 'medium',
    owner VARCHAR(30) NOT NULL,
    owner_id INTEGER FOREIGN KEY (users.id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
-- Indexes: id, title, owner, owner_id
-- Foreign Key: owner_id -> users.id
```

## Logging

### Application Logs (`logs/app.log`)
- Startup/shutdown events
- Database operations
- User registration/login
- Task CRUD operations
- API request/response (via middleware)
- Errors and warnings

### Notification Logs (`logs/notifications.log`)
- Task creation background task (async)
- Format: `[TIMESTAMP] Task '<title>' created by <owner> — notification sent`

## Testing

### Pytest Fixtures (Updated)
Tests now use SQLAlchemy fixtures instead of JSON:
```python
@pytest.fixture
def db_session():
    """Database session for testing."""
    return SessionLocal()
```

### Running Tests
```bash
pytest tests/ -v
```

## Comparison: JSON vs SQLAlchemy

### JSON Approach (Day 2)
```
Pro:
  ✓ Simple, file-based
  ✓ No database setup
  ✓ Easy to understand

Con:
  ✗ Manual ID management
  ✗ Load entire file for queries
  ✗ Race conditions (no locking)
  ✗ Not scalable
```

### SQLAlchemy (Day 3)
```
Pro:
  ✓ Connection pooling (efficient)
  ✓ SQL indexes (fast queries)
  ✓ Relationships (join support)
  ✓ Transactions (ACID compliance)
  ✓ Migrations (schema versioning)
  ✓ Scalable (many concurrent users)

Con:
  ✗ More complex setup
  ✗ Database dependency
```

## Supabase Setup

### Step 1: Create Supabase Project
1. Go to https://supabase.com
2. Create new project
3. Copy connection string from Settings → Database

### Step 2: Update .env
```env
DATABASE_URL=postgresql://postgres:<your_password>@<project_id>.supabase.co:5432/postgres
```

### Step 3: Run Migrations
```bash
alembic upgrade head
```

## DIP (Dependency Inversion Principle) Validation

To verify the system adheres to DIP:

1. **Create `repositories/json_repository.py`** implementing `BaseRepository`
2. **Update** `routers/task_router.py`:
   ```python
   def get_task_repository():
       return JsonRepository(settings.tasks_db_path)  # Not SQLAlchemy
   ```
3. **Run tests**: Should pass without changes to services!
   ```bash
   pytest tests/ -v
   ```

This proves the architecture is truly decoupled.

## Submission Checklist

- [x] All source files present
- [x] SQLAlchemy models (db_models.py)
- [x] Repository implementation (sqlalchemy_repository.py)
- [x] Database configuration (database.py)
- [x] Alembic migrations (alembic/ folder with 001_initial.py)
- [x] Background tasks (utils/background_tasks.py)
- [x] notifications.log with ≥2 entries
- [x] app.log with logged entries
- [x] requirements.txt with pinned versions
- [x] .env file with DATABASE_URL placeholder
- [x] DIP validation (swappable repositories)

## Running a Quick Test

```python
# Test imports
python -c "import main; print('✓ Main imported')"

# Test database connection
python -c "
from database import engine
engine.execute('SELECT 1')
print('✓ Database connected')
"

# Start server
uvicorn main:app --reload
```

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'sqlalchemy'`
```bash
pip install sqlalchemy==2.0.35
```

### Issue: `psycopg2 not found`
```bash
pip install psycopg2-binary==2.9.10
```

### Issue: `AlembicConfigurationError`
Ensure `alembic.ini` is in the project root and `PYTHONPATH` includes the project directory.

### Issue: Connection refused
Verify `DATABASE_URL` in `.env` is correct:
```
postgresql://user:password@host:port/database
```

## References

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)
- [Supabase PostgreSQL](https://supabase.com/docs)
- [FastAPI Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)

## Summary

This migration demonstrates:
- ✅ Scalable database architecture with connection pooling
- ✅ Proper ORM usage with relationships and cascading
- ✅ Database migrations for schema versioning
- ✅ Async background tasks
- ✅ Strict adherence to SOLID principles (especially DIP)
- ✅ Production-ready error handling and logging
- ✅ Security best practices (password hashing)

The system is now ready for deployment to production with a real database!
