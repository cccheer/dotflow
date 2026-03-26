from datetime import datetime

from pydantic import BaseModel, Field


class ServiceBase(BaseModel):
    name: str
    type: str
    enabled: bool = True
    schedule: str | None = None
    device_id: str
    config: dict = Field(default_factory=dict)


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    name: str | None = None
    type: str | None = None
    enabled: bool | None = None
    schedule: str | None = None
    device_id: str | None = None
    config: dict | None = None


class ServiceRead(ServiceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ServiceListResponse(BaseModel):
    items: list[ServiceRead]
