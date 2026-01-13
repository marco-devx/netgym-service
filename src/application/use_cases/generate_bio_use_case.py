import uuid
from src.application.dtos.player_response_dto import PlayerResponseDTO
from src.domain.entities.bio_generation_job import BioGenerationJob
from src.domain.value_objects.job_status import JobStatus
from src.domain.ports.repositories import BioJobRepository
from src.domain.ports.services.llm_service_port import LLMServicePort

class GenerateBioUseCase:
    def __init__(self, bio_job_repository: BioJobRepository, llm_service: LLMServicePort):
        self.bio_job_repository = bio_job_repository
        self.llm_service = llm_service

    def execute(self, player_data: PlayerResponseDTO) -> str:
        job_id = str(uuid.uuid4())
        job = BioGenerationJob(
            id=job_id,
            status=JobStatus.PENDING,
            player_name=player_data.name
        )
        self.bio_job_repository.save(job)
        return job_id
