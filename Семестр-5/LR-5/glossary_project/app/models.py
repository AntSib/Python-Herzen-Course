from sqlalchemy import Column, Integer, String, UniqueConstraint

from .db.session import Base


class Term(Base):
    __tablename__ = "terms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint("name", name="uq_term_name"),)

    def __repr__(self):
        return f"Term(id={self.id!r}, name={self.name!r}, description={self.description!r})"
