from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.database import init_db
from app.core.logging import configure_logging
from app.core.config import settings
from app.services.scheduler_service import scheduler_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    init_db()
    scheduler_service.start()
    try:
        yield
    finally:
        scheduler_service.shutdown()


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)
app.include_router(api_router, prefix=settings.api_prefix)

