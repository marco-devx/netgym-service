from abc import ABC, abstractmethod
from src.application.dtos.player_response_dto import PlayerResponseDTO

class LLMServicePort(ABC):
    @abstractmethod
    def generate_player_bio(self, player_data: PlayerResponseDTO) -> str:
        pass
