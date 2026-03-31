"""Background task utilities."""
from datetime import datetime
from pathlib import Path
from utils.logger import setup_logger

logger = setup_logger(__name__)


def log_task_notification(task_title: str, owner: str) -> None:
    """
    Log a task creation notification to notifications.log file.
    
    Args:
        task_title: Title of the created task
        owner: Username of the task owner
    """
    try:
        # Ensure notifications directory exists
        log_file = Path("./logs/notifications.log")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Format: [TIMESTAMP] Task '<title>' created by <owner> — notification sent
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{timestamp}] Task '{task_title}' created by {owner} — notification sent\n"
        
        # Append to file
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(message)
        
        logger.info(f"Notification logged for task: {task_title} by {owner}")
        
    except Exception as e:
        logger.error(f"Error logging notification: {str(e)}")
