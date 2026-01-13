import pytest
from unittest.mock import MagicMock, ANY
from src.application.use_cases.generate_bio_use_case import GenerateBioUseCase
from src.domain.ports.repositories.bio_job_repository import BioJobRepository
from src.domain.ports.services.llm_service_port import LLMServicePort
from src.application.dtos.player_response_dto import PlayerResponseDTO
from src.domain.value_objects.job_status import JobStatus
from src.domain.entities.bio_generation_job import BioGenerationJob

@pytest.fixture
def mock_bio_job_repository():
    return MagicMock(spec=BioJobRepository)

@pytest.fixture
def mock_llm_service():
    return MagicMock(spec=LLMServicePort)

@pytest.fixture
def generate_bio_use_case(mock_bio_job_repository, mock_llm_service):
    return GenerateBioUseCase(mock_bio_job_repository, mock_llm_service)

def test_generate_bio_creates_job(generate_bio_use_case, mock_bio_job_repository):
    # Arrange
    player_dto = PlayerResponseDTO(
        name="Test Player",
        position="P",
        hits=0,
        homeruns=0
    )

    # Act
    job_id = generate_bio_use_case.execute(player_dto)

    # Assert
    assert job_id is not None
    mock_bio_job_repository.save.assert_called_once()
    
    # Check that called with correct job arguments
    saved_job = mock_bio_job_repository.save.call_args[0][0]
    assert isinstance(saved_job, BioGenerationJob)
    assert saved_job.id == job_id
    assert saved_job.status == JobStatus.PENDING
    assert saved_job.player_name == "Test Player"
