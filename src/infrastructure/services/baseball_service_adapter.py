from typing import List

import requests
from src.domain.entities.player import Player
from src.domain.ports.services import BaseballServicePort
from src.infrastructure.config.settings import get_settings
from src.shared.exceptions import BaseballAPIException


class BaseballServiceAdapter(BaseballServicePort):
    def _safe_int(self, value):
        if value == "--" or value is None:
            return 0
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0

    def _safe_float(self, value):
        if value == "--" or value is None:
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def get_players(self) -> List[Player]:
        settings = get_settings()
        url = settings.baseball_data_url
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
           
            raise BaseballAPIException(f"Failed to fetch baseball data: {str(e)}") from e
        
        data = response.json()
        players = []
        for item in data:
            players.append(
                Player(
                    name=item.get("Player name"),
        
                    position=item.get("position"),
                    games=self._safe_int(item.get("Games")),
                    at_bats=self._safe_int(item.get("At-bat")),
                    runs=self._safe_int(item.get("Runs")),
                    hits=self._safe_int(item.get("Hits")),
                    doubles=self._safe_int(item.get("Double (2B)")),
                    triples=self._safe_int(item.get("third baseman")),
                    homeruns=self._safe_int(item.get("home run")),
                    rbi=self._safe_int(item.get("run batted in")),
                    walks=self._safe_int(item.get("a walk")),
                    strikeouts=self._safe_int(item.get("Strikeouts")),
                    stolen_bases=self._safe_int(item.get("stolen base")),
                    caught_stealing=self._safe_int(item.get("Caught stealing")),
                    average=self._safe_float(item.get("AVG")),
                    obp=self._safe_float(item.get("On-base Percentage")),
                    slg=self._safe_float(item.get("Slugging Percentage")),
                    ops=self._safe_float(item.get("On-base Plus Slugging"))
                )
            )
        return players
