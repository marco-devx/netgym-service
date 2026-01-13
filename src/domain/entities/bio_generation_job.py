from dataclasses import dataclass
from typing import Optional
from src.domain.value_objects.job_status import JobStatus

@dataclass
class BioGenerationJob:
    id: str
    status: JobStatus
    result: Optional[str] = None
    player_name: Optional[str] = None
