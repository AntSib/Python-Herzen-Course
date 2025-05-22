from flask import Flask
from project.config import Configuration
from project.app.extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Configuration)

    db.init_app(app)

    with app.app_context():
        from project.app.models import currency
        db.create_all()

    from project.app.controllers.routes import bp
    app.register_blueprint(bp)

    return app
