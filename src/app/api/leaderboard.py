from fastapi import APIRouter, HTTPException

from app.api.crud import *
from app.api.models import *

router = APIRouter(prefix="/leaderboard")

@router.get("/winrate")
async def read_top_winrate(count: int = 100) -> list[PlayerScheme]:
    return await get_top_winrate(count=count)

@router.get("/kd")
async def read_top_kd(count: int = 100) -> list[PlayerScheme]:
    return await get_top_kd(count=count)

@router.get("/kills")
async def read_top_kills(count: int = 100) -> list[PlayerScheme]:
    return await get_top_kills(count=count)

@router.get("/wins")
async def read_top_wins(count: int = 100) -> list[PlayerScheme]:
    return await get_top_wins(count=count)

@router.get("/battles")
async def read_top_battles(count: int = 100) -> list[PlayerScheme]:
    return await get_top_battles(count=count)