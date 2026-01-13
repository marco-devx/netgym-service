from sqlalchemy import Column, String, Text, Enum as SAEnum
from src.infrastructure.config.databases.base import Base
from src.domain.value_objects.job_status import JobStatus

class BioJobModel(Base):
    __tablename__ = "bio_generation_jobs"

    id = Column(String, primary_key=True, index=True)
    status = Column(SAEnum(JobStatus), default=JobStatus.PENDING)
    result = Column(Text, nullable=True)
    player_name = Column(String, nullable=True)
