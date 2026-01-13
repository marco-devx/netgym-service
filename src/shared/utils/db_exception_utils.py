from __future__ import annotations

import re
from typing import Optional

from sqlalchemy.exc import DataError, IntegrityError, SQLAlchemyError

from src.shared.exceptions import (
    DatabaseException,
    DatabaseExceptionMsg,
    DBDataError,
    DBDataTooLongError,
    DBForeignKeyConstraintError,
    DBIntegrityError,
    DBInvalidNumericError,
    DBUniqueConstraintError,
)


def _extract_constraint_name(msg: str) -> Optional[str]:
    match = re.search(r"constraint '([^']+)'", msg)
    if match:
        return match.group(1)
    return None


def _extract_duplicate_value(msg: str) -> Optional[str]:
    match = re.search(r"The duplicate key value is \((.*?)\)", msg)
    if match:
        return match.group(1).strip()
    return None


def translate_sqlalchemy_error(
    e: SQLAlchemyError,
    entity: str | None = None,
    repository: str | None = None,
) -> DatabaseException:
    msg = str(getattr(e, "orig", e))
    details = {"raw_message": msg}

    if isinstance(e, IntegrityError):
        constraint_name = _extract_constraint_name(msg)

        if (
            "Violation of UNIQUE KEY constraint" in msg
            or "2627" in msg
            or "2601" in msg
        ):
            dup_value = _extract_duplicate_value(msg)
            return DBUniqueConstraintError(
                constraint_name=constraint_name,
                offending_value=dup_value,
                entity=entity,
                repository=repository,
                details=details,
            )

        if "547" in msg:
            return DBForeignKeyConstraintError(
                constraint_name=constraint_name,
                entity=entity,
                repository=repository,
                details=details,
            )

        return DBIntegrityError(
            message=DatabaseExceptionMsg.INTEGRITY,
            entity=entity,
            repository=repository,
            details=details,
        )

    if isinstance(e, DataError):
        if "8152" in msg or "2628" in msg:
            return DBDataTooLongError(
                entity=entity,
                repository=repository,
                details=details,
            )

        if "8115" in msg:
            return DBInvalidNumericError(
                entity=entity,
                repository=repository,
                details=details,
            )

        return DBDataError(
            message=DatabaseExceptionMsg.DATA_ERROR,
            entity=entity,
            repository=repository,
            details=details,
        )

    return DatabaseException(
        message=DatabaseExceptionMsg.DB_ERROR,
        entity=entity,
        repository=repository,
        details=details,
    )
