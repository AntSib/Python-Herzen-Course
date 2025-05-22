from sqlalchemy.orm import Session
from patterns.patterns import Singleton
from models.term import Term
from schemas.term import TermCreate


class CRUDTerm(metaclass=Singleton):
    def __init__(self, db: Session, model: Term) -> None:
        self.db = db
        self.model = model
    
    def get(self, term_name: str) -> Term | None:
        term = self.db.query(self.model).filter(self.model.name == term_name).first()
        if not term:
            return None
        return term
    
    def get_all(self) -> list[Term]:
        return self.db.query(self.model).all()

    def create(self, new_term: TermCreate) -> Term | None:
        term = self.model(**new_term.dict())
        db_term = self.db.query(self.model).filter(self.model.name == term.name).first()
        if db_term:
            return None
        self.db.add(term)
        self.db.commit()
        self.db.refresh(term)
        return term

    def update(self, term_update: TermCreate) -> Term:
        print('term_update', term_update)
        term = self.get(term_update.name)
        print('term', term)
        if not term:
            return None
        else:
            term.description = term_update.description
        self.db.commit()
        self.db.refresh(term)
        return term
    
    def delete(self, term_name: str) -> None:
        term = self.get(term_name)
        if not term:
            return None
        self.db.delete(term)
        self.db.commit()
        return True
