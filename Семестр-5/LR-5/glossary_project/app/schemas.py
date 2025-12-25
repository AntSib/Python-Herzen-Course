from pydantic import BaseModel, Field


class TermBase(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)


class TermCreate(TermBase):
    pass


class TermUpdate(BaseModel):
    new_name: str | None = None
    new_description: str | None = None


class TermOut(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True
