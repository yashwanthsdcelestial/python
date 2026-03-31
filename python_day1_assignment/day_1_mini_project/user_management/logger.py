# logger.py
# This file handles all logging - writing messages with timestamps to logs.txt

from datetime import datetime

def log_message(level, message):
    """
    Write a log entry to logs.txt
    
    level   = "INFO", "WARNING", or "ERROR"
    message = what happened
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_line = f"{timestamp} - {level} - {message}\n"
    
    # Open in append mode "a" so old logs are kept
    with open("logs.txt", "a") as log_file:
        log_file.write(log_line)
