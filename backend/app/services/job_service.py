from sqlalchemy.orm import Session

from app.models.job import Job
from app.schemas.job import JobRead


class JobService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_jobs(self) -> list[JobRead]:
        items = self.db.query(Job).order_by(Job.run_at.desc(), Job.id.desc()).all()
        return [JobRead.model_validate(item) for item in items]

    def get_job_or_none(self, job_id: int) -> JobRead | None:
        item = self.db.get(Job, job_id)
        if item is None:
            return None
        return JobRead.model_validate(item)
