from fastapi import APIRouter, Depends, status, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from src.infrastructure.config.databases.db_config import get_db_session
from src.application.dtos.player_response_dto import PlayerResponseDTO
from src.application.use_cases import GenerateBioUseCase, GetBioStatusUseCase
from src.infrastructure.repositories import BioJobRepositoryAdapter
from src.infrastructure.services.openai_service_adapter import OpenAIServiceAdapter
from src.domain.entities.bio_generation_job import BioGenerationJob

router = APIRouter(tags=["Player Bio"])

def dep_generate_bio_uc(db: Session = Depends(get_db_session)) -> GenerateBioUseCase:
    return GenerateBioUseCase(
        bio_job_repository=BioJobRepositoryAdapter(db),
        llm_service=OpenAIServiceAdapter()
    )

def dep_get_bio_status_uc(db: Session = Depends(get_db_session)) -> GetBioStatusUseCase:
    return GetBioStatusUseCase(
        bio_job_repository=BioJobRepositoryAdapter(db)
    )

from src.infrastructure.background_tasks.bio_tasks import run_process_bio_background

# ... imports ...

@router.post(
    "/generate",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger bio generation",
)
def generate_bio(
    player_data: PlayerResponseDTO,
    background_tasks: BackgroundTasks,
    uc: GenerateBioUseCase = Depends(dep_generate_bio_uc)
):
    job_id = uc.execute(player_data)
    background_tasks.add_task(run_process_bio_background, job_id, player_data)
    return {"job_id": job_id, "status": "PENDING"}

@router.get(
    "/{job_id}",
    response_model=BioGenerationJob,
    status_code=status.HTTP_200_OK,
    summary="Get bio generation status",
)
def get_bio_status(
    job_id: str,
    uc: GetBioStatusUseCase = Depends(dep_get_bio_status_uc)
):
    job = uc.execute(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
