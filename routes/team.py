from fastapi import APIRouter, Request
from db.models.team import Team
from db.models.team_statistics import TeamStatistics
from db.database import SessionLocal
from datetime import datetime

#DB
db = SessionLocal()

#Router
router = APIRouter()

@router.get("/get-all-teams")
async def getTeams():
    try:
        teams = db.query(Team).all()
        db.close()
        
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
            db.close()

        statistic = TeamStatistics(
            wins=0,
            losts=0,
            total_score=0,
            created_at=datetime.now(),
            created_by='user_administrator'
        )
        
        save(statistic)
            
        team = Team(
            name=data['name'],
            team_statistics_id=statistic.id,
            created_at=datetime.now(),
            created_by='user_administrator'
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
        
        if Team:
            team.deleted_at = datetime.now()
            team.deleted_by = 'user_administrator'

            db.commit()
            db.close()
            
            return {"mensagem": 'O Time foi removido com sucesso'}   
        else:
            return {'mensagem': 'Time não encontrado'}
  
    except ValueError as e:
        return {'mensagem': e}

