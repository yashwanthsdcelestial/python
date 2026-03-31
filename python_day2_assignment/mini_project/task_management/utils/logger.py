"""Logging configuration for the application."""
import logging
import logging.handlers
from pathlib import Path
from config import settings


def setup_logger(name: str) -> logging.Logger:
    """Set up structured logger with file and console handlers."""
    # Ensure logs directory exists
    log_dir = Path(settings.log_file)
    log_dir.parent.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.log_level))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Format: [TIMESTAMP] - LEVEL - MODULE - MESSAGE
    formatter = logging.Formatter(
        fmt='[%(asctime)s] - %(levelname)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    file_handler = logging.FileHandler(settings.log_file, encoding='utf-8')
    file_handler.setLevel(getattr(logging, settings.log_level))
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, settings.log_level))
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
