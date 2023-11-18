#from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import players, leaderboard
from app.db import engine, metadata

metadata.create_all(engine)

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     db = await engine.connect()
#     yield
#     await db.disconnect()

app = FastAPI()

app.include_router(players.router)
app.include_router(leaderboard.router)