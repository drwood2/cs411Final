import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
#
# db = SQLAlchemy()

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/project'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #DATABASE_URL = os.environ['DATABASE_URL']
    #heroku = Heroku(app)

    #DATABASE_URL = os.environ['DATABASE_URL']
    db = SQLAlchemy(app)
    app.config['SECRET_KEY'] = 'this-is-my-secret-key'

    # app.config.from_mapping(
    #     # a default secret that should be overridden by instance config
    #     SECRET_KEY="dev",
    #     # store the database in the instance folder
    #     DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    # )

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile("config.py", silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.update(test_config)
    #
    # # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    # register the database commands
    from flaskr import db

    db.init_app(app)


    # apply the blueprints to the app
    from flaskr import auth, user_req

    app.register_blueprint(auth.bp)
    app.register_blueprint(user_req.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app
