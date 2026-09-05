from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

# User 
class PlayerBase(BaseModel):
    name: str
    gender: str
    age: int
    race: str
    email: EmailStr
    password: str

class PlayerCreate(PlayerBase):
    pass   

class Player(BaseModel):
    name: str
    gender: str
    age: int
    race: str

    class Config:
        from_attributes = True

class PlayerLogin(BaseModel):
    email: EmailStr
    password: str  

# Power
class PowerBase(BaseModel):
    name: str
    description: str
    damage: int

class CreatePower(PowerBase):
    pass

class UpdatePower(PowerBase):
    pass

class Power(PowerBase):
    player_id: int
    learned_at: datetime
    player: Player

    class Config:
        from_attributes = True

class PowerShow(BaseModel):
    Power: Power
    loves: int


# Likes
class Love(BaseModel):
    power_id: int
    dir: conint(le=1)



# Token
class Token(BaseModel):
    access_token: str
    bearer_type: str

class TokenData(BaseModel):
    player_id: int
    name: str
    race: str