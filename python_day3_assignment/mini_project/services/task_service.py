"""Task service with business logic (SRP)."""
from datetime import datetime
from typing import List, Optional
from repositories.base_repository import BaseRepository
from models.schemas import TaskCreate, TaskUpdate, TaskResponse
from models.enums import TaskStatus, TaskPriority
from exceptions.custom_exceptions import TaskNotFoundError
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TaskService:
    """Task service - handles all task business logic (SRP + DIP)."""
    
    def __init__(self, repository: BaseRepository):
        """Initialize with injected repository (DIP)."""
        self.repository = repository
    
    def create_task(self, task_data: TaskCreate) -> TaskResponse:
        """Create a new task."""
        task = {
            'title': task_data.title,
            'description': task_data.description,
            'priority': task_data.priority.value,
            'status': task_data.status.value,
            'owner': task_data.owner,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        saved_task = self.repository.save(task)
        logger.info(f"Task '{task_data.title}' created for {task_data.owner}")
        
        return self._task_to_response(saved_task)
    
    def get_task(self, task_id: int) -> TaskResponse:
        """Get task by ID."""
        task = self.repository.find_by_id(task_id)
        if not task:
            logger.error(f"Task ID {task_id} not found")
            raise TaskNotFoundError(task_id)
        
        return self._task_to_response(task)
    
    def list_tasks(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        owner: Optional[str] = None,
        page: int = 1,
        limit: int = 10
    ) -> tuple[List[TaskResponse], int]:
        """List tasks with optional filtering and pagination."""
        all_tasks = self.repository.find_all()
        
        # Apply filters
        filtered_tasks = all_tasks
        
        if status:
            filtered_tasks = [t for t in filtered_tasks if t.get('status') == status]
        
        if priority:
            filtered_tasks = [t for t in filtered_tasks if t.get('priority') == priority]
        
        if owner:
            filtered_tasks = [t for t in filtered_tasks if t.get('owner') == owner]
        
        # Apply pagination
        total = len(filtered_tasks)
        start = (page - 1) * limit
        end = start + limit
        paginated_tasks = filtered_tasks[start:end]
        
        logger.info(f"Listed {len(paginated_tasks)} tasks (page {page})")
        
        return (
            [self._task_to_response(t) for t in paginated_tasks],
            total
        )
    
    def update_task(self, task_id: int, task_data: TaskUpdate) -> TaskResponse:
        """Full/partial update of task."""
        if not self.repository.exists(task_id):
            logger.error(f"Task ID {task_id} not found for update")
            raise TaskNotFoundError(task_id)
        
        # Build update dict with only provided fields
        updates = {
            'updated_at': datetime.now().isoformat()
        }
        
        if task_data.title is not None:
            updates['title'] = task_data.title
        if task_data.description is not None:
            updates['description'] = task_data.description
        if task_data.priority is not None:
            updates['priority'] = task_data.priority.value
        if task_data.status is not None:
            updates['status'] = task_data.status.value
        
        updated_task = self.repository.update(task_id, updates)
        logger.info(f"Task ID {task_id} updated")
        
        return self._task_to_response(updated_task)
    
    def delete_task(self, task_id: int) -> bool:
        """Delete task by ID."""
        if not self.repository.exists(task_id):
            logger.error(f"Task ID {task_id} not found for deletion")
            raise TaskNotFoundError(task_id)
        
        result = self.repository.delete(task_id)
        if result:
            logger.info(f"Task ID {task_id} deleted")
        return result
    
    def _task_to_response(self, task: dict) -> TaskResponse:
        """Convert task dict to TaskResponse."""
        return TaskResponse(
            id=task['id'],
            title=task['title'],
            description=task.get('description'),
            status=TaskStatus(task['status']),
            priority=TaskPriority(task['priority']),
            owner=task['owner'],
            created_at=task['created_at'],
            updated_at=task['updated_at']
        )
