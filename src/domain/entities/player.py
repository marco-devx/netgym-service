from dataclasses import dataclass
from typing import Optional

@dataclass
class Player:
    name: str
    position: str
    
    # Detailed Stats
    games: Optional[int] = 0
    at_bats: Optional[int] = 0
    runs: Optional[int] = 0
    hits: Optional[int] = 0
    doubles: Optional[int] = 0
    triples: Optional[int] = 0
    homeruns: Optional[int] = 0
    rbi: Optional[int] = 0
    walks: Optional[int] = 0
    strikeouts: Optional[int] = 0
    stolen_bases: Optional[int] = 0
    caught_stealing: Optional[int] = 0
    
    # Averages
    average: Optional[float] = 0.0
    obp: Optional[float] = 0.0
    slg: Optional[float] = 0.0
    ops: Optional[float] = 0.0
