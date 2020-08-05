import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import (get_db, get_rows)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kkyceuncyvjkxe:b1b3ee8a9abc4efccab51570abf6888e48ff80d6570781338d6bdc1d8999cc57@ec2-52-202-66-191.compute-1.amazonaws.com:5432/dccmmcosuglg9u'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DATABASE_URL = 'postgres://kkyceuncyvjkxe:b1b3ee8a9abc4efccab51570abf6888e48ff80d6570781338d6bdc1d8999cc57@ec2-52-202-66-191.compute-1.amazonaws.com:5432/dccmmcosuglg9u'
DATABASE = 'postgres://kkyceuncyvjkxe:b1b3ee8a9abc4efccab51570abf6888e48ff80d6570781338d6bdc1d8999cc57@ec2-52-202-66-191.compute-1.amazonaws.com:5432/dccmmcosuglg9u'

def main():
	


if __name__ == "__main__":
    # execute only if run as a script
    main()