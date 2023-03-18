# app/__init__.py

from flask import Flask
from .routes import main


def create_app():
    app = Flask(__name__)

    # register routes
    app.register_blueprint(main)

    return app
