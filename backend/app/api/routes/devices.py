from fastapi import APIRouter, Depends

from app.api.deps import DBSession
from app.core.security import verify_admin_token
from app.schemas.common import ApiResponse
from app.schemas.device import DeviceListResponse, DeviceRead, DeviceUpdate
from app.services.device_service import DeviceService


router = APIRouter(dependencies=[Depends(verify_admin_token)])


@router.get("", response_model=ApiResponse[DeviceListResponse])
def list_devices(db: DBSession) -> ApiResponse[DeviceListResponse]:
    items = DeviceService(db).list_devices()
    return ApiResponse(data=DeviceListResponse(items=items))


@router.post("/sync", response_model=ApiResponse[DeviceListResponse])
def sync_devices(db: DBSession) -> ApiResponse[DeviceListResponse]:
    items = DeviceService(db).sync_devices()
    return ApiResponse(data=DeviceListResponse(items=items), message="Devices synced")


@router.put("/{device_id}", response_model=ApiResponse[DeviceRead])
def update_device(device_id: str, payload: DeviceUpdate, db: DBSession) -> ApiResponse[DeviceRead]:
    item = DeviceService(db).update_device(device_id=device_id, payload=payload)
    return ApiResponse(data=item, message="Device updated")
