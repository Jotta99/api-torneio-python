from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base

class ParticipantType(Base):
    __tablename__ = "participant_type"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    created_at = Column(DateTime)
    created_by = Column(String)
    deleted_at = Column(DateTime)
    deleted_by = Column(String)
    updated_at = Column(DateTime)
    updated_by = Column(String)
