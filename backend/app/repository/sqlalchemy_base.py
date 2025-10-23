from typing import Type, TypeVar, Generic, List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sa_update, delete as sa_delete
from sqlalchemy.orm import DeclarativeMeta

T = TypeVar("T", bound=DeclarativeMeta)


class SQLAlchemyBaseRepository(Generic[T]):
    """
    Generic async repository for SQLAlchemy models.
    Mirrors the Beanie BaseRepository pattern.
    """

    def __init__(self, model: Type[T]):
        self.model = model

    async def create(self, db: AsyncSession, obj_data: Dict[str, Any]) -> T:
        """Create a new record."""
        obj = self.model(**obj_data)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def get_by_id(self, db: AsyncSession, obj_id: Any) -> Optional[T]:
        """Retrieve a record by primary key."""
        result = await db.execute(select(self.model).where(self.model.id == obj_id))
        return result.scalar_one_or_none()

    async def find_one(self, db: AsyncSession, filters: Dict[str, Any]) -> Optional[T]:
        """Find one record matching filters."""
        stmt = select(self.model).filter_by(**filters)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def find_many(self, db: AsyncSession, filters: Dict[str, Any] = {}) -> List[T]:
        """Find many records matching filters."""
        stmt = select(self.model).filter_by(**filters)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def update(self, db: AsyncSession, obj_id: Any, update_dict: Dict[str, Any]) -> Optional[T]:
        """Update a record and return the updated instance."""
        stmt = (
            sa_update(self.model)
            .where(self.model.id == obj_id)
            .values(**update_dict)
            .returning(self.model)
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one_or_none()

    async def delete(self, db: AsyncSession, obj_id: Any) -> bool:
        """Delete a record by ID."""
        stmt = sa_delete(self.model).where(self.model.id == obj_id)
        await db.execute(stmt)
        await db.commit()
        return True
