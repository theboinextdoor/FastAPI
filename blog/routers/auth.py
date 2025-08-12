from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import  database , models , hashing, JWTtoken
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=['auth'])
get_db = database.get_db


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db:Session= Depends(get_db)):
  user = db.query(models.User).filter(models.User.email == request.username).first()
  if not user:
    raise HTTPException(
            status_code=404,
            detail=f"User not found..."
        )
  if not hashing.Hash.verify(user.password , request.password):
    raise HTTPException(
            status_code=404,
            detail=f"Incorrect Password..."
        )
  #TODO: generate jwt token the password:- 
  access_token = JWTtoken.create_access_token(
        data={"sub": user.email}
    )
  return {"access_token":access_token, "token_type":"bearer"}