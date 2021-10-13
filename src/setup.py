import logging

from app import app
from models import setup  # noqa # initialize model configurations
from routes import setup  # noqa # initialize route configurations

app.logger.setLevel(logging.INFO)
