'''
Day 3
Async database engine adn session factory for the ORM 
models to use

DATABASE_URL is read from an env so that today's demo can point
at a mock db for testing purposes

Later, we will replace this with a proper .env file and 
a Pydantic settigns class in the future
'''

import os 
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql+asyncpg://joe:1234@localhost:5432/robopulse_dev",
)

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)