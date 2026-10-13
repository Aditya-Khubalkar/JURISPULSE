from typing import Generic, TypeVar, Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .base import Base
T = TypeVar("T", bound=Base)
class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session
    async def get_by_id(self, id: str) -> Optional[T]:
        res = await self.session.execute(select(self.model).where(self.model.id == id))
        return res.scalar_one_or_none()
