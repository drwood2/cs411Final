import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from flaskr.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.maker is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    """If a maker id is stored in the session, load the maker object from
    the database into ``g.user``."""

    maker_id = session.get("maker_id")
    db = get_db()
    cur = db.cursor()
    if maker_id is None:
        g.maker = None
    else:
        cur.execute("SELECT * FROM maker WHERE id=%s", [maker_id])
        g.maker = (
            cur.fetchone()
        )


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        if request.form.get("isAdmin"):
            isAdmin = True
        else:
            isAdmin = False
        db = get_db()
        cur = db.cursor()
        error = None

        if not username:
            error = "please enter a username"
        if not password:
            error = "please enter a password"
        if not email:
            error = "please enter an email"

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            db.cursor().execute(
                "INSERT INTO maker (username, password, email, isAdmin) VALUES (%s, %s, %s, %s)", (username, generate_password_hash(password), email, isAdmin),
            )
            db.commit()
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered maker by adding the maker id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        admin_login = request.form.get("admin_login")
        db = get_db()
        cur = db.cursor()
        error = None

        cur.execute(
            "SELECT * FROM maker WHERE username = %s", (username,)
        )
        maker = cur.fetchone()
        if maker is None:
            error = "Incorrect username."

        if not check_password_hash(maker[2], password):
            error = "Incorrect password."

        if admin_login:
            cur.execute(
                "SELECT * FROM maker WHERE username = %s AND isAdmin = TRUE", (username,)
            )
            if cur.fetchone() is None:
                error = "You do not have admin access."

        if error is None:
            # store the maker id in a new session and return to the index
            session.clear()
            session["maker_id"] = maker[0]
            if admin_login:
                return redirect(url_for("admin.home"))
            else:
                return redirect(url_for("user_req.index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored maker id."""
    session.clear()
    return redirect(url_for("user_req.index"))
