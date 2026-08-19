'''
Robot Model - Day 1 
'''

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
    