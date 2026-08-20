from typing import ClassVar

class Operator: 
    registry: ClassVar[list["Operator"]] = []

    def __init__(self, operator_id: int, name: str, facility_id: int): 
        self.operator_id = operator_id
        self.name = name
        self.facility_id = facility_id
        Operator.registry.append(self)

    def __repr__(self) -> str:
        return(f"Operator(operator_id={self.operator_id}, name={self.name!r}, facility_id={self.facility_id})")

    @classmethod
    def find_by_id(cls, operator_id: int) -> "Operator | None":
        for operator in Operator.registry: 
            if operator.operator_id == operator_id:
                return operator

        return None