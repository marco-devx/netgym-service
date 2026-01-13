from fastapi import APIRouter

from .health import router as health_router
from .player_controller import router as player_router
from .bio_controller import router as bio_router


api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(player_router, prefix="/players")
api_router.include_router(bio_router, prefix="/players/bio")

api_router_admin = APIRouter()
