from sqlalchemy import text
async def init_pgvector(session):
    await session.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
