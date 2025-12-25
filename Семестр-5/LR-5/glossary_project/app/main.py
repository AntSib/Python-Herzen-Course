import asyncio
import os

import uvicorn
from fastapi import FastAPI

from . import models
from .api.routers import router as glossary_router
from .db.session import Base, engine


# Try to run alembic upgrade head. If failed, fallback to create_all
def run_migrations():
    try:
        from alembic import command
        from alembic.config import Config

        alembic_cfg = Config(
            os.path.join(os.path.dirname(__file__), "..", "alembic.ini")
        )
        # If alembic.ini doesn't exist or fails, exception will be thrown
        command.upgrade(alembic_cfg, "head")
        print("Alembic upgrade head applied")
    except Exception as e:
        print(
            f"Alembic migration failed or not configured ({e}), falling back to create_all()",
        )
        Base.metadata.create_all(bind=engine)
        print("Tables created via SQLAlchemy create_all()")


app = FastAPI(title="Glossary (REST & gRPC)")

app.include_router(glossary_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    run_migrations()
    print("Startup: migrations checked")


# Start gRPC server in background and uvicorn
def start():
    import threading

    from .grpc_server import server as grpc_server

    loop = asyncio.get_event_loop()

    async def run_both():
        grpc_task = asyncio.create_task(
            grpc_server.serve(host="0.0.0.0", port=int(os.getenv("GRPC_PORT", 50051))),
        )

        # Run uvicorn in another thread because uvicorn.run is blocking
        def run_uvicorn():
            uvicorn.run(
                "app.main:app",
                host="0.0.0.0",
                port=int(os.getenv("HTTP_PORT", 8000)),
                log_level="info",
                reload=False,
            )

        thread = threading.Thread(target=run_uvicorn, daemon=True)
        thread.start()
        await grpc_task

    asyncio.run(run_both())


if __name__ == "__main__":
    start()
