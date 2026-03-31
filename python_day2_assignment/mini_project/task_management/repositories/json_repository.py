"""JSON file-based repository implementation."""
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from repositories.base_repository import BaseRepository
from utils.logger import setup_logger

logger = setup_logger(__name__)


class JSONRepository(BaseRepository):
    """JSON file-based repository implementation (LSP compatible)."""
    
    def __init__(self, filepath: Path, collection_name: str = "items"):
        """
        Initialize JSON repository.
        
        Args:
            filepath: Path to JSON file
            collection_name: Name of the collection/key in JSON
        """
        self.filepath = Path(filepath)
        self.collection_name = collection_name
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """Ensure JSON file exists with proper structure."""
        if not self.filepath.exists():
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump({self.collection_name: []}, f, indent=2)
            logger.info(f"Created JSON file: {self.filepath}")
    
    def _load_data(self) -> Dict[str, Any]:
        """Load data from JSON file."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.error(f"Error loading JSON file {self.filepath}: {e}")
            # Return default structure if file is corrupted
            return {self.collection_name: []}
    
    def _save_data(self, data: Dict[str, Any]) -> None:
        """Save data to JSON file."""
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            logger.error(f"Error saving JSON file {self.filepath}: {e}")
            raise
    
    def save(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Save entity and assign ID."""
        data = self._load_data()
        
        # Assign ID if not present
        if 'id' not in entity:
            entity['id'] = self.get_next_id()
        
        data[self.collection_name].append(entity)
        self._save_data(data)
        logger.info(f"Saved {self.collection_name} with ID {entity['id']}")
        return entity
    
    def find_by_id(self, entity_id: int) -> Optional[Dict[str, Any]]:
        """Find entity by ID."""
        data = self._load_data()
        for entity in data[self.collection_name]:
            if entity.get('id') == entity_id:
                return entity
        return None
    
    def find_all(self) -> List[Dict[str, Any]]:
        """Find all entities."""
        data = self._load_data()
        return data.get(self.collection_name, [])
    
    def update(self, entity_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update entity by ID."""
        data = self._load_data()
        
        for i, entity in enumerate(data[self.collection_name]):
            if entity.get('id') == entity_id:
                entity.update(updates)
                data[self.collection_name][i] = entity
                self._save_data(data)
                logger.info(f"Updated {self.collection_name} with ID {entity_id}")
                return entity
        
        return None
    
    def delete(self, entity_id: int) -> bool:
        """Delete entity by ID."""
        data = self._load_data()
        original_length = len(data[self.collection_name])
        
        data[self.collection_name] = [
            e for e in data[self.collection_name]
            if e.get('id') != entity_id
        ]
        
        if len(data[self.collection_name]) < original_length:
            self._save_data(data)
            logger.info(f"Deleted {self.collection_name} with ID {entity_id}")
            return True
        
        return False
    
    def exists(self, entity_id: int) -> bool:
        """Check if entity exists."""
        return self.find_by_id(entity_id) is not None
    
    def get_next_id(self) -> int:
        """Get next ID for new entity."""
        data = self._load_data()
        entities = data.get(self.collection_name, [])
        if not entities:
            return 1
        return max(e.get('id', 0) for e in entities) + 1
