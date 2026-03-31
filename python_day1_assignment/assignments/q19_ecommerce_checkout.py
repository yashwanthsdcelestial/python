# Q19: E-Commerce Checkout System (SOLID Principles)
#
# SOLID Principles used here:
#   SRP  - Each class does ONE job (payment, discount, logging, checkout)
#   OCP  - Add new payment/discount WITHOUT changing existing code
#   LSP  - UPI and Card are interchangeable (both have process())
#   ISP  - Small, focused classes (not one giant class)
#   DIP  - Checkout depends on abstract behavior, not specific classes


# ---- Discount Classes ----

class NoDiscount:
    def apply(self, amount):
        return amount   # No change


class FestivalDiscount:
    def apply(self, amount):
        discount = amount * 0.10    # 10% off
        return amount - discount


class PremiumDiscount:
    def apply(self, amount):
        discount = amount * 0.20    # 20% off
        return amount - discount


# ---- Payment Classes ----

class UPI:
    def pay(self, amount):
        print(f"Payment Successful via UPI. Amount: {amount}")


class Card:
    def pay(self, amount):
        print(f"Payment Successful via Card. Amount: {amount}")


# ---- Logger Class ----

class Logger:
    def log(self, message):
        print(f"LOG: {message}")


# ---- Checkout Class (uses all of the above) ----

class Checkout:
    
    def __init__(self, payment, discount):
        self.payment = payment       # Could be UPI() or Card()
        self.discount = discount     # Could be FestivalDiscount() or PremiumDiscount()
        self.logger = Logger()
    
    def process(self, amount):
        # Step 1: Apply discount
        final_amount = self.discount.apply(amount)
        
        # Step 2: Show final amount
        print(f"Final Amount: {final_amount}")
        
        # Step 3: Process payment
        self.payment.pay(final_amount)
        
        # Step 4: Log
        self.logger.log(f"Order processed. Original: {amount}, Final: {final_amount}")


# ---- Test ----
checkout = Checkout(payment=UPI(), discount=FestivalDiscount())
checkout.process(1000)

# Output:
# Final Amount: 900.0
# Payment Successful via UPI. Amount: 900.0
# LOG: Order processed. Original: 1000, Final: 900.0

print()

# Try with Card + Premium Discount - no code changes needed!
checkout2 = Checkout(payment=Card(), discount=PremiumDiscount())
checkout2.process(1000)
