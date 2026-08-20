-- Robopulse Command Center day 2 schema

--Enums
CREATE TYPE robot_status as ENUM ('Idle', 'In-Mission', 'Maintenance', 'Offline');
CREATE TYPE mission_priority as ENUM ('Low', 'Medium', 'Critical');
CREATE TYPE mission_status as ENUM ('Pending', 'In-Progress', 'Completed', 'Failed');

--Facilities table
CREATE TABLE facilities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location_region VARCHAR(50) NOT NULL,
    capacity INTEGER NOT NULL,
    supervisor_id INTEGER NOT NULL
);

--Operators table
CREATE TABLE operators (
    id SERIAL PRIMARY KEY, 
    name VARCHAR(100) NOT NULL,
    facility_id INTEGER NOT NULL REFERENCES facilities(id) --foreign key,  * - 1 every operator to facility 
);

--Robots table
CREATE TABLE robots (
    id SERIAL PRIMARY KEY, 
    serial_number VARCHAR(50) NOT NULL UNIQUE,
    model VARCHAR(100) NOT NULL,
    status robot_status NOT NULL DEFAULT 'Idle',
    battery_level NUMERIC(5,2) NOT NULL CHECK (battery_level BETWEEN 0 AND 100),
    facility_id INTEGER NOT NULL REFERENCES facilities(id)
);

--Missions table
CREATE TABLE missions (
    id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    priority mission_priority NOT NULL,
    status mission_status NOT NULL DEFAULT 'Pending',
    robot_id INTEGER NOT NULL REFERENCES robots(id),
    operator_id INTEGER NOT NULL REFERENCES operators(id)
);

--Diagnostic logs tables
CREATE TABLE diagnostic_logs (
    id SERIAL PRIMARY KEY,
    mission_id INTEGER NOT NULL REFERENCES missions(id),
    file_url TEXT NOT NULL, 
    notes TEXT,
    create_at TIMESTAMP NOT NULL DEFAULT NOW()
);