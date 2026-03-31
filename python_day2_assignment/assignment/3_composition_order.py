class Address:
    """Class responsible for managing address information."""
    
    def __init__(self, city, zip_code):
        """
        Initialize an Address.
        
        Args:
            city: The city name
            zip_code: The postal code
        """
        self.city = city
        self.zip_code = zip_code
    
    def get_formatted_address(self):
        """Return formatted address string."""
        return f"{self.city} - {self.zip_code}"


class PaymentInfo:
    """Class responsible for managing payment information."""
    
    def __init__(self, method, amount):
        """
        Initialize PaymentInfo.
        
        Args:
            method: The payment method (e.g., "UPI", "Credit Card")
            amount: The payment amount
        """
        self.method = method
        self.amount = amount
    
    def get_payment_details(self):
        """Return formatted payment details."""
        return f"{self.method}"


class OrderItem:
    """Class responsible for managing individual order items."""
    
    def __init__(self, name, qty, price):
        """
        Initialize an OrderItem.
        
        Args:
            name: The item name
            qty: The quantity ordered
            price: The price per unit
        """
        self.name = name
        self.qty = qty
        self.price = price
    
    def get_total(self):
        """Calculate and return the total for this item."""
        return self.qty * self.price
    
    def get_item_summary(self):
        """Return formatted item summary."""
        return f"{self.name} x{self.qty} = {self.get_total()}"


class Order:
    """Class responsible for managing orders using composition."""
    
    def __init__(self, address, payment_info, items):
        """
        Initialize an Order with address, payment info, and items.
        
        Args:
            address: An Address object
            payment_info: A PaymentInfo object
            items: A list of OrderItem objects
        """
        self.address = address
        self.payment_info = payment_info
        self.items = items
    
    def order_summary(self):
        """Display the complete order summary."""
        # Shipping information
        print(f"Shipping: {self.address.get_formatted_address()}")
        
        # Items summary
        items_summary = ", ".join([item.get_item_summary() for item in self.items])
        print(f"Items: {items_summary}")
        
        # Total amount
        total = sum(item.get_total() for item in self.items)
        print(f"Total: {total}")
        
        # Payment information
        print(f"Payment: {self.payment_info.get_payment_details()}")


# Test code demonstrating composition and SRP
if __name__ == "__main__":
    # Create components
    addr = Address("Bangalore", "560001")
    pay = PaymentInfo("UPI", 1500)
    items = [
        OrderItem("Book", 2, 500),
        OrderItem("Pen", 5, 100)
    ]
    
    # Create an order with composed objects
    order = Order(addr, pay, items)
    
    # Display order summary
    order.order_summary()
