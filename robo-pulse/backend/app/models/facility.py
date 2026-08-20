'''
Facility Model - Day 1
(No DB yet)

Here we are demonstrating simple classes, class attributes, 
and class methods. In teh future we will be using SQLAlchemy
to manage our DB models. 
'''

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