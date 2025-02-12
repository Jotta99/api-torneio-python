from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base

class MatchTeamStatistics(Base):
    __tablename__ = "match_team_statistics"
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer)
    team_id = Column(Integer)
    winner = Column(Integer)
    team_id = Column(Integer)
    score = Column(Integer)
    created_at = Column(DateTime)
    created_by = Column(String)
    deleted_at = Column(DateTime)
    deleted_by = Column(String)
    updated_at = Column(DateTime)
    updated_by = Column(String)
