from config import Configuration
from flask import Flask
from flask_socketio import SocketIO

from app.database_setup import db

socketio = SocketIO(async_mode="eventlet")


def create_app():
    """
    Creates a Flask app with the given configuration and initializes the database and SocketIO.

    Registers the "main" blueprint and sets up the RatesSubject to start observing currency rates.

    Returns the created Flask app.
    """
    app = Flask(__name__)
    app.config.from_object(Configuration)

    db.init_app(app)
    socketio.init_app(app)

    with app.app_context():
        db.create_all()

    from app.controllers.routes import bp

    app.register_blueprint(bp)

    from app.sockets.events import register_socket_events

    register_socket_events(socketio)

    from app.observers.rates_subject import RatesSubject

    rates_subject = RatesSubject(app, socketio)
    rates_subject.start()
    app.extensions["rates_subject"] = rates_subject

    return app
