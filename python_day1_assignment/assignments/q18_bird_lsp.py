# Q18: Bird System Fix (LSP - Liskov Substitution Principle)
#
# PROBLEM with original code:
#   Penguin inherits fly() from Bird but throws an error - this BREAKS LSP
#   LSP says: a subclass should work wherever the parent class is used
#
# SOLUTION:
#   Separate birds that CAN fly from birds that CANNOT fly
#   Don't force Penguin to have a fly() method it can't use


# ---- Base class: Bird (all birds) ----
class Bird:
    def __init__(self, name):
        self.name = name
    
    def describe(self):
        print(f"I am {self.name}")


# ---- Class for birds that can FLY ----
class FlyingBird(Bird):
    def move(self):
        print(f"{self.name} flies")


# ---- Class for birds that can SWIM (but not fly) ----
class SwimmingBird(Bird):
    def move(self):
        print(f"{self.name} swims")


# ---- Specific birds ----
class Sparrow(FlyingBird):
    pass   # Sparrow can fly, inherits from FlyingBird


class Penguin(SwimmingBird):
    pass   # Penguin can swim, inherits from SwimmingBird


# ---- Test ----
sparrow = Sparrow("Sparrow")
penguin = Penguin("Penguin")

sparrow.move()   # Output: Sparrow flies
penguin.move()   # Output: Penguin swims

# Now no class throws unexpected errors - LSP is followed!
