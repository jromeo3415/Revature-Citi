'''
Facility MOdel - Day 3 SQLAlchemy 2.0 ORM version
'''

# tells python to treat every type annotation as a string
# literal, allowing forward references to classes that are
# defined later in the file or other modules
from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .operator import Operator
    from .robot import Robot

class Facility(Base): 
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    location_region: Mapped[str] = mapped_column(String(50))
    capacity: Mapped[int] = mapped_column(Integer)
    supervisor_id: Mapped[int] = mapped_column(Integer)

    robots: Mapped[list["Robot"]] = relationship(back_populates="facility")
    operators: Mapped[list["Operator"]] = relationship(back_populates="facility")

    def __repr__(self) -> str:
        return(f"Facility(id={self.id}, name={self.name!r}, location_region={self.location_region!r}")



        





'''
Facility Model - Day 1
(No DB yet)

Here we are demonstrating simple classes, class attributes, 
and class methods. In teh future we will be using SQLAlchemy
to manage our DB models. 


from typing import ClassVar

class Facility:
    registry: ClassVar[list["Facility"]] = []

    def __init__(self, facility_id: int, name: str, location_region: str, capacity: int, supervisor_id: int):
        self.id = facility_id
        self.name = name
        self.location_region = location_region
        self.capacity = capacity
        self.supervisor_id = supervisor_id
        Facility.registry.append(self)

    def __repr__(self) -> str:
        return (f"Facility(id={self.id}, name={self.name}, location_region={self.location_region})")

    @classmethod
    def find_by_id(cls, facility_id: int) -> "Facility | None":
        for facility in cls.registry:
            if facility.id == facility_id:
                return facility

        return None

'''