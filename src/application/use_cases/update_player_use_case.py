from src.application.dtos import PlayerResponseDTO, PlayerRequestDTO
from src.domain.entities import Player
from src.domain.ports.repositories import PlayerRepository
from src.domain.ports.services import BaseballServicePort


class UpdatePlayerUseCase:
    def __init__(self, player_repository: PlayerRepository, baseball_service: BaseballServicePort):
        self.player_repository = player_repository
        self.baseball_service = baseball_service

    def execute(self, player_dto: PlayerRequestDTO) -> PlayerResponseDTO:
        # 1. Fetch existing override
        existing_override = self.player_repository.get_override_by_name(player_dto.name)
        
        # 2. Prepare new values, starting with existing or empty
        if existing_override:
            # Update existing values using non-None fields from DTO
            updated_data = {
                field: getattr(existing_override, field) 
                for field in existing_override.__dataclass_fields__
            }
        else:
            # New override, initialize all to None/default structure
            updated_data = {
                field: None
                for field in Player.__dataclass_fields__
            }
            updated_data['name'] = player_dto.name # PK must be set

        # 3. Apply updates from DTO
        for field in player_dto.model_fields:
            if field == 'name': continue
            value = getattr(player_dto, field)
            if value is not None:
                updated_data[field] = value
                
        # 4. Create Entity and Save
        player_override = Player(**updated_data)
        saved_override = self.player_repository.save(player_override)
        
        # 5. Fetch all players from API to augment the response
        # In a real scenario, we might want a get_by_id on the service, but here we scan.
        api_players = self.baseball_service.get_players()
        target_player = next((p for p in api_players if p.name == player_dto.name), None)
        
        if target_player:
            # Merge logic: applies override to api_player
            final_player = self._merge_player(target_player, saved_override)
        else:
            # If not found in API, return the override as is (might fail validation if fields are missing)
            # But based on requirements, we assume API is source of truth.
            final_player = saved_override

        # 6. Return as DTO
        return PlayerResponseDTO(
            name=final_player.name,
            position=final_player.position,
            hits=final_player.hits,
            homeruns=final_player.homeruns,
            average=final_player.average,
            games=final_player.games,
            at_bats=final_player.at_bats,
            runs=final_player.runs,
            doubles=final_player.doubles,
            triples=final_player.triples,
            rbi=final_player.rbi,
            walks=final_player.walks,
            strikeouts=final_player.strikeouts,
            stolen_bases=final_player.stolen_bases,
            caught_stealing=final_player.caught_stealing,
            obp=final_player.obp,
            slg=final_player.slg,
            ops=final_player.ops
        )

    def _merge_player(self, original: Player, override: Player) -> Player:
        """Merge override values into original player."""
        for field in original.__dataclass_fields__:
            if field == 'name': continue
            
            override_val = getattr(override, field)
            if override_val is not None:
                setattr(original, field, override_val)
        return original
