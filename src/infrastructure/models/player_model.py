from typing import Optional

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.models.base_model import BaseModel


class PlayerModel(BaseModel):
    __tablename__ = "players"

    name: Mapped[str] = mapped_column(String, primary_key=True)
    position: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Detailed Stats
    games: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    at_bats: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    runs: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    hits: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    doubles: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    triples: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    homeruns: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    rbi: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    walks: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    strikeouts: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    stolen_bases: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    caught_stealing: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Averages
    average: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    obp: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    slg: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ops: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
