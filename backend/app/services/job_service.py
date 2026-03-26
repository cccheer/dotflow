from sqlalchemy.orm import Session

from app.models.job import Job
from app.schemas.job import JobRead


class JobService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_jobs(self) -> list[JobRead]:
        items = self.db.query(Job).order_by(Job.run_at.desc(), Job.id.desc()).all()
        return [JobRead.model_validate(item) for item in items]
