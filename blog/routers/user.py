from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import database, models, schemas , hashing

router = APIRouter()

get_db = database.get_db



@router.post('/user', tags=["user"])
def create_user(request: schemas.User , db : Session = Depends(get_db)):
  new_User = models.User(name = request.name, 
                         email = request.email,
                         password = hashing.Hash.bcrypt(request.password))
  
  db.add(new_User)
  db.commit()
  db.refresh(new_User)
  return new_User


@router.get('/user/{id}', status_code=200, response_model=schemas.ShowUser, tags=["user"])
def get_user(id : int , db: Session= Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == id).first()
  if not user:
    raise HTTPException(
            status_code=404,
            detail=f"User {id} not found"
        ) 
  return user


@router.get("/allUser" , status_code=200, response_model=List[schemas.ShowUser], tags=["user"])
def show_all_user(db:Session = Depends(get_db)):
  all_users = db.query(models.User).all()
  return all_users

@router.delete("/user/{id}", tags=["user"])
def del_user(id: int, db: Session = Depends(get_db)):
  current_user = db.query(models.User).filter(models.User.id == id).first()
  if not current_user:
    raise HTTPException(status_code=404, detail=f"User with id {id} doesn't exist")
  db.delete(current_user)
  db.commit()
  return {"User Deleted..."}
   
