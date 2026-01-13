import pytest
from unittest.mock import MagicMock
from src.application.use_cases.get_players_use_case import GetPlayersUseCase
from src.domain.ports.services.baseball_service_port import BaseballServicePort
from src.domain.entities.player import Player
from src.domain.value_objects.player_sort_criteria import PlayerSortCriteria
from src.application.dtos.player_response_dto import PlayerResponseDTO

@pytest.fixture
def mock_baseball_service():
    return MagicMock(spec=BaseballServicePort)

@pytest.fixture
def get_players_use_case(mock_baseball_service):
    return GetPlayersUseCase(mock_baseball_service)

def test_get_players_no_sort(get_players_use_case, mock_baseball_service):
    # Arrange
    mock_players = [
        Player(name="Player A", position="P", hits=10, homeruns=1),
        Player(name="Player B", position="C", hits=20, homeruns=5)
    ]
    mock_baseball_service.get_players.return_value = mock_players

    # Act
    result = get_players_use_case.execute()

    # Assert
    mock_baseball_service.get_players.assert_called_once()
    assert len(result) == 2
    assert isinstance(result[0], PlayerResponseDTO)
    assert result[0].name == "Player A"
    assert result[1].name == "Player B"

def test_get_players_sort_by_hits(get_players_use_case, mock_baseball_service):
    # Arrange
    mock_players = [
        Player(name="Player A", position="P", hits=10, homeruns=1),
        Player(name="Player B", position="C", hits=30, homeruns=5),
        Player(name="Player C", position="IF", hits=20, homeruns=2)
    ]
    mock_baseball_service.get_players.return_value = mock_players

    # Act
    result = get_players_use_case.execute(sort_by=PlayerSortCriteria.HITS)

    # Assert
    assert len(result) == 3
    assert result[0].hits == 30
    assert result[1].hits == 20
    assert result[2].hits == 10

def test_get_players_sort_by_hr(get_players_use_case, mock_baseball_service):
    # Arrange
    mock_players = [
        Player(name="Player A", position="P", hits=10, homeruns=1),
        Player(name="Player B", position="C", hits=30, homeruns=5),
        Player(name="Player C", position="IF", hits=20, homeruns=10)
    ]
    mock_baseball_service.get_players.return_value = mock_players

    # Act
    result = get_players_use_case.execute(sort_by=PlayerSortCriteria.HR)

    # Assert
    assert len(result) == 3
    assert result[0].homeruns == 10
    assert result[1].homeruns == 5
    assert result[2].homeruns == 1
