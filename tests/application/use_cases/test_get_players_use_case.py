import pytest
from unittest.mock import MagicMock
from src.application.use_cases.get_players_use_case import GetPlayersUseCase
from src.domain.ports.services.baseball_service_port import BaseballServicePort
from src.domain.ports.repositories import PlayerRepository
from src.domain.entities.player import Player
from src.domain.value_objects.player_sort_criteria import PlayerSortCriteria
from src.application.dtos.player_response_dto import PlayerResponseDTO

@pytest.fixture
def mock_baseball_service():
    return MagicMock(spec=BaseballServicePort)

@pytest.fixture
def mock_player_repository():
    return MagicMock(spec=PlayerRepository)

@pytest.fixture
def get_players_use_case(mock_baseball_service, mock_player_repository):
    return GetPlayersUseCase(mock_baseball_service, mock_player_repository)

def test_get_players_no_sort_no_overrides(get_players_use_case, mock_baseball_service, mock_player_repository):
    # Arrange
    mock_players = [
        Player(name="Player A", position="P", hits=10, homeruns=1),
        Player(name="Player B", position="C", hits=20, homeruns=5)
    ]
    mock_baseball_service.get_players.return_value = mock_players
    mock_player_repository.get_all_overrides.return_value = []

    # Act
    result = get_players_use_case.execute()

    # Assert
    mock_baseball_service.get_players.assert_called_once()
    mock_player_repository.get_all_overrides.assert_called_once()
    assert len(result) == 2
    assert result[0].name == "Player A"
    assert result[0].hits == 10
    assert result[1].name == "Player B"
    assert result[1].hits == 20

def test_get_players_with_overrides(get_players_use_case, mock_baseball_service, mock_player_repository):
    # Arrange
    mock_players = [
        Player(name="Player A", position="P", hits=10, homeruns=1),
        Player(name="Player B", position="C", hits=20, homeruns=5)
    ]
    mock_baseball_service.get_players.return_value = mock_players
    
    # Override for Player A: hits changed to 99
    override_player = Player(name="Player A", position=None, hits=99, homeruns=None)
    mock_player_repository.get_all_overrides.return_value = [override_player]

    # Act
    result = get_players_use_case.execute()

    # Assert
    assert len(result) == 2
    # Player A should have overridden hits but original homeruns (since override is None logic handled in UC? 
    # Wait, in the UC current implementation check: "override_val = getattr(override, field)... if override_val is not None: setattr"
    # So yes, if override has None, it shouldn't overwrite original.
    
    assert result[0].name == "Player A"
    assert result[0].hits == 99  # Overridden
    assert result[0].homeruns == 1 # Original preserved
    
    assert result[1].name == "Player B"
    assert result[1].hits == 20

def test_get_players_sort_by_hits_with_overrides(get_players_use_case, mock_baseball_service, mock_player_repository):
    # Arrange
    mock_players = [
        Player(name="Player A", position="P", hits=10, homeruns=1),
        Player(name="Player B", position="C", hits=20, homeruns=2),
        Player(name="Player C", position="IF", hits=30, homeruns=3)
    ]
    mock_baseball_service.get_players.return_value = mock_players
    
    # Override Player A to have 100 hits, making it first
    override = Player(name="Player A", position=None, hits=100)
    mock_player_repository.get_all_overrides.return_value = [override]

    # Act
    result = get_players_use_case.execute(sort_by=PlayerSortCriteria.HITS)

    # Assert
    assert len(result) == 3
    assert result[0].name == "Player A"
    assert result[0].hits == 100
    assert result[1].name == "Player C"
    assert result[1].hits == 30
    assert result[2].name == "Player B"
    assert result[2].hits == 20
