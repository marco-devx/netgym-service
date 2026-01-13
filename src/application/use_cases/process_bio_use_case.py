from src.application.dtos.player_response_dto import PlayerResponseDTO
from src.domain.value_objects.job_status import JobStatus
from src.domain.ports.repositories import BioJobRepository
from src.domain.ports.services.llm_service_port import LLMServicePort

class ProcessBioUseCase:
    def __init__(self, bio_job_repository: BioJobRepository, llm_service: LLMServicePort):
        self.bio_job_repository = bio_job_repository
        self.llm_service = llm_service

    def execute(self, job_id: str, player_data: PlayerResponseDTO):
        try:
            bio_text = self.llm_service.generate_player_bio(player_data)
            
            job = self.bio_job_repository.get_by_id(job_id)
            if job:
                job.status = JobStatus.COMPLETED
                job.result = bio_text
                self.bio_job_repository.save(job)
        except Exception:
            try:
                job = self.bio_job_repository.get_by_id(job_id)
                if job:
                    job.status = JobStatus.FAILED
                    self.bio_job_repository.save(job)
            except Exception:
                pass
