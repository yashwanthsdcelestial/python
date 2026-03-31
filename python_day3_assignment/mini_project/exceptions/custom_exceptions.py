"""Custom exceptions for Task Management System (SRP)."""


class TaskManagementException(Exception):
    """Base exception for all task management errors."""
    
    def __init__(self, message: str, status_code: int = 500):
        """Initialize exception with message and HTTP status code."""
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class TaskNotFoundError(TaskManagementException):
    """Raised when a task is not found."""
    
    def __init__(self, task_id: int):
        """Initialize with task ID."""
        super().__init__(
            message=f"Task with ID {task_id} not found",
            status_code=404
        )


class UserNotFoundError(TaskManagementException):
    """Raised when a user is not found."""
    
    def __init__(self, user_id: int = None, username: str = None):
        """Initialize with user ID or username."""
        if user_id:
            message = f"User with ID {user_id} not found"
        elif username:
            message = f"User '{username}' not found"
        else:
            message = "User not found"
        
        super().__init__(message=message, status_code=404)


class DuplicateUserError(TaskManagementException):
    """Raised when user already exists."""
    
    def __init__(self, username: str):
        """Initialize with username."""
        super().__init__(
            message=f"User '{username}' already exists",
            status_code=409
        )


class InvalidCredentialsError(TaskManagementException):
    """Raised when credentials are invalid."""
    
    def __init__(self):
        """Initialize with generic message."""
        super().__init__(
            message="Invalid username or password",
            status_code=401
        )


class DatabaseError(TaskManagementException):
    """Raised when database operations fail."""
    
    def __init__(self, message: str = "Database error"):
        """Initialize with error message."""
        super().__init__(message=message, status_code=500)
