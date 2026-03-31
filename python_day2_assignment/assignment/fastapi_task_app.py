from fastapi import FastAPI, HTTPException, status, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
import time
import logging


# ============================================================================
# CUSTOM EXCEPTIONS
# ============================================================================

class TaskNotFoundError(Exception):
    """Custom exception for when a task is not found."""
    
    def __init__(self, task_id: int):
        """
        Initialize the exception.
        
        Args:
            task_id: The task ID that was not found
        """
        self.task_id = task_id
        self.message = f"Task with id {task_id} not found"
        super().__init__(self.message)


class InvalidStatusError(Exception):
    """Custom exception for invalid status values."""
    
    def __init__(self, status: str):
        """
        Initialize the exception.
        
        Args:
            status: The invalid status value
        """
        self.status = status
        self.message = f"Invalid status: {status}. Must be one of: pending, in_progress, completed"
        super().__init__(self.message)


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class TaskCreate(BaseModel):
    """Model for creating a new task."""
    
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: str = Field(..., min_length=1, description="Task description")
    status: Literal["pending", "in_progress", "completed"] = Field(
        default="pending",
        description="Task status"
    )


class TaskUpdate(BaseModel):
    """Model for updating a task."""
    
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, min_length=1, description="Task description")
    status: Optional[Literal["pending", "in_progress", "completed"]] = Field(
        None,
        description="Task status"
    )


class TaskResponse(BaseModel):
    """Model for task response (includes ID and timestamps)."""
    
    id: int = Field(..., description="Task ID")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Task description")
    status: Literal["pending", "in_progress", "completed"] = Field(..., description="Task status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str = Field(..., description="Health status")


class ErrorResponse(BaseModel):
    """Structured error response."""
    
    error: str = Field(..., description="Exception class name")
    message: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")


# ============================================================================
# IN-MEMORY STORAGE
# ============================================================================

class Task:
    """Internal Task class for storage."""
    
    def __init__(self, task_id: int, title: str, description: str, status: str):
        self.id = task_id
        self.title = title
        self.description = description
        self.status = status
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_response(self) -> TaskResponse:
        """Convert to TaskResponse model."""
        return TaskResponse(
            id=self.id,
            title=self.title,
            description=self.description,
            status=self.status,
            created_at=self.created_at,
            updated_at=self.updated_at
        )


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="Task Management API",
    description="A simple task management API with CRUD operations",
    version="1.0.0"
)

# In-memory storage
task_database: dict[int, Task] = {}
current_id = 0


# ============================================================================
# MIDDLEWARE
# ============================================================================

@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    """
    Middleware to log every incoming request with timestamp, method, path,
    status code, and response time.
    
    Logs to api_logs.txt with format:
    YYYY-MM-DD HH:MM:SS | METHOD /path | Status: CODE | Time: XXms
    
    Args:
        request: The HTTP request
        call_next: The next middleware or endpoint
        
    Returns:
        The response from the endpoint
    """
    # Record start time
    start_time = time.time()
    
    # Call the next middleware/endpoint
    response = await call_next(request)
    
    # Calculate response time in milliseconds
    end_time = time.time()
    process_time_ms = (end_time - start_time) * 1000
    
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Extract request details
    method = request.method
    path = request.url.path
    status_code = response.status_code
    
    # Format log entry
    log_entry = f"{timestamp} | {method} {path} | Status: {status_code} | Time: {process_time_ms:.0f}ms"
    
    # Write to log file
    try:
        with open("api_logs.txt", "a") as log_file:
            log_file.write(log_entry + "\n")
    except Exception as e:
        # If logging fails, don't crash the application
        print(f"Failed to write log: {e}")
    
    return response


# ============================================================================
# EXCEPTION HANDLERS
# ============================================================================

@app.exception_handler(TaskNotFoundError)
async def task_not_found_exception_handler(request: Request, exc: TaskNotFoundError):
    """
    Handle TaskNotFoundError exceptions.
    
    Args:
        request: The HTTP request
        exc: The TaskNotFoundError exception
        
    Returns:
        JSONResponse with structured error response
    """
    return JSONResponse(
        status_code=404,
        content={
            "error": "TaskNotFoundError",
            "message": exc.message,
            "status_code": 404
        }
    )


@app.exception_handler(InvalidStatusError)
async def invalid_status_exception_handler(request: Request, exc: InvalidStatusError):
    """
    Handle InvalidStatusError exceptions.
    
    Args:
        request: The HTTP request
        exc: The InvalidStatusError exception
        
    Returns:
        JSONResponse with structured error response
    """
    return JSONResponse(
        status_code=400,
        content={
            "error": "InvalidStatusError",
            "message": exc.message,
            "status_code": 400
        }
    )


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_next_id() -> int:
    """Get the next task ID."""
    global current_id
    current_id += 1
    return current_id


def get_task_or_404(task_id: int) -> Task:
    """Get a task by ID or raise TaskNotFoundError."""
    if task_id not in task_database:
        raise TaskNotFoundError(task_id)
    return task_database[task_id]


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Status of the API
    """
    return HealthResponse(status="healthy")


@app.post("/tasks", response_model=TaskResponse, status_code=201)
async def create_task(task: TaskCreate):
    """
    Create a new task.
    
    Args:
        task: Task creation data
        
    Returns:
        TaskResponse: Created task with ID and timestamps
    """
    task_id = get_next_id()
    new_task = Task(
        task_id=task_id,
        title=task.title,
        description=task.description,
        status=task.status
    )
    task_database[task_id] = new_task
    return new_task.to_response()


@app.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(status: Optional[str] = Query(None, description="Filter by status")):
    """
    List all tasks with optional status filter.
    
    Args:
        status: Optional status filter (pending, in_progress, completed)
        
    Returns:
        List[TaskResponse]: List of tasks matching the filter
    """
    tasks = list(task_database.values())
    
    # Filter by status if provided
    if status:
        if status not in ["pending", "in_progress", "completed"]:
            raise InvalidStatusError(status)
        tasks = [t for t in tasks if t.status == status]
    
    # Sort by creation date, most recent first
    tasks.sort(key=lambda t: t.created_at, reverse=True)
    
    return [t.to_response() for t in tasks]


@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    """
    Get a specific task by ID.
    
    Args:
        task_id: Task ID
        
    Returns:
        TaskResponse: The requested task
    """
    task = get_task_or_404(task_id)
    return task.to_response()


@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskUpdate):
    """
    Update a task.
    
    Args:
        task_id: Task ID
        task_update: Updated task data (partial update allowed)
        
    Returns:
        TaskResponse: Updated task
    """
    task = get_task_or_404(task_id)
    
    # Update only provided fields
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.status is not None:
        task.status = task_update.status
    
    task.updated_at = datetime.now()
    
    return task.to_response()


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    """
    Delete a task.
    
    Args:
        task_id: Task ID
    """
    task = get_task_or_404(task_id)
    del task_database[task_id]
    return None


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Task Management API",
        "version": "1.0.0",
        "endpoints": {
            "health": "GET /health",
            "create_task": "POST /tasks",
            "list_tasks": "GET /tasks",
            "get_task": "GET /tasks/{task_id}",
            "update_task": "PUT /tasks/{task_id}",
            "delete_task": "DELETE /tasks/{task_id}",
            "docs": "/docs (Swagger UI)",
            "redoc": "/redoc (ReDoc)"
        }
    }
