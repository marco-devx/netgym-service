import socket

from sqlalchemy import text
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from ...logging import get_logger
from ..settings import get_settings
from .db_config import engine

logger = get_logger()
settings = get_settings()


def verify_connection():
    db_host = settings.db_host
    db_port = settings.db_port

    context = {"host": db_host, "port": db_port}

    logger.info("Starting database connection verification...", context=context)

    try:
        ip = socket.gethostbyname(db_host)
        logger.info(f"DNS resolved: {db_host} → {ip}", context={**context, "ip": ip})
    except socket.gaierror as e:
        logger.error(f"DNS resolution error for {db_host}: {e}", context=context)

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful", context=context)
    except OperationalError as e:
        logger.error(f"Connection error (OperationalError): {e}", context=context)
    except SQLAlchemyError as e:
        logger.error(f"Unexpected SQLAlchemy error: {e}", context=context)
