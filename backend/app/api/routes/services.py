from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import DBSession
from app.core.security import verify_admin_token
from app.schemas.common import ApiResponse
from app.schemas.service import ServiceCreate, ServiceListResponse, ServiceRead, ServiceUpdate
from app.services.execution_service import ExecutionService
from app.services.service_service import ServiceService


router = APIRouter(dependencies=[Depends(verify_admin_token)])


@router.get("", response_model=ApiResponse[ServiceListResponse])
def list_services(db: DBSession) -> ApiResponse[ServiceListResponse]:
    items = ServiceService(db).list_services()
    return ApiResponse(data=ServiceListResponse(items=items))


@router.post("", response_model=ApiResponse[ServiceRead], status_code=status.HTTP_201_CREATED)
def create_service(payload: ServiceCreate, db: DBSession) -> ApiResponse[ServiceRead]:
    item = ServiceService(db).create_service(payload)
    return ApiResponse(data=item, message="Service created")


@router.put("/{service_id}", response_model=ApiResponse[ServiceRead])
def update_service(service_id: int, payload: ServiceUpdate, db: DBSession) -> ApiResponse[ServiceRead]:
    item = ServiceService(db).update_service(service_id, payload)
    return ApiResponse(data=item, message="Service updated")


@router.post("/{service_id}/run", response_model=ApiResponse[dict])
def run_service(service_id: int, db: DBSession) -> ApiResponse[dict]:
    service = ServiceService(db).get_service_or_none(service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    job = ExecutionService(db).run_service(service, trigger_type="manual")
    return ApiResponse(data={"job_id": job.id, "status": job.status}, message="Service executed")
