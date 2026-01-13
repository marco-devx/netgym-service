from abc import ABC, abstractmethod
from typing import Literal, Optional

logLevel = Literal["info", "warning", "error", "debug"]


class LoggerPort(ABC):
    @abstractmethod
    def info(self, message: str, context: Optional[dict] = None) -> None:
        """
        Logs a message at the INFO level.
        :param message: The main log message to record.
        :param context: Optional contextual data (e.g., tenant, operation, user_id).
        :return: None
        """

    @abstractmethod
    def warning(self, message: str, context: Optional[dict] = None) -> None:
        """
        Logs a message at the WARNING level.
        :param message: The warning message to log.
        :param context: Optional metadata relevant to the warning context.
        :return: None
        """

    @abstractmethod
    def error(self, message: str, context: Optional[dict] = None) -> None:
        """
        Logs a message at the ERROR level.
        :param message: A description of the error or failure.
        :param context: Optional data such as stack traces or exception info.
        :return: None
        """

    @abstractmethod
    def debug(self, message: str, context: Optional[dict] = None) -> None:
        """
        Logs a message at the DEBUG level.
        :param message: A message useful for debugging (e.g., internal state).
        :param context: Optional additional context for tracing behavior.
        :return: None
        """
