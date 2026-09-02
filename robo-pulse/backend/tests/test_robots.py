'''
Day 10 Endpoint Tests for /robots
'''

from tests.conftest import auth_header, seeded_facility

# if there is no auth header at all, it should be rejected
async def test_list_robots_requires_authentication(client):
    response = await client.get("/robots")
    assert response.status_code == 401

'''
The auditor role is the most restricted in the app. If 
auditor can read the fleet list, then every other role can too
'''
async def test_list_robots_any_authenticated_role(client, seeded_users):
    response = await client.get("/robots", headers=auth_header(seeded_users["auditor"]))
    assert response.status_code == 200

'''
Field operator is authenticated but not a fleet admin, then creating a 
robot should be blocked
'''
async def test_create_robot_forbidden_for_field_operator(client, seeded_users, seeded_facility):
    payload = {
        "serial_number": "TX-1001", 
        "model": "Test-Bot",
        "battery_level": 50.0,
        "facility_id": seeded_facility.id,
        "status": "Idle"
    }
    response = await client.post("/robots", json=payload, headers=auth_header(seeded_users["operator"]))
    assert response.status_code == 403

'''
Matching positive test case for a genuine fleet admin to create a robot
'''
async def test_create_robot_succeeds_for_fleet_admin(client, seeded_users, seeded_facility):
    payload = {
        "serial_number": "TX-1001", 
        "model": "Test-Bot",
        "battery_level": 50.0,
        "facility_id": seeded_facility.id,
        "status": "Idle"
    }
    response = await client.post("/robots", json=payload, headers=auth_header(seeded_users["admin"]))
    assert response.status_code == 201  
    assert response.json()["serial_number"] == "TX-1001"

'''
Verify battery level is within constraints
'''
async def test_low_battery_filter(client, seeded_users, seeded_facility):
    admin_headers = auth_header(seeded_users["admin"])
    low = {"serial_number": "LOW-01", "model": "Test-Bot", "battery_level": 10, "facility_id": seeded_facility.id, "status": "Idle"}
    high = {"serial_number": "HIGH-01", "model": "Test-Bot", "battery_level": 90, "facility_id": seeded_facility.id, "status": "Idle"}

    await client.post("/robots", json=low, headers=admin_headers)
    await client.post("/robots", json=high, headers=admin_headers)

    response = await client.get("/robots?max_battery=20", headers=admin_headers)
    serials = [robot["serial_number"] for robot in response.json()]

    assert "LOW-01" in serials
    assert "HIGH-01" not in serials