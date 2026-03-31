# storage.py
# This file handles reading and writing user data to users.json

import json
import os

USERS_FILE = "users.json"   # Name of the file where users are stored

def load_users():
    """
    Read users from users.json and return as a dictionary.
    If file doesn't exist or is broken, return empty user list.
    """
    # If file doesn't exist yet, return empty structure
    if not os.path.exists(USERS_FILE):
        return {"users": []}
    
    try:
        with open(USERS_FILE, "r") as file:
            data = json.load(file)   # Parse JSON into Python dictionary
            return data
    except json.JSONDecodeError:
        # File exists but content is broken/corrupted
        print("Warning: users.json is corrupted. Starting fresh.")
        return {"users": []}


def save_users(data):
    """
    Save the user data dictionary to users.json
    """
    with open(USERS_FILE, "w") as file:
        json.dump(data, file, indent=4)   # indent=4 makes the file readable
