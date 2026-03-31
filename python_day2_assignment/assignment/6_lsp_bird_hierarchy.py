from abc import ABC, abstractmethod


class Bird(ABC):
    """Abstract base class for all birds. Defines the contract that all birds must implement."""
    
    def __init__(self, name=None):
        """
        Initialize a Bird.
        
        Args:
            name: The bird's name/species (optional, defaults to class name)
        """
        self.name = name or self.__class__.__name__
    
    @abstractmethod
    def move(self):
        """
        Each bird must implement its own movement behavior.
        This is the contract that all subclasses must respect.
        """
        pass


class FlyingBird(Bird):
    """Abstract class for birds that can fly. Respects LSP by implementing fly behavior properly."""
    
    def move(self):
        """Flying birds fly - this is the expected behavior for all FlyingBird subclasses."""
        print(f"{self.__class__.__name__} flies")


class SwimmingBird(Bird):
    """Abstract class for birds that can swim. Respects LSP by implementing swim behavior properly."""
    
    def move(self):
        """Swimming birds swim - this is the expected behavior for all SwimmingBird subclasses."""
        print(f"{self.__class__.__name__} swims")


class Sparrow(FlyingBird):
    """A sparrow that can fly."""
    pass


class Eagle(FlyingBird):
    """An eagle that can fly."""
    pass


class Penguin(SwimmingBird):
    """A penguin that can swim (but not fly)."""
    pass


class Duck(Bird):
    """A duck that can both fly and swim. Demonstrates multiple capability implementation."""
    
    def move(self):
        """Duck flies and swims - overrides Bird's move() to provide its unique behavior."""
        print(f"{self.__class__.__name__} flies and swims")


# Test code demonstrating LSP-compliant design
if __name__ == "__main__":
    print("=== Bird Hierarchy Test (LSP Compliant) ===\n")
    
    # Create birds of different types
    birds = [Sparrow(), Eagle(), Penguin(), Duck()]
    
    # Each bird's move() method works correctly - no exceptions
    # This demonstrates LSP: all subclasses are substitutable for Bird
    for bird in birds:
        bird.move()
    
    print("\n=== Demonstrating Substitutability (LSP) ===")
    
    def make_bird_move(bird: Bird):
        """
        Function that accepts any Bird object.
        This works because all Bird subclasses properly implement move().
        Respects LSP - no unexpected exceptions or violations.
        """
        bird.move()
    
    print("\nCalling make_bird_move() with different bird types:")
    make_bird_move(Sparrow())
    make_bird_move(Penguin())
    make_bird_move(Duck())
    
    print("\n=== Why This Design Respects LSP ===")
    print("""
1. No subclass raises an exception that the parent doesn't define
2. Every subclass properly implements the Bird contract
3. All birds can be treated uniformly as Bird objects
4. Each bird's move() method works as expected for its type
5. Duck can implement multiple capabilities without violating contracts
    """)
