from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app.database_setup import db

class Currency(db.Model):
    __tablename__ = 'currencies'

    currency_code = db.Column(db.String, primary_key=True)
    rate = db.Column(db.Float, nullable=False)
    datetime = db.Column(db.String, default=lambda: datetime.utcnow().isoformat())

    def __repr__(self) -> str:
        return f"Currency(currency_code={self.currency_code}, rate={self.rate}, datetime={self.datetime})"