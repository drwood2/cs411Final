from flask import (Blueprint, flash, g, redirect,
render_template, request, session, url_for)

#from flask_admin import Admin
#from flask_admin.contrib.sqla import ModelView
from werkzeug.exceptions import abort

from flaskr.auth import (login_required)
from flaskr.db import get_db, get_rows



bp = Blueprint("admin", __name__)


@bp.route("/home")
def home():
    """Show all the requests, most recent first."""


    """cur = get_rows("SELECT r.id, r.maker_id, r.created, r.req_date, r.req_time, r.location, r.priority, r.capacity, m.username FROM req r JOIN maker m ON r.maker_id = m.id ORDER BY created DESC;")"""

    cur = get_rows("SELECT location_name, opens_at, closes_at, l.capacity FROM times t LEFT JOIN locations l on l.name = t.location_name")
    return render_template("admininputs/home.html", reqs=cur.fetchall())



@bp.route("/create/location", methods=("GET", "POST"))
@login_required
def add_locations():
    if request.method == "POST":
        name = request.form["location"]
        capacity = request.form["capacity"]
        opens_at = request.form["opens_at"]
        closes_at = request.form["closes_at"]
        error = None

        if not name:
            error = "location name is required"

        if not capacity:
            error = "location capacity is required"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.cursor().execute("INSERT INTO locations (name, capacity)" "VALUES (%s, %s)", (name, capacity))
            db.commit()
            db.cursor().execute("INSERT INTO times (location_name, opens_at, closes_at)" "VALUES (%s, %s, %s)", (name, opens_at, closes_at))
            db.commit()
        return redirect(url_for("admin.home"))
    return render_template("admininputs/add_locations.html")


@bp.route("/edit/location", methods=("GET", "POST"))
@login_required
def add_times():
    if request.method == "POST":
        opens_at = request.form["opens_at"]
        closes_at = request.form["closes_at"]
        edit_location = request.form["location"]
        error = None

        if not opens_at:
            error = "please enter an opening time for the location"
        if not closes_at:
            error = "please enter a closing time for the location"
        if not edit_location:
            error = "please select a location"

        if error is not None:
            flash(error)

        else:
            db = get_db()
            ex_cur = db.cursor()
            ex_cur.execute("UPDATE times SET opens_at = %s, closes_at = %s WHERE location_name = %s", (opens_at, closes_at, edit_location))
            db.commit()
            return redirect(url_for("admin.home"))
    cur = get_rows("SELECT name FROM locations")
    return render_template("admininputs/add_times.html", locations=cur.fetchall())


@bp.route("/schedule", methods=("GET", "POST"))
@login_required
def schedule():
    if request.method == "POST":
        error = None

        if error is not None:
            flash(error)
        else:
            if(runScheduler() == 0):
                print("schedule works!")
            return redirect(url_for("admin.home"))

    return render_template("admininputs/schedule.html")




def runScheduler():
    db = get_db()
    ex_cur = db.cursor()
    db = get_db()
    cur = db.cursor()
    cur.execute("DROP TABLE IF EXISTS schedule CASCADE;")
    cur.execute("""CREATE TABLE schedule (
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
);""")
    cur.execute("SELECT r.id,r.maker_id, r.created, r.req_date, r.req_time, r.location, r.priority, r.capacity, m.username FROM req r JOIN maker m ON r.maker_id = m.id ORDER BY r.priority DESC;")
    reqs=cur.fetchall()
    #Order to process queries by who has made the fewest requests
    cur.execute("SELECT maker_id FROM (SELECT maker_id, count(id) as REQ_count from req group by maker_id ORDER BY req_count ASC) temp;")
    execute_order=cur.fetchall()
    print(execute_order)
    while(len(reqs) !=0):
        for ex_id in execute_order:
            print(ex_id[0])
            for req in reqs:
                print(req[1])
                if req[1] == ex_id[0]:
                    print("req is time:" +str(req[4]) + "at date:"+str(req[3]))
                    print("check conflict at: " + str(req[4])+ str(req[5])+ str(req[3]))
                    cur.execute("SELECT r.id,r.maker_id, r.created, r.req_date, r.req_time, r.location, r.capacity FROM schedule r WHERE r.req_time = %s AND r.location=%s AND r.req_date = %s;", (req[4],req[5],req[3]))
                    conflicts =cur.fetchall()
                    print("conflicts exist!!\n")
                    print(conflicts)
                    print("conflict len is: "+ str(len(conflicts)))
                    if(len(conflicts)==0):
                        print("SHOULD BE 0")
                        print("conflict len is: "+ str(len(conflicts)))
                        print("insert user:"+str(req[8])+"at time: " +str(req[4]))
                        db.cursor().execute(
                            "INSERT INTO schedule (req_date, capacity, location, req_time, maker_id,username)" "VALUES (%s, %s, %s, %s, %s,%s)",
                            (req[3], req[7], req[5], req[4], req[1],req[8])
                        )
                        db.commit()
                        reqs.remove(req)
                        break

                    else:
                        reqs.remove(req)




    for req in reqs:
        print(req)
        print(type(reqs))



    return 0
