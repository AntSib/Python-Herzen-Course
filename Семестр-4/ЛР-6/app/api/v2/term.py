from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import SessionLocal, get_db_session
from models.term import Term
from schemas.term import TermCreate, TermRead
from services.term_service import CRUDTerm

router = APIRouter()


@router.get("/terms", response_model=list[TermRead])
def read_terms(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_session)) -> list[TermRead]:
    """Retrieve terms.

    Args:
        skip (int, optional): skip. Defaults to 0.
        limit (int, optional): limit. Defaults to 10.

    Returns:
        list[TermRead]: list of terms.
    """
    crud = CRUDTerm(db, TermRead)
    return crud.get_all()

@router.get("/terms/{term_name}", response_model=TermRead)
def read_term(term_name, db: Session = Depends(get_db_session)) -> TermRead:
    """Retrieve term by name.

    Args:
        term_name (str): term name.

    Raises:
        HTTPException: 404 if term not found.

    Returns:
        TermRead: term.
    """
    crud = CRUDTerm(db, TermRead)
    term = crud.get(term_name)
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    return term

@router.post("/terms/{term}", response_model=TermRead)
def create_term(term: TermCreate = Depends(), db: Session = Depends(get_db_session)) -> TermCreate:
    """Create term.

    Args:
        term (TermCreate): term to create.

    Raises:
        HTTPException: 409 if term already exists.

    Returns:
        TermCreate: created term.
    """
    crud = CRUDTerm(db, Term)
    created = crud.create(term)
    if not created:
        raise HTTPException(status_code=409, detail="Term already exists")
    return created

@router.put("/terms/{term}", response_model=TermCreate)
def update_term(term: TermCreate = Depends(), db: Session = Depends(get_db_session)) -> TermCreate:
    """Update an existing term.

    Args:
        term (TermCreate): The term data to update.
        db (Session): Database session dependency.

    Raises:
        HTTPException: 404 error if the term is not found.

    Returns:
        TermCreate: The updated term data.
    """
    crud = CRUDTerm(db, Term)
    updated = crud.update(term)
    if not updated:
        raise HTTPException(status_code=404, detail="Term not found. Cannot update")
    return updated

@router.delete("/terms/{term_name}")
def delete_term(term_name: str, db: Session = Depends(get_db_session)):
    """Delete term by name.

    Args:
        term_name (str): term name.

    Raises:
        HTTPException: 404 if term not found.

    Returns:
        dict[str, str]: deleted term name with message 'deleted successfully'.
    """
    crud = CRUDTerm(db, Term)
    deleted = crud.delete(term_name)
    if not deleted:
        raise HTTPException(status_code=404, detail="Term not found. Cannot delete")
    return {term_name: "deleted successfully"}


@router.get("/author")
def author() -> dict[str, str]:
    """Return author name and current date/time in Russian locale."""
    from datetime import datetime
    import locale
    locale.setlocale(locale.LC_ALL, 'ru_RU')
    today = datetime.now().strftime("%A, %d.%m.%Y, %H:%M").title()
    return {'author': "Anton", "datetime": f'{today}'}

@router.get('/favicon.ico', include_in_schema=False)
async def favicon() -> None:
    """
    Plug for favicon.ico, returns None to prevent FastAPI from returning 
    a 404 error when it is accessed
    """
    return None
