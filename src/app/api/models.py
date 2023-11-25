from datetime import datetime
from typing import List

from pydantic import BaseModel


class PlayerCreate(BaseModel):
    steamid64: str
    player_name: str
    email: str

class PlayerScheme(PlayerCreate):
    total_kills: int
    total_deaths: int
    total_assists: int
    total_wins: int
    total_battles: int
    kd: float
    winrate: float

class GameSessionCreate(BaseModel):
    player_id: str
    map_id: int
    total_kills: int
    total_deaths: int
    total_assists: int
    is_win: bool

class GameSessionScheme(GameSessionCreate):
    session_id: int
    session_date: datetime

class SessionWeaponCreate(BaseModel):
    weapon_id: int
    kills: int

class SessionWeaponScheme(BaseModel):
    steamid64: str
    weapon_id: int
    kills: int

class WeaponStat(BaseModel):
    weapon_id: int
    weapon_name: str
    total_kills: int

class PlayerFront(BaseModel):
    player_stat: PlayerScheme
    last_sessions: List[GameSessionScheme]
    top_weapons: List[WeaponStat]

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str