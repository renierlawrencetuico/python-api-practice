from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oath2
from ..database import engine, get_db
from typing import Optional
from sqlalchemy import func

router = APIRouter(prefix="/alchemy-powers", tags=["Powers"])

#SQL BUT with PYTHON syntax instead of the query language by using SQLalchemy
@router.get("/all", response_model=list[schemas.PowerShow])
def get_all_powers(db: Session = Depends(get_db), check_token: int = Depends(oath2.get_current_player), limit: int = 3, skip: int = 2, search: Optional[str] = ""):
    powers = db.query(models.Power).filter(models.Power.name.contains(search)).limit(limit).offset(skip).all()

    # get results with likes feature using joins **Use schemas.PowerShow for the response_model**
    join_results = db.query(models.Power, func.count(models.Love.power_id).label("loves")).join(models.Love, models.Love.power_id == models.Power.id, isouter=True).group_by(models.Power.id).filter(models.Power.name.contains(search)).limit(limit).offset(skip).all()

    return join_results
    
@router.get("/", response_model=list[schemas.PowerShow])
def get_powers(db: Session = Depends(get_db), check_token: int = Depends(oath2.get_current_player)):
    powers = db.query(models.Power).filter(models.Power.player_id == check_token.id).all()

    join_results = db.query(models.Power, func.count(models.Love.power_id).label("loves")).join(models.Love, models.Love.power_id == models.Power.id, isouter=True).group_by(models.Power.id).all()
    
    return join_results

@router.get("/{id}", response_model=schemas.PowerShow)
def get_power(id: int, db: Session = Depends(get_db), check_token: int = Depends(oath2.get_current_player)):

    power = db.query(models.Power).filter(models.Power.id == id).first()

    join_result = db.query(models.Power, func.count(models.Love.power_id).label("loves")).join(models.Love, models.Love.power_id == models.Power.id, isouter=True).group_by(models.Power.id).filter(models.Power.id == id).first()

    if join_result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You didn't even have this power. >:(")

    if join_result.Power.player_id != check_token.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's bad to steal powers. >:(")
        
    return join_result

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_power(power: schemas.CreatePower, db: Session = Depends(get_db), check_token: int = Depends(oath2.get_current_player)):
    # new_power = models.Power(name=power.name, description=power.description, damage=power.damage)
    #shorter way
    new_power = models.Power(player_id=check_token.id, **power.model_dump())
    db.add(new_power)
    db.commit()
    return {"message" : "Successfully learned a new Power!"}

@router.delete("/{id}")
def delete_power(id: int, db: Session = Depends(get_db), check_token: int = Depends(oath2.get_current_player)):
    power = db.query(models.Power).filter(models.Power.id == id).first()

    if power == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You didn't even have this power. >:(")

    if power.player_id != check_token.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's bad to steal powers. >:(")

    db.delete(power)

    db.commit()
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_power(id: int, power: schemas.UpdatePower, db: Session = Depends(get_db), check_token: int = Depends(oath2.get_current_player)):
    get_power = db.query(models.Power).filter(models.Power.id == id)

    if get_power.first() == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You didn't even have this power. >:(")

    if get_power.first().player_id != check_token.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's bad to steal powers. >:(")

    get_power.update(power.model_dump(), synchronize_session=False)
    db.commit()

    return {"message" : "Power successfully change into a new form!"}



#SQL (the normal way) (Raw SQL)
# @router.get("/powers", response_model=list[schemas.Power])
# def get_powers():
#     cursor.execute("""SELECT * FROM Powers""")
#     powers = cursor.fetchall()
#     return powers

# @router.get("/powers/{id}", response_model=schemas.Power)
# def get_power(id: int, response: Response):
#     cursor.execute("""SELECT * FROM Powers WHERE id = %s""", (str(id)))
#     single_power = cursor.fetchone()

#     if single_power == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You didn't even have this power. >:(") 

#     return single_power

# @router.post("/powers", status_code=status.HTTP_201_CREATED)
# def create_power(new_power: schemas.CreatePower):
#     cursor.execute("""INSERT INTO Powers(name, description, damage) VALUES (%s, %s, %s)""", (new_power.name, new_power.description, new_power.damage))

#     conn.commit()
    
#     return {"message": "Successfully learned new power!"}

# @router.delete("/powers/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_power(id: int):
#     cursor.execute("""DELETE FROM Powers WHERE id = %s RETURNING * """, (str(id), ))
#     single_power = cursor.fetchone()

#     if single_power == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You didn't even have this power. >:(")

#     conn.commit()    

#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @router.put("/powers/{id}")
# def update_power(id: int, power: schemas.UpdatePower):
#     cursor.execute("""UPDATE Powers SET name = %s, description = %s, damage = %s WHERE id = %s RETURNING *""", (power.name, power.description, power.damage, str(id)))

#     upgraded_power = cursor.fetchone()

#     if upgraded_power == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You didn't even have this power. >:(")

#     conn.commit()

#     return {"message" : "Power successfully modified!"}