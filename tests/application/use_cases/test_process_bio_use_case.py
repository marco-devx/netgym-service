import pytest
from unittest.mock import MagicMock
from src.application.use_cases.process_bio_use_case import ProcessBioUseCase
from src.domain.ports.repositories.bio_job_repository import BioJobRepository
from src.domain.ports.services.llm_service_port import LLMServicePort
from src.application.dtos.player_response_dto import PlayerResponseDTO
from src.domain.entities.bio_generation_job import BioGenerationJob
from src.domain.value_objects.job_status import JobStatus

@pytest.fixture
def mock_bio_job_repository():
    return MagicMock(spec=BioJobRepository)

@pytest.fixture
def mock_llm_service():
    return MagicMock(spec=LLMServicePort)

@pytest.fixture
def process_bio_use_case(mock_bio_job_repository, mock_llm_service):
    return ProcessBioUseCase(mock_bio_job_repository, mock_llm_service)

def test_process_bio_success(process_bio_use_case, mock_bio_job_repository, mock_llm_service):
    # Arrange
    job_id = "job-123"
    player_data = PlayerResponseDTO(name="Player", position="P", hits=10, homeruns=1)
    generated_bio = "Generated Bio"
    
    existing_job = BioGenerationJob(id=job_id, status=JobStatus.PENDING, player_name="Player")
    
    mock_llm_service.generate_player_bio.return_value = generated_bio
    mock_bio_job_repository.get_by_id.return_value = existing_job

    # Act
    process_bio_use_case.execute(job_id, player_data)

    # Assert
    mock_llm_service.generate_player_bio.assert_called_once_with(player_data)
    mock_bio_job_repository.get_by_id.assert_called_with(job_id)
    
    # Verify save was called with completed status
    saved_job = mock_bio_job_repository.save.call_args[0][0]
    assert saved_job.status == JobStatus.COMPLETED
    assert saved_job.result == generated_bio

def test_process_bio_llm_failure(process_bio_use_case, mock_bio_job_repository, mock_llm_service):
    # Arrange
    job_id = "job-123"
    player_data = PlayerResponseDTO(name="Player", position="P", hits=10, homeruns=1)
    
    existing_job = BioGenerationJob(id=job_id, status=JobStatus.PENDING, player_name="Player")
    
    mock_llm_service.generate_player_bio.side_effect = Exception("API Error")
    mock_bio_job_repository.get_by_id.return_value = existing_job

    # Act
    process_bio_use_case.execute(job_id, player_data)

    # Assert
    mock_llm_service.generate_player_bio.assert_called_once()
    
    # Verify save was called with FAILED status
    saved_job = mock_bio_job_repository.save.call_args[0][0]
    assert saved_job.status == JobStatus.FAILED

def test_process_bio_repo_failure(process_bio_use_case, mock_bio_job_repository, mock_llm_service):
    # Arrange
    job_id = "job-123"
    player_data = PlayerResponseDTO(name="Player", position="P", hits=10, homeruns=1)
    
    mock_llm_service.generate_player_bio.return_value = "Bio"
    # First get_by_id fails or whatever logic triggers the outer exception handling
    # In the code, if generate_player_bio fails -> catch -> try save FAILED
    # If the first part succeeds, but save fails?
    
    # Let's clean up the test assumption.
    # The code logic:
    # try: 
    #   generate
    #   get job
    #   save completed
    # except:
    #   try:
    #     save failed
    
    # Case: generate success, save completed crashes
    mock_llm_service.generate_player_bio.return_value = "Bio"
    existing_job = BioGenerationJob(id=job_id, status=JobStatus.PENDING)
    mock_bio_job_repository.get_by_id.return_value = existing_job
    mock_bio_job_repository.save.side_effect = [Exception("DB Error"), None] # First save fails, second succeeds
    
    # Act
    process_bio_use_case.execute(job_id, player_data)
    
    # Assert
    # Should catch exception and try to save FAILED
    assert mock_bio_job_repository.save.call_count == 2
    failed_job = mock_bio_job_repository.save.call_args[0][0]
    assert failed_job.status == JobStatus.FAILED
