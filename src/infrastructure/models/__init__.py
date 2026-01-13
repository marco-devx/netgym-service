from sqlmodel import SQLModel
from src.infrastructure.config.databases.db_config import engine
from src.infrastructure.config.databases.base import Base
# Ensure model is registered
from src.infrastructure.models.bio_job_model import BioJobModel

def init_db() -> None:
    SQLModel.metadata.create_all(engine)
    Base.metadata.create_all(engine)



def init_db() -> None:
    SQLModel.metadata.create_all(engine)
