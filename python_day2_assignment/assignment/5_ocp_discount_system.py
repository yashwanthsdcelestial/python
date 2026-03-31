from abc import ABC, abstractmethod


class Discount(ABC):
    """Abstract base class for all discount types."""
    
    @abstractmethod
    def apply(self, amount):
        """
        Apply discount to the given amount.
        
        Args:
            amount: The original amount
            
        Returns:
            The discounted amount (minimum 0)
        """
        pass


class NoDiscount(Discount):
    """No discount applied."""
    
    def apply(self, amount):
        """Return the amount unchanged."""
        return amount


class PercentageDiscount(Discount):
    """Percentage-based discount (10% off)."""
    
    def __init__(self, percentage=10):
        """
        Initialize PercentageDiscount.
        
        Args:
            percentage: The discount percentage (default 10%)
        """
        self.percentage = percentage
    
    def apply(self, amount):
        """Apply percentage discount and return the result."""
        discounted = amount - (amount * self.percentage / 100)
        return max(0, discounted)  # Ensure minimum 0


class FlatDiscount(Discount):
    """Flat amount discount (Rs 200 off)."""
    
    def __init__(self, discount_amount=200):
        """
        Initialize FlatDiscount.
        
        Args:
            discount_amount: The flat discount amount (default Rs 200)
        """
        self.discount_amount = discount_amount
    
    def apply(self, amount):
        """Apply flat discount and return the result."""
        discounted = amount - self.discount_amount
        return max(0, discounted)  # Ensure minimum 0


class BuyOneGetOneFree(Discount):
    """Buy one get one free discount (50% off)."""
    
    def __init__(self, discount_percentage=50):
        """
        Initialize BuyOneGetOneFree.
        
        Args:
            discount_percentage: The discount percentage (default 50%)
        """
        self.discount_percentage = discount_percentage
    
    def apply(self, amount):
        """Apply buy one get one free discount and return the result."""
        discounted = amount - (amount * self.discount_percentage / 100)
        return max(0, discounted)  # Ensure minimum 0


def calculate_total(amount, discount):
    """
    Calculate the total amount after applying discount.
    
    This function is open for extension but closed for modification.
    New discount types can be added by creating new Discount subclasses
    without modifying this function.
    
    Args:
        amount: The original amount
        discount: A Discount object (any subclass of Discount)
        
    Returns:
        The final amount after applying the discount
    """
    return discount.apply(amount)


# Test code demonstrating OCP
if __name__ == "__main__":
    # Test each discount type
    print("=== Discount System Test ===")
    print(f"Original Amount: Rs 1000")
    print()
    
    # No Discount
    print(f"No Discount: Rs {calculate_total(1000, NoDiscount())}")
    
    # Percentage Discount (10%)
    print(f"Percentage Discount (10%): Rs {calculate_total(1000, PercentageDiscount())}")
    
    # Flat Discount (Rs 200)
    print(f"Flat Discount (Rs 200): Rs {calculate_total(1000, FlatDiscount())}")
    
    # Buy One Get One Free (50%)
    print(f"Buy One Get One Free (50%): Rs {calculate_total(1000, BuyOneGetOneFree())}")
    
    print("\n=== Edge Case: Discount Exceeds Amount ===")
    # Test that discount doesn't go below 0
    print(f"Flat Discount (Rs 200) on Rs 100: Rs {calculate_total(100, FlatDiscount())}")
    print(f"Percentage Discount (50%) on Rs 100: Rs {calculate_total(100, PercentageDiscount(50))}")
    
    print("\n=== Custom Discount Example (OCP in Action) ===")
    # Example: Adding a new discount type without modifying calculate_total()
    class StudentDiscount(Discount):
        """Custom student discount (15% off) - new discount type added without modifying existing code."""
        
        def apply(self, amount):
            discounted = amount - (amount * 15 / 100)
            return max(0, discounted)
    
    print(f"Student Discount (15%): Rs {calculate_total(1000, StudentDiscount())}")
