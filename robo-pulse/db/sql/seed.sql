--Robopulse Command Center day 2 seed data

INSERT INTO facilities (id, name, location_region, capacity, supervisor_id) VALUES (1, 'Houston Fabrication Plant', 'US-South', 40, 101),
(2, 'Rotterdam Logistics Hub', 'EU-West', 25, 102);

INSERT INTO operators (id, name, facility_id) VALUES (201, 'John Isidore', 1),
(202, 'Rick Deckard', 1);

INSERT INTO robots (id, serial_number, model, status, battery_level, facility_id) VALUES (1, 'RX-1001', 'Sentinel-V2', 'In-Mission', 18.5, 1),
(2, 'RX-1002', 'Sentinel-V2', 'Idle', 76.0, 1),
(3, 'AD-2050', 'SkyHawk-Drone', 'In-Mission', 9.0, 2),
(4, 'RX-1003', 'Sentinel-V2', 'Maintenance', 42.0, 1);

INSERT INTO missions (id, title, priority, status, robot_id, operator_id) VALUES (1, 'Pipeline Corrosion Sweep', 'Critical', 'Pending', 1, 201), 
(2, 'Warehouse Perimeter Patrol', 'Low', 'Pending', 3, 202),
(3, 'Cooling Tower Inspection', 'Medium', 'Completed', 2, 201),
(4, 'Fence Line Survey', 'Low', 'Failed', 4, 201);

INSERT INTO diagnostic_logs (mission_id, file_url, notes) VALUES (1, 's3://robopulse-diagnostics/rx1001-001.pdf', 'Vibration sensor reading nominal');

--Select Statements
SELECT setval('facilities_id_seq', (SELECT MAX(id) FROM facilities));
SELECT setval('operators_id_seq', (SELECT MAX(id) FROM operators));
SELECT setval('robots_id_seq', (SELECT MAX(id) FROM robots));
SELECT setval('missions_id_seq', (SELECT MAX(id) FROM missions));