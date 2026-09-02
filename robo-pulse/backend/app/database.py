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
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.config import settings

#load_dotenv()

DATABASE_URL = settings.database_url #os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)