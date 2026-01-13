from typing import Optional
from src.domain.entities.bio_generation_job import BioGenerationJob
from src.domain.ports.repositories.bio_job_repository import BioJobRepository
 
class GetBioStatusUseCase:
    def __init__(self, bio_job_repository: BioJobRepository):
        self.bio_job_repository = bio_job_repository

    def execute(self, job_id: str) -> Optional[BioGenerationJob]:
        return self.bio_job_repository.get_by_id(job_id)
