from fastapi import APIRouter, Request
from db.models.participant import Participant
from db.models.participant_statistics import ParticipantStatistics
from db.database import SessionLocal
from sqlalchemy import text
from datetime import datetime

#DB
db = SessionLocal()

#Router
router = APIRouter()

@router.get("/get-all")
async def getParticipants():
    try:
        participants = db.query(Participant).filter(Participant.deleted_at.is_(None)).all()
        
        return participants
    except ValueError as e:
        return {'mensagem': e}

@router.get("/get-participant/{participant_id}")
async def getParticipant(participant_id: int):
    try:
        query = text(f'SELECT participant.id AS participant_id, participant.name AS participant_name, participant_statistics.wins AS total_wins, participant_statistics.losts AS total_losts, participant_statistics.total_score AS total_score, team.id AS team_id, team.name AS team_name, team_statistics.wins AS team_wins, team_statistics.losts AS team_losts, team_statistics.total_score AS team_total_score FROM participant LEFT JOIN team ON team.id = participant.team_id AND team.deleted_at IS NULL LEFT JOIN team_statistics ON team_statistics.id = team.team_statistics_id AND team_statistics.deleted_at IS NULL INNER JOIN participant_statistics ON participant_statistics.id = participant.participant_statistics_id AND participant_statistics.deleted_at IS NULL WHERE participant.deleted_at IS NULL AND participant.id = {participant_id}')
        result = db.execute(query)
        participant = result.mappings().all()
        
        return {"participant": participant[0]}
    except ValueError as e:
        return {'mensagem': e}     

@router.put("/new-participant")
async def newParticipant(req: Request):
    try:
        data = await req.json()

        def save(objSave: ParticipantStatistics | Participant):
            db.add(objSave)
            db.commit()
            db.refresh(objSave)

        statistic = ParticipantStatistics(
            wins=0,
            losts=0,
            total_score=0,
            created_at=datetime.now(),
            created_by='admin'
        )
        
        save(statistic)
            
        participant = Participant(
            name=data['name'],
            nick=data['nick'],
            age=data['age'],
            participant_type_id=data['participant_type_id'],
            participant_statistics_id=statistic.id,
            password=data['password'],
            created_at=datetime.now(),
            created_by='admin'
        )
            
        save(participant)
        
        return {"mensagem": f'O Participante {data['name']} foi salvo com sucesso'}
    except ValueError as e:
        return {'mensagem': e}        

@router.put("/delete-participant")
async def deleteParticipant(req: Request):
    try:
        data = await req.json()
        participant = db.query(Participant).filter(Participant.deleted_at.is_(None)).filter_by(id=data['id']).first()
        
        if participant:
            participant.deleted_at = datetime.now()
            participant.deleted_by = 'admin'

            db.commit()
            
            return {"mensagem": 'O Participante foi removido com sucesso'}   
        else:
            return {'mensagem': 'Participante não encontrado'}
  
    except ValueError as e:
        return {'mensagem': e}

@router.put("/join-team")
async def joinTeam(req: Request):
    try:
        data = await req.json()
        
        team = db.query(Participant).filter(Participant.deleted_at.is_(None)).filter_by(id=data['team_id']).first()

        if team:
            participant = db.query(Participant).filter(Participant.deleted_at.is_(None)).filter_by(id=data['participant_id']).first()
            
            if participant:
                participant.team_id = data['team_id']

                db.commit()
                
                statistic = db.query(ParticipantStatistics).filter(ParticipantStatistics.deleted_at.is_(None)).filter_by(id=participant.participant_statistics_id).first()
                
                if statistic:
                    statistic.team_id = data['team_id']

                    db.commit()

            else:
                return {'mensagem': 'Participante não encontrado'}
        else:
            return {'mensagem': 'Time não encontrado'}
  
        return {"mensagem": 'O Participante adicionado ao time!'}
    except ValueError as e:
        return {'mensagem': e}