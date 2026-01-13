import logging
from typing import Optional

from src.domain.ports.services.logger_port import LoggerPort


class StandardLogger(LoggerPort):
    _instance = None
    logger: Optional[logging.Logger] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StandardLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialize_logger()
        self._initialized = True

    def _initialize_logger(self):
        self.logger = logging.getLogger("ApplicationLogger")
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s - context: %(context)s"
        )
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def info(self, message: str, context: Optional[dict] = None) -> None:
        self.logger.info(message, extra={"context": context or {}})

    def warning(self, message: str, context: Optional[dict] = None) -> None:
        self.logger.warning(message, extra={"context": context or {}})

    def error(self, message: str, context: Optional[dict] = None) -> None:
        self.logger.error(message, extra={"context": context or {}})

    def debug(self, message: str, context: Optional[dict] = None) -> None:
        self.logger.debug(message, extra={"context": context or {}})
