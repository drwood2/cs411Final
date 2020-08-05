DROP TABLE IF EXISTS req CASCADE;
DROP TABLE IF EXISTS schedule CASCADE;
DROP TABLE IF EXISTS locations CASCADE;
DROP TABLE IF EXISTS times CASCADE;
DROP TABLE IF EXISTS perms CASCADE;
DROP TABLE IF EXISTS maker CASCADE;

CREATE TABLE maker (
 id SERIAL PRIMARY KEY,
 username TEXT UNIQUE NOT NULL,
 password TEXT NOT NULL,
 email TEXT NOT NULL,
 isAdmin BOOLEAN NOT NULL DEFAULT FALSE
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

CREATE TABLE schedule (
 id SERIAL PRIMARY KEY,
 maker_id INTEGER NOT NULL,
 created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 req_date TEXT NOT NULL,
 username TEXT NOT NULL,
 capacity INTEGER NOT NULL,
 location TEXT NOT NULL,
 req_time TEXT NOT NULL,
 FOREIGN KEY (maker_id) REFERENCES maker (id),
 FOREIGN KEY (username) REFERENCES maker (username)
);

CREATE TABLE locations (
 id SERIAL,
 name TEXT NOT NULL PRIMARY KEY,
 capacity INTEGER NOT NULL
);

CREATE TABLE times (
 id SERIAL PRIMARY KEY,
 location_name TEXT NOT NULL,
 opens_at TEXT NOT NULL,
 closes_at TEXT NOT NULL,
 FOREIGN KEY (location_name) REFERENCES locations (name)
);

CREATE TABLE perms (
 id SERIAL PRIMARY KEY,
 isAdmin BOOLEAN NOT NULL DEFAULT FALSE,
 p1NumReq INTEGER NOT NULL,
 p2NumReq INTEGER NOT NULL
);
