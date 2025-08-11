from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import database, models, schemas 
from ..repository import userRepo

router = APIRouter(
  prefix="/user",
  tags=["users"]
)

get_db = database.get_db



@router.post('/')
def create_user(request: schemas.User , db : Session = Depends(get_db)):
  return userRepo.create(request,db)

@router.get('/{id}', status_code=200, response_model=schemas.ShowUser)
def get_user(id : int , db: Session= Depends(get_db)):
  return userRepo.user(id, db) 

@router.get("/" , status_code=200, response_model=List[schemas.ShowUser])
def show_all_user(db:Session = Depends(get_db)):
  return userRepo.all_users(db)

@router.delete("/{id}")
def del_user(id: int, db: Session = Depends(get_db)):
  return userRepo.destroy(id, db)
   
