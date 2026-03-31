class User:
    """User class with encapsulation and validation."""
    
    def __init__(self, username, email, age):
        """
        Initialize a User with username, email, and age.
        
        Args:
            username: The user's username
            email: The user's email address
            age: The user's age
            
        Raises:
            ValueError: If email or age are invalid
        """
        self._username = username
        self.set_email(email)  # Validate through setter
        self.set_age(age)      # Validate through setter
    
    # Username getters and setters
    def get_username(self):
        """Get the username."""
        return self._username
    
    def set_username(self, username):
        """Set the username."""
        self._username = username
    
    # Email getters and setters with validation
    def get_email(self):
        """Get the email address."""
        return self._email
    
    def set_email(self, email):
        """
        Set the email address with validation.
        
        Args:
            email: The email address to set
            
        Raises:
            ValueError: If email doesn't contain '@' and '.' characters
        """
        if '@' not in email or '.' not in email:
            raise ValueError("Invalid email format")
        self._email = email
    
    # Age getters and setters with validation
    def get_age(self):
        """Get the age."""
        return self._age
    
    def set_age(self, age):
        """
        Set the age with validation.
        
        Args:
            age: The age to set
            
        Raises:
            ValueError: If age is not between 18 and 120
        """
        if age < 18 or age > 120:
            raise ValueError("Age must be between 18 and 120")
        self._age = age


# Test code demonstrating the requirements
if __name__ == "__main__":
    # Create a user with valid data
    user = User("alice", "alice@mail.com", 25)
    
    # Try to set invalid email
    try:
        user.set_email("invalid")
    except ValueError as e:
        print(f"ValueError: {e}")
    
    # Try to set invalid age
    try:
        user.set_age(150)
    except ValueError as e:
        print(f"ValueError: {e}")
    
    # Print valid values (unchanged from initialization)
    print(user.get_email())
    print(user.get_age())
