from fastapi import FastAPI
from api.v2 import term

from core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Routers
app.include_router(term.router, prefix="/api/v2/term", tags=["Terms"])

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
