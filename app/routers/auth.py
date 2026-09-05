from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oath2
from ..database import engine, get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(prefix="/alchemy-player", tags=["Authentication"])

@router.post('/login', response_model=schemas.Token)
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    player = db.query(models.Player).filter(models.Player.email == credentials.username).first()

    if player == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't exist in this world")

    password = utils.verify_password(credentials.password, player.password)

    if not password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="YOu SHall NOt PaSs!")    

    token = oath2.create_token(data = {"player_id": player.id, "name": player.name, "race" : player.race})

    return {"access_token" : token, "bearer_type": "Bearer"}