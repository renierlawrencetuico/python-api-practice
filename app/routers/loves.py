from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oath2
from ..database import engine, get_db

router = APIRouter(prefix="/alchemy-loves", tags=["Love"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def hit_vote(love: schemas.Love, db: Session = Depends(get_db), loggedin_player: int = Depends(oath2.get_current_player)):
    check_love = db.query(models.Love).filter(models.Love.power_id == love.power_id, models.Love.player_id == loggedin_player.id)
    love_exist = check_love.first()

    if love_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This power doesn't exist")

    if(love.dir == 1):
        if love_exist:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Your already in love with this power")
        
        add_love = models.Love(power_id = love.power_id, player_id = loggedin_player.id)
        db.add(add_love)
        db.commit()

        return {"message": "Successfully putted your love and support for this power"}
    else:
        if not love_exist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This power doesn't exist")

        check_love.delete(synchronize_session=False)
        db.commit()

        return {"message": "you don't love this power anymore"}