from sqlmodel import SQLModel
from src.infrastructure.config.databases.db_config import engine
from src.infrastructure.config.databases.base import Base

from .bio_job_model import BioJobModel
from .player_model import PlayerModel

def init_db() -> None:
    SQLModel.metadata.create_all(engine)
    Base.metadata.create_all(engine)
