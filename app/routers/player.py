from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import engine, get_db

router = APIRouter(prefix="/alchemy-player", tags=['Player'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):

    # hashing user password
    hashed_password = utils.hash(player.password)
    player.password = hashed_password

    new_player = models.Player(**player.model_dump())
    db.add(new_player)
    db.commit()

    return {"message" : "Welcome Peasant"}

@router.get("/{id}", response_model=schemas.Player)
def get_player(id: int, db: Session = Depends(get_db)):
    player = db.query(models.Player).filter(models.Player.id == id).first()

    if player == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This player doesn't exist in this universe")

    return player