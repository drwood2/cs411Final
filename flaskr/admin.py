from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.auth import admin_required
from flaskr.db import get_db

bp = Blueprint("admin", __name__)

@bp.route("/")
def index():
	"""Need to add functionality of what the home admin page will display"""



@bp.route("/create", methods=("GET", "POST"))
@admin_required
def add_locations():
	if request.method == "POST":
        	addedLocation = request.form["addedLocation"]
                error = None

		if not addedLocation:
			error = "location is required"

		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.cursor().execute("INSERT INTO locations (addedLocation, location_id)" "VALUES (%s, %s)", (addedLocation, location_id))
			db.commit()
			return redirect(url_for("admin.index"))
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
			return redirect(url_for("admin.index"))
	return render_template("admininputs/addTimes.html")
