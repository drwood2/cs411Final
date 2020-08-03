import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
<<<<<<< HEAD
from flask_admin import Admin


#
# db = SQLAlchemy()

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    #lets this work locally as well as remotely
    #if this is deployed to Heroku os.environ will be populated already. If local it won't be

    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        DATABASE_URL = os.environ['DATABASE_URL']
        DATABASE = os.environ['DATABASE_URL']
    except Exception as e:
        print("Exception occured \n")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kkyceuncyvjkxe:b1b3ee8a9abc4efccab51570abf6888e48ff80d6570781338d6bdc1d8999cc57@ec2-52-202-66-191.compute-1.amazonaws.com:5432/dccmmcosuglg9u'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        DATABASE_URL = 'postgres://kkyceuncyvjkxe:b1b3ee8a9abc4efccab51570abf6888e48ff80d6570781338d6bdc1d8999cc57@ec2-52-202-66-191.compute-1.amazonaws.com:5432/dccmmcosuglg9u'
        DATABASE = 'postgres://kkyceuncyvjkxe:b1b3ee8a9abc4efccab51570abf6888e48ff80d6570781338d6bdc1d8999cc57@ec2-52-202-66-191.compute-1.amazonaws.com:5432/dccmmcosuglg9u'

    db = SQLAlchemy(app)
    app.config['SECRET_KEY'] = 'this-is-my-secret-key'


    # register the database commands
    from flaskr import db

    db.init_app(app)



    # apply the blueprints to the app
    from flaskr import auth, user_req, admin

    app.register_blueprint(auth.bp)
    app.register_blueprint(user_req.bp)
    app.register_blueprint(admin.bp)

    app.add_url_rule("/", endpoint="index")

    # admin = Admin(app)
    # admin.add_view(ModelView(g.maker, db.session))

    return app
