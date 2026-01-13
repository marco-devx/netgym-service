from typing import Optional
from sqlalchemy.orm import Session
from src.domain.entities.bio_generation_job import BioGenerationJob
from src.domain.value_objects.job_status import JobStatus
from src.domain.ports.repositories.bio_job_repository import BioJobRepository
from src.infrastructure.models.bio_job_model import BioJobModel

class BioJobRepositoryAdapter(BioJobRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, job: BioGenerationJob) -> BioGenerationJob:
        job_model = self.session.query(BioJobModel).filter_by(id=job.id).first()
        if job_model:
            job_model.status = job.status
            job_model.result = job.result
        else:
            job_model = BioJobModel(
                id=job.id,
                status=job.status,
                result=job.result,
                player_name=job.player_name
            )
            self.session.add(job_model)
        
        self.session.commit()
        self.session.refresh(job_model)
        return BioGenerationJob(
            id=job_model.id,
            status=job_model.status,
            result=job_model.result,
            player_name=job_model.player_name
        )

    def get_by_id(self, job_id: str) -> Optional[BioGenerationJob]:
        job_model = self.session.query(BioJobModel).filter_by(id=job_id).first()
        if not job_model:
            return None
        return BioGenerationJob(
            id=job_model.id,
            status=job_model.status,
            result=job_model.result,
            player_name=job_model.player_name
        )
