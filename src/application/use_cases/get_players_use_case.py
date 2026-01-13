from typing import List

from src.application.dtos import PlayerResponseDTO
from src.domain.entities.player import Player
from src.domain.ports.repositories import PlayerRepository
from src.domain.ports.services import BaseballServicePort
from src.domain.value_objects import PlayerSortCriteria


class GetPlayersUseCase:
    def __init__(self, baseball_service: BaseballServicePort, player_repository: PlayerRepository):
        self.baseball_service = baseball_service
        self.player_repository = player_repository

    def execute(self, sort_by: PlayerSortCriteria | None = None) -> List[PlayerResponseDTO]:
        # Fetch from API
        api_players = self.baseball_service.get_players()
        
        # Fetch overrides
        overrides = self.player_repository.get_all_overrides()
        overrides_map = {p.name: p for p in overrides}
        
        # Merge logic
        merged_players = []
        for player in api_players:
            if player.name in overrides_map:
                override = overrides_map[player.name]
                # Update fields if they are not None in override
                # Since we want to merge, we check each field. 
                # However, the override model allows nulls, but our Save logic saves the whole object.
                # Assuming the frontend sends the complete object on edit, the override will contain values for all fields.
                # If we only want to support partial edits in the future, we'd need to check each field.
                # For now, let's assume the override takes precedence if it exists.
                # Or wait, let's be safer and merge field by field if needed, but for now full replacement on match seems correct if the edit form is full validation.
                # Actually, let's implement a merge helper to be safe.
                player = self._merge_player(player, override)
            merged_players.append(player)
            
        if sort_by:
            if sort_by == PlayerSortCriteria.HITS:
                merged_players.sort(key=lambda x: x.hits or 0, reverse=True)
            elif sort_by == PlayerSortCriteria.HR:
                merged_players.sort(key=lambda x: x.homeruns or 0, reverse=True)
                
        return [
            PlayerResponseDTO(
                name=p.name,
                position=p.position,
                hits=p.hits,
                homeruns=p.homeruns,
                average=p.average,
                games=p.games,
                at_bats=p.at_bats,
                runs=p.runs,
                doubles=p.doubles,
                triples=p.triples,
                rbi=p.rbi,
                walks=p.walks,
                strikeouts=p.strikeouts,
                stolen_bases=p.stolen_bases,
                caught_stealing=p.caught_stealing,
                obp=p.obp,
                slg=p.slg,
                ops=p.ops
            ) for p in merged_players
        ]

    def _merge_player(self, original: Player, override: Player) -> Player:
        """Merge override values into original player."""
        # We iterate through the dataclass fields
        for field in original.__dataclass_fields__:
            if field == 'name': continue # PK
            
            override_val = getattr(override, field)
            if override_val is not None:
                setattr(original, field, override_val)
        return original
