from typing import List

from sqlalchemy import select, func, join

from app.api.models import GameSessionCreate, PlayerCreate, SessionWeaponCreate
from app.db import game_sessions, players, session_weapons, sessions, weapon_types
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta


async def get_player(steamid64: str):
    with sessions() as session:
        with session.begin():
            result = session.execute(players.select().where(players.c.steamid64 == steamid64)).fetchone()
    return result


async def get_sessions(steamid64: str, count: int | None = None, start_date: datetime | None = None, end_date: datetime | None = None):

    query = select(game_sessions).where(game_sessions.c.player_id == steamid64)

    if start_date != None:
        query=query.where(game_sessions.c.session_date >= start_date)
    if end_date != None:
        query=query.where(game_sessions.c.session_date <= end_date)
    
    query=query.order_by(game_sessions.c.session_date.desc())

    if count != None:
        query=query.limit(count)
    

    with sessions() as session:
        with session.begin():
            result = session.execute(query).fetchall()
    return result

def create_player(player_create: PlayerCreate):
    try:
        with sessions() as session:
            with session.begin():
                result = session.execute(players.insert().values(**player_create.model_dump()))
            return result
    except IntegrityError as err:
        print(err.params)
    

async def create_game_session(game_session_create: GameSessionCreate, sessions_weapon_create: List[SessionWeaponCreate]):
    with sessions() as session:
        with session.begin():  
            result = session.execute(game_sessions.insert().values(**game_session_create.model_dump()).returning(game_sessions.c.session_id))  
            print(result)
            generated_session_id = result.fetchone()[0]
            for swc in sessions_weapon_create:
                session.execute(session_weapons.insert().values(session_id=generated_session_id, **swc.model_dump()))
            session.execute(players.update().where(players.c.steamid64 == game_session_create.player_id).values(
                    total_kills=players.c.total_kills + game_session_create.total_kills,
                    total_deaths=players.c.total_deaths + game_session_create.total_deaths,
                    total_assists=players.c.total_assists + game_session_create.total_assists,
                    total_wins=players.c.total_wins + int(game_session_create.is_win),
                    total_battles=players.c.total_battles + 1,
                    kd=(players.c.total_kills + game_session_create.total_kills)/(players.c.total_deaths + game_session_create.total_deaths),
                    winrate=(players.c.total_wins + int(game_session_create.is_win))/(players.c.total_battles + 1),
                )
            )
    return result



async def get_player_weapons(steamid64: str, count: int | None=None, start_date: datetime | None = None, end_date: datetime | None = None):
    sel_wp = (
    select(
        weapon_types.c.weapon_id,
        weapon_types.c.weapon_name,
        func.sum(session_weapons.c.kills).label('total_kills')
    )
    .select_from(
        join(players, game_sessions, players.c.steamid64 == game_sessions.c.player_id)
        .join(session_weapons, game_sessions.c.session_id == session_weapons.c.session_id)
        .join(weapon_types, session_weapons.c.weapon_id == weapon_types.c.weapon_id)
    )
    .where(players.c.steamid64 == steamid64)
    )
    if start_date!=None:
        sel_wp=sel_wp.where(game_sessions.c.session_date >= start_date)
    if end_date!=None:
        sel_wp=sel_wp.where(game_sessions.c.session_date <= end_date+timedelta(days=1))
    sel_wp=sel_wp.group_by(weapon_types.c.weapon_id, weapon_types.c.weapon_name)
    if count!=None:
        sel_wp=sel_wp.order_by(func.sum(session_weapons.c.kills).desc()).limit(count)
    
    with sessions() as session:
        with session.begin():  
            result = session.execute(sel_wp).fetchall()
    return result


async def get_top_winrate(count: int):
    query = (
        select(players)
        .order_by(players.c.winrate.desc())
        .limit(count)
    )
    with sessions() as session:
        with session.begin():  
            result = session.execute(query).fetchall()
    return result

async def get_top_kd(count: int):
    query = (
        select(players)
        .order_by(players.c.kd.desc())
        .limit(count)
    )
    with sessions() as session:
        with session.begin():  
            result = session.execute(query).fetchall()
    return result

async def get_top_kills(count: int):
    query = (
        select(players)
        .order_by(players.c.total_kills.desc())
        .limit(count)
    )
    with sessions() as session:
        with session.begin():  
            result = session.execute(query).fetchall()
    return result

async def get_top_wins(count: int):
    query = (
        select(players)
        .order_by(players.c.total_wins.desc())
        .limit(count)
    )
    with sessions() as session:
        with session.begin():  
            result = session.execute(query).fetchall()
    return result

async def get_top_battles(count: int):
    query = (
        select(players)
        .order_by(players.c.total_battles.desc())
        .limit(count)
    )
    with sessions() as session:
        with session.begin():  
            result = session.execute(query).fetchall()
    return result