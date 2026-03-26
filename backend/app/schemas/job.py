from datetime import datetime

from pydantic import BaseModel


class JobRead(BaseModel):
    id: int
    service_id: int
    device_id: str
    trigger_type: str
    run_at: datetime
    status: str
    request_payload: dict | None = None
    response_payload: dict | None = None
    output: dict | None = None
    error: str | None = None

    model_config = {"from_attributes": True}


class JobListResponse(BaseModel):
    items: list[JobRead]
