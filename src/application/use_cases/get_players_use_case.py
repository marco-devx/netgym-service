from typing import List

from src.application.dtos import PlayerResponseDTO
from src.domain.entities.player import Player
from src.domain.ports.services import BaseballServicePort
from src.domain.value_objects import PlayerSortCriteria


class GetPlayersUseCase:
    def __init__(self, baseball_service: BaseballServicePort):
        self.baseball_service = baseball_service

    def execute(self, sort_by: PlayerSortCriteria | None = None) -> List[PlayerResponseDTO]:
        players = self.baseball_service.get_players()
        
        if sort_by:
            if sort_by == PlayerSortCriteria.HITS:
                players.sort(key=lambda x: x.hits or 0, reverse=True)
            elif sort_by == PlayerSortCriteria.HR:
                players.sort(key=lambda x: x.homeruns or 0, reverse=True)
                
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
            ) for p in players
        ]
