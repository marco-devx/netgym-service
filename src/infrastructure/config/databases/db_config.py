from ..settings import Settings
from . import postgresql as db

settings = Settings()
database_url = db.database_url
engine = db.engine
SessionLocal = db.SessionLocal


def get_db_session():
    db_session = SessionLocal()
    try:
        yield db_session
        db_session.commit()
    except Exception:  # noqa: BLE001
        db_session.rollback()
        raise
    finally:
        db_session.close()
