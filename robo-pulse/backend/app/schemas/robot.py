'''
Day 4 Pydantic v2 Schema for the robot resource
'''

from decimal import Decimal
from app.models.enums import RobotStatus
from pydantic import BaseModel, Field, ConfigDict

class RobotBase(BaseModel):
    serial_number: str = Field(min_length=1, max_length=50)
    model: str = Field(min_length=1, max_length=100)
    battery_level: Decimal = Field(ge=0, le=100)
    facility_id: int
    status: RobotStatus = RobotStatus.IDLE

class RobotCreate(RobotBase):
    pass

class RobotRead(RobotBase):
    id: int
    model_config = ConfigDict(from_attributes=True)