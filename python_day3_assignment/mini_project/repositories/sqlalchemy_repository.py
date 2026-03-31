"""SQLAlchemy repository implementation."""
from typing import List, Dict, Any, Optional, Type
from sqlalchemy.orm import Session
from sqlalchemy import desc
from repositories.base_repository import BaseRepository
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SQLAlchemyRepository(BaseRepository):
    """SQLAlchemy-based repository implementation (DIP - implements BaseRepository interface)."""
    
    def __init__(self, model: Type, db_session: Session):
        """
        Initialize repository with model class and database session.
        
        Args:
            model: SQLAlchemy model class
            db_session: Database session
        """
        self.model = model
        self.db = db_session
    
    def save(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save an entity and return it with ID.
        
        Args:
            entity: Dictionary containing entity data
        
        Returns:
            Saved entity as dictionary with ID
        """
        try:
            # Create model instance from dictionary
            db_entity = self.model(**entity)
            
            # Add to session and flush to get ID
            self.db.add(db_entity)
            self.db.flush()
            self.db.commit()
            
            # Refresh to ensure all fields are populated
            self.db.refresh(db_entity)
            
            logger.info(f"Saved {self.model.__name__} with ID {db_entity.id}")
            return db_entity.to_dict()
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error saving {self.model.__name__}: {str(e)}")
            raise
    
    def find_by_id(self, entity_id: int) -> Optional[Dict[str, Any]]:
        """
        Find entity by ID.
        
        Args:
            entity_id: Entity ID
        
        Returns:
            Entity as dictionary or None if not found
        """
        try:
            entity = self.db.query(self.model).filter(self.model.id == entity_id).first()
            if entity:
                return entity.to_dict()
            return None
        except Exception as e:
            logger.error(f"Error finding {self.model.__name__} by ID {entity_id}: {str(e)}")
            raise
    
    def find_all(self) -> List[Dict[str, Any]]:
        """
        Find all entities.
        
        Returns:
            List of entities as dictionaries
        """
        try:
            entities = self.db.query(self.model).order_by(desc(self.model.id)).all()
            return [entity.to_dict() for entity in entities]
        except Exception as e:
            logger.error(f"Error finding all {self.model.__name__}: {str(e)}")
            raise
    
    def update(self, entity_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update entity by ID.
        
        Args:
            entity_id: Entity ID
            data: Dictionary with fields to update
        
        Returns:
            Updated entity as dictionary
        """
        try:
            entity = self.db.query(self.model).filter(self.model.id == entity_id).first()
            if not entity:
                return None
            
            # Update fields
            for key, value in data.items():
                if hasattr(entity, key):
                    setattr(entity, key, value)
            
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            
            logger.info(f"Updated {self.model.__name__} with ID {entity_id}")
            return entity.to_dict()
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating {self.model.__name__} ID {entity_id}: {str(e)}")
            raise
    
    def delete(self, entity_id: int) -> bool:
        """
        Delete entity by ID.
        
        Args:
            entity_id: Entity ID
        
        Returns:
            True if deleted, False if not found
        """
        try:
            entity = self.db.query(self.model).filter(self.model.id == entity_id).first()
            if not entity:
                return False
            
            self.db.delete(entity)
            self.db.commit()
            
            logger.info(f"Deleted {self.model.__name__} with ID {entity_id}")
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting {self.model.__name__} ID {entity_id}: {str(e)}")
            raise
    
    def exists(self, entity_id: int) -> bool:
        """
        Check if entity exists.
        
        Args:
            entity_id: Entity ID
        
        Returns:
            True if exists, False otherwise
        """
        try:
            count = self.db.query(self.model).filter(self.model.id == entity_id).count()
            return count > 0
        except Exception as e:
            logger.error(f"Error checking if {self.model.__name__} ID {entity_id} exists: {str(e)}")
            raise
    
    def get_next_id(self) -> int:
        """
        Get next ID for new entity.
        
        Returns:
            Next auto-increment ID (for compatibility with BaseRepository interface)
        """
        # With SQLAlchemy and auto-increment, this is handled automatically
        # Return 0 or the next ID would be max_id + 1
        try:
            max_entity = self.db.query(self.model).order_by(desc(self.model.id)).first()
            if max_entity:
                return max_entity.id + 1
            return 1
        except Exception as e:
            logger.error(f"Error getting next ID for {self.model.__name__}: {str(e)}")
            return 1
