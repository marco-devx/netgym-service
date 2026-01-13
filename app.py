from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.infrastructure.config.databases import verify_connection
from src.infrastructure.config.settings import get_settings
from src.infrastructure.controllers import api_router
from src.infrastructure.exceptions import register_exception_handlers
from src.infrastructure.models import init_db


def create_app() -> FastAPI:
    settings = get_settings()
    debug_mode = settings.app_env == "development"

    api = FastAPI(
        title="NetGym API",
        description="NetGym API",
        version="1.0.0",
        debug=debug_mode,
    )

    api.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if debug_mode:
        init_db()
        verify_connection()

    api.include_router(api_router, prefix="/api")
    register_exception_handlers(api)

    return api


app = create_app()
