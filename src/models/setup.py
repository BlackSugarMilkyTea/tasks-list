from app import app
from .conf import db
from . import tasks  # initialize Tables of tasks

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.create_all()  # create db tables after model initialization
