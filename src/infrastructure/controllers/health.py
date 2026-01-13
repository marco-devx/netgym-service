import socket

from fastapi import APIRouter, status
from sqlalchemy.exc import OperationalError

from src.infrastructure.config.databases import verify_connection

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    try:
        verify_connection()
        return {"status": "ok", "database": "connected"}
    except (OperationalError, socket.gaierror, ConnectionError) as e:
        return {"status": "error", "database": "unreachable", "details": str(e)}
