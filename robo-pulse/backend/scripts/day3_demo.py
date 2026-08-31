'''
Day 3 Demo Script

Queries the same robopuls_dev_24788 data from Day 2's seeq.sql already loaded.
This script just prves the ORM model data lines up with what already exists.
'''

import asyncio
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import AsyncSessionLocal
from app.models import Robot, RobotStatus

async def find_low_battery_robots(session, threshold: int = 20) -> list[Robot]:
    statement = (
        select(Robot)
        .options(selectinload(Robot.facility))
        .where(Robot.status != RobotStatus.OFFLINE, Robot.battery_level < threshold)
        .order_by(Robot.id)
    )
    result = awarobo-pulse/frontendit session.execute(statement)

    return list(result.scalars().all())

async def main() -> None:
    async with AsyncSessionLocal() as session:
        print("== Full Robot Registry (via ORM) ==")

        all_robots_stmt = select(Robot).options(selectinload(Robot.facility)).order_by(Robot.id) 
        all_robots = await session.execute(all_robots_stmt)
        for robot in all_robots.scalars():
            print(f"{robot!r} -> facility: {robot.facility.name}")
        print("===================================")

        print("\n== Low Battery Alert (<20%) ==")
        alerts = await find_low_battery_robots(session)
        if not alerts:
            print("No robots below threshold")

        for robot in alerts:
            print(f"ALERT: {robot.serial_number} at {robot.battery_level}% Facility: {robot.facility.name}")

if __name__ == "__main__":
    asyncio.run(main())