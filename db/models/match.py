from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base

class Match(Base):
    __tablename__ = "match"
    id = Column(Integer, primary_key=True, index=True)
    data_hour = Column(DateTime)
    match_team_statistics_id = Column(Integer)
    created_at = Column(DateTime)
    created_by = Column(String)
    deleted_at = Column(DateTime)
    deleted_by = Column(String)
    updated_at = Column(DateTime)
    updated_by = Column(String)
