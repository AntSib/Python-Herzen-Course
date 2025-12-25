from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas  # noqa: TID252
from ..db.session import SessionLocal  # noqa: TID252

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/terms", response_model=list[str])
def list_terms(db: Session = Depends(get_db)):
    return crud.list_term_names(db)


@router.get("/terms/{name}", response_model=schemas.TermOut)
def get_term(name: str, db: Session = Depends(get_db)):
    obj = crud.get_term_by_name(db, name)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Term not found",
        )
    return obj


@router.post(
    "/terms", response_model=schemas.TermOut, status_code=status.HTTP_201_CREATED
)
def create_term(term_in: schemas.TermCreate, db: Session = Depends(get_db)):
    try:
        obj = crud.create_term(db, term_in)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    else:
        return obj


@router.put("/terms/{name}", response_model=schemas.TermOut)
def update_term(name: str, update: schemas.TermUpdate, db: Session = Depends(get_db)):
    obj = crud.update_term(db, name, update.new_name, update.new_description)
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Term not found",
        )
    return obj


@router.delete("/terms/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_term(name: str, db: Session = Depends(get_db)):
    ok = crud.delete_term(db, name)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Term not found",
        )
