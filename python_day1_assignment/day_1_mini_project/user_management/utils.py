# utils.py
# This file contains all the core user operations:
# register, login, view, delete

from storage import load_users, save_users
from logger import log_message


def register_user():
    """Ask for username and password, then save the new user."""
    
    print("\n--- Register New User ---")
    
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    # Validate: inputs must not be empty
    if not username or not password:
        print("Username and password cannot be empty!")
        log_message("ERROR", "Registration failed - empty input provided")
        return
    
    # Load current users from file
    data = load_users()
    
    # Check if username already exists
    for user in data["users"]:
        if user["username"] == username:
            print(f"Username '{username}' already exists. Please choose another.")
            log_message("WARNING", f"Duplicate registration attempt for username '{username}'")
            return
    
    # Add the new user
    new_user = {"username": username, "password": password}
    data["users"].append(new_user)
    
    # Save updated data back to file
    save_users(data)
    
    print(f"User '{username}' registered successfully!")
    log_message("INFO", f"User '{username}' registered successfully")


def login_user():
    """Ask for credentials, allow max 3 attempts."""
    
    print("\n--- Login ---")
    
    max_attempts = 3
    
    for attempt in range(1, max_attempts + 1):
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        
        # Validate: inputs must not be empty
        if not username or not password:
            print("Username and password cannot be empty!")
            continue
        
        # Load users and check credentials
        data = load_users()
        
        user_found = False
        for user in data["users"]:
            if user["username"] == username and user["password"] == password:
                user_found = True
                break
        
        if user_found:
            print(f"Welcome, {username}! Login successful.")
            log_message("INFO", f"User '{username}' logged in successfully")
            return
        else:
            remaining = max_attempts - attempt
            print(f"Wrong username or password. Attempts remaining: {remaining}")
            log_message("ERROR", f"Failed login attempt {attempt} for user '{username}'")
    
    # All 3 attempts failed
    print("Too many failed attempts. Account temporarily locked.")
    log_message("WARNING", f"Account locked after 3 failed attempts for user '{username}'")


def view_users():
    """Display all registered usernames (NOT passwords)."""
    
    print("\n--- Registered Users ---")
    
    data = load_users()
    
    if not data["users"]:
        print("No users registered yet.")
    else:
        for i, user in enumerate(data["users"], start=1):
            print(f"{i}. {user['username']}")   # Only show username, not password
    
    log_message("INFO", "User list accessed")


def delete_user():
    """Delete a user by username."""
    
    print("\n--- Delete User ---")
    
    username = input("Enter username to delete: ").strip()
    
    if not username:
        print("Username cannot be empty!")
        return
    
    data = load_users()
    
    # Find and remove the user
    original_count = len(data["users"])
    data["users"] = [user for user in data["users"] if user["username"] != username]
    
    if len(data["users"]) < original_count:
        # User was found and removed
        save_users(data)
        print(f"User '{username}' deleted successfully.")
        log_message("INFO", f"User '{username}' deleted successfully")
    else:
        # User was not found
        print(f"User '{username}' not found.")
        log_message("ERROR", f"Attempt to delete non-existing user '{username}'")
