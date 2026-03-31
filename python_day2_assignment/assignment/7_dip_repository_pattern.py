from abc import ABC, abstractmethod
import json
import os


class UserRepository(ABC):
    """Abstract base class defining the repository interface."""
    
    @abstractmethod
    def save(self, user):
        """
        Save a user.
        
        Args:
            user: A dictionary containing user information
        """
        pass
    
    @abstractmethod
    def find(self, username):
        """
        Find a user by username.
        
        Args:
            username: The username to search for
            
        Returns:
            A dictionary containing user information, or None if not found
        """
        pass


class InMemoryUserRepository(UserRepository):
    """In-memory repository implementation using a dictionary."""
    
    def __init__(self):
        """Initialize with an empty user dictionary."""
        self.users = {}
    
    def save(self, user):
        """
        Save a user in memory.
        
        Args:
            user: A dictionary with 'username' and other user data
        """
        username = user.get("username")
        if username:
            self.users[username] = user
    
    def find(self, username):
        """
        Find a user by username from memory.
        
        Args:
            username: The username to search for
            
        Returns:
            User dictionary if found, None otherwise
        """
        return self.users.get(username)


class JSONUserRepository(UserRepository):
    """File-based JSON repository implementation."""
    
    def __init__(self, filename="users_db.json"):
        """
        Initialize the JSON repository.
        
        Args:
            filename: The JSON file to store users in
        """
        self.filename = filename
    
    def save(self, user):
        """
        Save a user to JSON file.
        
        Args:
            user: A dictionary with 'username' and other user data
        """
        users = self._load_users()
        username = user.get("username")
        if username:
            users[username] = user
            self._write_users(users)
    
    def find(self, username):
        """
        Find a user by username from JSON file.
        
        Args:
            username: The username to search for
            
        Returns:
            User dictionary if found, None otherwise
        """
        users = self._load_users()
        return users.get(username)
    
    def _load_users(self):
        """Load users from JSON file or return empty dict."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def _write_users(self, users):
        """Write users to JSON file."""
        with open(self.filename, "w") as f:
            json.dump(users, f, indent=2)


class UserService:
    """
    Service class that depends on UserRepository abstraction (DIP).
    
    This class demonstrates the Dependency Inversion Principle:
    - It depends on the abstraction (UserRepository), not concrete implementations
    - The repository is injected at runtime
    - Swapping repository implementations requires no changes to UserService
    """
    
    def __init__(self, repository: UserRepository):
        """
        Initialize UserService with a repository.
        
        Args:
            repository: A UserRepository instance (can be any concrete implementation)
        """
        self.repository = repository
    
    def register(self, user_data):
        """
        Register a new user.
        
        Args:
            user_data: A dictionary with user information
        """
        self.repository.save(user_data)
    
    def get_user(self, username):
        """
        Get user information.
        
        Args:
            username: The username to retrieve
            
        Returns:
            User dictionary if found, None otherwise
        """
        return self.repository.find(username)


# Test code demonstrating DIP and Dependency Injection
if __name__ == "__main__":
    print("=== Dependency Inversion Pattern Test ===\n")
    
    # Test 1: Using InMemoryUserRepository
    print("--- Test 1: InMemoryUserRepository ---")
    in_memory_repo = InMemoryUserRepository()
    service1 = UserService(in_memory_repo)
    
    service1.register({"username": "alice", "email": "a@b.com"})
    result1 = service1.get_user("alice")
    print(f"Result: {result1}")
    
    print("\n--- Test 2: JSONUserRepository ---")
    json_repo = JSONUserRepository("test_users.json")
    service2 = UserService(json_repo)
    
    service2.register({"username": "bob", "email": "b@c.com"})
    result2 = service2.get_user("bob")
    print(f"Result: {result2}")
    
    print("\n--- Test 3: Demonstrating Repository Swapping ---")
    print("Same UserService code, different repository implementation:")
    
    # Create a new JSON-based service
    json_repo2 = JSONUserRepository("test_users.json")
    service3 = UserService(json_repo2)
    
    # Register multiple users
    service3.register({"username": "charlie", "email": "c@d.com"})
    service3.register({"username": "diana", "email": "d@e.com"})
    
    # Retrieve users
    print(f"Charlie: {service3.get_user('charlie')}")
    print(f"Diana: {service3.get_user('diana')}")
    print(f"Bob (from earlier): {service3.get_user('bob')}")
    
    print("\n=== Why This Design Demonstrates DIP ===")
    print("""
1. UserService depends on UserRepository (abstraction), not concrete classes
2. No coupling to InMemoryUserRepository or JSONUserRepository
3. New repository types can be added without modifying UserService
4. Runtime injection allows testing with mock repositories
5. Repository implementation can be swapped with a single line of code
    """)
