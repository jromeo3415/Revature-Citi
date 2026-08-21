'''
Day 3 - This script creates every table and enum type defined by the
SQLAlchemy models via Base.metadata.create_all through the asyn engine
'''

import asyncio
from app.database import engine
from app.models import Base

async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())