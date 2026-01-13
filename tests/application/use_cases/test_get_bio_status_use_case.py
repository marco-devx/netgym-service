import pytest
from unittest.mock import MagicMock
from src.application.use_cases.get_bio_status_use_case import GetBioStatusUseCase
from src.domain.ports.repositories.bio_job_repository import BioJobRepository
from src.domain.entities.bio_generation_job import BioGenerationJob
from src.domain.value_objects.job_status import JobStatus

@pytest.fixture
def mock_bio_job_repository():
    return MagicMock(spec=BioJobRepository)

@pytest.fixture
def get_bio_status_use_case(mock_bio_job_repository):
    return GetBioStatusUseCase(mock_bio_job_repository)

def test_get_bio_status_found(get_bio_status_use_case, mock_bio_job_repository):
    # Arrange
    job_id = "job-123"
    expected_job = BioGenerationJob(id=job_id, status=JobStatus.COMPLETED, result="Bio content", player_name="Test")
    mock_bio_job_repository.get_by_id.return_value = expected_job

    # Act
    result = get_bio_status_use_case.execute(job_id)

    # Assert
    mock_bio_job_repository.get_by_id.assert_called_once_with(job_id)
    assert result == expected_job
    assert result.status == JobStatus.COMPLETED

def test_get_bio_status_not_found(get_bio_status_use_case, mock_bio_job_repository):
    # Arrange
    job_id = "job-404"
    mock_bio_job_repository.get_by_id.return_value = None

    # Act
    result = get_bio_status_use_case.execute(job_id)

    # Assert
    mock_bio_job_repository.get_by_id.assert_called_once_with(job_id)
    assert result is None
