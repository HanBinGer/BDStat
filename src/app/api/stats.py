from app.api.crud import *
from app.api.models import *
from fastapi import APIRouter, HTTPException
from typing import List


router = APIRouter()

@router.post("/players/")
async def create_player_api(player_create: PlayerCreate):
    result = await create_player(player_create=player_create)
    print(result)
    return result

@router.post("/players/{steamid64}/sessions/")
async def create_game_session_api(game_session_create: GameSessionCreate, sessions_weapon_create: List[SessionWeaponCreate]):
    print(type(sessions_weapon_create))
    player = await get_player(steamid64=game_session_create.player_id)
    if player:
        return await create_game_session(game_session_create=game_session_create, sessions_weapon_create=sessions_weapon_create)
    raise HTTPException(status_code=404, detail="Player not found")

# @router.post("/sessions/{session_id}/weapons/")
# async def create_session_weapon_api(session_weapon_create: SessionWeaponCreate):
#     return await create_session_weapon(session_weapon_create=session_weapon_create)

@router.get("/players/{steamid64}/sessions")
async def read_all_sessions_api(steamid64: int):
    player = await get_player(steamid64=steamid64)
    if player:
        return await get_all_sessions(player_id=steamid64)
    raise HTTPException(status_code=404, detail="Player not found")

@router.get("/players/{steamid64}")
async def read_player_api(steamid64: int):
    player = await get_player(steamid64=steamid64)
    if player:
        return player
    raise HTTPException(status_code=404, detail="Player not found")
