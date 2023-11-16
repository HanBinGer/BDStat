from pydantic import BaseModel
from typing import List

class PlayerCreate(BaseModel):
    steamid64: int
    player_name: str
    email: str

class PlayerScheme(PlayerCreate):
    total_kills: int
    total_deaths: int
    total_assists: int
    total_wins: int
    total_battles: int

class GameSessionCreate(BaseModel):
    player_id: int
    map_id: int
    total_kills: int
    total_deaths: int
    total_assists: int
    is_win: bool

class SessionWeaponCreate(BaseModel):
    weapon_id: int
    kills: int

class SessionWeaponList(BaseModel):
    sessions: List[SessionWeaponCreate]
