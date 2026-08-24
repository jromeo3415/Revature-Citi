'''
Day 4 - Robot Endpoints

Common pattern for REST endpoints: 
GET /robots -> gets all robots
GET /robots/1 -> gets all robots with id 1
POST /robots -> Create a robot resource
PUT /robots/2 -> Updates robot with id = 2
DELETE /robots/3 -> delete the robot with id = 3

Query parameter
GET robots?max_battery=20 -> gets all robots where max bettry is 20
'''


from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status, Query

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.models.robot import Robot
from app.schemas.robot import RobotCreate, RobotRead
from app.models.enums import RobotStatus

router = APIRouter(prefix="/robots", tags=["robots"])

@router.get("", response_model = list[RobotRead])
async def list_robots(max_battery: Decimal | None = Query(
                        default = None, #this makes it optional
                        ge = 0,
                        le = 100,
                        description = "Only return robots strictly below this battery percentage"
                    ), 
                    db: AsyncSession = Depends(get_db)):

    statement = select(Robot).where(Robot.status != RobotStatus.OFFLINE)

    # check for max battery query parameter
    if max_battery is not None:
        statement=statement.where(Robot.battery_level < max_battery)

    result = await db.execute(statement)

    return list(result.scalars().all())

@router.get("/{robot_id}", response_model = RobotRead)
async def get_robot(robot_id: int, db: AsyncSession = Depends(get_db)) -> Robot:
    robot = await db.get(Robot, robot_id)

    if robot is None: 
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"Robot {robot_id} not found"
        )

    return robot

@router.post("", response_model=RobotRead, status_code=status.HTTP_201_CREATED)
async def create_robot(payload: RobotCreate, db: AsyncSession = Depends(get_db)):

    # Dumps the payload into the Robot constructor
    # ** is the unpackaging operator which takes all the attributes and puts them inside the construcor to make a new object
    robot = Robot(**payload.model_dump())

    db.add(robot)
    await db.commit()
    await db.refresh(robot)
    return robot
