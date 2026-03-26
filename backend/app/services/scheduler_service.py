import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.service import Service


logger = logging.getLogger(__name__)


class SchedulerService:
    def __init__(self) -> None:
        self.scheduler = BackgroundScheduler(timezone=settings.scheduler_timezone)
        self._started = False

    def start(self) -> None:
        if self._started:
            return
        self.scheduler.start()
        self._started = True
        self.sync_all()

    def shutdown(self) -> None:
        if self._started:
            self.scheduler.shutdown(wait=False)
            self._started = False

    def sync_all(self) -> None:
        with SessionLocal() as db:
            services = db.query(Service).all()
            for service in services:
                self._upsert_job(service)

    def sync_service(self, service_id: int) -> None:
        if not self._started:
            return
        with SessionLocal() as db:
            service = db.get(Service, service_id)
            if service is None:
                if self.scheduler.get_job(self._job_id(service_id)):
                    self.scheduler.remove_job(job_id=self._job_id(service_id))
                return
            self._upsert_job(service)

    def _upsert_job(self, service: Service) -> None:
        job_id = self._job_id(service.id)
        if not service.enabled or not service.schedule:
            if self.scheduler.get_job(job_id):
                self.scheduler.remove_job(job_id)
            return

        trigger = CronTrigger.from_crontab(service.schedule, timezone=settings.scheduler_timezone)
        if self.scheduler.get_job(job_id):
            self.scheduler.reschedule_job(job_id=job_id, trigger=trigger)
        else:
            self.scheduler.add_job(
                func=self._execute_service,
                trigger=trigger,
                args=[service.id],
                id=job_id,
                replace_existing=True,
            )

    def _execute_service(self, service_id: int) -> None:
        from app.services.execution_service import ExecutionService

        with SessionLocal() as db:
            service = db.get(Service, service_id)
            if service is None or not service.enabled:
                logger.warning("Skipping scheduled job for missing or disabled service %s", service_id)
                return

            ExecutionService(db).run_service(service, trigger_type="schedule")

    @staticmethod
    def _job_id(service_id: int) -> str:
        return f"service:{service_id}"


scheduler_service = SchedulerService()
