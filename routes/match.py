from fastapi import APIRouter, Request
from db.models.team import Team
from db.models.team_statistics import TeamStatistics
from db.models.participant import Participant
from db.models.participant_statistics import ParticipantStatistics
from db.models.match import Match
from db.database import SessionLocal
from datetime import datetime
from sqlalchemy import text
import random

#DB
db = SessionLocal()

#Router
router = APIRouter()

@router.put("/begin-match")
async def beginMatch(req: Request):
    try:
        data = await req.json()
        
        query = text(f'SELECT * FROM team WHERE deleted_at IS NULL AND id IN ({data['team_1_id']},{data['team_2_id']})')
        result = db.execute(query)
        teams = result.mappings().all()

        if teams:
            team1 = teams[0]
            team2 = teams[1]

            # for t in teams:
            #     match = Match(
            #         data_hour=datetime.now(),
            #         match_team_statistics_id=t.team_statistics_id,
            #         created_at=datetime.now(),
            #         created_by='admin'
            #     )
                
            #     db.add(match)
            #     db.commit()
        else:
            return {'mensagem': 'Os times informados não existem'}
        
        players = {}
        
        for p in range(2):
            players[f'player_team_{p+1}'] = db.query(Participant).filter(Participant.deleted_at.is_(None)).filter_by(team_id=data[f'team_{p+1}_id']).all()
        
        all_players = players['player_team_1'] + players['player_team_2']

        scores: list = []

        def insertPoints(id: int,name: str, score: int):
            scores.append({"id": id, "name": name, "score": score})

        for p in all_players:
            insertPoints(p.id, p.nick, random.randint(60,100))

        return scores
    
    except ValueError as e:
        return {'mensagem': e}