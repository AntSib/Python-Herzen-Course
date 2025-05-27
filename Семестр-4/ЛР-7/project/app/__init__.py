from flask import Flask
from config import Configuration
from app.extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Configuration)

    db.init_app(app)

    with app.app_context():
        from app.models import currency
        # db.create_all()

    from app.controllers.routes import bp
    app.register_blueprint(bp)

    return app
