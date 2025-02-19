from fastapi import FastAPI
app = FastAPI()

# Config Routes
from routes.team import router as team_routes
from routes.participant import router as participants
from routes.match import router as match

app.include_router(team_routes, prefix="/teams", tags=["Teams"])
app.include_router(participants, prefix="/participants", tags=["Participants"])
app.include_router(match, prefix="/match", tags=["Match"])

@app.get("/")
async def helloWorld():
    return 'Hello World!'