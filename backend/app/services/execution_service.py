import logging

from sqlalchemy.orm import Session

from app.clients.dot_client import DotClient
from app.models.device import Device
from app.models.job import Job
from app.models.service import Service
from app.plugins.registry import plugin_registry


logger = logging.getLogger(__name__)


class ExecutionService:
    def __init__(self, db: Session, dot_client: DotClient | None = None) -> None:
        self.db = db
        self.dot_client = dot_client or DotClient()

    def run_service(self, service: Service, trigger_type: str) -> Job:
        device = self.db.get(Device, service.device_id)
        if device is None:
            raise ValueError(f"Device {service.device_id} not found")

        plugin = plugin_registry.get(service.type)
        plugin_output = plugin.generate(service.config)

        request_payload = {
            "refreshNow": True,
            "title": plugin_output.get("title"),
            "message": plugin_output.get("message"),
            "signature": plugin_output.get("signature"),
        }
        if device.text_task_key:
            request_payload["taskKey"] = device.text_task_key

        job = Job(
            service_id=service.id,
            device_id=device.id,
            trigger_type=trigger_type,
            status="running",
            output=plugin_output,
            request_payload=request_payload,
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)

        try:
            response_payload = self.dot_client.push_text(device.id, request_payload)
            job.status = "success"
            job.response_payload = response_payload
        except Exception as exc:  # noqa: BLE001
            logger.exception("Service execution failed", extra={"service_id": service.id})
            job.status = "failed"
            job.error = str(exc)

        self.db.commit()
        self.db.refresh(job)
        return job
