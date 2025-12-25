from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import models, schemas


def list_term_names(db: Session) -> list[str]:
    rows = db.query(models.Term.name).order_by(models.Term.name).all()
    return [r[0] for r in rows]


def get_term_by_name(db: Session, name: str):
    return db.query(models.Term).filter(models.Term.name == name).first()


def create_term(db: Session, term_in: schemas.TermCreate):
    obj = models.Term(
        name=term_in.name.strip(),
        description=term_in.description.strip(),
    )
    db.add(obj)
    try:
        db.commit()
        db.refresh(obj)
    except IntegrityError:
        db.rollback()
        raise
    else:
        return obj


def update_term(
    db: Session,
    current_name: str,
    new_name: str | None,
    new_description: str | None,
):
    obj = get_term_by_name(db, current_name)
    if not obj:
        return None
    if new_name and new_name.strip():
        obj.name = new_name.strip()
    if new_description and new_description.strip():
        obj.description = new_description.strip()
    try:
        db.commit()
        db.refresh(obj)
    except IntegrityError:
        db.rollback()
        raise
    else:
        return obj


def delete_term(db: Session, name: str) -> bool:
    obj = get_term_by_name(db, name)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
