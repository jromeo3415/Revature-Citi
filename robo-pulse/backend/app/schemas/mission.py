'''
Day 4 Phase B Student Challenge
'''

from pydantic import Field, BaseModel, ConfigDict

from app.models.enums import MissionPriority, MissionStatus

'''
class MissionBase(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    priority: MissionPriority 
    status: MissionStatus = MissionStatus.PENDING
    robot_id: int
    operator_id: int

class MissionRead(MissionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class MissionCreate(MissionBase):
    pass
'''

class DiscrepancyRead(BaseModel):
    id: int
    title: str = Field(min_length=1, max_length=150)
    robot_facility_id: int
    operator_facility_id: int