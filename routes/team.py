from fastapi import APIRouter, Request
from db.models.team import Team
from db.models.team_statistics import TeamStatistics
from db.models.participant import Participant
from db.database import SessionLocal
from datetime import datetime

#DB
db = SessionLocal()

#Router
router = APIRouter()

@router.get("/get-all")
async def getTeams():
    try:
        teams = db.query(Team).all()
        
        return teams
    except ValueError as e:
        return {'mensagem': e}

@router.put("/new-team")
async def newTeam(req: Request):
    try:
        data = await req.json()
        
        def save(objSave: TeamStatistics | Team):
            db.add(objSave)
            db.commit()
            db.refresh(objSave)

        statistic = TeamStatistics(
            wins=0,
            losts=0,
            total_score=0,
            created_at=datetime.now(),
            created_by='admin'
        )
        
        save(statistic)
            
        team = Team(
            name=data['name'],
            team_statistics_id=statistic.id,
            created_at=datetime.now(),
            created_by='admin'
        )
            
        save(team)

        return {"mensagem": f'O Time {data['name']} foi criado com sucesso'}
    except ValueError as e:
        return {'mensagem': e}
    
@router.put("/delete-team")
async def deleteTeam(req: Request):
    try:
        data = await req.json()
        team = db.query(Team).filter(Team.deleted_at.is_(None)).filter_by(id=data['id']).first()
        
        if team:
            team.deleted_at = datetime.now()
            team.deleted_by = 'admin'

            db.commit()
            
            participantsTeam = db.query(Participant).filter(Participant.deleted_at.is_(None)).filter_by(team_id=data['id']).all()
        
            if participantsTeam:
                for p in participantsTeam:
                    participant = db.query(Participant).filter(Participant.deleted_at.is_(None)).filter_by(id=p.id).first()
                if participant:
                    participant.team_id = None
                    db.commit()        
            
            return {"mensagem": 'O Time foi removido com sucesso'}   
        else:
            return {'mensagem': 'Time não encontrado'}
  
    except ValueError as e:
        return {'mensagem': e}
