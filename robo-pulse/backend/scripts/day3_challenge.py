import asyncio
from app.models import Mission, Robot, Operator
from app.database import AsyncSessionLocal
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def find_colocation_discrepancies_orm(session) -> list[Mission]: 
    stmnt = (
        select(Mission)
        .join(Robot, Mission.robot)
        .join(Operator, Mission.operator)
        .options(selectinload(Mission.robot))
        .options(selectinload(Mission.operator))
        .where(Robot.facility_id != Operator.facility_id)
    )

    result = await session.execute(stmnt)

    return list(result.scalars().all())

async def main() -> None:
    async with AsyncSessionLocal() as session:
        print("== Co-Location Discrepancy Report (via ORM) ==")

        discrepancies = await find_colocation_discrepancies_orm(session)

        if not discrepancies:
            print("No locatoin discrepancies")

        else:
            for mission in discrepancies:
                print(f"Mission {mission.id} ({mission.title}): robot at facility {mission.robot.facility_id}, operator at facility {mission.operator.facility_id}")

'''
   == Co-Location Discrepancy Report (via ORM) ==
     Mission 2 (Warehouse Perimeter Patrol): robot at facility 2, operator at facility 1
'''

if __name__ == "__main__":
    asyncio.run(main())