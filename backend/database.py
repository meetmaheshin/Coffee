"""
Database configuration and connection management
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

# Base class for models
Base = declarative_base()

def get_async_engine_and_session():
    """Create and return async engine and session maker."""
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
    import os
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./coffee_feedback.db")
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        future=True
    )
    async_session_maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    return engine, async_session_maker

async def init_db():
    """Initialize database tables"""
    engine, _ = get_async_engine_and_session()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    """Dependency for getting database session"""
    _, async_session_maker = get_async_engine_and_session()
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
