import pytest_asyncio

from app.models import Mission, MissionPriority, MissionStatus, Operator, Robot, RobotStatus
from tests.conftest import auth_header

@pytest_asyncio.fixture
async def seeded_mission(db_session, seeded_facility):
    robot = Robot(
        serial_number="MX-0001",
        model="Test_Bot",
        status=RobotStatus.IDLE,
        battery_level=75,
        facility_id=seeded_facility.id
    )

    operator = Operator(name="Test Operator", facility_id=seeded_facility.id)

    db_session.add_all([robot, operator])
    await db_session.commit()
    await db_session.refresh(robot)
    await db_session.refresh(operator)

    mission = Mission(
        title="Test Mission",
        priority=MissionPriority.LOW,
        status=MissionStatus.PENDING,
        robot_id=robot.id,
        operator_id=operator.id
    )
    db_session.add(mission)
    await db_session.commit()
    await db_session.refresh(mission)
    return mission

'''
Ensure fleet admin has full CRUD according to the problem statement
'''
async def test_fleet_admin_can_update_status(client, seeded_users, seeded_mission):
    response = await client.patch(
        f"/missions/{seeded_mission.id}/status",
        json={"status": "Completed"},
        headers=auth_header(seeded_users["admin"]),
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Completed"

'''
Field operator is the second role that can trigger mission status changes
'''
async def test_field_operator_can_update_status(client, seeded_users, seeded_mission):
    response = await client.patch(
        f"/missions/{seeded_mission.id}/status",
        json={"status": "Failed"},
        headers=auth_header(seeded_users["operator"]),
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Failed"

async def test_auditor_cannot_update_status(client, seeded_users, seeded_mission):
    response = await client.patch(
        f"/missions/{seeded_mission.id}/status",
        json={"status": "Completed"},
        headers=auth_header(seeded_users["auditor"]),
    )

    assert response.status_code == 403

async def test_nonexistent_mission_returns_404(client, seeded_users):
    response = await client.patch(
        "/missions/999999999/status",
        json={"status": "Completed"},
        headers=auth_header(seeded_users["admin"])
    )

    assert response.status_code == 404