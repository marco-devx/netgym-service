from typing import Any, Dict, Optional


class DatabaseExceptionMsg:
    DB_ERROR = "Database Error"
    INTEGRITY = "Integrity Error"
    DATA_ERROR = "Data Error"
    DATA_TOO_LONG = "Data too long"
    INVALID_NUMERIC = "Invalid numeric value"
    FOREIGN_KEY = "Foreign key violation"
    UNIQUE_CONSTRAINT = "Unique constraint violation"
    FOREIGN_KEY_CONSTRAINT = "Foreign key constraint violation"


class DatabaseException(Exception):
    def __init__(
        self,
        message: str = DatabaseExceptionMsg.DB_ERROR,
        entity: Optional[str] = None,
        repository: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        self.entity = entity
        self.repository = repository
        self.details = details or {}

        super().__init__(message)


class DBIntegrityError(DatabaseException):
    def __init__(
        self,
        message: str = DatabaseExceptionMsg.INTEGRITY,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, **kwargs)


class DBUniqueConstraintError(DBIntegrityError):
    def __init__(
        self,
        message: str = DatabaseExceptionMsg.UNIQUE_CONSTRAINT,
        constraint_name: Optional[str] = None,
        offending_value: Any = None,
        **kwargs: Any,
    ) -> None:
        self.constraint_name = constraint_name
        self.offending_value = offending_value
        super().__init__(message, **kwargs)


class DBForeignKeyConstraintError(DBIntegrityError):
    def __init__(
        self,
        message: str = DatabaseExceptionMsg.FOREIGN_KEY_CONSTRAINT,
        constraint_name: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.constraint_name = constraint_name
        super().__init__(message, **kwargs)


class DBDataError(DatabaseException):
    def __init__(
        self,
        message: str = DatabaseExceptionMsg.DATA_ERROR,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, **kwargs)


class DBDataTooLongError(DBDataError):
    def __init__(
        self,
        message: str = DatabaseExceptionMsg.DATA_TOO_LONG,
        column: Optional[str] = None,
        max_length: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        self.column = column
        self.max_length = max_length
        super().__init__(message, **kwargs)


class DBInvalidNumericError(DBDataError):
    def __init__(
        self,
        message: str = DatabaseExceptionMsg.INVALID_NUMERIC,
        column: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.column = column
        super().__init__(message, **kwargs)