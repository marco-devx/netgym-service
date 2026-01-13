from fastapi import APIRouter, Depends, status
from typing import List

from src.application.dtos import BaseResponseDTO, PlayerResponseDTO
from src.application.use_cases import GetPlayersUseCase
from src.infrastructure.services import BaseballServiceAdapter

router = APIRouter(tags=["Players"])


def dep_get_players_uc() -> GetPlayersUseCase:
    return GetPlayersUseCase(baseball_service=BaseballServiceAdapter())


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
