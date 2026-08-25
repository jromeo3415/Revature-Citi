from fastapi import APIRouter, Depends, APIRouter, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dependencies import get_db
from app.models.user import User
from app.models.robot import Robot
from app.models.mission import Mission
from app.models.operator import Operator
from app.schemas.mission import DiscrepancyRead, MissionRead, MissionStatusUpdate
from app.models.enums import MissionPriority, MissionStatus
from app.dependencies import require_role, UserRole

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

@router.patch("/{mission_id}/status", response_model=MissionRead)
async def get_mission_status(mission_id: int, payload: MissionStatusUpdate, db: AsyncSession = Depends(get_db), _: User = Depends(require_role(UserRole.FLEET_ADMIN, UserRole.FIELD_OPERATOR))) -> MissionStatus:
    mission = await db.get(Mission, mission_id)

    if mission is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Mission {mission_id} not found"
        )

    if payload.status == MissionStatus.COMPLETED:
        mission.mark_completed()

    elif payload.status == MissionStatus.FAILED:
        mission.mark_failed()

    else:
        mission.status = payload.status

    await db.commit()
    await db.refresh(mission)

    return mission