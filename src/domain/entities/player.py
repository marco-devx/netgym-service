from dataclasses import dataclass
from typing import Optional

@dataclass
class Player:
    name: str
    position: Optional[str] = None
    
    # Detailed Stats
    games: Optional[int] = None
    at_bats: Optional[int] = None
    runs: Optional[int] = None
    hits: Optional[int] = None
    doubles: Optional[int] = None
    triples: Optional[int] = None
    homeruns: Optional[int] = None
    rbi: Optional[int] = None
    walks: Optional[int] = None
    strikeouts: Optional[int] = None
    stolen_bases: Optional[int] = None
    caught_stealing: Optional[int] = None
    
    # Averages
    average: Optional[float] = None
    obp: Optional[float] = None
    slg: Optional[float] = None
    ops: Optional[float] = None
