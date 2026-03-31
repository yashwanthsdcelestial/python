from typing import Optional, Type, TypeVar, List
from sqlalchemy.orm import Session
from repositories.base_repository import BaseRepository

T = TypeVar("T")


class SQLAlchemyRepository(BaseRepository[T]):
    """Concrete SQLAlchemy implementation of BaseRepository."""

    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def save(self, entity: T) -> T:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def find(self, entity_id: int) -> Optional[T]:
        return self.db.query(self.model).filter(self.model.id == entity_id).first()

    def find_all(self, **filters) -> List[T]:
        query = self.db.query(self.model)
        for attr, value in filters.items():
            if value is not None:
                query = query.filter(getattr(self.model, attr) == value)
        return query.all()

    def update(self, entity: T) -> T:
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, entity_id: int) -> bool:
        entity = self.find(entity_id)
        if entity:
            self.db.delete(entity)
            self.db.commit()
            return True
        return False

    def find_by(self, **kwargs) -> Optional[T]:
        return self.db.query(self.model).filter_by(**kwargs).first()

    def count_by(self, **kwargs) -> int:
        return self.db.query(self.model).filter_by(**kwargs).count()

    def find_all_filtered(self, filters: list, order_by=None, offset: int = 0, limit: int = 10) -> List[T]:
        query = self.db.query(self.model)
        for f in filters:
            query = query.filter(f)
        if order_by is not None:
            query = query.order_by(order_by)
        return query.offset(offset).limit(limit).all()

    def find_all_raw(self) -> List[T]:
        return self.db.query(self.model).all()