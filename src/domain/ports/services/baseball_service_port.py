from abc import ABC, abstractmethod
from typing import List

from src.domain.entities.player import Player


class BaseballServicePort(ABC):
    @abstractmethod
    def get_players(self) -> List[Player]:
        """Fetches a list of baseball players from the external source."""
        pass
