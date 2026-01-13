from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.config.databases.base import Base


class BaseModel(Base):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.sysutcdatetime()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=func.sysutcdatetime()
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
