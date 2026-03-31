# Q11: Logging System
# Log error messages with a timestamp to a file

from datetime import datetime   # To get current date and time

def log_error(message):
    # Get current timestamp in the format: 2026-01-01 10:00:00
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_line = f"{timestamp} ERROR {message}\n"
    
    # Open file in append mode ("a") so we don't overwrite old logs
    with open("error_log.txt", "a") as log_file:
        log_file.write(log_line)
    
    print(log_line.strip())   # Also print to screen

# Test it
log_error("Something failed")
log_error("Database connection lost")

# Output (example):
# 2026-01-01 10:00:00 ERROR Something failed
# 2026-01-01 10:00:01 ERROR Database connection lost
