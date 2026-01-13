from typing import Optional

from pydantic import BaseModel


class PlayerResponseDTO(BaseModel):
    name: str
    position: str
    hits: int
    homeruns: int
    average: Optional[float] = 0.0
    
    # Detailed Stats (Optional for list view, but user requested comprehensive mapping)
    games: Optional[int] = 0
    at_bats: Optional[int] = 0
    runs: Optional[int] = 0
    doubles: Optional[int] = 0
    triples: Optional[int] = 0
    rbi: Optional[int] = 0
    walks: Optional[int] = 0
    strikeouts: Optional[int] = 0
    stolen_bases: Optional[int] = 0
    caught_stealing: Optional[int] = 0
    obp: Optional[float] = 0.0
    slg: Optional[float] = 0.0
    ops: Optional[float] = 0.0
