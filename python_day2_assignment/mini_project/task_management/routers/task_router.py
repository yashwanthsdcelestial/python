"""Task router - handles task HTTP requests/responses (SRP)."""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from models.schemas import TaskCreate, TaskUpdate, TaskResponse
from services.task_service import TaskService
from repositories.json_repository import JSONRepository
from exceptions.custom_exceptions import TaskManagementException
from config import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_repository() -> JSONRepository:
    """Dependency injection for task repository."""
    return JSONRepository(settings.tasks_db_path, "tasks")


def get_task_service(repo: JSONRepository = Depends(get_task_repository)) -> TaskService:
    """Dependency injection for task service."""
    return TaskService(repo)


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(
    task_data: TaskCreate,
    service: TaskService = Depends(get_task_service)
):
    """Create a new task."""
    try:
        return service.create_task(task_data)
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid task data")


@router.get("", status_code=200)
async def list_tasks(
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    owner: Optional[str] = Query(None, description="Filter by owner"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    service: TaskService = Depends(get_task_service)
):
    """List tasks with optional filtering and pagination."""
    try:
        tasks, total = service.list_tasks(
            status=status,
            priority=priority,
            owner=owner,
            page=page,
            limit=limit
        )
        return {
            "data": tasks,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit
            }
        }
    except Exception as e:
        logger.error(f"Error listing tasks: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    """Get task by ID."""
    try:
        return service.get_task(task_id)
    except TaskManagementException as e:
        logger.error(f"Error getting task: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    service: TaskService = Depends(get_task_service)
):
    """Full update of task."""
    try:
        return service.update_task(task_id, task_data)
    except TaskManagementException as e:
        logger.error(f"Error updating task: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid task data")


@router.patch("/{task_id}", response_model=TaskResponse)
async def partial_update_task(
    task_id: int,
    task_data: TaskUpdate,
    service: TaskService = Depends(get_task_service)
):
    """Partial update of task."""
    try:
        return service.update_task(task_id, task_data)
    except TaskManagementException as e:
        logger.error(f"Error updating task: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid task data")


@router.delete("/{task_id}", status_code=200)
async def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    """Delete task by ID."""
    try:
        service.delete_task(task_id)
        return {"message": f"Task {task_id} deleted successfully"}
    except TaskManagementException as e:
        logger.error(f"Error deleting task: {e.message}")
        raise HTTPException(status_code=e.status_code, detail=e.message)
