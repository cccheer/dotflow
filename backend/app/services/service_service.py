from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.device import Device
from app.models.service import Service
from app.plugins.registry import plugin_registry
from app.schemas.service import ServiceCreate, ServiceRead, ServiceUpdate
from app.services.scheduler_service import scheduler_service


class ServiceService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_services(self) -> list[ServiceRead]:
        items = self.db.query(Service).order_by(Service.created_at.desc()).all()
        return [ServiceRead.model_validate(item) for item in items]

    def get_service_or_none(self, service_id: int) -> Service | None:
        return self.db.get(Service, service_id)

    def create_service(self, payload: ServiceCreate) -> ServiceRead:
        self._ensure_device_exists(payload.device_id)
        plugin_registry.get(payload.type).validate_config(payload.config)

        item = Service(**payload.model_dump())
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        scheduler_service.sync_service(item.id)
        return ServiceRead.model_validate(item)

    def update_service(self, service_id: int, payload: ServiceUpdate) -> ServiceRead:
        item = self.db.get(Service, service_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Service not found")

        updates = payload.model_dump(exclude_unset=True)
        next_type = updates.get("type", item.type)
        next_config = updates.get("config", item.config)
        next_device_id = updates.get("device_id", item.device_id)

        self._ensure_device_exists(next_device_id)
        plugin_registry.get(next_type).validate_config(next_config)

        for field, value in updates.items():
            setattr(item, field, value)

        self.db.commit()
        self.db.refresh(item)
        scheduler_service.sync_service(item.id)
        return ServiceRead.model_validate(item)

    def _ensure_device_exists(self, device_id: str) -> None:
        if self.db.get(Device, device_id) is None:
            raise HTTPException(status_code=400, detail="Referenced device does not exist")
