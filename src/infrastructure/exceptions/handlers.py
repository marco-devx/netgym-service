from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.shared.exceptions import (
    BaseballAPIException,
    DatabaseException,
    DBUniqueConstraintError,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def handle_request_validation_exception(
        _request: Request, exc: RequestValidationError
    ):
        first_error = exc.errors()[0] if exc.errors() else {}
        detail_msg = first_error.get("msg", "Validation error")

        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "message": "Validation error",
                "status_code": 422,
                "data": None,
                "errors": {
                    "detail": detail_msg,
                    "input": first_error.get("input"),
                    "loc": first_error.get("loc"),
                },
            },
        )

    exception_map = [
        (BaseballAPIException, 503, "External Service Error"),
        (DBUniqueConstraintError, 409, "Resource already exists"),
        (DatabaseException, 500, "Internal Database Error"),
    ]

    def _make_handler(http_status: int, message: str):
        async def handler(_request: Request, exc: Exception):
            return JSONResponse(
                status_code=http_status,
                content={
                    "success": False,
                    "message": message,
                    "status_code": http_status,
                    "data": None,
                    "errors": {
                        "detail": str(exc),
                    },
                },
            )

        return handler

    for exc_cls, status_code, generic_message in exception_map:
        app.exception_handler(exc_cls)(
            _make_handler(http_status=status_code, message=generic_message)
        )


def handle_db_exception(e: Exception, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": message,
            "status_code": 500,
            "data": None,
            "errors": {
                "detail": str(e),
            },
        },
    )