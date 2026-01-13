from functools import lru_cache

from .standar_logger import StandardLogger


@lru_cache(maxsize=1)
def get_logger() -> StandardLogger:
    return StandardLogger()
