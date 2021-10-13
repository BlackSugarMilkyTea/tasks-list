from app import app
from .conf import tasks_api
from . import tasks  # initialize routes of tasks

tasks_api.init_app(app)
