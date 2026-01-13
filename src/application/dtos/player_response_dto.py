from typing import Optional

from pydantic import BaseModel


class PlayerResponseDTO(BaseModel):
    name: str
    position: str
    hits: int
    homeruns: int
    average: Optional[float] = 0.0
    
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

class PlayerRequestDTO(BaseModel):
    name: Optional[str] = None
    position: Optional[str] = None
    hits: Optional[int] = None
    homeruns: Optional[int] = None
    average: Optional[float] = None
    games: Optional[int] = None
    at_bats: Optional[int] = None
    runs: Optional[int] = None
    doubles: Optional[int] = None
    triples: Optional[int] = None
    rbi: Optional[int] = None
    walks: Optional[int] = None
    strikeouts: Optional[int] = None
    stolen_bases: Optional[int] = None
    caught_stealing: Optional[int] = None
    obp: Optional[float] = None
    slg: Optional[float] = None
    ops: Optional[float] = None