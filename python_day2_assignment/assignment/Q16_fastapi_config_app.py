"""
Q16 - FastAPI app with Environment Variables and Config Management.

This app demonstrates using Pydantic BaseSettings to load configuration
from a .env file. All settings are loaded at startup and used throughout
the application as a singleton.
"""

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
import time
import logging
import os

# Import the settings singleton
from settings import settings

# Configure logging based on settings
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class TaskCreate(BaseModel):
    """Model for creating a new task."""
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    status: Literal["pending", "in_progress", "completed"] = Field(default="pending")


class TaskUpdate(BaseModel):
    """Model for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    status: Optional[Literal["pending", "in_progress", "completed"]] = None


class TaskResponse(BaseModel):
    """Model for task response."""
    id: int
    title: str
    description: str
    status: Literal["pending", "in_progress", "completed"]
    created_at: datetime
    updated_at: datetime


class ConfigResponse(BaseModel):
    """Model for configuration response."""
    app_name: str
    debug: bool
    json_db_path: str
    log_level: str


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

# Create app with name from settings
app = FastAPI(
    title=settings.app_name,
    description="Task Management API with Configuration Management",
    version="1.0.0"
)

# In-memory storage
task_database: dict[int, Task] = {}
current_id = 0


# ============================================================================
# STARTUP EVENT
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """
    Log configuration at startup.
    
    This demonstrates that settings are loaded from the .env file
    and displayed on startup as required.
    """
    startup_message = (
        f"App: {settings.app_name} | "
        f"Debug: {settings.debug} | "
        f"DB: {settings.json_db_path}"
    )
    print("\n" + "=" * 70)
    print("FASTAPI APPLICATION STARTUP")
    print("=" * 70)
    print(startup_message)
    print("=" * 70 + "\n")
    
    logger.info(f"Application: {settings.app_name}")
    logger.info(f"Debug Mode: {settings.debug}")
    logger.info(f"Database Path: {settings.json_db_path}")
    logger.info(f"Log Level: {settings.log_level}")


# ============================================================================
# MIDDLEWARE
# ============================================================================

@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    """Middleware to log requests."""
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    
    process_time_ms = (end_time - start_time) * 1000
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    method = request.method
    path = request.url.path
    status_code = response.status_code
    
    log_entry = f"{timestamp} | {method} {path} | Status: {status_code} | Time: {process_time_ms:.0f}ms"
    
    try:
        with open("api_logs.txt", "a") as log_file:
            log_file.write(log_entry + "\n")
    except Exception as e:
        logger.error(f"Failed to write log: {e}")
    
    return response


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/config", response_model=ConfigResponse)
async def get_config():
    """
    Return current configuration.
    
    This endpoint demonstrates that settings are loaded and accessible.
    """
    return ConfigResponse(
        app_name=settings.app_name,
        debug=settings.debug,
        json_db_path=settings.json_db_path,
        log_level=settings.log_level
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "debug": settings.debug
    }


@app.post("/tasks", response_model=TaskResponse, status_code=201)
async def create_task(task: TaskCreate):
    """Create a new task."""
    global current_id
    current_id += 1
    
    new_task = Task(
        task_id=current_id,
        title=task.title,
        description=task.description,
        status=task.status
    )
    task_database[current_id] = new_task
    
    logger.info(f"Task created: {current_id} - {task.title}")
    return new_task.to_response()


@app.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(status: Optional[str] = None):
    """List all tasks with optional status filter."""
    tasks = list(task_database.values())
    
    if status:
        if status not in ["pending", "in_progress", "completed"]:
            logger.warning(f"Invalid status filter: {status}")
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
        tasks = [t for t in tasks if t.status == status]
    
    tasks.sort(key=lambda t: t.created_at, reverse=True)
    logger.info(f"Listed {len(tasks)} tasks with status filter: {status}")
    
    return [t.to_response() for t in tasks]


@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    """Get a specific task by ID."""
    if task_id not in task_database:
        logger.warning(f"Task not found: {task_id}")
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    task = task_database[task_id]
    logger.info(f"Retrieved task: {task_id}")
    return task.to_response()


@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskUpdate):
    """Update a task."""
    if task_id not in task_database:
        logger.warning(f"Task not found for update: {task_id}")
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    task = task_database[task_id]
    
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.status is not None:
        task.status = task_update.status
    
    task.updated_at = datetime.now()
    
    logger.info(f"Task updated: {task_id}")
    return task.to_response()


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    """Delete a task."""
    if task_id not in task_database:
        logger.warning(f"Task not found for deletion: {task_id}")
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    del task_database[task_id]
    logger.info(f"Task deleted: {task_id}")
    return None


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": settings.app_name,
        "description": "Task Management API with Configuration Management",
        "version": "1.0.0",
        "debug": settings.debug,
        "endpoints": {
            "config": "GET /config",
            "health": "GET /health",
            "create_task": "POST /tasks",
            "list_tasks": "GET /tasks",
            "get_task": "GET /tasks/{task_id}",
            "update_task": "PUT /tasks/{task_id}",
            "delete_task": "DELETE /tasks/{task_id}",
            "docs": "/docs (Swagger UI)"
        }
    }
