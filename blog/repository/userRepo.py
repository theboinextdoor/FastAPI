from sqlalchemy.orm import Session
from fastapi import HTTPException
from .. import models, schemas
from .. import hashing


def create(request: schemas.User , db:Session):
  new_User = models.User(name = request.name, 
                         email = request.email,
                         password = hashing.Hash.bcrypt(request.password))
  
  db.add(new_User)
  db.commit()
  db.refresh(new_User)
  return new_User

def user(id , db: Session):
  user = db.query(models.User).filter(models.User.id == id).first()
  if not user:
    raise HTTPException(
            status_code=404,
            detail=f"User {id} not found"
        ) 
  return user

def all_users(db:Session):
  all_users = db.query(models.User).all()
  return all_users

def destroy(id , db:Session):
  current_user = db.query(models.User).filter(models.User.id == id).first()
  if not current_user:
    raise HTTPException(status_code=404, detail=f"User with id {id} doesn't exist")
  db.delete(current_user)
  db.commit()
  return {"User Deleted..."}