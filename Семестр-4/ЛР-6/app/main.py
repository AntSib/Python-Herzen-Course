from fastapi import FastAPI
# 
# from app.api.v1 import user
from api.v2 import term

from core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Routers
app.include_router(term.router, prefix="/api/v2/term", tags=["Terms"])
