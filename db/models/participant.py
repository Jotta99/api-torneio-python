from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base

class Participant(Base):
    __tablename__ = "participant"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    nick = Column(String)
    participant_type_id = Column(Integer)
    age = Column(Integer)
    password = Column(String)
    team_id = Column(Integer)
    participant_statistics_id = Column(Integer)
    created_at = Column(DateTime)
    created_by = Column(String)
    deleted_at = Column(DateTime)
    deleted_by = Column(String)
    updated_at = Column(DateTime)
    updated_by = Column(String)
