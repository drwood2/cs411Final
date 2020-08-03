-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS maker;
DROP TABLE IF EXISTS req;
DROP TABLE IF EXISTS FinalSchedule;
DROP TABLE IF EXISTS Locations;
DROP TABLE IF EXISTS Times;
DROP TABLE IF EXISTS Perms;

CREATE TABLE maker (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  firstName TEXT NOT NULL,
  lastName TEXT NOT NULL,
  email TEXT NOT NULL,
  orgId TEXT NOT NULL
);

CREATE TABLE req (
  id SERIAL PRIMARY KEY,
  maker_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  req_date TEXT NOT NULL,
  req_time TEXT NOT NULL,
  location TEXT NOT NULL,
  priority INTEGER NOT NULL,
  capacity INTEGER NOT NULL,
  FOREIGN KEY (maker_id) REFERENCES maker (id)
);

CREATE TABLE FinalSchedule (
  id SERIAL PRIMARY KEY,
  maker_id INTEGER NOT NULL,
  req_date TEXT NOT NULL,
  firstName TEXT NOT NULL,
  lastName TEXT NOT NULL,
  capacity INTEGER NOT NULL,
  location TEXT NOT NULL,
  req_time TEXT NOT NULL,
  FOREIGN KEY (maker_id) REFERENCES maker (id)
);

CREATE TABLE Locations (
  locationId SERIAL PRIMARY KEY,
  locationName TEXT NOT NULL,
  locationCapacity INTEGER NOT NULL
);

CREATE TABLE Times (
  id SERIAL PRIMARY KEY,
  locationId INTEGER NOT NULL,
  locationName TEXT NOT NULL,
  locationCapacity INTEGER NOT NULL,
  FOREIGN KEY (locationId) REFERENCES Locations (locationId)
);

CREATE TABLE Perms (
  id SERIAL PRIMARY KEY,
  orgId INTEGER NOT NULL,
  p1NumReq INTEGER NOT NULL,
  p2NumReq INTEGER NOT NULL
);