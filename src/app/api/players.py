from typing import List

from fastapi import APIRouter, HTTPException

from app.api.crud import *
from app.api.models import *
from datetime import date

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

@router.get("/{steamid64}/sessions")
async def read_sessions_api(steamid64: str, start_date: date | None = None, end_date: date | None = None) -> List[GameSessionScheme]:
    player = await get_player(steamid64=steamid64)
    if player:
        return await get_sessions(steamid64=steamid64,start_date=start_date, end_date=end_date)
    raise HTTPException(status_code=404, detail="Player not found")

@router.get("/{steamid64}")
async def read_player_api(steamid64: str, start_date: date | None = None, end_date: date | None = None) -> PlayerFront:
    player = await get_player(steamid64=steamid64)
    
    if player:
        if(start_date==None and end_date==None):
            last_sessions = await get_sessions(steamid64=steamid64, count=10)
            top_weapons = await get_player_weapons(steamid64=steamid64, count=10)
            result = PlayerFront(player_stat=player._asdict(),last_sessions=[i._asdict() for i in last_sessions],top_weapons=[i._asdict() for i in top_weapons])
            return result
        else:
            player = PlayerScheme.model_validate(player._asdict())
            last_sessions = await get_sessions(steamid64=steamid64, count=10, start_date=start_date, end_date=end_date)
            top_weapons = await get_player_weapons(steamid64=steamid64, count=10,start_date=start_date, end_date=end_date)
            
            player.total_battles = len(last_sessions)
            player.total_wins = 0
            player.total_kills = 0
            player.total_deaths = 0
            player.total_assists = 0
            for session in last_sessions:
                session=GameSessionScheme.model_validate(session._asdict())
                player.total_wins+=int(session.is_win)
                player.total_kills+=session.total_kills
                player.total_deaths+=session.total_deaths
                player.total_assists+=session.total_assists
            player.kd = player.total_kills / player.total_deaths
            player.winrate = player.total_wins / player.total_battles

            result = PlayerFront(player_stat=player,last_sessions=[i._asdict() for i in last_sessions],top_weapons=[i._asdict() for i in top_weapons])
            return result
    raise HTTPException(status_code=404, detail="Player not found")

@router.get("/{steamid64}/weapons")
async def read_player_weapons_api(steamid64: str) -> List[WeaponStat]:
    player = await get_player(steamid64=steamid64)
    if player:
        return await get_player_weapons(steamid64=steamid64)
    raise HTTPException(status_code=404, detail="Player not found")

