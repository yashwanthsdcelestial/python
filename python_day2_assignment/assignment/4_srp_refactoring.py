import json
import os


class UserValidator:
    """Class responsible for validating user data."""
    
    def validate(self, data):
        """
        Validate user data.
        
        Args:
            data: A dictionary with username and email
            
        Raises:
            ValueError: If data is invalid
        """
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
        
        if "username" not in data or not data["username"]:
            raise ValueError("Username is required")
        
        if "email" not in data or not data["email"]:
            raise ValueError("Email is required")
        
        if "@" not in data["email"] or "." not in data["email"]:
            raise ValueError("Invalid email format")
        
        print("Validation passed")


class UserStorage:
    """Class responsible for storing user data to JSON."""
    
    def __init__(self, filename="users.json"):
        """
        Initialize UserStorage with a filename.
        
        Args:
            filename: The JSON file to store users in
        """
        self.filename = filename
    
    def save(self, data):
        """
        Save user data to JSON file.
        
        Args:
            data: A dictionary with user information
        """
        users = self._load_users()
        users.append(data)
        
        with open(self.filename, "w") as f:
            json.dump(users, f, indent=2)
        
        print(f"User saved to {self.filename}")
    
    def _load_users(self):
        """Load existing users from JSON file or return empty list."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def get_all_users(self):
        """Retrieve all users from storage."""
        return self._load_users()


class UserNotifier:
    """Class responsible for sending user notifications."""
    
    def send_welcome_notification(self, email):
        """
        Send a welcome notification to the user.
        
        Args:
            email: The user's email address
        """
        print(f"Welcome email sent to {email}")
    
    def send_email(self, email, message):
        """
        Send an email notification.
        
        Args:
            email: The recipient's email address
            message: The message to send
        """
        print(f"Email sent to {email}: {message}")


def register_user(data):
    """
    Orchestrator function that coordinates user registration.
    
    This function uses all three SRP-compliant classes to:
    1. Validate user data
    2. Store the user
    3. Send a welcome notification
    
    Args:
        data: A dictionary with username and email
    """
    # Step 1: Validate
    validator = UserValidator()
    validator.validate(data)
    
    # Step 2: Store
    storage = UserStorage()
    storage.save(data)
    
    # Step 3: Notify
    notifier = UserNotifier()
    notifier.send_welcome_notification(data["email"])


# Test code demonstrating SRP
if __name__ == "__main__":
    # Test case 1: Valid user registration
    print("=== Test Case 1: Valid User Registration ===")
    data = {"username": "alice", "email": "alice@mail.com"}
    register_user(data)
    
    print("\n=== Test Case 2: Invalid Email ===")
    try:
        invalid_data = {"username": "bob", "email": "invalid-email"}
        register_user(invalid_data)
    except ValueError as e:
        print(f"Validation Error: {e}")
    
    print("\n=== Test Case 3: Missing Username ===")
    try:
        invalid_data = {"email": "charlie@mail.com"}
        register_user(invalid_data)
    except ValueError as e:
        print(f"Validation Error: {e}")
