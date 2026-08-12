from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from .config import config


engine = create_async_engine(
    config.db.build_url, 
    echo=config.logs.show_debug_logs,
)

async_sessionmaker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_session():
    async with async_sessionmaker() as session:
        yield session