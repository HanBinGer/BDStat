from app.api.models import PlayerCreate, GameSessionCreate, SessionWeaponCreate
from app.db import players, game_sessions, session_weapons, db
from typing import List

async def get_player(steamid64: int):
    return await db.fetch_one(players.select().where(players.c.steamid64 == steamid64))

async def get_all_sessions(player_id: int):
    return await db.fetch_all(game_sessions.select().where(game_sessions.c.player_id == player_id).order_by(game_sessions.c.session_date.desc()))

async def create_player(player_create: PlayerCreate):
    result = await db.execute(players.insert().values(**player_create.model_dump()))
    #db.add()
    #db.commit()
    return result

async def create_game_session(game_session_create: GameSessionCreate, sessions_weapon_create: List[SessionWeaponCreate]):
    result = await db.fetch_one(game_sessions.insert().values(**game_session_create.model_dump()).returning(game_sessions.c.session_id))
    generated_session_id = result[0]
    for swc in sessions_weapon_create:
        await db.execute(session_weapons.insert().values(session_id=generated_session_id, **swc.model_dump()))
    await db.execute(players.update().where(players.c.steamid64 == game_session_create.player_id).values(
            total_kills=players.c.total_kills + game_session_create.total_kills,
            total_deaths=players.c.total_deaths + game_session_create.total_deaths,
            total_assists=players.c.total_assists + game_session_create.total_assists,
            total_wins=players.c.total_wins + int(game_session_create.is_win),
            total_battles=players.c.total_battles + 1,
        )
    )
    #db.commit()
    return result
