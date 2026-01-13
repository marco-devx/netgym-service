import pytest
from unittest.mock import MagicMock
from src.application.use_cases.update_player_use_case import UpdatePlayerUseCase
from src.domain.ports.repositories import PlayerRepository
from src.domain.ports.services.baseball_service_port import BaseballServicePort
from src.domain.entities.player import Player
from src.application.dtos.player_response_dto import PlayerRequestDTO

@pytest.fixture
def mock_player_repository():
    return MagicMock(spec=PlayerRepository)

@pytest.fixture
def mock_baseball_service():
    return MagicMock(spec=BaseballServicePort)

@pytest.fixture
def update_player_use_case(mock_player_repository, mock_baseball_service):
    return UpdatePlayerUseCase(mock_player_repository, mock_baseball_service)

def test_update_player_new_override(update_player_use_case, mock_player_repository, mock_baseball_service):
    # Arrange
    dto = PlayerRequestDTO(name="Player A", hits=50)
    
    # No existing override
    mock_player_repository.get_override_by_name.return_value = None
    
    # Mock save to return the object
    def save_side_effect(player):
        return player
    mock_player_repository.save.side_effect = save_side_effect
    
    # Mock API return
    mock_api_player = Player(name="Player A", position="P", hits=10, homeruns=1, games=5)
    mock_baseball_service.get_players.return_value = [mock_api_player]

    # Act
    result = update_player_use_case.execute(dto)

    # Assert
    # Verify repository calls
    mock_player_repository.get_override_by_name.assert_called_with("Player A")
    
    # Verify save called with correct merged data (None for unspecified fields, 50 for hits)
    # The UC creates defaults as None, sets name=Player A, then updates hits=50
    mock_player_repository.save.assert_called_once()
    saved_arg = mock_player_repository.save.call_args[0][0]
    assert saved_arg.name == "Player A"
    assert saved_arg.hits == 50
    assert saved_arg.position is None
    
    # Verify result is merged with API data
    assert result.name == "Player A"
    assert result.hits == 50   # From override
    assert result.homeruns == 1 # From API
    assert result.games == 5    # From API

def test_update_player_existing_override(update_player_use_case, mock_player_repository, mock_baseball_service):
    # Arrange
    dto = PlayerRequestDTO(name="Player A", homeruns=20)
    
    # Existing override has hits=50
    existing_override = Player(name="Player A", position=None, hits=50, homeruns=1)
    mock_player_repository.get_override_by_name.return_value = existing_override
    
    mock_player_repository.save.side_effect = lambda p: p
    
    mock_api_player = Player(name="Player A", position="P", hits=10, homeruns=1, games=5)
    mock_baseball_service.get_players.return_value = [mock_api_player]

    # Act
    result = update_player_use_case.execute(dto)

    # Assert
    mock_player_repository.save.assert_called_once()
    saved_arg = mock_player_repository.save.call_args[0][0]
    
    assert saved_arg.hits == 50     # Preserved from existing override
    assert saved_arg.homeruns == 20 # Updated from DTO
    
    # Result should reflect merged state (API + Existing Override + New Update)
    assert result.hits == 50
    assert result.homeruns == 20
    assert result.games == 5

def test_update_player_not_found_in_api(update_player_use_case, mock_player_repository, mock_baseball_service):
    # Should handle gracefully if not in API (return override data)
    # Arrange
    dto = PlayerRequestDTO(name="Unknown", hits=100, position="P", homeruns=10)
    mock_player_repository.get_override_by_name.return_value = None
    mock_player_repository.save.side_effect = lambda p: p
    mock_baseball_service.get_players.return_value = [] # Empty API

    # Act
    result = update_player_use_case.execute(dto)

    # Assert
    assert result.name == "Unknown"
    assert result.hits == 100
    # Other fields default (0.0 or 0 from DTO/Entity defaults if any, likely None or 0)
    # The PlayerResponseDTO defaults are 0/0.0
