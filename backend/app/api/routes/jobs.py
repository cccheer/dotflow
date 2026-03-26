from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import DBSession
from app.core.security import verify_admin_token
from app.schemas.common import ApiResponse
from app.schemas.job import JobListResponse, JobRead
from app.services.job_service import JobService


router = APIRouter(dependencies=[Depends(verify_admin_token)])


@router.get("", response_model=ApiResponse[JobListResponse])
def list_jobs(db: DBSession) -> ApiResponse[JobListResponse]:
    items = JobService(db).list_jobs()
    return ApiResponse(data=JobListResponse(items=items))


@router.get("/{job_id}", response_model=ApiResponse[JobRead])
def get_job(job_id: int, db: DBSession) -> ApiResponse[JobRead]:
    item = JobService(db).get_job_or_none(job_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return ApiResponse(data=item)
