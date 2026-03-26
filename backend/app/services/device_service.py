from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.clients.dot_client import DotClient
from app.models.device import Device
from app.schemas.device import DeviceRead, DeviceUpdate


class DeviceService:
    def __init__(self, db: Session, dot_client: DotClient | None = None) -> None:
        self.db = db
        self.dot_client = dot_client or DotClient()

    def list_devices(self) -> list[DeviceRead]:
        items = self.db.query(Device).order_by(Device.created_at.desc()).all()
        return [DeviceRead.model_validate(item) for item in items]

    def sync_devices(self) -> list[DeviceRead]:
        external_devices = self.dot_client.list_devices()
        for item in external_devices:
            existing = self.db.get(Device, item["id"])
            if existing is None:
                existing = Device(id=item["id"], name=item["name"])
                self.db.add(existing)

            existing.name = item.get("name", existing.name)
            existing.api_base_url = item.get("api_base_url", existing.api_base_url)

        self.db.commit()
        return self.list_devices()

    def update_device(self, device_id: str, payload: DeviceUpdate) -> DeviceRead:
        device = self.db.get(Device, device_id)
        if device is None:
            raise HTTPException(status_code=404, detail="Device not found")

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(device, field, value)

        self.db.commit()
        self.db.refresh(device)
        return DeviceRead.model_validate(device)
