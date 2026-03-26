from fastapi import APIRouter

from app.schemas.common import ApiResponse


router = APIRouter()


@router.get("/health", response_model=ApiResponse[dict])
def healthcheck() -> ApiResponse[dict]:
    return ApiResponse(data={"status": "ok"})
