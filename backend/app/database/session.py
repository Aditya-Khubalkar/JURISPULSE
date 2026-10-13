from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from backend.app.core.config.settings import settings

engine = create_async_engine(str(settings.DATABASE_URL), pool_size=10, pool_pre_ping=True)
async_session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Session factory generator
async def get_session() -> AsyncSession:
    async with async_session_factory() as s: yield s
