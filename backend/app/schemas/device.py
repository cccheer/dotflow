from datetime import datetime

from pydantic import BaseModel


class DeviceBase(BaseModel):
    name: str
    api_base_url: str | None = None
    text_task_key: str | None = None
    image_task_key: str | None = None
    default_content_type: str | None = None


class DeviceRead(DeviceBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DeviceUpdate(BaseModel):
    name: str | None = None
    api_base_url: str | None = None
    text_task_key: str | None = None
    image_task_key: str | None = None
    default_content_type: str | None = None


class DeviceListResponse(BaseModel):
    items: list[DeviceRead]
