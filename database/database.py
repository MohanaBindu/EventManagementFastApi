# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from contextlib import asynccontextmanager
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import AsyncGenerator

from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from contextlib import asynccontextmanager
SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///./events_api.db'
 
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # optional: shows SQL in console
    future=True
)
 
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)
 
Base = declarative_base()
 
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session