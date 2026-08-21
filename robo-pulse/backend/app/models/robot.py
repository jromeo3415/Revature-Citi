'''
Robot Model - Day 3
'''

from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .enums import RobotStatus

if TYPE_CHECKING:
    from .facility import Facility
    from .mission import Mission

class Robot(Base):
    __tablename__ = "robots"

    # table level contstraint for battery level
    __table_args__ = (
        CheckConstraint("battery_level BETWEEN 0 AND 100", name="battery_level_range"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    serial_number: Mapped[str] = mapped_column(String(50), unique=True)
    model: Mapped[str] = mapped_column(String(100))
    status: Mapped[RobotStatus] = mapped_column(
        SqlEnum(
            RobotStatus, 
            name="robot_status",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],

        ),
        default=RobotStatus.IDLE
    )

    battery_level: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    facility_id: Mapped[int] = mapped_column(Integer, ForeignKey("facilities.id"))
    facility: Mapped[Facility] = relationship(back_populates="robots")
    missions: Mapped[list["Mission"]] = relationship(back_populates="robot")

    LOW_BATTERY_THRESHOLD: int = 20

    def is_low_battery(self, threshold: int | None = None) -> bool:
        limit = threshold if threshold is not None else Robot.LOW_BATTERY_THRESHOLD
        return self.battery_level < limit

    def needs_maintenance(self) -> bool:
        return self.status == RobotStatus.MAINTENANCE
    
    def __repr__(self) -> str:
        return(f"Robot(serial={self.serial_number!r}, model={self.model!r}, battery={self.battery_level}%, status={self.status.value})")
    



'''
Robot Model - Day 1 


from typing import ClassVar
from .enums import RobotStatus

class Robot:
    registry: ClassVar[list["Robot"]] = []
    LOW_BATTERY_THRESHOLD: ClassVar[int] = 20

    def __init__(self, robot_id: int, serial_number: str, model: str, battery_level: float, facility_id: int, status: RobotStatus = RobotStatus.IDLE):
        self.id = robot_id
        self.serial_number = serial_number
        self.model = model
        self.battery_level = self._validate_battery(battery_level)
        self.facility_id = facility_id
        self.status = status
        Robot.registry.append(self)

    @staticmethod
    def _validate_battery(level: float) -> float:
        if level < 0:
            print(f"Warning: battery_level {level} is below 0, clamping to 0")
            return 0.0

        if level > 100:
            print(f"Warning: battery_level {level} is above 100, clamping to 100")
            return 100.0

        return float(level)      

    def is_low_battery(self, threshold: int | None = None) -> bool:
        limit = threshold if threshold is not None else Robot.LOW_BATTER_THRESHOLD
        return self.battery_level < limit

    def needs_maintenance(self) -> bool:
        return self.status == RobotStatus.MAINTENANCE

    @classmethod
    def find_by_id(cls, robot_id: int) -> "Robot | None":
        for robot in cls.registry:
            if robot.id  == robot_id:
                return robot

        return None

    def __repr__(self) -> str:
        return(f"Robot(serial={self.serial_number!r}, model={self.model!r}, battery={self.battery_level}%, status={self.status.value})")
    
'''