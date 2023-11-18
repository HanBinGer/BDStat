from typing import List

from fastapi import APIRouter, HTTPException

from app.api.crud import *
from app.api.models import *

router = APIRouter(prefix="/players")

@router.post("/")
async def create_player_api(player_create: PlayerCreate):
    result = create_player(player_create=player_create)
    return result

@router.post("/{steamid64}/sessions/")
async def create_game_session_api(game_session_create: GameSessionCreate, sessions_weapon_create: List[SessionWeaponCreate]):
    player = await get_player(steamid64=game_session_create.player_id)
    if player:
        return await create_game_session(game_session_create=game_session_create, sessions_weapon_create=sessions_weapon_create)
    raise HTTPException(status_code=404, detail="Player not found")

# @router.post("/sessions/{session_id}/weapons/")
# async def create_session_weapon_api(session_weapon_create: SessionWeaponCreate):
#     return await create_session_weapon(session_weapon_create=session_weapon_create)

@router.get("/{steamid64}/sessions")
async def read_all_sessions_api(steamid64: str) -> List[GameSessionScheme]:
    player = await get_player(steamid64=steamid64)
    if player:
        return await get_all_sessions(player_id=steamid64)
    raise HTTPException(status_code=404, detail="Player not found")

@router.get("/{steamid64}")
async def read_player_api(steamid64: str) -> PlayerFront:
    player = await get_player(steamid64=steamid64)
    if player:
        last_sessions = await get_last_sessions(steamid64=steamid64)
        top_weapons = await get_player_weapons_top(steamid64=steamid64)
        result = {"player_stat":player, "last_sessions":last_sessions, "top_weapons": top_weapons}
        return result
    raise HTTPException(status_code=404, detail="Player not found")

@router.get("/{steamid64}/weapons")
async def read_player_weapons_api(steamid64: str) -> List[WeaponStat]:
    player = await get_player(steamid64=steamid64)
    if player:
        return await get_player_weapons(steamid64=steamid64)
    raise HTTPException(status_code=404, detail="Player not found")

