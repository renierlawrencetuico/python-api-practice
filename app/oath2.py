from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from .schemas import TokenData
from fastapi import Response, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from . import database, models
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="alchemy-player/login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_token(data: dict):
    to_encode = data.copy()

    time_expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": time_expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)

        id: str = payload.get("player_id")
        name: str = payload.get("name")
        race: str = payload.get("race")

        if id == None:
            raise credentials_exception

        token_data = TokenData(player_id = id, name = name, race = race)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_player(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"This player still hasn't gain conciousness", headers={"WWW-Authenticate": "Bearer"})

    token = verify_token(token, credentials_exception)

    player = db.query(models.Player).filter(models.Player.id == token.player_id).first()

    return player