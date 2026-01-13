from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.bio_generation_job import BioGenerationJob

class BioJobRepository(ABC):
    @abstractmethod
    def save(self, job: BioGenerationJob) -> BioGenerationJob:
        pass

    @abstractmethod
    def get_by_id(self, job_id: str) -> Optional[BioGenerationJob]:
        pass
