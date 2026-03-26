from fastapi import APIRouter, Depends

from app.api.deps import DBSession
from app.core.security import verify_admin_token
from app.schemas.common import ApiResponse
from app.schemas.job import JobListResponse
from app.services.job_service import JobService


router = APIRouter(dependencies=[Depends(verify_admin_token)])


@router.get("", response_model=ApiResponse[JobListResponse])
def list_jobs(db: DBSession) -> ApiResponse[JobListResponse]:
    items = JobService(db).list_jobs()
    return ApiResponse(data=JobListResponse(items=items))
