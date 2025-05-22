from pydantic import BaseModel

class TermCreate(BaseModel):
    name: str
    description: str

class TermRead(TermCreate):
    class Config:
        orm_mode = True
