from sqlalchemy import Column, Integer, String
from core.database import Base


class Term(Base):
    __tablename__ = "terms"

    name = Column(String, primary_key=True, index=True, unique=True)
    description = Column(String, index=True)

    def __repr__(self):
        return f"Term(name={self.name}, description={self.description})"
