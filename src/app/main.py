from fastapi import FastAPI


from app.api import leaderboard, players, security
from app.db import engine, metadata


metadata.create_all(engine)

app = FastAPI()

app.include_router(security.router)
app.include_router(players.router)
app.include_router(leaderboard.router)