"""Base repository abstract class (DIP)."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseRepository(ABC):
    """Abstract base repository defining interface for data access (DIP)."""
    
    @abstractmethod
    def save(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Save an entity and return it with ID."""
        pass
    
    @abstractmethod
    def find_by_id(self, entity_id: int) -> Optional[Dict[str, Any]]:
        """Find entity by ID."""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Dict[str, Any]]:
        """Find all entities."""
        pass
    
    @abstractmethod
    def update(self, entity_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update entity by ID."""
        pass
    
    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """Delete entity by ID."""
        pass
    
    @abstractmethod
    def exists(self, entity_id: int) -> bool:
        """Check if entity exists."""
        pass
    
    @abstractmethod
    def get_next_id(self) -> int:
        """Get next ID for new entity."""
        pass
