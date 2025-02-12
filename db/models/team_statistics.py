from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base

class TeamStatistics(Base):
    __tablename__ = "team_statistics"
    id = Column(Integer, primary_key=True, index=True)
    wins = Column(Integer)
    losts = Column(Integer)
    total_score = Column(Integer)
    created_at = Column(DateTime)
    created_by = Column(String)
    deleted_at = Column(DateTime)
    deleted_by = Column(String)
    updated_at = Column(DateTime)
    updated_by = Column(String)