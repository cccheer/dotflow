from fastapi import APIRouter

from app.api.routes import devices, health, jobs, services


api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])
api_router.include_router(services.router, prefix="/services", tags=["services"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
