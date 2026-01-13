from src.infrastructure.config.databases.db_config import SessionLocal
from src.infrastructure.repositories.bio_job_repository import BioJobRepositoryAdapter
from src.infrastructure.services.openai_service_adapter import OpenAIServiceAdapter
from src.application.use_cases.process_bio_use_case import ProcessBioUseCase
from src.application.dtos.player_response_dto import PlayerResponseDTO

def run_process_bio_background(job_id: str, player_data: PlayerResponseDTO):
    """
    Infrastructure helper to run bio generation in a background thread.
    Manages its own database session.
    """
    session = SessionLocal()
    try:
        repo = BioJobRepositoryAdapter(session)
        llm_service = OpenAIServiceAdapter() # Assuming stateless or handles own config
        
        process_uc = ProcessBioUseCase(bio_job_repository=repo, llm_service=llm_service)
        process_uc.execute(job_id, player_data)
    except Exception as e:
        # Log critical error if needed
        print(f"Critical error in background task: {e}")
    finally:
        session.close()
