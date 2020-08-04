from flask import (Blueprint, flash, g, redirect,
render_template, request, session, url_for)

#from flask_admin import Admin
#from flask_admin.contrib.sqla import ModelView
from werkzeug.exceptions import abort

from flaskr.auth import (login_required, admin_required)
from flaskr.db import get_db



bp = Blueprint("admin", __name__)



@bp.route("/")
def index():
    """Show all the requests, most recent first."""


    """cur = get_rows("SELECT r.id, r.maker_id, r.created, r.req_date, r.req_time, r.location, r.priority, r.capacity, m.username FROM req r JOIN maker m ON r.maker_id = m.id ORDER BY created DESC;")"""

    cur = get_rows("SELECT * FROM Locations loc, Times times;")
    return render_template("admin/displayinfo.html", reqs=cur.fetchall())



@bp.route("/create", methods=("GET", "POST"))
@admin_required
def add_locations():
	if request.method == "POST":
		addedLocation = request.form["addedLocation"]
                addedLocationCapacity = request.form["addedLocationCapacity"]
		error = None

		if not addedLocation:
			error = "location is required"

		if not addedLocationCapacity:
			error = "location capacity is required"

	if error is not None:
		flash(error)
	else:
		db = get_db()
		db.cursor().execute("INSERT INTO locations (addedLocation, addedLocationCapacity, locationId)" "VALUES (%s, %s, %s)", (addedLocation, addedLocationCapacity, locationId))
		db.commit()
	return redirect(url_for("admininputs.displayinfo"))
	return render_template("admininputs/addLocations.html")


@bp.route("/create", methods=("GET", "POST"))
@admin_required
def add_times():
	if request.method == "POST":
		addedTime = request.form["addedTime"]
		error = None

		if not addedTime:
			error = "time is required"

		if error is not None:
			flash(error)

		else:
			db = get_db()
			db.cursor().execute("INSERT INTO times (addedTime, time_id)" "VALUES (%s, %s)", (addedTime, time_id))
			db.commit()
			return redirect(url_for("admininputs.displayinfo"))
	return render_template("admininputs/addTimes.html")
