

import psycopg2
import psycopg2.extras


import click
from flask import (current_app, g)
from flask.cli import with_appcontext
import os

try:
    DATABASE = os.environ['DATABASE_URL']
except Exception as e:
    DATABASE = 'postgres://kkyceuncyvjkxe:b1b3ee8a9abc4efccab51570abf6888e48ff80d6570781338d6bdc1d8999cc57@ec2-52-202-66-191.compute-1.amazonaws.com:5432/dccmmcosuglg9u'

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    # if "db" not in g:
    #     g.db = psycopg2.connect(
    #         current_app.config["DATABASE"], detect_types=psycopg2.PARSE_DECLTYPES
    #     )
    #     g.db.row_factory = psycopg2.Row
    #
    # return g.db
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(DATABASE)
    return db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()
    cur = db.cursor()

    cur.execute("DROP TABLE IF EXISTS req CASCADE;")
    cur.execute("DROP TABLE IF EXISTS maker CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Locations CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Priority CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Perms CASCADE;")
    cur.execute("DROP TABLE IF EXISTS Times CASCADE;")
    cur.execute("DROP TABLE IF EXISTS FinalSchedule CASCADE;")
    
    cur.execute("CREATE TABLE maker(id SERIAL PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL);")

    cur.execute("CREATE TABLE req(id SERIAL PRIMARY KEY, maker_id INTEGER NOT NULL, created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, req_date TEXT NOT NULL, req_time TEXT NOT NULL, location TEXT NOT NULL, priority INTEGER NOT NULL, capacity INTEGER NOT NULL, FOREIGN KEY (maker_id) REFERENCES maker (id));")

    cur.execute("CREATE TABLE FinalSchedule(id SERIAL PRIMARY KEY, maker_id INTEGER NOT NULL, req_date TEXT NOT NULL, firstName TEXT NOT NULL,lastName TEXT NOT NULL, capacity INTEGER NOT NULL, location TEXT NOT NULL, req_time TEXT NOT NULL, FOREIGN KEY (maker_id) REFERENCES maker (id));")

    cur.execute("CREATE TABLE Locations(locationId SERIAL PRIMARY KEY, locationName TEXT NOT NULL, locationCapacity INTEGER NOT NULL);")

    cur.execute("CREATE TABLE Times(timeId SERIAL PRIMARY KEY, timeAvailability TEXT NOT NULL);")

    cur.execute("CREATE TABLE Perms (id SERIAL PRIMARY KEY, isAdmin BOOLEAN NOT NULL DEFAULT FALSE, p1NumReq INTEGER NOT NULL, p2NumReq INTEGER NOT NULL);")


    # with current_app.open_resource("schema.sql") as f:
    #     db.cursor().execute(f.read())
    #     db.commit()
    #     db.cursor().close()
    #     #db.executescript(f.read().decode("utf8"))

def get_rows(query):
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query)
    return cur

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
