from flask import (Blueprint, flash, g, redirect,
render_template, request, session, url_for)

#from flask_admin import Admin
#from flask_admin.contrib.sqla import ModelView
from werkzeug.exceptions import abort

from flaskr.auth import (login_required, admin_required)
from flaskr.db import get_db



bp = Blueprint("admin", __name__)



# @bp.route("/")
# def index():
# 	"""Need to add functionality of what the home admin page will display"""
#

# admin = Admin(current_app)
# admin.add_view(ModelView(get_rows("SELECT * FROM maker").fetchall()))
@bp.route("/")
def index():
    """Show all the requests, most recent first."""


    cur = get_rows("SELECT r.id, r.maker_id, r.created, r.req_date, r.req_time, r.location, r.priority, r.capacity, m.username FROM req r JOIN maker m ON r.maker_id = m.id ORDER BY created DESC;")

    return render_template("user_req/index.html", reqs=cur.fetchall())


def get_req (id, check_author=True):
    """Get a post and its author by id.
    Checks that the id exists and optionally that the current user is
    the author.
    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    db = get_db()
    cur = db.cursor()
    cur.execute(
            "SELECT r.id, r.maker_id, created, req_date, req_time, location, priority, capacity, m.username"
            " FROM req r JOIN maker m ON r.maker_id = m.id"
            " WHERE r.id = %s",
            (id,))
    req = cur.fetchone()


    if req is None:
        abort(404, "request id {0} does not exist".format(id))

    if check_author and req[1] != g.maker[0]:
        abort(403)

    return req


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
