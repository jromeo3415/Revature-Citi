'''
Day 1 demo script
'''

from app.models import Robot, RobotStatus, MissionPriority, MissionStatus, Facility, Mission, DiagnosticLog

def find_low_battery_robots(robots: list[Robot], threshold: int = 20) -> list[Robot]:
    return [
        robot for robot in robots
        if robot.status != RobotStatus.OFFLINE and robot.is_low_battery(threshold)
    ]

def seed_demo_data() -> None:
    Facility(1, "Houston Fabrication Plant", "US-South", 40, 101)
    Facility(2, "Rotterdam Logistics Hub", "EU-East", capacity=25, supervisor_id=102)

    Robot(1, "RX-1001", "Sentinel-V2", 18.5, 1, RobotStatus.IN_MISSION)
    Robot(2, "RX-1002", "Sentinel-V2", battery_level=76.0, facility_id=1, status=RobotStatus.IDLE)
    Robot(3, "AD-2050", "SkyHawk-Drone", 9.0, 2, RobotStatus.IN_MISSION)
    Robot(4, "RX-1003", "Sentinel-V2", battery_level=42.0, facility_id=2, status=RobotStatus.MAINTENANCE)

    Mission(1, "Pipeline Corrosion Sweep", MissionPriority.CRITICAL, 1, 201)
    Mission(2, "Warehouse Perimeter Patrol", MissionPriority.LOW, robot_id=3, operator_id=202)

    DiagnosticLog(1, 1, "s3://robopulse-diagnostics/rx1001-001.pdf", "Vibration sensor reading normal")

def main() -> None:
    seed_demo_data()

    print("==Full Robot Registry==")
    for robot in Robot.registry:
        print(robot)
    print("=======================\n")

    print("===Low Battery Alert===")
    alerts = find_low_battery_robots(Robot.registry, threshold=20)
    if not alerts:
        print("No robots below threshold")
    for robot in alerts:
        print(f" ALERT: {robot.serial_number} at {robot.battery_level}% (facility{robot.facility_id})")
    print("=======================\n")

if __name__ == "__main__":
    main()