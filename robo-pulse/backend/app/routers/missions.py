from fastapi import APIRouter, Depends, APIRouter, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dependencies import get_db
from app.models.robot import Robot
from app.models.mission import Mission
from app.models.operator import Operator
from app.schemas.mission import DiscrepancyRead
from app.models.enums import MissionPriority

router = APIRouter(prefix="/missions", tags=["missions"])

@router.get("/discrepancies", response_model=list[DiscrepancyRead])
async def get_discrepancies(priority: MissionPriority | None = Query(
                                                                        default = None,
                                                                    ),
                            db: AsyncSession = Depends(get_db), ) -> list[DiscrepancyRead]:
    
    statement = select(Mission.id, Mission.title, Robot.facility_id.label("robot_facility_id"), Operator.facility_id.label("operator_facility_id")).join(Robot, Robot.id == Mission.robot_id).join(Operator, Operator.id == Mission.operator_id).where(Operator.facility_id != Robot.facility_id)

    if priority is not None:
        statement = statement.where(Mission.priority == priority)

    result = await db.execute(statement)
    
    return list(result.mappings().all())