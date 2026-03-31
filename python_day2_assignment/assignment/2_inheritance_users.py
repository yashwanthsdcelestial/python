class User:
    """Base class for all users."""
    
    def __init__(self, username, role):
        """
        Initialize a User with username and role.
        
        Args:
            username: The user's username
            role: The user's role
        """
        self.username = username
        self.role = role
    
    def display_profile(self):
        """Display the user's profile (to be overridden in subclasses)."""
        print(f"User: {self.username} | Role: {self.role}")


class AdminUser(User):
    """Admin user with additional permissions."""
    
    def __init__(self, username, permissions):
        """
        Initialize an AdminUser with username and permissions.
        
        Args:
            username: The admin's username
            permissions: A list of permission strings
        """
        super().__init__(username, "Admin")
        self.permissions = permissions
    
    def display_profile(self):
        """Display the admin's profile with permissions."""
        permissions_str = ", ".join(self.permissions)
        print(f"Admin: {self.username} | Permissions: {permissions_str}")


class CustomerUser(User):
    """Customer user with order tracking."""
    
    def __init__(self, username, orders):
        """
        Initialize a CustomerUser with username and orders count.
        
        Args:
            username: The customer's username
            orders: The number of orders placed
        """
        super().__init__(username, "Customer")
        self.orders = orders
    
    def display_profile(self):
        """Display the customer's profile with order count."""
        print(f"Customer: {self.username} | Orders: {self.orders}")


# Test code demonstrating inheritance and polymorphism
if __name__ == "__main__":
    # Create an admin user
    admin = AdminUser("admin1", ["manage_users", "view_logs"])
    
    # Create a customer user
    customer = CustomerUser("cust1", 5)
    
    # Display profiles (polymorphism in action)
    admin.display_profile()
    customer.display_profile()
