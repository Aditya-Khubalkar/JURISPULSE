from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for s in get_session(): yield s
