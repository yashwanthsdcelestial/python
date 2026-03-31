"""Custom exceptions for Task Management System."""


class TaskManagementException(Exception):
    """Base exception for task management system."""
    
    def __init__(self, message: str, status_code: int = 500):
        """Initialize exception."""
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class UserNotFoundError(TaskManagementException):
    """Raised when user is not found."""
    
    def __init__(self, user_id: int = None, username: str = None):
        """Initialize exception."""
        if user_id:
            message = f"User with id {user_id} not found"
        elif username:
            message = f"User '{username}' not found"
        else:
            message = "User not found"
        super().__init__(message, status_code=404)


class TaskNotFoundError(TaskManagementException):
    """Raised when task is not found."""
    
    def __init__(self, task_id: int):
        """Initialize exception."""
        message = f"Task with id {task_id} not found"
        super().__init__(message, status_code=404)


class DuplicateUserError(TaskManagementException):
    """Raised when user already exists."""
    
    def __init__(self, username: str):
        """Initialize exception."""
        message = f"User '{username}' already exists"
        super().__init__(message, status_code=409)


class InvalidCredentialsError(TaskManagementException):
    """Raised when credentials are invalid."""
    
    def __init__(self):
        """Initialize exception."""
        message = "Invalid username or password"
        super().__init__(message, status_code=401)


class ValidationError(TaskManagementException):
    """Raised when validation fails."""
    
    def __init__(self, message: str):
        """Initialize exception."""
        super().__init__(message, status_code=422)
