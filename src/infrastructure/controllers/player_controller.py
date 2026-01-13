from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from src.application.dtos import BaseResponseDTO, PlayerResponseDTO, PlayerRequestDTO
from src.application.use_cases import GetPlayersUseCase
from src.application.use_cases import UpdatePlayerUseCase
from src.infrastructure.services import BaseballServiceAdapter
from src.infrastructure.repositories import PlayerRepositoryAdapter

router = APIRouter(tags=["Players"])


def dep_get_players_uc() -> GetPlayersUseCase:
    return GetPlayersUseCase(
        baseball_service=BaseballServiceAdapter(),
        player_repository=PlayerRepositoryAdapter()
    )


def dep_update_player_uc() -> UpdatePlayerUseCase:
    return UpdatePlayerUseCase(
        player_repository=PlayerRepositoryAdapter(),
        baseball_service=BaseballServiceAdapter()
    )


@router.get(
    "/",
    response_model=BaseResponseDTO[List[PlayerResponseDTO]],
    status_code=status.HTTP_200_OK,
    summary="Get list of baseball players",
)
def get_players_json(
    sort_by: str | None = None,
    get_players_uc: GetPlayersUseCase = Depends(dep_get_players_uc),
):
    players = get_players_uc.execute(sort_by=sort_by)
    return BaseResponseDTO(
        success=True,
        message="Players retrieved successfully",
        status_code=status.HTTP_200_OK,
        data=players,
    )


@router.patch(
    "/{name}",
    response_model=BaseResponseDTO[PlayerResponseDTO],
    status_code=status.HTTP_200_OK,
    summary="Update player details",
)
def update_player(
    name: str,
    player_dto: PlayerRequestDTO,
    update_player_uc: UpdatePlayerUseCase = Depends(dep_update_player_uc),
):
    player_dto.name = name
    updated_player = update_player_uc.execute(player_dto)
    return BaseResponseDTO(
        success=True,
        message="Player updated successfully",
        status_code=status.HTTP_200_OK,
        data=updated_player,
    )
