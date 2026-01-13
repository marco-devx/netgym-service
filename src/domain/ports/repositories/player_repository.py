from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities import Player


class PlayerRepository(ABC):
    @abstractmethod
    def save(self, player_override: Player) -> Player:
        """Save a player override."""
        pass

    @abstractmethod
    def get_all_overrides(self) -> List[Player]:
        """Get all player overrides."""
        pass

    @abstractmethod
    def get_override_by_name(self, name: str) -> Optional[Player]:
        """Get a specific player override by name."""
        pass
